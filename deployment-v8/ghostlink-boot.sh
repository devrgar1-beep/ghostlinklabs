#!/usr/bin/env bash
set -euo pipefail

################################################################################
# GHOSTLINK v8 MASTER BOOT ORCHESTRATOR
# "The Machine" - Production Boot Sequence for Distributed AI Coordination
#
# Author: Robert Christopher George (Ghost)
# Purpose: Zero-failure boot sequence for 64-agent FCC lattice topology
# Architecture: Multi-stack distributed system with Byzantine fault tolerance
#
# Usage:
#   chmod +x ghostlink-boot.sh
#   ./ghostlink-boot.sh [command] [options]
#
# Commands:
#   init        - Initialize infrastructure and dependencies
#   start       - Start all GhostLink subsystems
#   stop        - Gracefully shutdown all subsystems
#   restart     - Full restart sequence
#   status      - Health check across all components
#   logs        - Aggregate logs from all subsystems
#   validate    - Pre-flight validation without starting
#
# Environment:
#   GHOSTLINK_ROOT     - Installation directory (default: /opt/ghostlink)
#   GHOSTLINK_ENV      - Environment: dev|staging|production (default: dev)
#   GHOSTLINK_LOG_DIR  - Log aggregation directory
################################################################################

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION MATRIX
# ═══════════════════════════════════════════════════════════════════════════

readonly VERSION="8.0.0"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Installation paths
GHOSTLINK_ROOT="${GHOSTLINK_ROOT:-/opt/ghostlink}"
GHOSTLINK_ENV="${GHOSTLINK_ENV:-dev}"
GHOSTLINK_LOG_DIR="${GHOSTLINK_LOG_DIR:-${GHOSTLINK_ROOT}/logs}"

# Component paths
readonly PYTHON_ROOT="${GHOSTLINK_ROOT}/python"
readonly NODE_ROOT="${GHOSTLINK_ROOT}/node"
readonly DOCKER_ROOT="${GHOSTLINK_ROOT}/docker"
readonly CONFIG_ROOT="${GHOSTLINK_ROOT}/config"
readonly DATA_ROOT="${GHOSTLINK_ROOT}/data"

# Service PIDs and status files
readonly PID_DIR="${GHOSTLINK_ROOT}/var/run"
readonly STATUS_DIR="${GHOSTLINK_ROOT}/var/status"

# Network configuration
readonly MCP_PORT="${MCP_PORT:-3000}"
readonly ORCHESTRATOR_PORT="${ORCHESTRATOR_PORT:-8000}"
readonly DASHBOARD_PORT="${DASHBOARD_PORT:-5173}"
readonly WEBSOCKET_PORT="${WEBSOCKET_PORT:-8765}"

# Lattice configuration
readonly LATTICE_SIZE=64
readonly LATTICE_TOPOLOGY="fcc"
readonly AGENT_DIMENSIONS=4

# Timing thresholds (milliseconds)
readonly BOOT_TIMEOUT=300000        # 5 minutes max boot time
readonly HEALTH_CHECK_INTERVAL=5000 # 5 second health checks
readonly STIGMERGY_THRESHOLD=700    # 0.7 in milliseconds

# Color codes for terminal output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════
# LOGGING AND OUTPUT UTILITIES
# ═══════════════════════════════════════════════════════════════════════════

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S.%3N')
    
    case "$level" in
        INFO)  echo -e "${CYAN}[${timestamp}]${NC} ${BLUE}[INFO]${NC}  ${message}" ;;
        WARN)  echo -e "${CYAN}[${timestamp}]${NC} ${YELLOW}[WARN]${NC}  ${message}" ;;
        ERROR) echo -e "${CYAN}[${timestamp}]${NC} ${RED}[ERROR]${NC} ${message}" >&2 ;;
        SUCCESS) echo -e "${CYAN}[${timestamp}]${NC} ${GREEN}[OK]${NC}    ${message}" ;;
        DEBUG) [[ "${GHOSTLINK_DEBUG:-0}" == "1" ]] && \
               echo -e "${CYAN}[${timestamp}]${NC} [DEBUG] ${message}" ;;
    esac
    
    # Also write to master log file
    echo "[${timestamp}] [${level}] ${message}" >> "${GHOSTLINK_LOG_DIR}/ghostlink-boot.log"
}

section() {
    local title="$1"
    echo ""
    log INFO "════════════════════════════════════════════════════════════════"
    log INFO "  ${title}"
    log INFO "════════════════════════════════════════════════════════════════"
}

subsection() {
    local title="$1"
    log INFO "──── ${title}"
}

# ═══════════════════════════════════════════════════════════════════════════
# ERROR HANDLING AND CLEANUP
# ═══════════════════════════════════════════════════════════════════════════

cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        log ERROR "Boot sequence failed with exit code: ${exit_code}"
        log ERROR "Initiating emergency shutdown sequence..."
        emergency_shutdown
    fi
}

emergency_shutdown() {
    log WARN "Emergency shutdown initiated - attempting graceful degradation"
    
    # Kill processes in reverse dependency order
    for service in dashboard orchestrator mcp-servers redis postgres docker; do
        stop_service "$service" 2>/dev/null || true
    done
    
    log WARN "Emergency shutdown complete"
}

trap cleanup EXIT
trap 'log ERROR "Interrupted by user"; exit 130' INT TERM

# ═══════════════════════════════════════════════════════════════════════════
# PREREQUISITE VALIDATION
# ═══════════════════════════════════════════════════════════════════════════

check_system_requirements() {
    section "SYSTEM REQUIREMENTS VALIDATION"
    
    local required_commands=(
        "docker:Docker Engine"
        "docker-compose:Docker Compose"
        "python3:Python 3.9+"
        "node:Node.js 18+"
        "npm:NPM Package Manager"
        "redis-cli:Redis CLI Tools"
        "psql:PostgreSQL Client"
        "curl:HTTP Client"
        "jq:JSON Processor"
    )
    
    local missing=()
    
    for item in "${required_commands[@]}"; do
        IFS=: read -r cmd desc <<< "$item"
        if command -v "$cmd" &>/dev/null; then
            log SUCCESS "${desc} detected: $(command -v $cmd)"
        else
            log ERROR "${desc} not found (${cmd})"
            missing+=("$desc")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        log ERROR "Missing required dependencies:"
        for dep in "${missing[@]}"; do
            log ERROR "  - ${dep}"
        done
        log ERROR "Install missing dependencies and retry"
        return 1
    fi
    
    # Verify versions
    subsection "Version Verification"
    
    local python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
    local node_version=$(node --version | grep -oE '[0-9]+' | head -1)
    
    if [[ $(echo "$python_version >= 3.9" | bc -l) -eq 0 ]]; then
        log ERROR "Python 3.9+ required, found: ${python_version}"
        return 1
    fi
    log SUCCESS "Python version: ${python_version}"
    
    if [[ $node_version -lt 18 ]]; then
        log ERROR "Node.js 18+ required, found: ${node_version}"
        return 1
    fi
    log SUCCESS "Node.js version: ${node_version}"
    
    # Check system resources
    subsection "System Resources"
    
    local total_mem=$(free -g | awk '/^Mem:/{print $2}')
    local available_disk=$(df -BG "${GHOSTLINK_ROOT}" 2>/dev/null | awk 'NR==2{print $4}' | tr -d 'G')
    
    if [[ $total_mem -lt 8 ]]; then
        log WARN "Recommended 8GB+ RAM, found: ${total_mem}GB"
    else
        log SUCCESS "Memory: ${total_mem}GB available"
    fi
    
    if [[ ${available_disk:-100} -lt 20 ]]; then
        log WARN "Recommended 20GB+ disk space, found: ${available_disk}GB"
    else
        log SUCCESS "Disk space: ${available_disk}GB available"
    fi
    
    # Check network connectivity
    subsection "Network Connectivity"
    
    local test_endpoints=(
        "api.openai.com"
        "api.anthropic.com"
        "api.together.xyz"
    )
    
    for endpoint in "${test_endpoints[@]}"; do
        if curl -s --connect-timeout 5 "https://${endpoint}" &>/dev/null; then
            log SUCCESS "Network: ${endpoint} reachable"
        else
            log WARN "Network: ${endpoint} unreachable (check firewall/proxy)"
        fi
    done
    
    return 0
}

validate_configuration() {
    section "CONFIGURATION VALIDATION"
    
    # Check for .env file
    if [[ ! -f "${GHOSTLINK_ROOT}/.env" ]]; then
        log ERROR ".env file not found at ${GHOSTLINK_ROOT}/.env"
        log ERROR "Run 'ghostlink-boot.sh init' to generate template"
        return 1
    fi
    
    # Source environment variables
    set -a
    source "${GHOSTLINK_ROOT}/.env"
    set +a
    
    # Validate critical API keys
    subsection "API Key Validation"
    
    local required_keys=(
        "OPENAI_API_KEY"
        "ANTHROPIC_API_KEY"
        "GOOGLE_API_KEY"
    )
    
    local missing_keys=()
    
    for key in "${required_keys[@]}"; do
        if [[ -z "${!key:-}" ]]; then
            log WARN "${key} not configured"
            missing_keys+=("$key")
        else
            local masked_key="${!key:0:8}...${!key: -4}"
            log SUCCESS "${key}: ${masked_key}"
        fi
    done
    
    if [[ ${#missing_keys[@]} -gt 0 && "${GHOSTLINK_ENV}" == "production" ]]; then
        log ERROR "Production environment requires all API keys"
        return 1
    fi
    
    # Validate lattice configuration
    subsection "Lattice Configuration"
    
    log INFO "Lattice Size: ${LATTICE_SIZE} agents"
    log INFO "Topology: ${LATTICE_TOPOLOGY} (Face-Centered Cubic)"
    log INFO "Agent Dimensions: ${AGENT_DIMENSIONS}D coordinate space"
    log INFO "Stigmergy Threshold: ${STIGMERGY_THRESHOLD}ms"
    
    return 0
}

# ═══════════════════════════════════════════════════════════════════════════
# INITIALIZATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

initialize_filesystem() {
    section "FILESYSTEM INITIALIZATION"
    
    local directories=(
        "${GHOSTLINK_ROOT}"
        "${GHOSTLINK_LOG_DIR}"
        "${PID_DIR}"
        "${STATUS_DIR}"
        "${DATA_ROOT}"
        "${CONFIG_ROOT}"
        "${PYTHON_ROOT}"
        "${NODE_ROOT}"
        "${DOCKER_ROOT}"
    )
    
    for dir in "${directories[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            log SUCCESS "Created directory: ${dir}"
        else
            log INFO "Directory exists: ${dir}"
        fi
    done
    
    # Set proper permissions
    chmod 755 "${GHOSTLINK_ROOT}"
    chmod 700 "${PID_DIR}" "${STATUS_DIR}"
    
    return 0
}

generate_config_templates() {
    section "CONFIGURATION TEMPLATE GENERATION"
    
    # Generate .env template
    if [[ ! -f "${GHOSTLINK_ROOT}/.env" ]]; then
        cat > "${GHOSTLINK_ROOT}/.env" <<'EOF'
# ═══════════════════════════════════════════════════════════════════════════
# GHOSTLINK v8 ENVIRONMENT CONFIGURATION
# Edit this file with your actual API keys and configuration values
# ═══════════════════════════════════════════════════════════════════════════

# ──── Core AI Provider API Keys ────────────────────────────────────────────
OPENAI_API_KEY=""
ANTHROPIC_API_KEY=""
GOOGLE_API_KEY=""
MISTRAL_API_KEY=""
COHERE_API_KEY=""
TOGETHER_API_KEY=""
PERPLEXITY_API_KEY=""
DEEPSEEK_API_KEY=""

# ──── GhostLink Core Configuration ─────────────────────────────────────────
GHOSTLINK_ENV="dev"
GHOSTLINK_LOG_LEVEL="INFO"
GHOSTLINK_LATTICE_SIZE="64"
GHOSTLINK_TOPOLOGY="fcc"
GHOSTLINK_AGENT_DIMENSIONS="4"

# ──── Coordination Settings ────────────────────────────────────────────────
STIGMERGY_THRESHOLD="0.7"
VARIANCE_ANALYSIS_ENABLED="true"
CMFL_CYCLE_INTERVAL="500"
PHEROMONE_EVAPORATION_RATE="0.1"
COORDINATION_TIMEOUT="30000"

# ──── Infrastructure Services ──────────────────────────────────────────────
DATABASE_URL="postgresql://ghostlink:ghostlink@localhost:5432/ghostlink"
REDIS_URL="redis://localhost:6379/0"

# Cloudflare (for distributed deployment)
CLOUDFLARE_ACCOUNT_ID=""
CLOUDFLARE_API_TOKEN=""
CLOUDFLARE_WORKERS_ENABLED="false"

# ──── Network Configuration ────────────────────────────────────────────────
MCP_PORT="3000"
ORCHESTRATOR_PORT="8000"
DASHBOARD_PORT="5173"
WEBSOCKET_PORT="8765"

# ──── Security & Authentication ────────────────────────────────────────────
JWT_SECRET=""
ADMIN_API_KEY=""
ENABLE_AUTH="true"

# ──── Monitoring & Observability ───────────────────────────────────────────
ENABLE_METRICS="true"
ENABLE_TRACING="false"
SENTRY_DSN=""

# ──── Development Options ──────────────────────────────────────────────────
DEBUG_MODE="false"
ENABLE_HOT_RELOAD="true"
MOCK_AI_PROVIDERS="false"

EOF
        log SUCCESS "Generated .env template at ${GHOSTLINK_ROOT}/.env"
        log WARN "Edit .env with your actual configuration before proceeding"
    else
        log INFO ".env file already exists"
    fi
    
    # Generate docker-compose.yml
    if [[ ! -f "${DOCKER_ROOT}/docker-compose.yml" ]]; then
        cat > "${DOCKER_ROOT}/docker-compose.yml" <<'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: ghostlink-postgres
    environment:
      POSTGRES_DB: ghostlink
      POSTGRES_USER: ghostlink
      POSTGRES_PASSWORD: ghostlink
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ghostlink"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: ghostlink-redis
    command: redis-server --appendonly yes
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  grafana:
    image: grafana/grafana:latest
    container_name: ghostlink-grafana
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ghostlink
      GF_INSTALL_PLUGINS: redis-datasource
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - postgres
      - redis

volumes:
  postgres-data:
  redis-data:
  grafana-data:

networks:
  default:
    name: ghostlink-network
EOF
        log SUCCESS "Generated docker-compose.yml at ${DOCKER_ROOT}/docker-compose.yml"
    fi
    
    # Generate database initialization script
    if [[ ! -f "${DOCKER_ROOT}/init-db.sql" ]]; then
        cat > "${DOCKER_ROOT}/init-db.sql" <<'EOF'
-- ═══════════════════════════════════════════════════════════════════════════
-- GHOSTLINK v8 DATABASE SCHEMA
-- ═══════════════════════════════════════════════════════════════════════════

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Agent coordination state
CREATE TABLE IF NOT EXISTS agents (
    agent_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lattice_position INTEGER[] NOT NULL,
    topology_layer INTEGER NOT NULL,
    cmfl_phase VARCHAR(20) NOT NULL,
    last_heartbeat TIMESTAMP DEFAULT NOW(),
    variance_score FLOAT,
    coordination_weight FLOAT DEFAULT 1.0,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Stigmergic pheromone trails
CREATE TABLE IF NOT EXISTS pheromones (
    pheromone_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(agent_id),
    trail_type VARCHAR(50) NOT NULL,
    concentration FLOAT NOT NULL,
    position INTEGER[] NOT NULL,
    evaporation_rate FLOAT DEFAULT 0.1,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

-- CMFL cycle records
CREATE TABLE IF NOT EXISTS cmfl_cycles (
    cycle_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_number BIGINT NOT NULL,
    phase VARCHAR(20) NOT NULL,
    agent_id UUID REFERENCES agents(agent_id),
    input_data JSONB,
    output_data JSONB,
    variance_detected FLOAT,
    duration_ms INTEGER,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Variance analysis results
CREATE TABLE IF NOT EXISTS variance_analysis (
    analysis_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query_hash VARCHAR(64) NOT NULL,
    provider_responses JSONB NOT NULL,
    variance_score FLOAT NOT NULL,
    disagreement_regions TEXT[],
    consensus_regions TEXT[],
    meta_insights JSONB,
    analyzed_at TIMESTAMP DEFAULT NOW()
);

-- System metrics and telemetry
CREATE TABLE IF NOT EXISTS system_metrics (
    metric_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    metric_unit VARCHAR(20),
    agent_id UUID REFERENCES agents(agent_id),
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_agents_position ON agents USING GIN(lattice_position);
CREATE INDEX idx_agents_heartbeat ON agents(last_heartbeat DESC);
CREATE INDEX idx_pheromones_position ON pheromones USING GIN(position);
CREATE INDEX idx_pheromones_expires ON pheromones(expires_at);
CREATE INDEX idx_cmfl_cycles_agent ON cmfl_cycles(agent_id, cycle_number);
CREATE INDEX idx_variance_query_hash ON variance_analysis(query_hash);
CREATE INDEX idx_metrics_name_time ON system_metrics(metric_name, recorded_at DESC);

-- Trigger for updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Initialize 64-agent lattice in FCC topology
INSERT INTO agents (lattice_position, topology_layer, cmfl_phase)
SELECT 
    ARRAY[x, y, z, w]::INTEGER[],
    (x + y + z + w) % 4,
    'collapse'
FROM generate_series(0, 3) AS x,
     generate_series(0, 3) AS y,
     generate_series(0, 3) AS z,
     generate_series(0, 3) AS w;
EOF
        log SUCCESS "Generated database initialization script"
    fi
    
    return 0
}

# ═══════════════════════════════════════════════════════════════════════════
# SERVICE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

start_infrastructure() {
    section "INFRASTRUCTURE SERVICES INITIALIZATION"
    
    subsection "Docker Infrastructure"
    
    cd "${DOCKER_ROOT}" || return 1
    
    log INFO "Starting PostgreSQL and Redis containers..."
    docker-compose up -d postgres redis
    
    # Wait for services to be healthy
    local max_wait=60
    local waited=0
    
    while [[ $waited -lt $max_wait ]]; do
        if docker-compose ps postgres | grep -q "healthy" && \
           docker-compose ps redis | grep -q "healthy"; then
            log SUCCESS "Infrastructure services healthy"
            break
        fi
        sleep 2
        waited=$((waited + 2))
        log INFO "Waiting for infrastructure... (${waited}s/${max_wait}s)"
    done
    
    if [[ $waited -ge $max_wait ]]; then
        log ERROR "Infrastructure services failed to start within ${max_wait}s"
        return 1
    fi
    
    # Verify database connectivity
    subsection "Database Verification"
    
    if PGPASSWORD=ghostlink psql -h localhost -U ghostlink -d ghostlink -c '\dt' &>/dev/null; then
        local table_count=$(PGPASSWORD=ghostlink psql -h localhost -U ghostlink -d ghostlink -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
        log SUCCESS "Database connected: ${table_count} tables initialized"
    else
        log ERROR "Database connection failed"
        return 1
    fi
    
    # Verify Redis connectivity
    if redis-cli ping &>/dev/null; then
        log SUCCESS "Redis connected and responsive"
    else
        log ERROR "Redis connection failed"
        return 1
    fi
    
    return 0
}

start_mcp_servers() {
    section "MCP SERVER LAYER INITIALIZATION"
    
    cd "${NODE_ROOT}" || return 1
    
    # Check if node_modules exists
    if [[ ! -d "node_modules" ]]; then
        log INFO "Installing Node.js dependencies..."
        npm install
    fi
    
    # Start MCP server cluster
    log INFO "Starting MCP server cluster on port ${MCP_PORT}..."
    
    npm run start:mcp &> "${GHOSTLINK_LOG_DIR}/mcp-servers.log" &
    local mcp_pid=$!
    echo "$mcp_pid" > "${PID_DIR}/mcp-servers.pid"
    
    # Wait for MCP servers to be responsive
    local max_wait=30
    local waited=0
    
    while [[ $waited -lt $max_wait ]]; do
        if curl -s "http://localhost:${MCP_PORT}/health" &>/dev/null; then
            log SUCCESS "MCP servers responding on port ${MCP_PORT}"
            echo "healthy" > "${STATUS_DIR}/mcp-servers.status"
            return 0
        fi
        sleep 2
        waited=$((waited + 2))
        log INFO "Waiting for MCP servers... (${waited}s/${max_wait}s)"
    done
    
    log ERROR "MCP servers failed to start within ${max_wait}s"
    return 1
}

start_orchestrator() {
    section "PYTHON ORCHESTRATOR INITIALIZATION"
    
    cd "${PYTHON_ROOT}" || return 1
    
    # Activate virtual environment or create if missing
    if [[ ! -d ".venv" ]]; then
        log INFO "Creating Python virtual environment..."
        python3 -m venv .venv
        source .venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
    else
        source .venv/bin/activate
    fi
    
    # Start orchestrator with 64-agent lattice
    log INFO "Initializing 64-agent FCC lattice orchestrator..."
    log INFO "CMFL cycle interval: ${CMFL_CYCLE_INTERVAL}ms"
    
    python -m ghostlink.orchestrator \
        --lattice-size "${LATTICE_SIZE}" \
        --topology "${LATTICE_TOPOLOGY}" \
        --port "${ORCHESTRATOR_PORT}" \
        &> "${GHOSTLINK_LOG_DIR}/orchestrator.log" &
    
    local orch_pid=$!
    echo "$orch_pid" > "${PID_DIR}/orchestrator.pid"
    
    # Wait for orchestrator initialization
    local max_wait=60
    local waited=0
    
    while [[ $waited -lt $max_wait ]]; do
        if curl -s "http://localhost:${ORCHESTRATOR_PORT}/health" &>/dev/null; then
            local agent_count=$(curl -s "http://localhost:${ORCHESTRATOR_PORT}/agents/count" | jq -r '.count')
            if [[ "$agent_count" == "$LATTICE_SIZE" ]]; then
                log SUCCESS "Orchestrator initialized: ${agent_count}/${LATTICE_SIZE} agents active"
                echo "healthy" > "${STATUS_DIR}/orchestrator.status"
                return 0
            fi
        fi
        sleep 3
        waited=$((waited + 3))
        log INFO "Waiting for orchestrator... (${waited}s/${max_wait}s)"
    done
    
    log ERROR "Orchestrator failed to initialize within ${max_wait}s"
    return 1
}

start_dashboard() {
    section "MONITORING DASHBOARD INITIALIZATION"
    
    cd "${NODE_ROOT}/dashboard" || return 1
    
    # Build React dashboard if needed
    if [[ ! -d "dist" ]]; then
        log INFO "Building React dashboard..."
        npm run build
    fi
    
    # Start dashboard server
    log INFO "Starting monitoring dashboard on port ${DASHBOARD_PORT}..."
    
    npm run preview -- --port "${DASHBOARD_PORT}" \
        &> "${GHOSTLINK_LOG_DIR}/dashboard.log" &
    
    local dash_pid=$!
    echo "$dash_pid" > "${PID_DIR}/dashboard.pid"
    
    # Wait for dashboard to be responsive
    local max_wait=30
    local waited=0
    
    while [[ $waited -lt $max_wait ]]; do
        if curl -s "http://localhost:${DASHBOARD_PORT}" &>/dev/null; then
            log SUCCESS "Dashboard available at http://localhost:${DASHBOARD_PORT}"
            echo "healthy" > "${STATUS_DIR}/dashboard.status"
            return 0
        fi
        sleep 2
        waited=$((waited + 2))
        log INFO "Waiting for dashboard... (${waited}s/${max_wait}s)"
    done
    
    log ERROR "Dashboard failed to start within ${max_wait}s"
    return 1
}

# ═══════════════════════════════════════════════════════════════════════════
# HEALTH CHECKING AND MONITORING
# ═══════════════════════════════════════════════════════════════════════════

run_health_checks() {
    section "SYSTEM HEALTH VERIFICATION"
    
    local all_healthy=true
    
    # Check infrastructure
    subsection "Infrastructure Health"
    
    if docker-compose -f "${DOCKER_ROOT}/docker-compose.yml" ps postgres | grep -q "healthy"; then
        log SUCCESS "PostgreSQL: HEALTHY"
    else
        log ERROR "PostgreSQL: UNHEALTHY"
        all_healthy=false
    fi
    
    if docker-compose -f "${DOCKER_ROOT}/docker-compose.yml" ps redis | grep -q "healthy"; then
        log SUCCESS "Redis: HEALTHY"
    else
        log ERROR "Redis: UNHEALTHY"
        all_healthy=false
    fi
    
    # Check application services
    subsection "Application Services Health"
    
    if curl -s "http://localhost:${MCP_PORT}/health" | jq -e '.status == "healthy"' &>/dev/null; then
        log SUCCESS "MCP Servers: HEALTHY"
    else
        log ERROR "MCP Servers: UNHEALTHY"
        all_healthy=false
    fi
    
    if curl -s "http://localhost:${ORCHESTRATOR_PORT}/health" | jq -e '.status == "healthy"' &>/dev/null; then
        local agent_status=$(curl -s "http://localhost:${ORCHESTRATOR_PORT}/agents/status")
        local active_agents=$(echo "$agent_status" | jq -r '.active_count')
        log SUCCESS "Orchestrator: HEALTHY (${active_agents}/${LATTICE_SIZE} agents)"
    else
        log ERROR "Orchestrator: UNHEALTHY"
        all_healthy=false
    fi
    
    if curl -s "http://localhost:${DASHBOARD_PORT}" &>/dev/null; then
        log SUCCESS "Dashboard: HEALTHY"
    else
        log ERROR "Dashboard: UNHEALTHY"
        all_healthy=false
    fi
    
    # Check lattice coordination
    subsection "Lattice Coordination Health"
    
    local coordination_metrics=$(curl -s "http://localhost:${ORCHESTRATOR_PORT}/metrics/coordination")
    local stigmergy_active=$(echo "$coordination_metrics" | jq -r '.stigmergy_trails_active')
    local cmfl_cycles_complete=$(echo "$coordination_metrics" | jq -r '.cmfl_cycles_completed')
    
    log INFO "Active Stigmergy Trails: ${stigmergy_active}"
    log INFO "Completed CMFL Cycles: ${cmfl_cycles_complete}"
    
    if $all_healthy; then
        log SUCCESS "All systems healthy - GhostLink v8 operational"
        return 0
    else
        log ERROR "One or more systems unhealthy"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# SHUTDOWN AND CLEANUP
# ═══════════════════════════════════════════════════════════════════════════

stop_service() {
    local service="$1"
    
    case "$service" in
        dashboard)
            if [[ -f "${PID_DIR}/dashboard.pid" ]]; then
                local pid=$(cat "${PID_DIR}/dashboard.pid")
                log INFO "Stopping dashboard (PID: ${pid})..."
                kill -TERM "$pid" 2>/dev/null || true
                rm -f "${PID_DIR}/dashboard.pid" "${STATUS_DIR}/dashboard.status"
            fi
            ;;
        orchestrator)
            if [[ -f "${PID_DIR}/orchestrator.pid" ]]; then
                local pid=$(cat "${PID_DIR}/orchestrator.pid")
                log INFO "Stopping orchestrator (PID: ${pid})..."
                kill -TERM "$pid" 2>/dev/null || true
                sleep 5  # Give agents time for graceful shutdown
                rm -f "${PID_DIR}/orchestrator.pid" "${STATUS_DIR}/orchestrator.status"
            fi
            ;;
        mcp-servers)
            if [[ -f "${PID_DIR}/mcp-servers.pid" ]]; then
                local pid=$(cat "${PID_DIR}/mcp-servers.pid")
                log INFO "Stopping MCP servers (PID: ${pid})..."
                kill -TERM "$pid" 2>/dev/null || true
                rm -f "${PID_DIR}/mcp-servers.pid" "${STATUS_DIR}/mcp-servers.status"
            fi
            ;;
        docker|infrastructure)
            log INFO "Stopping Docker infrastructure..."
            cd "${DOCKER_ROOT}" && docker-compose down
            ;;
        *)
            log ERROR "Unknown service: ${service}"
            return 1
            ;;
    esac
}

graceful_shutdown() {
    section "GRACEFUL SHUTDOWN SEQUENCE"
    
    # Shutdown in reverse dependency order
    log INFO "Initiating shutdown sequence..."
    
    stop_service dashboard
    sleep 2
    
    stop_service orchestrator
    sleep 5  # Allow agents to complete current CMFL cycles
    
    stop_service mcp-servers
    sleep 2
    
    stop_service docker
    
    log SUCCESS "GhostLink v8 shutdown complete"
}

# ═══════════════════════════════════════════════════════════════════════════
# MAIN COMMAND DISPATCHER
# ═══════════════════════════════════════════════════════════════════════════

cmd_init() {
    log INFO "Starting GhostLink v${VERSION} initialization..."
    
    check_system_requirements || exit 1
    initialize_filesystem || exit 1
    generate_config_templates || exit 1
    
    section "INITIALIZATION COMPLETE"
    log SUCCESS "GhostLink v${VERSION} initialized at ${GHOSTLINK_ROOT}"
    log INFO "Next steps:"
    log INFO "  1. Edit ${GHOSTLINK_ROOT}/.env with your configuration"
    log INFO "  2. Run: ./ghostlink-boot.sh start"
}

cmd_start() {
    log INFO "Starting GhostLink v${VERSION}..."
    
    check_system_requirements || exit 1
    validate_configuration || exit 1
    
    start_infrastructure || exit 1
    sleep 2
    
    start_mcp_servers || exit 1
    sleep 2
    
    start_orchestrator || exit 1
    sleep 2
    
    start_dashboard || exit 1
    sleep 2
    
    run_health_checks || exit 1
    
    section "GHOSTLINK v${VERSION} OPERATIONAL"
    log SUCCESS "All systems online"
    log INFO "Dashboard: http://localhost:${DASHBOARD_PORT}"
    log INFO "Orchestrator API: http://localhost:${ORCHESTRATOR_PORT}"
    log INFO "MCP Servers: http://localhost:${MCP_PORT}"
    log INFO ""
    log INFO "Monitor logs: tail -f ${GHOSTLINK_LOG_DIR}/*.log"
    log INFO "Check status: ./ghostlink-boot.sh status"
}

cmd_stop() {
    graceful_shutdown
}

cmd_restart() {
    cmd_stop
    sleep 5
    cmd_start
}

cmd_status() {
    run_health_checks
}

cmd_logs() {
    local service="${1:-all}"
    
    case "$service" in
        all)
            tail -f "${GHOSTLINK_LOG_DIR}"/*.log
            ;;
        orchestrator|mcp|dashboard|boot)
            tail -f "${GHOSTLINK_LOG_DIR}/${service}.log" 2>/dev/null || \
                log ERROR "Log file not found: ${service}.log"
            ;;
        *)
            log ERROR "Unknown service: ${service}"
            log INFO "Available: all, orchestrator, mcp, dashboard, boot"
            exit 1
            ;;
    esac
}

cmd_validate() {
    log INFO "Running pre-flight validation..."
    
    check_system_requirements || exit 1
    validate_configuration || exit 1
    
    log SUCCESS "Pre-flight validation passed"
    log INFO "System ready for deployment"
}

# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

main() {
    local command="${1:-}"
    
    # Banner
    cat <<'EOF'
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗██╗     ██╗███╗   ██╗██╗  ██╗ ║
║  ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██║     ██║████╗  ██║██║ ██╔╝ ║
║  ██║  ███╗███████║██║   ██║███████╗   ██║   ██║     ██║██╔██╗ ██║█████╔╝  ║
║  ██║   ██║██╔══██║██║   ██║╚════██║   ██║   ██║     ██║██║╚██╗██║██╔═██╗  ║
║  ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ███████╗██║██║ ╚████║██║  ██╗ ║
║   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ║
║                                                                           ║
║                    v8.0 - Distributed AI Coordination                    ║
║                  64-Agent FCC Lattice • CMFL Reasoning                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
    
    # Initialize logging
    mkdir -p "${GHOSTLINK_LOG_DIR}"
    
    case "$command" in
        init)     cmd_init ;;
        start)    cmd_start ;;
        stop)     cmd_stop ;;
        restart)  cmd_restart ;;
        status)   cmd_status ;;
        logs)     cmd_logs "${2:-all}" ;;
        validate) cmd_validate ;;
        ""|help|-h|--help)
            cat <<EOF

Usage: ghostlink-boot.sh [command] [options]

Commands:
  init        Initialize GhostLink installation and generate configs
  start       Start all GhostLink subsystems
  stop        Gracefully shutdown all subsystems
  restart     Full restart sequence
  status      Run health checks across all components
  logs [svc]  Tail logs (services: all, orchestrator, mcp, dashboard, boot)
  validate    Pre-flight validation without starting services
  help        Show this help message

Environment Variables:
  GHOSTLINK_ROOT      Installation directory (default: /opt/ghostlink)
  GHOSTLINK_ENV       Environment: dev|staging|production (default: dev)
  GHOSTLINK_LOG_DIR   Log directory (default: \$GHOSTLINK_ROOT/logs)
  GHOSTLINK_DEBUG     Enable debug logging (0|1)

Examples:
  ./ghostlink-boot.sh init                # First-time setup
  ./ghostlink-boot.sh start               # Start all services
  ./ghostlink-boot.sh status              # Check system health
  ./ghostlink-boot.sh logs orchestrator   # View orchestrator logs
  ./ghostlink-boot.sh stop                # Graceful shutdown

Documentation: https://github.com/devrgar-cyber/ghostlinklabs
EOF
            ;;
        *)
            log ERROR "Unknown command: ${command}"
            log INFO "Run './ghostlink-boot.sh help' for usage"
            exit 1
            ;;
    esac
}

# Execute main function with all arguments
main "$@"

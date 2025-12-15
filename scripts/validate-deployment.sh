#!/usr/bin/env bash
set -euo pipefail

################################################################################
# GHOSTLINK v8 PRE-DEPLOYMENT VALIDATOR
# Comprehensive verification before production deployment
#
# This script validates:
# - File structure completeness
# - Configuration file syntax
# - Dependency availability
# - Network port availability
# - File permissions
# - Environment configuration
#
# Usage: ./validate-deployment.sh [--strict]
################################################################################

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly VERSION="8.0.0"

# Color codes
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Validation state
ERRORS=0
WARNINGS=0
CHECKS_PASSED=0
STRICT_MODE=false

# Parse arguments
if [[ "${1:-}" == "--strict" ]]; then
    STRICT_MODE=true
fi

# ══════════════════════════════════════════════════════════════════════════════
# LOGGING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $*"
    ((CHECKS_PASSED++))
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $*"
    ((WARNINGS++))
}

log_error() {
    echo -e "${RED}[✗]${NC} $*"
    ((ERRORS++))
}

section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $*${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# ══════════════════════════════════════════════════════════════════════════════
# FILE STRUCTURE VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_file_structure() {
    section "FILE STRUCTURE VALIDATION"
    
    local required_files=(
        "ghostlink-boot.sh"
        ".env.example"
        "README.md"
        "python/ghostlink/orchestrator.py"
        "python/ghostlink/__init__.py"
        "python/ghostlink/__main__.py"
        "python/requirements.txt"
        "node/src/mcp-coordinator.ts"
        "node/package.json"
        "node/tsconfig.json"
        "node/dashboard/src/App.tsx"
        "node/dashboard/src/main.tsx"
        "node/dashboard/src/index.css"
        "node/dashboard/package.json"
        "node/dashboard/vite.config.ts"
        "node/dashboard/tailwind.config.js"
        "node/dashboard/tsconfig.json"
        "node/dashboard/postcss.config.js"
        "node/dashboard/index.html"
        "docker/docker-compose.yml"
        "docker/init-db.sql"
        "docker/prometheus.yml"
    )
    
    log_info "Checking for required files..."
    
    for file in "${required_files[@]}"; do
        if [[ -f "${SCRIPT_DIR}/${file}" ]]; then
            log_success "${file}"
        else
            log_error "Missing: ${file}"
        fi
    done
}

# ══════════════════════════════════════════════════════════════════════════════
# FILE PERMISSIONS VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_permissions() {
    section "FILE PERMISSIONS VALIDATION"
    
    log_info "Checking executable permissions..."
    
    if [[ -x "${SCRIPT_DIR}/ghostlink-boot.sh" ]]; then
        log_success "ghostlink-boot.sh is executable"
    else
        log_error "ghostlink-boot.sh is not executable (run: chmod +x ghostlink-boot.sh)"
    fi
    
    if [[ -x "${SCRIPT_DIR}/validate-deployment.sh" ]]; then
        log_success "validate-deployment.sh is executable"
    else
        log_warning "validate-deployment.sh is not executable"
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
# DEPENDENCY VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_dependencies() {
    section "SYSTEM DEPENDENCIES VALIDATION"
    
    local required_commands=(
        "docker:Docker Engine"
        "docker-compose:Docker Compose"
        "python3:Python 3.9+"
        "node:Node.js 18+"
        "npm:NPM Package Manager"
        "curl:HTTP Client"
        "jq:JSON Processor"
    )
    
    log_info "Checking for required system commands..."
    
    for item in "${required_commands[@]}"; do
        IFS=: read -r cmd desc <<< "$item"
        if command -v "$cmd" &>/dev/null; then
            local version=""
            case "$cmd" in
                docker) version=$(docker --version | cut -d' ' -f3 | tr -d ',') ;;
                python3) version=$(python3 --version | cut -d' ' -f2) ;;
                node) version=$(node --version | tr -d 'v') ;;
                npm) version=$(npm --version) ;;
            esac
            log_success "${desc} (${version})"
        else
            log_error "${desc} not found (${cmd})"
        fi
    done
}

# ══════════════════════════════════════════════════════════════════════════════
# VERSION VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_versions() {
    section "VERSION REQUIREMENTS VALIDATION"
    
    log_info "Verifying minimum version requirements..."
    
    # Python version
    if command -v python3 &>/dev/null; then
        local python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
        local python_major=$(echo "$python_version" | cut -d. -f1)
        local python_minor=$(echo "$python_version" | cut -d. -f2)
        
        if [[ $python_major -ge 3 && $python_minor -ge 9 ]]; then
            log_success "Python ${python_version} (>= 3.9 required)"
        else
            log_error "Python ${python_version} found, but 3.9+ required"
        fi
    fi
    
    # Node version
    if command -v node &>/dev/null; then
        local node_version=$(node --version | grep -oE '[0-9]+' | head -1)
        
        if [[ $node_version -ge 18 ]]; then
            log_success "Node.js ${node_version} (>= 18 required)"
        else
            log_error "Node.js ${node_version} found, but 18+ required"
        fi
    fi
    
    # Docker version
    if command -v docker &>/dev/null; then
        local docker_version=$(docker --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
        log_success "Docker ${docker_version}"
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_configuration() {
    section "CONFIGURATION FILE VALIDATION"
    
    log_info "Checking configuration files..."
    
    # Check for .env file
    if [[ -f "${SCRIPT_DIR}/.env" ]]; then
        log_success ".env file exists"
        
        # Validate critical API keys
        local required_keys=("OPENAI_API_KEY" "ANTHROPIC_API_KEY")
        for key in "${required_keys[@]}"; do
            if grep -q "^${key}=" "${SCRIPT_DIR}/.env" && ! grep -q "^${key}=$" "${SCRIPT_DIR}/.env"; then
                log_success "${key} is configured"
            else
                log_warning "${key} not configured in .env"
            fi
        done
    else
        log_warning ".env file not found (copy from .env.example)"
    fi
    
    # Validate JSON files
    if command -v jq &>/dev/null; then
        for json_file in node/package.json node/dashboard/package.json; do
            if [[ -f "${SCRIPT_DIR}/${json_file}" ]]; then
                if jq empty "${SCRIPT_DIR}/${json_file}" 2>/dev/null; then
                    log_success "${json_file} is valid JSON"
                else
                    log_error "${json_file} contains invalid JSON"
                fi
            fi
        done
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
# PORT AVAILABILITY VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_ports() {
    section "PORT AVAILABILITY VALIDATION"
    
    local required_ports=(
        "3000:MCP Servers"
        "5173:Dashboard"
        "8000:Orchestrator"
        "5432:PostgreSQL"
        "6379:Redis"
        "3001:Grafana"
    )
    
    log_info "Checking if required ports are available..."
    
    for item in "${required_ports[@]}"; do
        IFS=: read -r port desc <<< "$item"
        
        if lsof -i ":${port}" &>/dev/null || netstat -tuln 2>/dev/null | grep -q ":${port} "; then
            log_warning "Port ${port} (${desc}) is already in use"
        else
            log_success "Port ${port} (${desc}) is available"
        fi
    done
}

# ══════════════════════════════════════════════════════════════════════════════
# DISK SPACE VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_disk_space() {
    section "DISK SPACE VALIDATION"
    
    log_info "Checking available disk space..."
    
    local available_space=$(df -BG "${SCRIPT_DIR}" | awk 'NR==2{print $4}' | tr -d 'G')
    local required_space=20
    
    if [[ ${available_space} -ge ${required_space} ]]; then
        log_success "Sufficient disk space: ${available_space}GB available (${required_space}GB required)"
    else
        log_error "Insufficient disk space: ${available_space}GB available, ${required_space}GB required"
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
# MEMORY VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_memory() {
    section "SYSTEM MEMORY VALIDATION"
    
    log_info "Checking available memory..."
    
    local total_mem=$(free -g | awk '/^Mem:/{print $2}')
    local required_mem=8
    
    if [[ ${total_mem} -ge ${required_mem} ]]; then
        log_success "Sufficient memory: ${total_mem}GB total (${required_mem}GB required)"
    else
        log_warning "Limited memory: ${total_mem}GB total, ${required_mem}GB recommended"
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
# DOCKER VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_docker() {
    section "DOCKER ENVIRONMENT VALIDATION"
    
    log_info "Checking Docker configuration..."
    
    # Check Docker daemon
    if docker info &>/dev/null; then
        log_success "Docker daemon is running"
    else
        log_error "Docker daemon is not running or not accessible"
        return
    fi
    
    # Check Docker Compose
    if docker-compose version &>/dev/null || docker compose version &>/dev/null; then
        log_success "Docker Compose is available"
    else
        log_error "Docker Compose is not available"
    fi
    
    # Validate docker-compose.yml
    if [[ -f "${SCRIPT_DIR}/docker/docker-compose.yml" ]]; then
        cd "${SCRIPT_DIR}/docker"
        if docker-compose config &>/dev/null || docker compose config &>/dev/null; then
            log_success "docker-compose.yml is valid"
        else
            log_error "docker-compose.yml contains errors"
        fi
        cd "${SCRIPT_DIR}"
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
# PYTHON ENVIRONMENT VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_python_environment() {
    section "PYTHON ENVIRONMENT VALIDATION"
    
    log_info "Checking Python environment..."
    
    if [[ -d "${SCRIPT_DIR}/python/.venv" ]]; then
        log_success "Python virtual environment exists"
    else
        log_warning "Python virtual environment not created (will be created on first run)"
    fi
    
    # Validate requirements.txt
    if [[ -f "${SCRIPT_DIR}/python/requirements.txt" ]]; then
        local pkg_count=$(grep -c "^[^#]" "${SCRIPT_DIR}/python/requirements.txt" || true)
        log_success "requirements.txt contains ${pkg_count} packages"
    else
        log_error "requirements.txt not found"
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
# NODE ENVIRONMENT VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_node_environment() {
    section "NODE.JS ENVIRONMENT VALIDATION"
    
    log_info "Checking Node.js environment..."
    
    if [[ -d "${SCRIPT_DIR}/node/node_modules" ]]; then
        log_success "Node.js dependencies installed"
    else
        log_warning "Node.js dependencies not installed (will be installed on first run)"
    fi
    
    if [[ -d "${SCRIPT_DIR}/node/dashboard/node_modules" ]]; then
        log_success "Dashboard dependencies installed"
    else
        log_warning "Dashboard dependencies not installed (will be installed on first run)"
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
# NETWORK CONNECTIVITY VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

validate_network() {
    section "NETWORK CONNECTIVITY VALIDATION"
    
    log_info "Checking network connectivity to AI providers..."
    
    local test_endpoints=(
        "api.openai.com:OpenAI"
        "api.anthropic.com:Anthropic"
        "generativelanguage.googleapis.com:Google"
    )
    
    for item in "${test_endpoints[@]}"; do
        IFS=: read -r endpoint name <<< "$item"
        if curl -s --connect-timeout 5 "https://${endpoint}" &>/dev/null; then
            log_success "${name} (${endpoint}) is reachable"
        else
            log_warning "${name} (${endpoint}) is not reachable (check firewall/proxy)"
        fi
    done
}

# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY REPORT
# ══════════════════════════════════════════════════════════════════════════════

print_summary() {
    section "VALIDATION SUMMARY"
    
    echo ""
    echo -e "${BLUE}Results:${NC}"
    echo -e "  ${GREEN}✓ Passed:${NC}   ${CHECKS_PASSED}"
    echo -e "  ${YELLOW}⚠ Warnings:${NC} ${WARNINGS}"
    echo -e "  ${RED}✗ Errors:${NC}   ${ERRORS}"
    echo ""
    
    if [[ $ERRORS -eq 0 ]]; then
        if [[ $WARNINGS -eq 0 ]]; then
            echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${GREEN}  ✓ ALL CHECKS PASSED - READY FOR DEPLOYMENT${NC}"
            echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo ""
            echo -e "${BLUE}Next Steps:${NC}"
            echo -e "  1. Review .env configuration: ${YELLOW}nano .env${NC}"
            echo -e "  2. Start GhostLink: ${GREEN}./ghostlink-boot.sh start${NC}"
            echo -e "  3. Verify deployment: ${GREEN}./ghostlink-boot.sh status${NC}"
            echo ""
            return 0
        else
            echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${YELLOW}  ⚠ PASSED WITH WARNINGS - REVIEW BEFORE DEPLOYMENT${NC}"
            echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo ""
            echo -e "${BLUE}Action Required:${NC}"
            echo -e "  Review warnings above and address if necessary"
            echo -e "  Deployment may proceed but warnings should be resolved for production"
            echo ""
            
            if [[ "$STRICT_MODE" == "true" ]]; then
                return 1
            fi
            return 0
        fi
    else
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}  ✗ VALIDATION FAILED - FIX ERRORS BEFORE DEPLOYMENT${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo -e "${BLUE}Action Required:${NC}"
        echo -e "  Fix all errors marked with ${RED}✗${NC} above"
        echo -e "  Re-run validation: ${YELLOW}./validate-deployment.sh${NC}"
        echo ""
        return 1
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ══════════════════════════════════════════════════════════════════════════════

main() {
    cat <<'EOF'
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                    GHOSTLINK v8 DEPLOYMENT VALIDATOR                     ║
║                    Comprehensive Pre-Deployment Check                    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
    
    echo ""
    log_info "Starting comprehensive validation..."
    log_info "Version: ${VERSION}"
    if [[ "$STRICT_MODE" == "true" ]]; then
        log_info "Running in STRICT MODE (warnings will fail validation)"
    fi
    
    # Run all validation checks
    validate_file_structure
    validate_permissions
    validate_dependencies
    validate_versions
    validate_configuration
    validate_ports
    validate_disk_space
    validate_memory
    validate_docker
    validate_python_environment
    validate_node_environment
    validate_network
    
    # Print summary and exit
    print_summary
    exit $?
}

main "$@"

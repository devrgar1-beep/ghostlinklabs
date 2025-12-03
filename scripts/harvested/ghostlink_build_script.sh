#!/usr/bin/env bash
# GhostLink Docker Build and Deployment Script
# Sovereign Computing System - ColdForge Builder

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."
GHOSTLINK_VERSION="${GHOSTLINK_VERSION:-7.0.0}"
REGISTRY="${REGISTRY:-ghcr.io/ghostlinklabs}"
BUILD_CONTEXT="${PROJECT_ROOT}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Show usage
show_usage() {
    cat << EOF
GhostLink Docker Build Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  build       Build Docker images
  deploy      Deploy using docker-compose
  stop        Stop running containers
  clean       Clean up containers and images
  logs        Show container logs
  health      Check container health
  shell       Open shell in running container

Options:
  --tag TAG           Specify image tag (default: ${GHOSTLINK_VERSION})
  --registry REG      Specify registry (default: ${REGISTRY})
  --no-cache          Build without cache
  --push              Push images to registry after build
  --dev               Development mode (mount source code)
  --help              Show this help message

Examples:
  $0 build --no-cache
  $0 deploy --dev
  $0 logs controller
  $0 shell controller
EOF
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Build Docker images
build_images() {
    local tag="${1:-${GHOSTLINK_VERSION}}"
    local registry="${2:-${REGISTRY}}"
    local no_cache="${3:-false}"
    local push="${4:-false}"
    
    log_info "Building GhostLink Docker images..."
    log_info "Tag: ${tag}"
    log_info "Registry: ${registry}"
    
    local cache_flag=""
    if [[ "${no_cache}" == "true" ]]; then
        cache_flag="--no-cache"
        log_warning "Building without cache"
    fi
    
    # Build main image
    log_info "Building main GhostLink image..."
    docker build ${cache_flag} \
        -t "${registry}/ghostlink:${tag}" \
        -t "${registry}/ghostlink:latest" \
        -f "${BUILD_CONTEXT}/Dockerfile" \
        "${BUILD_CONTEXT}"
    
    # Build console image if it exists
    if [[ -f "${BUILD_CONTEXT}/console/Dockerfile.console" ]]; then
        log_info "Building console image..."
        docker build ${cache_flag} \
            -t "${registry}/ghostlink-console:${tag}" \
            -t "${registry}/ghostlink-console:latest" \
            -f "${BUILD_CONTEXT}/console/Dockerfile.console" \
            "${BUILD_CONTEXT}/console"
    fi
    
    log_success "Docker images built successfully"
    
    # Push images if requested
    if [[ "${push}" == "true" ]]; then
        log_info "Pushing images to registry..."
        docker push "${registry}/ghostlink:${tag}"
        docker push "${registry}/ghostlink:latest"
        
        if docker images "${registry}/ghostlink-console:${tag}" &> /dev/null; then
            docker push "${registry}/ghostlink-console:${tag}"
            docker push "${registry}/ghostlink-console:latest"
        fi
        
        log_success "Images pushed to registry"
    fi
}

# Deploy using docker-compose
deploy_stack() {
    local dev_mode="${1:-false}"
    
    log_info "Deploying GhostLink stack..."
    
    # Prepare environment
    export GHOSTLINK_VERSION
    export REGISTRY
    
    # Create required directories
    mkdir -p "${PROJECT_ROOT}/data/vault"
    mkdir -p "${PROJECT_ROOT}/data/state"
    mkdir -p "${PROJECT_ROOT}/data/keys"
    mkdir -p "${PROJECT_ROOT}/logs"
    mkdir -p "${PROJECT_ROOT}/configs"
    
    # Set permissions
    chmod 700 "${PROJECT_ROOT}/data/keys"
    
    # Generate default configs if they don't exist
    generate_default_configs
    
    # Choose compose file
    local compose_file="${PROJECT_ROOT}/docker-compose.yml"
    if [[ "${dev_mode}" == "true" ]]; then
        if [[ -f "${PROJECT_ROOT}/docker-compose.dev.yml" ]]; then
            compose_file="${PROJECT_ROOT}/docker-compose.dev.yml"
            log_info "Using development compose configuration"
        else
            log_warning "Development compose file not found, using default"
        fi
    fi
    
    # Deploy
    docker-compose -f "${compose_file}" up -d
    
    log_success "GhostLink stack deployed"
    
    # Wait for health checks
    log_info "Waiting for services to become healthy..."
    sleep 10
    
    # Check health
    check_health
}

# Stop containers
stop_stack() {
    log_info "Stopping GhostLink stack..."
    
    if [[ -f "${PROJECT_ROOT}/docker-compose.yml" ]]; then
        docker-compose -f "${PROJECT_ROOT}/docker-compose.yml" down
    fi
    
    log_success "GhostLink stack stopped"
}

# Clean up
clean_up() {
    log_info "Cleaning up GhostLink containers and images..."
    
    # Stop and remove containers
    stop_stack
    
    # Remove containers
    docker ps -a --filter "name=ghostlink" --format "{{.ID}}" | xargs -r docker rm -f
    
    # Remove images
    docker images "${REGISTRY}/ghostlink*" --format "{{.ID}}" | xargs -r docker rmi -f
    
    # Remove volumes (with confirmation)
    echo -n "Remove Docker volumes? [y/N]: "
    read -r response
    if [[ "${response}" =~ ^[Yy]$ ]]; then
        docker volume ls --filter "name=ghostlink" --format "{{.Name}}" | xargs -r docker volume rm
        log_success "Volumes removed"
    fi
    
    log_success "Cleanup completed"
}

# Show logs
show_logs() {
    local service="${1:-}"
    
    if [[ -n "${service}" ]]; then
        log_info "Showing logs for ${service}..."
        docker-compose -f "${PROJECT_ROOT}/docker-compose.yml" logs -f "ghostlink-${service}"
    else
        log_info "Showing logs for all services..."
        docker-compose -f "${PROJECT_ROOT}/docker-compose.yml" logs -f
    fi
}

# Check health
check_health() {
    log_info "Checking container health..."
    
    local healthy=0
    local total=0
    
    for container in $(docker ps --filter "name=ghostlink" --format "{{.Names}}"); do
        total=$((total + 1))
        local health_status=$(docker inspect --format='{{.State.Health.Status}}' "${container}" 2>/dev/null || echo "no-health-check")
        
        if [[ "${health_status}" == "healthy" ]]; then
            healthy=$((healthy + 1))
            log_success "${container}: healthy"
        elif [[ "${health_status}" == "no-health-check" ]]; then
            # Check if container is running
            local status=$(docker inspect --format='{{.State.Status}}' "${container}")
            if [[ "${status}" == "running" ]]; then
                healthy=$((healthy + 1))
                log_success "${container}: running (no health check)"
            else
                log_error "${container}: ${status}"
            fi
        else
            log_error "${container}: ${health_status}"
        fi
    done
    
    log_info "Health check: ${healthy}/${total} containers healthy"
    
    if [[ ${healthy} -eq ${total} ]] && [[ ${total} -gt 0 ]]; then
        log_success "All services are healthy"
        return 0
    else
        log_error "Some services are unhealthy"
        return 1
    fi
}

# Open shell in container
open_shell() {
    local service="${1:-controller}"
    local container="ghostlink-${service}"
    
    log_info "Opening shell in ${container}..."
    
    if docker ps --filter "name=${container}" --format "{{.Names}}" | grep -q "${container}"; then
        docker exec -it "${container}" /bin/bash
    else
        log_error "Container ${container} is not running"
        exit 1
    fi
}

# Generate default configurations
generate_default_configs() {
    local configs_dir="${PROJECT_ROOT}/configs"
    
    # Neural config
    if [[ ! -f "${configs_dir}/neural_config.json" ]]; then
        cat > "${configs_dir}/neural_config.json" << 'EOF'
{
  "model_path": "/opt/ghostlink/models",
  "max_tokens": 4096,
  "temperature": 0.7,
  "offline_mode": true,
  "sovereignty_check": true
}
EOF
    fi
    
    # Wired config
    if [[ ! -f "${configs_dir}/wired_network.json" ]]; then
        cat > "${configs_dir}/wired_network.json" << 'EOF'
{
  "version": "v8",
  "network_mode": "isolated",
  "max_connections": 10,
  "heartbeat_interval": 30,
  "encryption_enabled": true
}
EOF
    fi
    
    # Prometheus config
    mkdir -p "${PROJECT_ROOT}/monitoring"
    if [[ ! -f "${PROJECT_ROOT}/monitoring/prometheus.yml" ]]; then
        cat > "${PROJECT_ROOT}/monitoring/prometheus.yml" << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ghostlink-controller'
    static_configs:
      - targets: ['ghostlink-controller:8080']
  
  - job_name: 'ghostlink-neural'
    static_configs:
      - targets: ['ghostlink-neural:8080']
  
  - job_name: 'ghostlink-wired'
    static_configs:
      - targets: ['ghostlink-wired:8080']
EOF
    fi
    
    log_success "Default configurations generated"
}

# Main function
main() {
    local command="${1:-}"
    shift || true
    
    # Parse options
    local tag="${GHOSTLINK_VERSION}"
    local registry="${REGISTRY}"
    local no_cache="false"
    local push="false"
    local dev_mode="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --tag)
                tag="$2"
                shift 2
                ;;
            --registry)
                registry="$2"
                shift 2
                ;;
            --no-cache)
                no_cache="true"
                shift
                ;;
            --push)
                push="true"
                shift
                ;;
            --dev)
                dev_mode="true"
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                break
                ;;
        esac
    done
    
    # Check prerequisites
    check_prerequisites
    
    # Execute command
    case "${command}" in
        build)
            build_images "${tag}" "${registry}" "${no_cache}" "${push}"
            ;;
        deploy)
            deploy_stack "${dev_mode}"
            ;;
        stop)
            stop_stack
            ;;
        clean)
            clean_up
            ;;
        logs)
            show_logs "$1"
            ;;
        health)
            check_health
            ;;
        shell)
            open_shell "$1"
            ;;
        "")
            log_error "No command specified"
            show_usage
            exit 1
            ;;
        *)
            log_error "Unknown command: ${command}"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
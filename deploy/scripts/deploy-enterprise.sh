#!/usr/bin/env bash

# ==========================================
# GhostLink Enterprise Deployment Script
# Automated setup for Dell R630 cluster with enterprise storage
# ==========================================

set -e

# Configuration
COMPOSE_FILE="docker-compose.enterprise.yml"
PROJECT_NAME="ghostlink-enterprise"
NETWORK_SUBNET="192.168.1.0/24"
GATEWAY="192.168.1.1"

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

# Pre-deployment checks
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if Docker is installed and running
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running. Please start Docker service."
        exit 1
    fi

    # Check if Docker Compose is available
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not available. Please install Docker Compose."
        exit 1
    fi

    # Check available disk space (need at least 50GB)
    AVAILABLE_SPACE=$(df / | tail -1 | awk '{print $4}')
    if [ "$AVAILABLE_SPACE" -lt 52428800 ]; then  # 50GB in KB
        log_warning "Low disk space detected. Ensure at least 50GB free space."
    fi

    log_success "Prerequisites check passed"
}

# Create Docker network
create_network() {
    log_info "Creating Docker network..."

    if docker network ls | grep -q "ghostlink-enterprise-br0"; then
        log_info "Network already exists, skipping creation"
    else
        docker network create \
            --driver bridge \
            --subnet="$NETWORK_SUBNET" \
            --gateway="$GATEWAY" \
            --opt com.docker.network.bridge.name=ghostlink-enterprise-br0 \
            --opt com.docker.network.bridge.enable_icc=true \
            --opt com.docker.network.bridge.enable_ip_masquerade=true \
            ghostlink-enterprise-br0

        log_success "Docker network created"
    fi
}

# Validate configuration
validate_config() {
    log_info "Validating configuration..."

    # Check if compose file exists
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_error "Compose file $COMPOSE_FILE not found"
        exit 1
    fi

    # Validate compose file
    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$COMPOSE_FILE" config > /dev/null
    else
        docker compose -f "$COMPOSE_FILE" config > /dev/null
    fi

    log_success "Configuration validation passed"
}

# Deploy services
deploy_services() {
    local profile="$1"

    log_info "Deploying GhostLink Enterprise services..."

    if [ -n "$profile" ]; then
        log_info "Using profile: $profile"
        COMPOSE_CMD="docker-compose -f $COMPOSE_FILE --profile $profile -p $PROJECT_NAME"
        DOCKER_COMPOSE_CMD="docker compose -f $COMPOSE_FILE --profile $profile -p $PROJECT_NAME"
    else
        COMPOSE_CMD="docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME"
        DOCKER_COMPOSE_CMD="docker compose -f $COMPOSE_FILE -p $PROJECT_NAME"
    fi

    # Use appropriate compose command
    if command -v docker-compose &> /dev/null; then
        $COMPOSE_CMD up -d
    else
        $DOCKER_COMPOSE_CMD up -d
    fi

    log_success "Services deployed successfully"
}

# Wait for services to be healthy
wait_for_services() {
    log_info "Waiting for services to become healthy..."

    local max_attempts=60
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost/health > /dev/null 2>&1; then
            log_success "Services are healthy"
            return 0
        fi

        log_info "Waiting for services... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done

    log_error "Services failed to become healthy within timeout"
    return 1
}

# Setup monitoring
setup_monitoring() {
    log_info "Setting up monitoring stack..."

    # Wait for Grafana to be ready
    sleep 30

    # Import dashboards (if any exist)
    if [ -d "monitoring/grafana/dashboards" ]; then
        log_info "Grafana dashboards directory found"
    fi

    log_success "Monitoring setup completed"
}

# Display deployment information
show_deployment_info() {
    log_success "GhostLink Enterprise deployment completed!"
    echo ""
    echo "Service Endpoints:"
    echo "=================="
    echo "Main API:         http://localhost/api/"
    echo "API Docs:         http://localhost/api/docs"
    echo "Grafana:          http://localhost:3000"
    echo "Prometheus:       http://localhost:9090"
    echo "Ollama API:       http://localhost:11434"
    echo ""
    echo "Network Information:"
    echo "===================="
    echo "Controller:       192.168.1.100"
    echo "Training Node:    192.168.1.101"
    echo "Inference Node:   192.168.1.102"
    echo "MD3600i Storage:  192.168.1.103"
    echo "Synology NAS:     192.168.1.104-192.168.1.106"
    echo ""
    echo "Management Commands:"
    echo "===================="
    echo "View logs:        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f"
    echo "Stop services:    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down"
    echo "Scale training:   docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d --scale ghostlink-trainer=2"
    echo "Update services:  docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME pull && docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d"
}

# Main deployment function
main() {
    local profile=""

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --profile)
                profile="$2"
                shift 2
                ;;
            --help)
                echo "Usage: $0 [--profile <profile>] [--help]"
                echo ""
                echo "Profiles:"
                echo "  training    - Deploy training services only"
                echo "  inference   - Deploy inference services only"
                echo "  monitoring  - Deploy monitoring stack only"
                echo "  (default)   - Deploy all services"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    echo "========================================="
    echo "GhostLink Enterprise Deployment"
    echo "========================================="

    check_prerequisites
    create_network
    validate_config
    deploy_services "$profile"
    wait_for_services
    setup_monitoring
    show_deployment_info

    echo ""
    log_success "Deployment completed successfully! 🎉"
}

# Run main function with all arguments
main "$@"
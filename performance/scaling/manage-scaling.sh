#!/bin/bash

# GhostLink Scaling Management Script
# Manual and automated scaling operations

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get current scale
get_current_scale() {
    local service=$1
    docker service ls | grep "$service" | awk '{print $4}' || echo "Service not found"
}

# Scale service manually
scale_service() {
    local service=$1
    local replicas=$2

    print_status "Scaling $service to $replicas replicas..."

    if command -v docker &> /dev/null && docker compose version &> /dev/null; then
        docker compose up -d --scale "$service=$replicas"
    else
        print_error "Docker Compose not available"
        exit 1
    fi

    print_success "$service scaled to $replicas replicas"
}

# Auto-scale based on metrics
auto_scale() {
    print_status "Checking auto-scaling conditions..."

    # Check CPU usage
    local cpu_usage=$(docker stats --no-stream --format "{{.CPUPerc}}" ghostlink-api-prod 2>/dev/null | sed 's/%//' | head -1)

    if [ -n "$cpu_usage" ] && [ "$(echo "$cpu_usage > 70" | bc -l)" -eq 1 ]; then
        print_warning "High CPU usage detected ($cpu_usage%), scaling up..."
        scale_service "ghostlink-api-prod" 3
    elif [ -n "$cpu_usage" ] && [ "$(echo "$cpu_usage < 20" | bc -l)" -eq 1 ]; then
        print_status "Low CPU usage detected ($cpu_usage%), scaling down..."
        scale_service "ghostlink-api-prod" 1
    else
        print_success "CPU usage normal ($cpu_usage%)"
    fi

    # Check memory usage
    local mem_usage=$(docker stats --no-stream --format "{{.MemPerc}}" ghostlink-api-prod 2>/dev/null | sed 's/%//' | head -1)

    if [ -n "$mem_usage" ] && [ "$(echo "$mem_usage > 80" | bc -l)" -eq 1 ]; then
        print_warning "High memory usage detected ($mem_usage%), scaling up..."
        scale_service "ghostlink-api-prod" 3
    fi
}

# Show scaling status
show_status() {
    print_status "Current scaling status:"

    echo "API Servers:"
    get_current_scale "ghostlink-api-prod"

    echo "AI Orchestrators:"
    get_current_scale "ghostlink-orchestrator-prod"

    echo ""
    echo "Container Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "Docker stats not available"
}

# Main function
main() {
    case "${1:-status}" in
        "status")
            show_status
            ;;
        "scale")
            if [ -z "$2" ] || [ -z "$3" ]; then
                echo "Usage: $0 scale <service> <replicas>"
                exit 1
            fi
            scale_service "$2" "$3"
            ;;
        "auto")
            auto_scale
            ;;
        "up")
            print_status "Scaling up all services..."
            scale_service "ghostlink-api-prod" 3
            scale_service "ghostlink-orchestrator-prod" 2
            ;;
        "down")
            print_status "Scaling down all services..."
            scale_service "ghostlink-api-prod" 1
            scale_service "ghostlink-orchestrator-prod" 1
            ;;
        *)
            echo "Usage: $0 [status|scale|auto|up|down]"
            echo "  status  - Show current scaling status"
            echo "  scale   - Scale specific service (scale <service> <replicas>)"
            echo "  auto    - Auto-scale based on metrics"
            echo "  up      - Scale up all services"
            echo "  down    - Scale down all services"
            exit 1
            ;;
    esac
}

main "$@"

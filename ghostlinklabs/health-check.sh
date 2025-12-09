#!/bin/bash

# GhostLink Production Health Check Script
# This script checks the health of all production services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if a service is running
check_service() {
    local service_name=$1
    local container_name=$2

    if docker ps --format "table {{.Names}}" | grep -q "^${container_name}$"; then
        print_success "$service_name is running"
        return 0
    else
        print_error "$service_name is not running"
        return 1
    fi
}

# Check service health via HTTP
check_http_health() {
    local service_name=$1
    local url=$2
    local expected_code=${3:-200}

    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "^$expected_code$"; then
        print_success "$service_name health check passed"
        return 0
    else
        print_error "$service_name health check failed"
        return 1
    fi
}

# Check Docker services
check_docker_services() {
    print_status "Checking Docker services..."

    local failed_services=0

    check_service "GhostLink API" "ghostlink-api-prod" || ((failed_services++))
    check_service "GhostLink Orchestrator" "ghostlink-orchestrator-prod" || ((failed_services++))
    check_service "Prometheus" "ghostlink-prometheus" || ((failed_services++))
    check_service "Grafana" "ghostlink-grafana" || ((failed_services++))
    check_service "Nginx" "ghostlink-nginx" || ((failed_services++))

    return $failed_services
}

# Check HTTP endpoints
check_http_endpoints() {
    print_status "Checking HTTP endpoints..."

    local failed_checks=0

    check_http_health "GhostLink API" "http://localhost:3000/health" || ((failed_checks++))
    check_http_health "GhostLink Web Interface" "http://localhost/" || ((failed_checks++))
    check_http_health "Grafana" "http://localhost:3001/api/health" || ((failed_checks++))
    check_http_health "Prometheus" "http://localhost:9090/-/healthy" || ((failed_checks++))

    return $failed_checks
}

# Check resource usage
check_resources() {
    print_status "Checking resource usage..."

    echo "Container Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

    echo ""
    echo "Disk Usage:"
    df -h | grep -E "(Filesystem|/)$"

    echo ""
    echo "Memory Usage:"
    free -h 2>/dev/null || vm_stat
}

# Check logs for errors
check_logs() {
    print_status "Checking recent logs for errors..."

    local services=("ghostlink-api-prod" "ghostlink-orchestrator-prod" "ghostlink-prometheus" "ghostlink-grafana" "ghostlink-nginx")

    for service in "${services[@]}"; do
        echo "Recent errors in $service:"
        docker logs --since 1h "$service" 2>&1 | grep -i error | tail -5 || echo "No recent errors"
        echo "---"
    done
}

# Main health check function
main() {
    echo "🏥 GhostLink Production Health Check"
    echo "===================================="

    local total_failures=0

    check_docker_services
    total_failures=$((total_failures + $?))

    check_http_endpoints
    total_failures=$((total_failures + $?))

    check_resources

    if [ "$1" = "--verbose" ] || [ "$1" = "-v" ]; then
        check_logs
    fi

    echo ""
    if [ $total_failures -eq 0 ]; then
        print_success "All health checks passed! ✅"
        exit 0
    else
        print_error "$total_failures health checks failed! ❌"
        exit 1
    fi
}

# Run main function
main "$@"
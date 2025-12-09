#!/bin/bash

# GhostLink Production Deployment Script
# This script sets up and deploys the complete GhostLink production stack

set -e

echo "🚀 Starting GhostLink Production Deployment..."

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

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    print_success "Docker and Docker Compose are installed"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."

    mkdir -p logs
    mkdir -p data
    mkdir -p monitoring/prometheus
    mkdir -p monitoring/grafana/provisioning/datasources
    mkdir -p monitoring/grafana/provisioning/dashboards
    mkdir -p nginx/ssl

    print_success "Directories created"
}

# Copy environment file if it doesn't exist
setup_environment() {
    if [ ! -f .env ]; then
        print_status "Setting up environment configuration..."
        cp .env.example .env
        print_warning "Please edit .env file with your production values before continuing"
        read -p "Press Enter after editing .env file..."
    else
        print_success "Environment file already exists"
    fi
}

# Build and start services
deploy_services() {
    print_status "Building and starting production services..."

    # Build the images
    docker-compose build --no-cache

    # Start all services
    docker-compose up -d

    print_success "Services deployed successfully"
}

# Wait for services to be healthy
wait_for_services() {
    print_status "Waiting for services to become healthy..."

    # Wait for API server
    max_attempts=30
    attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:3000/health &> /dev/null; then
            print_success "API server is healthy"
            break
        fi

        print_status "Waiting for API server... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done

    if [ $attempt -gt $max_attempts ]; then
        print_error "API server failed to become healthy"
        exit 1
    fi

    # Wait for Grafana
    attempt=1
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:3001/api/health &> /dev/null; then
            print_success "Grafana is healthy"
            break
        fi

        print_status "Waiting for Grafana... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done

    if [ $attempt -gt $max_attempts ]; then
        print_error "Grafana failed to become healthy"
        exit 1
    fi
}

# Setup Grafana admin password
setup_grafana() {
    print_status "Setting up Grafana..."

    # Default password from docker-compose
    GRAFANA_PASSWORD=${GRAFANA_PASSWORD:-ghostlink2025}

    print_success "Grafana setup complete (admin password: $GRAFANA_PASSWORD)"
}

# Display deployment information
show_deployment_info() {
    print_success "🎉 GhostLink Production Deployment Complete!"
    echo ""
    echo "📊 Service Endpoints:"
    echo "   🌐 GhostLink Web Interface: http://localhost"
    echo "   🔧 API Server: http://localhost:3000"
    echo "   📈 Grafana Monitoring: http://localhost:3001 (admin/ghostlink2025)"
    echo "   📊 Prometheus Metrics: http://localhost:9090"
    echo ""
    echo "🔧 Management Commands:"
    echo "   View logs: docker-compose logs -f"
    echo "   Stop services: docker-compose down"
    echo "   Restart services: docker-compose restart"
    echo "   Update services: docker-compose up -d --build"
    echo ""
    echo "📁 Important Files:"
    echo "   Configuration: .env"
    echo "   Logs: ./logs/"
    echo "   Data: ./data/"
    echo "   Monitoring: ./monitoring/"
}

# Main deployment function
main() {
    echo "🔥 GhostLink Production Deployment Script"
    echo "========================================"

    check_docker
    create_directories
    setup_environment
    deploy_services
    wait_for_services
    setup_grafana
    show_deployment_info

    print_success "Deployment completed successfully!"
}

# Run main function
main "$@"
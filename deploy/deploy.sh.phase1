#!/usr/bin/env bash
set -euo pipefail

# GhostLink Deployment Script
# Usage: ./deploy.sh [environment]

ENVIRONMENT="${1:-production}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=== GhostLink Deployment ==="
echo "Environment: ${ENVIRONMENT}"
echo "Project Root: ${PROJECT_ROOT}"
echo ""

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Error: docker not installed"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Error: docker-compose not installed"; exit 1; }

# Load environment-specific config
if [ -f "${SCRIPT_DIR}/config/${ENVIRONMENT}.env" ]; then
    echo "Loading environment config..."
    # shellcheck disable=SC1090
    source "${SCRIPT_DIR}/config/${ENVIRONMENT}.env"
else
    echo "Warning: No config file found for ${ENVIRONMENT}"
fi

# Build images
echo "Building Docker images..."
cd "${PROJECT_ROOT}"
docker-compose -f docker-compose.dev.yml build

# Stop existing services
echo "Stopping existing services..."
docker-compose -f docker-compose.dev.yml down || true

# Start services
echo "Starting services..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for health checks
echo "Waiting for services to be healthy..."
sleep 5

# Health checks
echo "Running health checks..."
CONTROLLER_HEALTH=$(curl -sf http://localhost:9108/metrics >/dev/null && echo "OK" || echo "FAIL")
BACKEND_HEALTH=$(curl -sf http://localhost:8000/health >/dev/null && echo "OK" || echo "FAIL")

echo ""
echo "=== Deployment Status ==="
echo "Controller: ${CONTROLLER_HEALTH}"
echo "Backend: ${BACKEND_HEALTH}"
echo ""

if [ "${CONTROLLER_HEALTH}" = "OK" ] && [ "${BACKEND_HEALTH}" = "OK" ]; then
    echo "✓ Deployment successful!"
    exit 0
else
    echo "✗ Deployment failed - some services unhealthy"
    echo "Checking logs..."
    docker-compose -f docker-compose.dev.yml logs --tail=50
    exit 1
fi

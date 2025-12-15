#!/usr/bin/env bash
set -euo pipefail

# GhostLink Phase 2 Infrastructure Deployment Script
# Usage: ./deploy.sh [environment] [services]

ENVIRONMENT="${1:-development}"
SERVICES="${2:-orchestrator,nats}"  # Default to core services
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "🚀 GhostLink Phase 2 Infrastructure Deployment"
echo "Environment: ${ENVIRONMENT}"
echo "Services: ${SERVICES}"
echo "Project Root: ${PROJECT_ROOT}"
echo ""

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Error: docker not installed"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Error: docker-compose not installed";
exit 1; }

# Load environment-specific config
if [ -f "${SCRIPT_DIR}/config/${ENVIRONMENT}.env" ]; then
    echo "Loading environment config..."
    # shellcheck disable=SC1090
    source "${SCRIPT_DIR}/config/${ENVIRONMENT}.env"
else
    echo "Warning: No config file found for ${ENVIRONMENT}"
fi

# Determine compose file based on environment
case "${ENVIRONMENT}" in
    "development"|"dev")
        COMPOSE_FILE="docker-compose.dev.yml"
        ;;
    "production"|"prod")
        COMPOSE_FILE="docker-compose.yml"
        ;;
    "ci")
        COMPOSE_FILE="docker-compose.ci.yml"
        ;;
    *)
        echo "Error: Unknown environment ${ENVIRONMENT}"
        exit 1
        ;;
esac

# Build images
echo "🏗️  Building Docker images..."
cd "${PROJECT_ROOT}"
docker-compose -f "${COMPOSE_FILE}" build

# Stop existing services
echo "🛑 Stopping existing services..."
docker-compose -f "${COMPOSE_FILE}" down || true

# Start services based on selection
echo "🚀 Starting services: ${SERVICES}"

if [ "${SERVICES}" = "all" ]; then
    # Start all services
    docker-compose -f "${COMPOSE_FILE}" up -d
elif [ "${SERVICES}" = "core" ] || [ "${SERVICES}" = "orchestrator,nats" ]; then
    # Start core services only
    docker-compose -f "${COMPOSE_FILE}" up -d ghostlink-orchestrator nats
else
    # Start specific services
    IFS=',' read -ra SERVICE_ARRAY <<< "${SERVICES}"
    docker-compose -f "${COMPOSE_FILE}" up -d "${SERVICE_ARRAY[@]}"
fi

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Health checks
echo "🔍 Running health checks..."

# Check orchestrator health
if docker-compose -f "${COMPOSE_FILE}" ps ghostlink-orchestrator | grep -q "Up"; then
    echo "Testing cold boot orchestrator..."
    if docker-compose -f "${COMPOSE_FILE}" exec -T ghostlink-orchestrator \
        python3 /app/cold_boot_orchestrator.py health >/dev/null 2>&1; then
        ORCHESTRATOR_HEALTH="✅ PASS"
    else
        ORCHESTRATOR_HEALTH="❌ FAIL"
    fi
else
    ORCHESTRATOR_HEALTH="❌ DOWN"
fi

# Check NATS health
if docker-compose -f "${COMPOSE_FILE}" ps nats | grep -q "Up"; then
    if curl -fsS http://localhost:8222 >/dev/null 2>&1; then
        NATS_HEALTH="✅ PASS"
    else
        NATS_HEALTH="❌ FAIL"
    fi
else
    NATS_HEALTH="❌ DOWN"
fi

# Check Prometheus (if running)
if docker-compose -f "${COMPOSE_FILE}" ps prometheus | grep -q "Up"; then
    if curl -fsS http://localhost:9090/-/healthy >/dev/null 2>&1; then
        PROMETHEUS_HEALTH="✅ PASS"
    else
        PROMETHEUS_HEALTH="❌ FAIL"
    fi
else
    PROMETHEUS_HEALTH="⏸️  SKIP"
fi

# Check Grafana (if running)
if docker-compose -f "${COMPOSE_FILE}" ps grafana | grep -q "Up"; then
    # Give Grafana time to start
    sleep 5
    if curl -fsS http://localhost:3000/api/health >/dev/null 2>&1; then
        GRAFANA_HEALTH="✅ PASS"
    else
        GRAFANA_HEALTH="❌ FAIL"
    fi
else
    GRAFANA_HEALTH="⏸️  SKIP"
fi

# Deployment summary
echo ""
echo "📊 PHASE 2 DEPLOYMENT STATUS"
echo "============================"
echo "Orchestrator: ${ORCHESTRATOR_HEALTH}"
echo "NATS:         ${NATS_HEALTH}"
echo "Prometheus:   ${PROMETHEUS_HEALTH}"
echo "Grafana:      ${GRAFANA_HEALTH}"
echo ""

# Overall assessment
if [ "${ORCHESTRATOR_HEALTH}" = "✅ PASS" ] && [ "${NATS_HEALTH}" = "✅ PASS" ]; then
    echo "🎯 OVERALL RESULT: SUCCESS"
    echo "✅ Phase 2 infrastructure deployed successfully!"
    echo ""
    echo "🌐 Service Endpoints:"
    echo "  Cold Boot Orchestrator: http://localhost:7420"
    echo "  NATS Monitoring:        http://localhost:8222"
    if [ "${PROMETHEUS_HEALTH}" = "✅ PASS" ]; then
        echo "  Prometheus:              http://localhost:9090"
    fi
    if [ "${GRAFANA_HEALTH}" = "✅ PASS" ]; then
        echo "  Grafana:                 http://localhost:3000 (admin/ghostlink)"
    fi
    echo ""
    echo "🧊 Cold Boot Commands:"
    echo "  Health Check:  docker-compose -f ${COMPOSE_FILE} exec ghostlink-orchestrator python3 /app/cold_boot_orchestrator.py health"
    echo "  System Metrics: docker-compose -f ${COMPOSE_FILE} exec ghostlink-orchestrator python3 /app/cold_boot_orchestrator.py task --task-type system_metrics"
    exit 0
else
    echo "❌ OVERALL RESULT: FAILED"
    echo "🔧 Some services failed to start properly"
    echo ""
    echo "🔍 Troubleshooting:"
    echo "  Check logs: docker-compose -f ${COMPOSE_FILE} logs"
    echo "  Restart:    docker-compose -f ${COMPOSE_FILE} restart"
    echo "  Clean up:   docker-compose -f ${COMPOSE_FILE} down"
    exit 1
fi

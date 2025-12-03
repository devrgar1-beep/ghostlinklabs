#!/usr/bin/env bash
# GhostLink Status and Control Script
# Provides quick overview and control of all services

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Service definitions
SERVICES=(
    "ghostlink:8000:GhostLink API"
    "prometheus:9090:Prometheus Monitoring"
    "grafana:3000:Grafana Dashboards"
    "redis:6379:Redis Cache"
    "postgres:5432:PostgreSQL Database"
    "ollama:11434:Ollama AI Models"
    "node-exporter:9100:Node Exporter"
    "cadvisor:8080:cAdvisor Containers"
)

check_service() {
    local service=$1
    local port=$2
    local description=$3

    if curl -s --max-time 2 "http://localhost:$port" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ $description (localhost:$port)${NC}"
        return 0
    else
        echo -e "${RED}❌ $description (localhost:$port)${NC}"
        return 1
    fi
}

check_docker_service() {
    local service_name=$1

    if docker ps --format "table {{.Names}}" | grep -q "^${service_name}$"; then
        echo -e "${GREEN}✅ $service_name${NC}"
        return 0
    else
        echo -e "${RED}❌ $service_name${NC}"
        return 1
    fi
}

show_status() {
    echo -e "${CYAN}🚀 GhostLink Full Agent Orchestration Status${NC}"
    echo "=============================================="

    echo -e "\n${BLUE}📊 Web Services:${NC}"
    local web_up=0
    local total_web=0

    for service in "${SERVICES[@]}"; do
        IFS=':' read -r name port desc <<< "$service"
        ((total_web++))
        if check_service "$name" "$port" "$desc"; then
            ((web_up++))
        fi
    done

    echo -e "\n${BLUE}🐳 Docker Services:${NC}"
    local docker_up=0
    local total_docker=0

    # Check main services
    for service in ghostlink prometheus grafana redis postgres; do
        ((total_docker++))
        if check_docker_service "ghostlink-$service"; then
            ((docker_up++))
        fi
    done

    # Check optional services
    echo -e "\n${BLUE}🔧 Optional Services:${NC}"
    for service in ollama node-exporter cadvisor; do
        if check_docker_service "ghostlink-$service"; then
            ((docker_up++))
        fi
        ((total_docker++))
    done

    echo -e "\n${PURPLE}📈 Summary:${NC}"
    echo "Web Services: $web_up/$total_web running"
    echo "Docker Services: $docker_up/$total_docker running"

    # LM Studio check
    echo -e "\n${BLUE}🤖 Local AI:${NC}"
    if curl -s --max-time 2 "http://localhost:1234/v1/models" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ LM Studio (localhost:1234)${NC}"
    else
        echo -e "${YELLOW}⚠️  LM Studio not detected (start LM Studio app if needed)${NC}"
    fi
}

start_services() {
    echo -e "${CYAN}🚀 Starting GhostLink Services...${NC}"

    cd "$PROJECT_ROOT"

    # Start basic services
    echo "Starting core services..."
    docker-compose up -d

    # Wait a bit for services to start
    sleep 5

    # Check if monitoring should be started
    if [[ "${1:-}" == "--monitoring" ]] || [[ "${1:-}" == "--all" ]]; then
        echo "Starting monitoring services..."
        docker-compose --profile monitoring up -d
    fi

    # Check if LLM services should be started
    if [[ "${1:-}" == "--llm" ]] || [[ "${1:-}" == "--all" ]]; then
        echo "Starting LLM services..."
        docker-compose --profile llm up -d
    fi

    echo -e "${GREEN}✅ Services started!${NC}"
    show_status
}

stop_services() {
    echo -e "${CYAN}🛑 Stopping GhostLink Services...${NC}"

    cd "$PROJECT_ROOT"
    docker-compose down

    echo -e "${GREEN}✅ Services stopped!${NC}"
}

restart_services() {
    echo -e "${CYAN}🔄 Restarting GhostLink Services...${NC}"

    cd "$PROJECT_ROOT"
    docker-compose restart

    echo -e "${GREEN}✅ Services restarted!${NC}"
    show_status
}

show_logs() {
    cd "$PROJECT_ROOT"

    case "${1:-all}" in
        "ghostlink")
            docker-compose logs -f ghostlink
            ;;
        "monitoring")
            docker-compose logs -f prometheus grafana
            ;;
        "database")
            docker-compose logs -f postgres redis
            ;;
        "all"|*)
            docker-compose logs -f
            ;;
    esac
}

show_help() {
    echo "GhostLink Control Script"
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  status              Show status of all services"
    echo "  start [--monitoring|--llm|--all]  Start services"
    echo "  stop                Stop all services"
    echo "  restart             Restart all services"
    echo "  logs [service]      Show logs (ghostlink|monitoring|database|all)"
    echo "  test                Run integration tests"
    echo "  setup               Run full setup"
    echo "  help                Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 status"
    echo "  $0 start --all"
    echo "  $0 logs ghostlink"
    echo "  $0 test"
}

run_tests() {
    echo -e "${CYAN}🧪 Running GhostLink Tests...${NC}"

    cd "$PROJECT_ROOT"

    # Activate virtual environment if it exists
    if [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
    fi

    # Run LM Studio test
    if [[ -f "test_lmstudio.py" ]]; then
        echo "Testing LM Studio integration..."
        python test_lmstudio.py || echo "LM Studio test failed (expected if LM Studio not running)"
    fi

    # Run pytest if available
    if command -v pytest >/dev/null 2>&1; then
        echo "Running pytest..."
        pytest tests/ -v || echo "Some tests failed"
    else
        echo "pytest not found, skipping unit tests"
    fi

    echo -e "${GREEN}✅ Testing complete!${NC}"
}

run_setup() {
    echo -e "${CYAN}⚙️  Running GhostLink Setup...${NC}"

    if [[ -f "setup_full_orchestration.sh" ]]; then
        bash setup_full_orchestration.sh --all
    else
        echo "Setup script not found. Run manual setup."
        exit 1
    fi
}

# Main command handling
case "${1:-status}" in
    "status")
        show_status
        ;;
    "start")
        start_services "${2:-}"
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "logs")
        show_logs "${2:-all}"
        ;;
    "test")
        run_tests
        ;;
    "setup")
        run_setup
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
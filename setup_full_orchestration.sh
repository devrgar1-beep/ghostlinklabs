#!/usr/bin/env bash
set -euo pipefail

# GhostLink Full Agent Orchestration Setup Script
# Automates installation of all dependencies, monitoring, and services

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_ROOT/setup_$(date +%Y%m%d_%H%M%S).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" | tee -a "$LOG_FILE" >&2
}

warn() {
    echo -e "${YELLOW}[WARN] $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}" | tee -a "$LOG_FILE"
}

# Check if running as root (for system-wide installations)
check_root() {
    if [[ $EUID -eq 0 ]]; then
        warn "Running as root - this will install system-wide components"
        return 0
    else
        info "Running as regular user - will install user-local components"
        return 1
    fi
}

# Detect OS and architecture
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v lsb_release >/dev/null 2>&1; then
            OS=$(lsb_release -si | tr '[:upper:]' '[:lower:]')
            VERSION=$(lsb_release -sr)
        elif [[ -f /etc/os-release ]]; then
            . /etc/os-release
            OS=$ID
            VERSION=$VERSION_ID
        else
            OS="linux"
            VERSION="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        VERSION=$(sw_vers -productVersion)
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        OS="windows"
        VERSION="unknown"
    else
        OS="unknown"
        VERSION="unknown"
    fi

    ARCH=$(uname -m)
    info "Detected OS: $OS $VERSION ($ARCH)"
}

# Check package manager availability
check_package_manager() {
    # Check for winget (cross-platform support)
    if command -v winget >/dev/null 2>&1; then
        info "Using winget for package management"
        PACKAGE_MANAGER="winget"
        return 0
    fi

    # Platform-specific package managers
    case "$OS" in
        ubuntu|debian)
            if command -v apt-get >/dev/null 2>&1; then
                PACKAGE_MANAGER="apt"
            fi
            ;;
        centos|rhel|fedora)
            if command -v dnf >/dev/null 2>&1; then
                PACKAGE_MANAGER="dnf"
            elif command -v yum >/dev/null 2>&1; then
                PACKAGE_MANAGER="yum"
            fi
            ;;
        macos)
            if command -v brew >/dev/null 2>&1; then
                PACKAGE_MANAGER="brew"
            fi
            ;;
        *)
            warn "No supported package manager found for $OS"
            return 1
            ;;
    esac

    if [[ -n "$PACKAGE_MANAGER" ]]; then
        info "Using $PACKAGE_MANAGER for package management"
        return 0
    else
        error "No package manager available"
        return 1
    fi
}

# Install system dependencies
install_system_deps() {
    log "Installing system dependencies..."

    case "$PACKAGE_MANAGER" in
        winget)
            log "Installing packages with winget..."
            # winget commands for cross-platform packages
            winget install --id Git.Git --accept-source-agreements --accept-package-agreements
            winget install --id Python.Python.3 --accept-source-agreements --accept-package-agreements
            winget install --id Docker.DockerDesktop --accept-source-agreements --accept-package-agreements
            winget install --id LMStudio.LMStudio --accept-source-agreements --accept-package-agreements
            ;;

        apt)
            sudo apt-get update
            sudo apt-get install -y \
                curl wget git \
                python3 python3-pip python3-venv \
                docker.io docker-compose \
                build-essential \
                libssl-dev libffi-dev python3-dev \
                postgresql-client redis-tools \
                jq htop tree
            ;;

        dnf)
            sudo dnf update -y
            sudo dnf install -y \
                curl wget git \
                python3 python3-pip \
                docker docker-compose \
                gcc openssl-devel python3-devel \
                postgresql redis \
                jq htop tree
            ;;

        yum)
            sudo yum update -y
            sudo yum install -y \
                curl wget git \
                python3 python3-pip \
                docker docker-compose \
                gcc openssl-devel python3-devel \
                postgresql redis \
                jq htop tree
            ;;

        brew)
            brew update
            brew install \
                curl wget git \
                python3 \
                docker docker-compose \
                postgresql redis \
                jq htop tree
            ;;

        *)
            warn "Unsupported package manager: $PACKAGE_MANAGER. Please install dependencies manually."
            return 1
            ;;
    esac

    # Start and enable Docker
    if command -v systemctl >/dev/null 2>&1; then
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker "$USER"
    fi

    log "System dependencies installed successfully"
}

# Setup Python virtual environment
setup_python_env() {
    log "Setting up Python virtual environment..."

    cd "$PROJECT_ROOT"

    # Create virtual environment
    python3 -m venv .venv

    # Activate virtual environment
    source .venv/bin/activate

    # Upgrade pip
    pip install --upgrade pip setuptools wheel

    # Install Python dependencies
    if [[ -f "pyproject.toml" ]]; then
        pip install -e .
    elif [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
    else
        pip install fastapi uvicorn redis sqlalchemy psycopg2-binary
    fi

    # Install development dependencies
    pip install -e .[dev,test,docs]

    log "Python environment setup complete"
}

# Setup Docker services
setup_docker_services() {
    log "Setting up Docker services..."

    cd "$PROJECT_ROOT"

    # Create necessary directories
    mkdir -p data logs models monitoring/grafana/provisioning/datasources monitoring/grafana/provisioning/dashboards

    # Generate environment file if it doesn't exist
    if [[ ! -f ".env" ]]; then
        cat > .env << EOF
# GhostLink Environment Configuration
# Copy this file to .env and customize as needed

# Application Settings
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
DEBUG=false

# Database Settings
DATABASE_URL=sqlite:///./data/ghostlink.db
POSTGRES_PASSWORD=changeme789

# AI Provider API Keys (set these to enable providers)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GROK_API_KEY=
GOOGLE_API_KEY=
LMSTUDIO_BASE_URL=http://lmstudio:1234

# Security Settings
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)

# Monitoring
GRAFANA_PASSWORD=admin
PROMETHEUS_RETENTION=200h

# Redis
REDIS_URL=redis://redis:6379
EOF
        info "Created .env file. Please edit it with your API keys and settings."
    fi

    # Pull Docker images
    docker-compose pull

    log "Docker services setup complete"
}

# Setup monitoring stack
setup_monitoring() {
    log "Setting up monitoring stack..."

    cd "$PROJECT_ROOT"

    # Create monitoring configuration if not exists
    if [[ ! -f "monitoring/prometheus.yml" ]]; then
        cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'ghostlink'
    static_configs:
      - targets: ['ghostlink:9108']
    scrape_interval: 5s
    metrics_path: '/metrics'

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:9187']

  - job_name: 'ollama'
    static_configs:
      - targets: ['ollama:11434']
    scrape_interval: 30s

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'grafana'
    static_configs:
      - targets: ['grafana:3000']
EOF
    fi

    # Setup Grafana provisioning
    mkdir -p monitoring/grafana/provisioning/datasources monitoring/grafana/provisioning/dashboards

    if [[ ! -f "monitoring/grafana/provisioning/datasources/prometheus.yml" ]]; then
        cat > monitoring/grafana/provisioning/datasources/prometheus.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
EOF
    fi

    if [[ ! -f "monitoring/grafana/provisioning/dashboards/dashboards.yml" ]]; then
        cat > monitoring/grafana/provisioning/dashboards/dashboards.yml << 'EOF'
apiVersion: 1

providers:
  - name: 'GhostLink'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
EOF
    fi

    log "Monitoring stack setup complete"
}

# Setup LM Studio integration
setup_lm_studio() {
    log "Setting up LM Studio integration..."

    # Check if LM Studio was installed via package manager
    if command -v lmstudio >/dev/null 2>&1 || [[ -d "/Applications/LM Studio.app" ]] || [[ -d "$HOME/.lmstudio" ]]; then
        info "LM Studio is already installed via package manager."
    else
        info "LM Studio Setup Instructions:"
        echo "1. Download LM Studio from: https://lmstudio.ai/"
        echo "2. Install and launch LM Studio"
    fi

    info "Setup Instructions:"
    echo "1. Launch LM Studio"
    echo "2. Download a model (recommended: llama-2-7b-chat or mistral-7b)"
    echo "3. Load the model in LM Studio"
    echo "4. Go to 'Local Server' tab and click 'Start Server'"
    echo "5. Ensure server is running on port 1234"
    echo "6. Test with: python test_lmstudio.py"

    # Create LM Studio test script if it doesn't exist
    if [[ ! -f "test_lmstudio.py" ]]; then
        cat > test_lmstudio.py << 'EOF'
#!/usr/bin/env python3
"""
LM Studio Integration Test Script
"""
import asyncio
import requests
from ghostlink.core.ai_providers import LMStudioProvider

async def test_lmstudio():
    print("🔗 Testing LM Studio Connection...")
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            print("✅ LM Studio is running!")
            provider = LMStudioProvider()
            models = provider.get_models()
            if models:
                response = await provider.ask("Hello, test message")
                print(f"✅ Response: {response[:100]}...")
        else:
            print("❌ LM Studio not responding")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_lmstudio())
EOF
    fi

    log "LM Studio integration setup complete"
}

# Setup development tools
setup_dev_tools() {
    log "Setting up development tools..."

    cd "$PROJECT_ROOT"

    # Install pre-commit hooks
    if [[ -f ".pre-commit-config.yaml" ]]; then
        pip install pre-commit
        pre-commit install
        info "Pre-commit hooks installed. Run 'pre-commit run --all-files' to test."
    fi

    # Setup git hooks for commit messages
    if command -v git >/dev/null 2>&1 && [[ -d ".git" ]]; then
        # Install commitizen for conventional commits
        pip install commitizen
        info "Commitizen installed. Use 'cz commit' for conventional commits."
    fi

    log "Development tools setup complete"
}

# Create systemd services (Linux only)
setup_systemd_services() {
    if [[ "$OS" != "linux" ]] || ! check_root; then
        return 0
    fi

    log "Setting up systemd services..."

    # Create systemd service for GhostLink
    cat > /etc/systemd/system/ghostlink.service << EOF
[Unit]
Description=GhostLink AI Framework
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_ROOT
ExecStart=$PROJECT_ROOT/.venv/bin/python -m ghostlink.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable ghostlink

    log "Systemd services setup complete"
}

# Main installation function
main() {
    log "🚀 Starting GhostLink Full Agent Orchestration Setup"
    log "Log file: $LOG_FILE"

    detect_os
    check_package_manager

    # Parse command line arguments
    MONITORING=false
    LM_STUDIO=false
    DEV_TOOLS=false
    SYSTEMD=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --monitoring)
                MONITORING=true
                shift
                ;;
            --lm-studio)
                LM_STUDIO=true
                shift
                ;;
            --dev-tools)
                DEV_TOOLS=true
                shift
                ;;
            --systemd)
                SYSTEMD=true
                shift
                ;;
            --all)
                MONITORING=true
                LM_STUDIO=true
                DEV_TOOLS=true
                SYSTEMD=true
                shift
                ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --monitoring    Setup Prometheus and Grafana monitoring"
                echo "  --lm-studio     Setup LM Studio integration"
                echo "  --dev-tools     Setup development tools (pre-commit, etc.)"
                echo "  --systemd       Setup systemd services (Linux only)"
                echo "  --all          Setup everything"
                echo "  --help         Show this help"
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    # Install system dependencies
    install_system_deps

    # Setup Python environment
    setup_python_env

    # Setup Docker services
    setup_docker_services

    # Conditional setups
    if [[ "$MONITORING" == "true" ]]; then
        setup_monitoring
    fi

    if [[ "$LM_STUDIO" == "true" ]]; then
        setup_lm_studio
    fi

    if [[ "$DEV_TOOLS" == "true" ]]; then
        setup_dev_tools
    fi

    if [[ "$SYSTEMD" == "true" ]]; then
        setup_systemd_services
    fi

    log "🎉 GhostLink setup complete!"
    echo ""
    info "Next steps:"
    echo "1. Edit .env file with your API keys"
    echo "2. Start services: docker-compose up -d"
    if [[ "$MONITORING" == "true" ]]; then
        echo "3. Access monitoring:"
        echo "   - Prometheus: http://localhost:9090"
        echo "   - Grafana: http://localhost:3000 (admin/admin)"
    fi
    if [[ "$LM_STUDIO" == "true" ]]; then
        echo "4. Setup LM Studio as described above"
    fi
    echo "5. Access GhostLink: http://localhost:8000"
    echo ""
    info "For help, run: docker-compose logs -f"
}

# Run main function
main "$@"
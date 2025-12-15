# GhostLink System Pipelines

Complete CI/CD, deployment, and monitoring infrastructure for GhostLink platform.

## Components

### 1. CI/CD Pipelines (GitHub Actions)

**CI Pipeline** (`.github/workflows/ci.yml`)
- Lint: ruff, black, isort, pylint
- ShellCheck for shell scripts
- Python tests (3.9, 3.10, 3.11)
- Docker image builds
- Security scanning with Trivy

**CD Pipeline** (`.github/workflows/cd.yml`)
- Build and push to GitHub Container Registry
- Multi-service deployment
- Automated production deployment on tags

### 2. Build Automation (Makefile)

```bash
make help       # Show all targets
make install    # Install dependencies
make test       # Run tests
make lint       # Run linters
make format     # Format code
make build      # Build Docker images
make run        # Run services (Docker)
make run-local  # Run services (local Python)
make stop       # Stop services
make logs       # View logs
make health     # Health checks
```

### 3. Deployment

**Docker Deployment**
```bash
cd deploy
./deploy.sh production
```

**Systemd Services (Linux)**
```bash
cd deploy
sudo ./setup.sh
```

Services created:
- `ghostlink-controller.service`
- `ghostlink-backend.service`

Commands:
```bash
systemctl status ghostlink-controller
systemctl restart ghostlink-backend
journalctl -u ghostlink-controller -f
```

### 4. Monitoring Stack

**Start Monitoring**
```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

Components:
- **Prometheus** (`:9090`) - Metrics collection
- **Grafana** (`:3000`) - Dashboards (admin/admin)
- **Loki** (`:3100`) - Log aggregation
- **Promtail** - Log collection

**Metrics Endpoints**
- Controller: `http://localhost:9108/metrics`
- Backend: `http://localhost:8000/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

### 5. Directory Structure

```
ghostlinklabs-main/
├── .github/workflows/     # CI/CD pipelines
│   ├── ci.yml
│   └── cd.yml
├── deploy/               # Deployment scripts
│   ├── deploy.sh
│   ├── setup.sh
│   ├── systemd/
│   │   ├── ghostlink-controller.service
│   │   └── ghostlink-backend.service
│   └── config/
├── monitoring/           # Monitoring configs
│   ├── prometheus.yml
│   ├── loki-config.yml
│   └── promtail-config.yml
├── Makefile             # Build automation
├── docker-compose.dev.yml        # Development
└── docker-compose.monitoring.yml # Monitoring
```

## Quick Start

### Local Development
```bash
make install
make run-local
make health
```

### Docker Development
```bash
make build
make run
make logs
```

### Production Deployment
```bash
# Via systemd
cd deploy && sudo ./setup.sh

# Via Docker
cd deploy && ./deploy.sh production

# Monitor
docker-compose -f docker-compose.monitoring.yml up -d
```

## Environment Variables

Create `deploy/config/production.env`:
```bash
DOCKER_REGISTRY=ghcr.io/yourusername
DEPLOY_HOST=ghostlink.local
# Or use your actual deployment server:
# DEPLOY_HOST=production.ghostlinklabs.com
GRAFANA_PASSWORD=your-password
```

## GitHub Secrets (for CD)

Required secrets in GitHub repository:
- `DEPLOY_HOST` - Production server hostname
- `DEPLOY_USER` - SSH user
- `DEPLOY_KEY` - SSH private key

## Health Checks

```bash
# Via Makefile
make health

# Manual
curl http://localhost:9108/metrics  # Controller
curl http://localhost:8000/health   # Backend
```

## Logs

```bash
# Docker
make logs

# Systemd
journalctl -u ghostlink-controller -f
journalctl -u ghostlink-backend -f

# Local
tail -f ghostlink_*.log
```

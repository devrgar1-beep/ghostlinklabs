# GhostLink Docker Container Setup Guide

## Overview

This guide helps you deploy GhostLink as a containerized sovereign computing system. GhostLink provides AI capabilities while maintaining complete user control and sovereignty over data and operations.

## Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB+ RAM (8GB recommended)
- 20GB+ storage space

### 1-Minute Deployment

```bash
# Clone and build
git clone https://github.com/ghostlinklabs/ghostlink.git
cd ghostlink

# Build and deploy
./scripts/build.sh build
./scripts/build.sh deploy

# Check status
./scripts/build.sh health
```

Your GhostLink system will be available at:
- **Controller**: http://localhost:8080
- **Console Dashboard**: http://localhost:3001
- **Monitoring**: http://localhost:3000 (Grafana)

## Architecture

### Core Components

1. **Controller** (Port 8080) - Main orchestration service
2. **Neural Node** (Port 8081) - AI processing with offline models
3. **Wired Core** (Port 8082) - Hardware interface and communication
4. **Bridge Service** (Port 8083) - External connectivity (sovereignty-gated)
5. **Console** (Port 3001) - React-based dashboard
6. **Monitoring** (Port 9090/3000) - Prometheus + Grafana

### Data Volumes

- `ghostlink_data` - Main application data
- `ghostlink_vault` - Secure document storage
- `ghostlink_state` - System state and logs
- `ghostlink_keys` - Encrypted credentials (read-only)
- `ghostlink_models` - AI model weights

## Configuration

### Environment Variables

```bash
# Core Settings
GHOSTLINK_MODE=controller          # controller|neural|wired|bridge|all
NEURAL_MODE=offline_local          # offline_local|cloud_bridge
SOVEREIGNTY_GATE=closed            # closed|audit|open

# Network
GHOSTLINK_CONTROLLER_HOST=0.0.0.0
GHOSTLINK_CONTROLLER_PORT=8080

# Security
GHOSTLINK_DATA=/data
LOG_LEVEL=INFO
```

### Sovereignty Gate Modes

- **closed** (default): All external actions blocked
- **audit**: External actions logged, require user approval
- **open**: External actions allowed (NOT recommended)

## Deployment Options

### Standard Deployment

```bash
# Build images
./scripts/build.sh build

# Deploy stack
./scripts/build.sh deploy

# View logs
./scripts/build.sh logs controller
```

### Development Mode

```bash
# Deploy with source code mounting
./scripts/build.sh deploy --dev

# Open shell for debugging
./scripts/build.sh shell controller
```

### Production Deployment

```bash
# Build with registry push
./scripts/build.sh build --tag v7.0.0 --push

# Deploy specific version
GHOSTLINK_VERSION=v7.0.0 ./scripts/build.sh deploy
```

## Security Configuration

### 1. API Keys Setup

```bash
# Create keys directory
mkdir -p ./data/keys
chmod 700 ./data/keys

# Add API keys (if using external services)
echo "OPENAI_API_KEY=your_key_here" > ./data/keys/.env
echo "ANTHROPIC_API_KEY=your_key_here" >> ./data/keys/.env
chmod 600 ./data/keys/.env
```

### 2. SSL/TLS Configuration

```bash
# Generate self-signed certificates (for development)
openssl req -x509 -newkey rsa:4096 -keyout ./configs/ghostlink.key -out ./configs/ghostlink.crt -days 365 -nodes

# For production, use proper certificates
cp your_cert.crt ./configs/ghostlink.crt
cp your_key.key ./configs/ghostlink.key
```

### 3. Network Security

```bash
# Firewall rules (adjust for your network)
sudo ufw allow 22/tcp          # SSH
sudo ufw allow 8080/tcp        # GhostLink Controller
sudo ufw allow 3001/tcp        # Console (if remote access needed)
sudo ufw deny 8081:8083/tcp    # Block direct service access
```

## Raspberry Pi Deployment

### Hardware Requirements

- Raspberry Pi 4B (8GB RAM) or Pi 5
- 64GB+ microSD card or SSD
- Official Pi power supply
- Ethernet connection (recommended)

### Pi-Specific Setup

```bash
# Update Pi OS
sudo apt update && sudo apt full-upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker pi

# Install Docker Compose
sudo apt install docker-compose -y

# Clone and deploy GhostLink
git clone https://github.com/ghostlinklabs/ghostlink.git
cd ghostlink
./scripts/build.sh build
./scripts/build.sh deploy
```

### Pi Optimizations

```bash
# Increase swap for neural processing
sudo dphys-swapfile swapoff
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

# GPU memory split (if using Pi GPU)
echo "gpu_mem=128" | sudo tee -a /boot/config.txt

# Reboot to apply changes
sudo reboot
```

## Usage Examples

### Basic API Usage

```bash
# Health check
curl http://localhost:8080/health

# System status
curl http://localhost:8080/status

# Neural processing (sovereignty-gated)
curl -X POST http://localhost:8080/neural/process \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze this data locally", "data": "..."}'

# Wired command execution
curl -X POST http://localhost:8080/wired/command \
  -H "Content-Type: application/json" \
  -d '{"command": "scan_network", "params": {}}'
```

### Console Dashboard

Navigate to http://localhost:3001 for the interactive dashboard:

- **Lattice Visualization**: Real-time system state visualization
- **Neural Monitor**: AI processing status and controls
- **Command Terminal**: Interactive command interface
- **System Inspector**: Component health and metrics

### Monitoring

Access Grafana at http://localhost:3000:
- Username: `admin`
- Password: `ghostlink`

Pre-configured dashboards:
- GhostLink System Overview
- Neural Node Performance
- Wired Core Network Status
- Sovereignty Gate Activity

## Troubleshooting

### Common Issues

1. **Container won't start**
```bash
# Check logs
./scripts/build.sh logs controller

# Verify permissions
ls -la ./data/
sudo chown -R 1000:1000 ./data/
```

2. **Neural node fails**
```bash
# Check model availability
docker exec ghostlink-neural ls -la /opt/ghostlink/models/

# Verify memory
docker stats ghostlink-neural
```

3. **Sovereignty gate blocks everything**
```bash
# Check gate status
curl http://localhost:8080/sovereignty/check \
  -d '{"action": "test", "context": {}}'

# Temporarily audit mode (CAUTION)
docker exec ghostlink-controller \
  env SOVEREIGNTY_GATE=audit python -m ghostlink.tools.gate_control
```

### Performance Tuning

```bash
# Increase container memory limits
# Edit docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 4G
    reservations:
      memory: 2G

# Optimize neural processing
# Edit configs/neural_config.json:
{
  "max_batch_size": 1,
  "cpu_threads": 4,
  "memory_limit": "2G"
}
```

## Maintenance

### Regular Tasks

```bash
# Update images
./scripts/build.sh build --no-cache
./scripts/build.sh deploy

# Backup data
docker run --rm -v ghostlink_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/ghostlink-backup-$(date +%Y%m%d).tar.gz -C /data .

# View system health
./scripts/build.sh health

# Clean up old containers
docker system prune -f
```

### Updates

```bash
# Pull latest code
git pull origin main

# Rebuild and redeploy
./scripts/build.sh build --no-cache
./scripts/build.sh stop
./scripts/build.sh deploy

# Verify upgrade
curl http://localhost:8080/health
```

## Advanced Configuration

### Multi-Node Setup

For distributed GhostLink deployment across multiple machines:

```bash
# Node 1 (Controller)
GHOSTLINK_MODE=controller ./scripts/build.sh deploy

# Node 2 (Neural)
GHOSTLINK_MODE=neural \
GHOSTLINK_CONTROLLER_URL=http://node1:8080 \
./scripts/build.sh deploy

# Node 3 (Wired)
GHOSTLINK_MODE=wired \
GHOSTLINK_CONTROLLER_URL=http://node1:8080 \
./scripts/build.sh deploy
```

### Custom Neural Models

```bash
# Download custom model
mkdir -p ./models/custom
wget https://huggingface.co/model/pytorch_model.bin -O ./models/custom/

# Update neural config
echo '{"model_path": "/opt/ghostlink/models/custom"}' > ./configs/neural_config.json

# Restart neural service
docker-compose restart ghostlink-neural
```

## Support

For issues and questions:
- **Documentation**: Check the `/docs` directory
- **Logs**: Use `./scripts/build.sh logs` for diagnostics
- **Health**: Use `./scripts/build.sh health` for status
- **Community**: GhostLink Labs forums

## License

GhostLink is released under the MIT License. See LICENSE file for details.
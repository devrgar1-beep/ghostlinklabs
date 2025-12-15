# GhostLink Enterprise Setup Guide

## Overview

This guide provides comprehensive instructions for deploying GhostLink across your enterprise hardware infrastructure consisting of 3 Dell R630 servers, Dell MD3600i storage array, and 3 Synology DS1813+ NAS units.

## Hardware Architecture

### Dell R630 Servers (192.168.1.100-102)
- **R630-1 (192.168.1.100)**: Primary Controller Node
  - Runs main GhostLink API, Redis, PostgreSQL
  - Handles orchestration and coordination
  - 16-64GB RAM, CPU optimized for I/O

- **R630-2 (192.168.1.101)**: Distributed Training Node
  - GPU-accelerated model training
  - Handles autonomous evolution algorithms
  - Maximum RAM and GPU resources

- **R630-3 (192.168.1.102)**: Inference & Serving Node
  - Optimized for model inference
  - Low-latency API responses
  - GPU acceleration for inference

### Storage Infrastructure
- **MD3600i (192.168.1.103)**: Enterprise SAN Storage (96TB)
  - High-performance model storage
  - RAID 6 configuration
  - iSCSI connectivity

- **Synology DS1813+ Cluster (192.168.1.104-106)**: NAS Storage (96TB total)
  - Dataset storage and backups
  - Btrfs filesystem with snapshots
  - NFS/CIFS sharing

## Network Configuration

### IP Address Scheme
```
192.168.1.100  - R630-1 (Controller)
192.168.1.101  - R630-2 (Training)
192.168.1.102  - R630-3 (Inference)
192.168.1.103  - MD3600i Storage
192.168.1.104  - Synology-1
192.168.1.105  - Synology-2
192.168.1.106  - Synology-3
192.168.1.107  - Prometheus
192.168.1.108  - Grafana
192.168.1.109  - Nginx Load Balancer
192.168.1.110  - Redis Controller
192.168.1.111  - PostgreSQL Controller
192.168.1.112  - Ollama Service
```

### Eero 7 Mesh Network Setup
1. Configure static IP reservations for all servers
2. Set up VLAN for enterprise traffic (if supported)
3. Enable port forwarding for external access
4. Configure QoS for AI workloads

## Prerequisites

### System Requirements
- Docker Engine 20.10+
- Docker Compose 2.0+
- NVIDIA Docker support (for GPU nodes)
- 100GB+ free disk space
- 64GB+ RAM per server

### Software Dependencies
```bash
# Install Docker and NVIDIA Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

## Deployment Instructions

### 1. Initial Setup
```bash
# Clone or ensure you're in the GhostLink workspace
cd /path/to/ghostlink

# Make deployment script executable
chmod +x deploy-enterprise.sh
```

### 2. Environment Configuration
Create a `.env` file with your configuration:
```bash
# Database
POSTGRES_PASSWORD=your_secure_password
POSTGRES_USER=ghostlink
POSTGRES_DB=ghostlink

# Redis
REDIS_PASSWORD=your_redis_password

# Grafana
GRAFANA_PASSWORD=your_grafana_password

# API Keys (for external services if needed)
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GROK_API_KEY=your_grok_key
```

### 3. Storage Setup
Configure NFS mounts for enterprise storage:

```bash
# Create mount points
sudo mkdir -p /mnt/models /mnt/datasets

# Add to /etc/fstab for persistent mounts
echo "192.168.1.103:/mnt/models /mnt/models nfs defaults 0 0" | sudo tee -a /etc/fstab
echo "192.168.1.104:/volume1/datasets /mnt/datasets nfs defaults 0 0" | sudo tee -a /etc/fstab

# Mount shares
sudo mount -a
```

### 4. Deploy Services
```bash
# Deploy all services
./deploy-enterprise.sh

# Or deploy specific profiles
./deploy-enterprise.sh --profile training    # Training only
./deploy-enterprise.sh --profile inference   # Inference only
./deploy-enterprise.sh --profile monitoring  # Monitoring only
```

### 5. Verify Deployment
```bash
# Check service status
docker-compose -f docker-compose.enterprise.yml -p ghostlink-enterprise ps

# View logs
docker-compose -f docker-compose.enterprise.yml -p ghostlink-enterprise logs -f

# Test API endpoints
curl http://localhost/health
curl http://localhost/api/docs
```

## Service Architecture

### Core Services
- **GhostLink Controller**: Main orchestration service
- **Training Node**: Distributed model training
- **Inference Node**: Optimized model serving
- **Redis Cluster**: High-performance caching
- **PostgreSQL**: Primary data storage

### Supporting Services
- **Ollama**: Local LLM serving
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards
- **Nginx**: Load balancing and reverse proxy

## Monitoring & Observability

### Accessing Monitoring
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Metrics Endpoint**: http://localhost/api/metrics

### Key Metrics to Monitor
- GPU utilization and memory
- Model training progress
- API response times
- Storage I/O performance
- Network throughput

## Scaling & Management

### Scaling Training Nodes
```bash
# Scale training services
docker-compose -f docker-compose.enterprise.yml -p ghostlink-enterprise up -d --scale ghostlink-trainer=3
```

### Updating Services
```bash
# Pull latest images and restart
docker-compose -f docker-compose.enterprise.yml -p ghostlink-enterprise pull
docker-compose -f docker-compose.enterprise.yml -p ghostlink-enterprise up -d
```

### Backup Strategy
```bash
# Database backup
docker exec ghostlink-postgres pg_dump -U ghostlink ghostlink > backup.sql

# Model backup
rsync -av /mnt/models/ /backup/models/

# Configuration backup
tar -czf config-backup.tar.gz docker-compose.enterprise.yml monitoring/ nginx/
```

## Troubleshooting

### Common Issues

**Services not starting:**
```bash
# Check Docker logs
docker-compose -f docker-compose.enterprise.yml -p ghostlink-enterprise logs

# Verify network
docker network ls
docker network inspect ghostlink-enterprise-br0
```

**GPU not detected:**
```bash
# Check NVIDIA drivers
nvidia-smi

# Verify NVIDIA Docker
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

**Storage mount failures:**
```bash
# Test NFS connectivity
showmount -e 192.168.1.103

# Check mount status
df -h | grep mnt
```

### Performance Optimization

**GPU Memory Issues:**
- Reduce batch sizes in training configurations
- Enable gradient checkpointing
- Use mixed precision training (FP16)

**Network Bottlenecks:**
- Ensure jumbo frames are enabled on switches
- Configure QoS for AI traffic
- Use RDMA if available

**Storage Performance:**
- Configure RAID properly on MD3600i
- Use SSD caching on Synology NAS
- Optimize NFS mount options

## Security Considerations

### Network Security
- Configure firewall rules for enterprise network
- Use VPN for remote access
- Implement network segmentation

### Access Control
- Change default passwords
- Implement role-based access control
- Enable audit logging

### Data Protection
- Encrypt sensitive data at rest
- Implement backup encryption
- Regular security updates

## Next Steps

1. **GPU Installation**: Install NVIDIA GPUs in R630-2 and R630-3
2. **Performance Testing**: Benchmark training and inference performance
3. **Model Development**: Begin sovereign AI model training
4. **Integration Testing**: Test end-to-end workflows
5. **Production Deployment**: Move to production environment

## Support

For issues or questions:
1. Check the logs: `docker-compose logs -f`
2. Review monitoring dashboards
3. Consult the troubleshooting section
4. Check GitHub issues for known problems

---

**Enterprise Deployment Complete** 🎉

Your GhostLink sovereign AI infrastructure is now ready for distributed training and inference across your enterprise hardware cluster.
# GhostLink Production Deployment

This directory contains the complete production deployment configuration for GhostLink, featuring containerized deployment with monitoring, reverse proxy, and automated management scripts.

## 🚀 Quick Start

1. **Prerequisites**
   - Docker and Docker Compose installed
   - At least 4GB RAM available
   - Ports 80, 3000-3001, 9090 available

2. **Deploy Production Stack**

   ```bash
   ./deploy-production.sh
   ```

3. **Access Services**
   - **GhostLink Web Interface**: <http://localhost>
   - **API Server**: <http://localhost:3000>
   - **Grafana Monitoring**: <http://localhost:3001> (admin/ghostlink2025)
   - **Prometheus Metrics**: <http://localhost:9090>

## 📁 Directory Structure

```
ghostlinklabs/
├── docker-compose.yml          # Production service orchestration
├── Dockerfile                  # Production container configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment configuration template
├── deploy-production.sh       # Automated deployment script
├── health-check.sh            # Production health monitoring
├── backup-production.sh       # Automated backup script
├── monitoring/                # Prometheus & Grafana configuration
│   ├── prometheus.yml
│   └── grafana/
│       └── provisioning/
│           ├── datasources/
│           └── dashboards/
├── nginx/                     # Reverse proxy configuration
│   ├── nginx.conf
│   └── ssl/
├── logs/                      # Application logs (created at runtime)
└── data/                      # Application data (created at runtime)
```

## 🛠️ Services Overview

### Core Services

- **ghostlink-api-prod**: FastAPI server with web interface (port 3000)
- **ghostlink-orchestrator-prod**: AI systems coordinator (port 8000)
- **ghostlink**: Core GhostLink controller (host networking)

### Monitoring Stack

- **prometheus**: Metrics collection (port 9090)
- **grafana**: Visualization dashboard (port 3001)

### Infrastructure

- **nginx**: Reverse proxy and load balancer (port 80)

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Application Settings
GHOSTLINK_ENV=production
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=3000
API_WORKERS=4

# Monitoring
GRAFANA_PASSWORD=your-secure-password

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
```

### Docker Compose Services

The `docker-compose.yml` defines all production services with:
- Health checks for service dependencies
- Proper resource limits and restart policies
- Volume mounts for persistent data
- Network isolation with custom bridge network

## 📊 Monitoring & Observability

### Prometheus Metrics
- API server response times and error rates
- AI orchestrator performance metrics
- System resource usage (CPU, memory, disk)
- Custom GhostLink business metrics

### Grafana Dashboards
- Pre-configured GhostLink monitoring dashboard
- Real-time metrics visualization
- Alerting capabilities
- Custom dashboard creation support

Access Grafana at http://localhost:3001 with admin/ghostlink2025

## 🔍 Health Monitoring

Run comprehensive health checks:

```bash
# Basic health check
./health-check.sh

# Detailed health check with logs
./health-check.sh --verbose
```

The health check script verifies:
- All Docker containers are running
- HTTP endpoints are responding
- Service health checks pass
- Resource usage is within limits

## 💾 Backup & Recovery

### Automated Backups

Run scheduled backups:

```bash
./backup-production.sh
```

Creates compressed backups including:
- Application data and logs
- Configuration files
- Docker volumes (Grafana & Prometheus data)
- Backup manifest with restoration instructions

### Manual Backup

```bash
# Stop services
docker-compose down

# Create backup
./backup-production.sh

# Restart services
docker-compose up -d
```

### Restoration

```bash
# Stop services
docker-compose down

# Extract backup
tar xzf backups/ghostlink_backup_20241201_120000.tar.gz -C .

# Restore Docker volumes (if needed)
# ... (follow manifest instructions)

# Restart services
docker-compose up -d
```

## 🔒 Security Features

### Container Security
- Non-root user execution
- Minimal base images
- No privileged containers
- Resource limits enforced

### Network Security
- Nginx reverse proxy with security headers
- Rate limiting on API endpoints
- CORS configuration
- No direct external access to internal services

### Application Security
- Environment-based configuration
- Secret management via environment variables
- Input validation and sanitization
- Secure default settings

## 🚦 Management Commands

### Service Management
```bash
# View service status
docker-compose ps

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart ghostlink-api-prod

# Scale services
docker-compose up -d --scale ghostlink-api-prod=3

# Stop all services
docker-compose down

# Update and redeploy
docker-compose up -d --build
```

### Log Management
```bash
# View specific service logs
docker-compose logs ghostlink-api-prod

# Follow logs in real-time
docker-compose logs -f ghostlink-api-prod

# Export logs for analysis
docker-compose logs ghostlink-api-prod > api_logs.txt
```

### Resource Monitoring
```bash
# View container resource usage
docker stats

# View disk usage
df -h

# View system resources
htop  # or top
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's using ports
   lsof -i :80
   lsof -i :3000

   # Change ports in docker-compose.yml if needed
   ```

2. **Service Startup Failures**
   ```bash
   # Check service logs
   docker-compose logs <service-name>

   # Validate configuration
   docker-compose config
   ```

3. **Resource Constraints**
   ```bash
   # Check system resources
   free -h
   df -h

   # Adjust Docker resource limits in docker-compose.yml
   ```

4. **Network Issues**
   ```bash
   # Check network connectivity
   docker network ls
   docker network inspect ghostlinklabs_ghostlink-network
   ```

### Performance Tuning

- **API Server**: Adjust `API_WORKERS` based on CPU cores
- **Memory**: Monitor and adjust container memory limits
- **Storage**: Configure log rotation and data cleanup
- **Caching**: Implement Redis for session storage if needed

## 📈 Scaling Considerations

### Horizontal Scaling
- Add more API server instances
- Load balance with Nginx upstream
- Shared database for session persistence

### Vertical Scaling
- Increase container resource limits
- Optimize application performance
- Implement caching layers

### High Availability
- Multiple host deployment
- Database replication
- Load balancer configuration
- Automated failover scripts

## 🔄 Updates & Maintenance

### Rolling Updates
```bash
# Update images
docker-compose pull

# Rolling restart
docker-compose up -d --no-deps ghostlink-api-prod
```

### Maintenance Windows
```bash
# Stop services for maintenance
docker-compose down

# Perform maintenance tasks
# ...

# Restart services
docker-compose up -d
```

## 📞 Support

For issues and questions:
1. Check logs: `docker-compose logs`
2. Run health checks: `./health-check.sh`
3. Review configuration files
4. Check system resources
5. Consult monitoring dashboards

## 📝 Changelog

### v1.0.0
- Initial production deployment configuration
- Docker containerization with multi-service orchestration
- Prometheus/Grafana monitoring stack
- Nginx reverse proxy with security headers
- Automated deployment, health check, and backup scripts
- Comprehensive documentation and troubleshooting guides
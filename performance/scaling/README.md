# GhostLink Auto-Scaling Configuration

This directory contains horizontal and vertical scaling configurations for the GhostLink production deployment.

## Scaling Architecture

### Horizontal Scaling
- **API Servers**: Multiple instances behind load balancer
- **AI Orchestrators**: Parallel processing instances
- **Load Balancer**: Nginx with least-connection algorithm

### Vertical Scaling
- **Resource Limits**: Configurable CPU and memory limits
- **Auto-scaling**: Metric-based scaling triggers
- **Resource Monitoring**: Real-time usage tracking

## Configuration Files

### Docker Compose (Scaled)
- `docker-compose-scaled.yml`: Production configuration with scaling
- Multiple replicas for API and orchestrator services
- Resource limits and health checks

### Load Balancer
- `nginx-lb.conf`: Nginx configuration for load balancing
- Upstream server groups with health checks
- Connection pooling and keep-alive

### Monitoring Rules
- `autoscaling-rules.yml`: Prometheus alerting rules for scaling
- CPU, memory, and response time thresholds
- Scale-up and scale-down triggers

## Scaling Management

### Manual Scaling
```bash
# Scale API servers to 3 replicas
./manage-scaling.sh scale ghostlink-api-prod 3

# Scale all services up
./manage-scaling.sh up

# Scale all services down
./manage-scaling.sh down
```

### Auto-Scaling
```bash
# Run auto-scaling check
./manage-scaling.sh auto

# Setup cron job for automatic scaling
echo "*/5 * * * * /path/to/manage-scaling.sh auto" | crontab -
```

### Monitoring Scaling
```bash
# Check current scaling status
./manage-scaling.sh status
```

## Scaling Thresholds

### Scale Up Triggers
- **CPU Usage**: > 70% for 5 minutes
- **Memory Usage**: > 80% for 5 minutes
- **Response Time**: > 2000ms (95th percentile) for 3 minutes
- **AI Memory**: > 85% for AI orchestrator

### Scale Down Triggers
- **Low Utilization**: CPU < 20% AND Memory < 30% for 15 minutes

## Deployment Instructions

### 1. Deploy Scaled Configuration
```bash
# Use the scaled docker-compose file
docker-compose -f performance/scaling/docker-compose-scaled.yml up -d

# Or switch to scaled configuration
cp performance/scaling/docker-compose-scaled.yml docker-compose.yml
docker-compose up -d
```

### 2. Configure Load Balancer
```bash
# The load balancer configuration is included in the scaled setup
# Nginx will automatically distribute requests across API server instances
```

### 3. Setup Monitoring
```bash
# Add scaling rules to Prometheus
cp performance/scaling/autoscaling-rules.yml monitoring/
# Restart Prometheus to pick up new rules
docker-compose restart prometheus
```

### 4. Import Dashboard
```bash
# Import the scaling dashboard into Grafana
# Dashboard JSON: performance/scaling/scaling-dashboard.json
```

## Performance Considerations

### Resource Allocation
- **API Servers**: 0.5-1 CPU core, 512MB-1GB RAM per instance
- **AI Orchestrators**: 1-2 CPU cores, 2-4GB RAM per instance
- **Load Balancer**: Minimal resources, handles routing only

### Network Considerations
- Internal service communication uses Docker networks
- Load balancer handles external traffic distribution
- Health checks ensure only healthy instances receive traffic

### Database Scaling
- Connection pooling is critical for multiple API instances
- Consider read replicas for high read loads
- Monitor connection usage and adjust pool sizes

## Troubleshooting

### Common Issues

1. **Uneven Load Distribution**
   - Check load balancer algorithm (least_conn)
   - Verify health check configurations
   - Monitor individual instance performance

2. **Scaling Not Triggering**
   - Verify Prometheus rules are loaded
   - Check metric collection is working
   - Validate threshold values

3. **Service Discovery Issues**
   - Ensure Docker networks are properly configured
   - Check service dependencies in docker-compose
   - Verify container naming conventions

### Monitoring Commands
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f ghostlink-api-prod

# Monitor resources
docker stats

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets
```

## Best Practices

### Scaling Strategy
1. **Start Small**: Begin with minimal replicas and scale up
2. **Monitor Always**: Keep detailed metrics and logs
3. **Test Scaling**: Regularly test scaling operations
4. **Plan Capacity**: Understand resource requirements

### Maintenance
- Regular performance testing
- Resource usage trend analysis
- Scaling rule optimization
- Capacity planning reviews

### Security
- Maintain security across scaled instances
- Update all instances simultaneously for patches
- Monitor for security events across all instances
- Implement proper access controls

## Advanced Configuration

### Custom Scaling Rules
Edit `autoscaling-rules.yml` to customize scaling thresholds and conditions.

### Resource Limits
Adjust CPU and memory limits in `docker-compose-scaled.yml` based on your infrastructure.

### Load Balancer Tuning
Modify `nginx-lb.conf` for custom load balancing algorithms and timeouts.

## Support

For scaling issues and questions:
- Check service logs: `docker-compose logs`
- Monitor metrics: Grafana dashboards
- Review scaling rules: Prometheus alerts
- Test manually: `./manage-scaling.sh` commands

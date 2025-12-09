#!/bin/bash

# GhostLink Auto-Scaling Configuration Script
# Sets up horizontal and vertical scaling for production deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCALING_DIR="./performance/scaling"
DOCKER_COMPOSE_FILE="docker-compose.yml"
SCALED_COMPOSE_FILE="docker-compose-scaled.yml"

# Scaling thresholds
CPU_THRESHOLD="${CPU_THRESHOLD:-70}"
MEMORY_THRESHOLD="${MEMORY_THRESHOLD:-80}"
RESPONSE_TIME_THRESHOLD="${RESPONSE_TIME_THRESHOLD:-2000}"  # milliseconds

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

# Create scaling directory
setup_scaling_dir() {
    mkdir -p "$SCALING_DIR"
    print_success "Scaling directory created: $SCALING_DIR"
}

# Create horizontal scaling configuration
create_horizontal_scaling() {
    print_status "Creating horizontal scaling configuration..."

    # Create scaled docker-compose file
    cat > "$SCALING_DIR/$SCALED_COMPOSE_FILE" << 'EOF'
version: '3.8'

services:
  ghostlink:
    build: .
    container_name: ghostlink
    restart: unless-stopped
    environment:
      - HOST=127.0.0.1
      - RUN_CONTROLLER=1
      - RUN_PEER=0
      - RUN_BRIDGE=0
      - RUN_MESH=0
      - RUN_RESPONDER=0
    network_mode: host
    volumes:
      - /sys/class/thermal:/sys/class/thermal:ro
      - ./creds:/run/ghostlink:ro
    user: "10001:10001"

  # Horizontally scalable API servers
  ghostlink-api-prod:
    build: .
    environment:
      - GHOSTLINK_ENV=production
      - PYTHONPATH=/app
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
    networks:
      - ghostlink-network

  # Horizontally scalable AI orchestrators
  ghostlink-orchestrator-prod:
    build: .
    command: ["python3", "optimized_ai_orchestrator.py"]
    environment:
      - GHOSTLINK_ENV=production
      - PYTHONPATH=/app
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    deploy:
      replicas: 1
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
    depends_on:
      ghostlink-api-prod:
        condition: service_healthy
    networks:
      - ghostlink-network

  # Load balancer for API servers
  nginx-load-balancer:
    image: nginx:alpine
    container_name: ghostlink-nginx-lb
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx-lb.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./logs/nginx:/var/log/nginx
    restart: unless-stopped
    depends_on:
      - ghostlink-api-prod
    networks:
      - ghostlink-network

  # Monitoring stack (unchanged)
  prometheus:
    image: prom/prometheus:latest
    container_name: ghostlink-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    restart: unless-stopped
    networks:
      - ghostlink-network

  grafana:
    image: grafana/grafana:latest
    container_name: ghostlink-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-ghostlink2025}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    restart: unless-stopped
    depends_on:
      - prometheus
    networks:
      - ghostlink-network

volumes:
  prometheus_data:
  grafana_data:

networks:
  ghostlink-network:
    driver: bridge
EOF

    print_success "Horizontal scaling configuration created"
}

# Create Nginx load balancer configuration
create_nginx_lb_config() {
    print_status "Creating Nginx load balancer configuration..."

    mkdir -p "./nginx"

    cat > "./nginx/nginx-lb.conf" << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Performance
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=static:10m rate=100r/s;

    # Upstream API servers (load balanced)
    upstream ghostlink_api_backends {
        least_conn;
        server ghostlink-api-prod:3000 max_fails=3 fail_timeout=30s;
        # Additional servers will be added dynamically by Docker
        keepalive 32;
    }

    server {
        listen 80;
        server_name localhost;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

        # Load balanced API
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://ghostlink_api_backends;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
            proxy_connect_timeout 5s;
            proxy_send_timeout 10s;
            proxy_read_timeout 10s;
        }

        # Static content (served directly)
        location / {
            limit_req zone=static burst=100 nodelay;
            root /usr/share/nginx/html;
            index index.html;
            try_files $uri $uri/ =404;
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
EOF

    print_success "Nginx load balancer configuration created"
}

# Create auto-scaling monitoring rules
create_autoscaling_rules() {
    print_status "Creating auto-scaling monitoring rules..."

    cat > "$SCALING_DIR/autoscaling-rules.yml" << EOF
groups:
  - name: autoscaling
    rules:
      # Scale up API servers when CPU > threshold
      - alert: HighCPUUsage
        expr: rate(container_cpu_usage_seconds_total{container="ghostlink-api-prod"}[5m]) > $CPU_THRESHOLD
        for: 5m
        labels:
          severity: warning
          service: api
          action: scale_up
        annotations:
          summary: "High CPU usage detected on API servers"
          description: "CPU usage is above ${CPU_THRESHOLD}% for 5 minutes"

      # Scale up API servers when memory > threshold
      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes{container="ghostlink-api-prod"} / container_spec_memory_limit_bytes > $MEMORY_THRESHOLD
        for: 5m
        labels:
          severity: warning
          service: api
          action: scale_up
        annotations:
          summary: "High memory usage detected on API servers"
          description: "Memory usage is above ${MEMORY_THRESHOLD}% for 5 minutes"

      # Scale up when response time > threshold
      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="ghostlink-api"}[5m])) > $RESPONSE_TIME_THRESHOLD
        for: 3m
        labels:
          severity: warning
          service: api
          action: scale_up
        annotations:
          summary: "Slow response times detected"
          description: "95th percentile response time above ${RESPONSE_TIME_THRESHOLD}ms"

      # Scale down when low utilization
      - alert: LowUtilization
        expr: rate(container_cpu_usage_seconds_total{container="ghostlink-api-prod"}[10m]) < 20 AND container_memory_usage_bytes{container="ghostlink-api-prod"} / container_spec_memory_limit_bytes < 30
        for: 15m
        labels:
          severity: info
          service: api
          action: scale_down
        annotations:
          summary: "Low resource utilization detected"
          description: "Resources underutilized, consider scaling down"

      # AI Orchestrator scaling rules
      - alert: HighAIMemoryUsage
        expr: container_memory_usage_bytes{container="ghostlink-orchestrator-prod"} / container_spec_memory_limit_bytes > 85
        for: 3m
        labels:
          severity: critical
          service: orchestrator
          action: scale_up
        annotations:
          summary: "AI Orchestrator high memory usage"
          description: "AI Orchestrator memory usage above 85%"

      # Database connection pool alerts
      - alert: HighDBConnections
        expr: db_connections_active > 80
        for: 2m
        labels:
          severity: warning
          service: database
          action: scale_up
        annotations:
          summary: "High database connection usage"
          description: "Database connections above 80% capacity"
EOF

    print_success "Auto-scaling monitoring rules created"
}

# Create scaling management script
create_scaling_manager() {
    print_status "Creating scaling management script..."

    cat > "$SCALING_DIR/manage-scaling.sh" << 'EOF'
#!/bin/bash

# GhostLink Scaling Management Script
# Manual and automated scaling operations

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get current scale
get_current_scale() {
    local service=$1
    docker service ls | grep "$service" | awk '{print $4}' || echo "Service not found"
}

# Scale service manually
scale_service() {
    local service=$1
    local replicas=$2

    print_status "Scaling $service to $replicas replicas..."

    if command -v docker &> /dev/null && docker compose version &> /dev/null; then
        docker compose up -d --scale "$service=$replicas"
    else
        print_error "Docker Compose not available"
        exit 1
    fi

    print_success "$service scaled to $replicas replicas"
}

# Auto-scale based on metrics
auto_scale() {
    print_status "Checking auto-scaling conditions..."

    # Check CPU usage
    local cpu_usage=$(docker stats --no-stream --format "{{.CPUPerc}}" ghostlink-api-prod 2>/dev/null | sed 's/%//' | head -1)

    if [ -n "$cpu_usage" ] && [ "$(echo "$cpu_usage > 70" | bc -l)" -eq 1 ]; then
        print_warning "High CPU usage detected ($cpu_usage%), scaling up..."
        scale_service "ghostlink-api-prod" 3
    elif [ -n "$cpu_usage" ] && [ "$(echo "$cpu_usage < 20" | bc -l)" -eq 1 ]; then
        print_status "Low CPU usage detected ($cpu_usage%), scaling down..."
        scale_service "ghostlink-api-prod" 1
    else
        print_success "CPU usage normal ($cpu_usage%)"
    fi

    # Check memory usage
    local mem_usage=$(docker stats --no-stream --format "{{.MemPerc}}" ghostlink-api-prod 2>/dev/null | sed 's/%//' | head -1)

    if [ -n "$mem_usage" ] && [ "$(echo "$mem_usage > 80" | bc -l)" -eq 1 ]; then
        print_warning "High memory usage detected ($mem_usage%), scaling up..."
        scale_service "ghostlink-api-prod" 3
    fi
}

# Show scaling status
show_status() {
    print_status "Current scaling status:"

    echo "API Servers:"
    get_current_scale "ghostlink-api-prod"

    echo "AI Orchestrators:"
    get_current_scale "ghostlink-orchestrator-prod"

    echo ""
    echo "Container Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "Docker stats not available"
}

# Main function
main() {
    case "${1:-status}" in
        "status")
            show_status
            ;;
        "scale")
            if [ -z "$2" ] || [ -z "$3" ]; then
                echo "Usage: $0 scale <service> <replicas>"
                exit 1
            fi
            scale_service "$2" "$3"
            ;;
        "auto")
            auto_scale
            ;;
        "up")
            print_status "Scaling up all services..."
            scale_service "ghostlink-api-prod" 3
            scale_service "ghostlink-orchestrator-prod" 2
            ;;
        "down")
            print_status "Scaling down all services..."
            scale_service "ghostlink-api-prod" 1
            scale_service "ghostlink-orchestrator-prod" 1
            ;;
        *)
            echo "Usage: $0 [status|scale|auto|up|down]"
            echo "  status  - Show current scaling status"
            echo "  scale   - Scale specific service (scale <service> <replicas>)"
            echo "  auto    - Auto-scale based on metrics"
            echo "  up      - Scale up all services"
            echo "  down    - Scale down all services"
            exit 1
            ;;
    esac
}

main "$@"
EOF

    chmod +x "$SCALING_DIR/manage-scaling.sh"

    print_success "Scaling management script created"
}

# Create resource monitoring dashboard
create_monitoring_dashboard() {
    print_status "Creating scaling monitoring dashboard..."

    cat > "$SCALING_DIR/scaling-dashboard.json" << 'EOF'
{
  "dashboard": {
    "title": "GhostLink Scaling Dashboard",
    "tags": ["ghostlink", "scaling", "performance"],
    "timezone": "browser",
    "panels": [
      {
        "title": "API Server CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(container_cpu_usage_seconds_total{container=\"ghostlink-api-prod\"}[5m]) * 100",
            "legendFormat": "CPU Usage %"
          }
        ]
      },
      {
        "title": "API Server Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "container_memory_usage_bytes{container=\"ghostlink-api-prod\"} / container_spec_memory_limit_bytes * 100",
            "legendFormat": "Memory Usage %"
          }
        ]
      },
      {
        "title": "Response Time (95th percentile)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"ghostlink-api\"}[5m])) * 1000",
            "legendFormat": "Response Time (ms)"
          }
        ]
      },
      {
        "title": "Active Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "nginx_connections_active",
            "legendFormat": "Active Connections"
          }
        ]
      },
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100",
            "legendFormat": "Error Rate %"
          }
        ]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
EOF

    print_success "Scaling monitoring dashboard created"
}

# Create scaling documentation
create_scaling_docs() {
    print_status "Creating scaling documentation..."

    cat > "$SCALING_DIR/README.md" << 'EOF'
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
EOF

    print_success "Scaling documentation created"
}

# Main scaling configuration function
main() {
    echo "⚖️ GhostLink Auto-Scaling Configuration"
    echo "======================================"

    setup_scaling_dir

    print_status "Creating comprehensive scaling configuration..."

    create_horizontal_scaling
    create_nginx_lb_config
    create_autoscaling_rules
    create_scaling_manager
    create_monitoring_dashboard
    create_scaling_docs

    print_success "🎉 Auto-scaling configuration completed!"
    print_status "📁 Scaling files created in: $SCALING_DIR"
    print_status "🚀 Deploy scaled configuration:"
    echo "   docker-compose -f $SCALING_DIR/$SCALED_COMPOSE_FILE up -d"
    print_status "📊 Monitor scaling:"
    echo "   ./$SCALING_DIR/manage-scaling.sh status"
    print_status "📚 Documentation: $SCALING_DIR/README.md"
}

# Run main function
main "$@"
EOF

    chmod +x "$SCALING_DIR/setup-scaling.sh"

    print_success "Auto-scaling configuration script created"
}

# Main scaling configuration function
main() {
    echo "⚖️ GhostLink Auto-Scaling Configuration"
    echo "======================================"

    setup_scaling_dir

    print_status "Creating comprehensive scaling configuration..."

    create_horizontal_scaling
    create_nginx_lb_config
    create_autoscaling_rules
    create_scaling_manager
    create_monitoring_dashboard
    create_scaling_docs

    print_success "🎉 Auto-scaling configuration completed!"
    print_status "📁 Scaling files created in: $SCALING_DIR"
    print_status "🚀 Deploy scaled configuration:"
    echo "   docker-compose -f $SCALING_DIR/$SCALED_COMPOSE_FILE up -d"
    print_status "📊 Monitor scaling:"
    echo "   ./$SCALING_DIR/manage-scaling.sh status"
    print_status "📚 Documentation: $SCALING_DIR/README.md"
}

# Run main function
main "$@"
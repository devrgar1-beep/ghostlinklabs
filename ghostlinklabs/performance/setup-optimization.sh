#!/bin/bash

# GhostLink Performance Optimization Script
# Implements caching, connection pooling, and performance optimizations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
OPTIMIZATION_DIR="./performance/optimization"
CACHE_DIR="./cache"
LOGS_DIR="./logs"

# Performance thresholds
MAX_RESPONSE_TIME="${MAX_RESPONSE_TIME:-1000}"  # milliseconds
MIN_CACHE_HIT_RATIO="${MIN_CACHE_HIT_RATIO:-0.8}"
MAX_MEMORY_USAGE="${MAX_MEMORY_USAGE:-85}"  # percentage

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

# Create optimization directory structure
setup_optimization_dirs() {
    mkdir -p "$OPTIMIZATION_DIR"
    mkdir -p "$CACHE_DIR/redis"
    mkdir -p "$CACHE_DIR/nginx"
    mkdir -p "$LOGS_DIR/performance"
    print_success "Optimization directories created"
}

# Create Redis caching configuration
create_redis_config() {
    print_status "Creating Redis caching configuration..."

    cat > "$OPTIMIZATION_DIR/redis.conf" << 'EOF'
# GhostLink Redis Configuration for Performance Caching

# Network
bind 127.0.0.1
port 6379
timeout 0
tcp-keepalive 300

# General
daemonize yes
supervised no
loglevel notice
logfile /var/log/redis/redis.log

# Snapshotting
save 900 1
save 300 10
save 60 10000

# Security
# requirepass yourpasswordhere

# Memory management
maxmemory 256mb
maxmemory-policy allkeys-lru

# Append only file
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

# Disable dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command SHUTDOWN SHUTDOWN_REDIS

# Performance optimizations
tcp-backlog 511
databases 16
EOF

    print_success "Redis configuration created"
}

# Create Nginx caching configuration
create_nginx_cache_config() {
    print_status "Creating Nginx caching configuration..."

    cat > "$OPTIMIZATION_DIR/nginx-cache.conf" << 'EOF'
# GhostLink Nginx Caching Configuration

# Cache settings
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=ghostlink_cache:10m max_size=1g inactive=60m use_temp_path=off;

# Cache key
proxy_cache_key "$scheme$request_method$host$request_uri";

# Upstream with caching
upstream ghostlink_api_cached {
    least_conn;
    server ghostlink-api-prod:3000;
    keepalive 32;
}

server {
    listen 80;
    server_name localhost;

    # SSL configuration (if needed)
    # listen 443 ssl http2;
    # ssl_certificate /etc/nginx/ssl/cert.pem;
    # ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # API endpoints with caching
    location /api/v1/health {
        proxy_pass http://ghostlink_api_cached;
        proxy_cache ghostlink_cache;
        proxy_cache_valid 200 10s;
        proxy_cache_use_stale error timeout invalid_header updating;
        add_header X-Cache-Status $upstream_cache_status;
    }

    location /api/v1/status {
        proxy_pass http://ghostlink_api_cached;
        proxy_cache ghostlink_cache;
        proxy_cache_valid 200 30s;
        proxy_cache_use_stale error timeout invalid_header updating;
        add_header X-Cache-Status $upstream_cache_status;
    }

    # Dynamic API endpoints (no caching)
    location /api/v1/ {
        proxy_pass http://ghostlink_api_cached;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
        add_header X-Cache-Status "BYPASS";
    }

    # Static content caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Cache-Status "STATIC";
    }

    # Health check (no caching)
    location /health {
        access_log off;
        proxy_pass http://ghostlink_api_cached/health;
        add_header X-Cache-Status "BYPASS";
    }
}
EOF

    print_success "Nginx caching configuration created"
}

# Create connection pooling configuration
create_connection_pool_config() {
    print_status "Creating connection pooling configuration..."

    cat > "$OPTIMIZATION_DIR/connection-pool.py" << 'EOF'
"""
GhostLink Connection Pooling Configuration
Optimizes database and external service connections
"""

import asyncio
import aiomysql
import aiohttp
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ConnectionPoolManager:
    """Manages connection pools for optimal performance"""

    def __init__(self):
        self.db_pool: Optional[aiomysql.Pool] = None
        self.http_session: Optional[aiohttp.ClientSession] = None
        self.redis_pool = None

    async def init_db_pool(self, host: str = 'localhost', port: int = 3306,
                          user: str = 'ghostlink', password: str = '',
                          db: str = 'ghostlink', minsize: int = 5, maxsize: int = 20):
        """Initialize database connection pool"""
        try:
            self.db_pool = await aiomysql.create_pool(
                host=host,
                port=port,
                user=user,
                password=password,
                db=db,
                minsize=minsize,
                maxsize=maxsize,
                autocommit=True,
                pool_recycle=3600  # Recycle connections every hour
            )
            logger.info(f"Database connection pool initialized (min: {minsize}, max: {maxsize})")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise

    async def init_http_session(self, connector: Optional[aiohttp.TCPConnector] = None):
        """Initialize HTTP client session with connection pooling"""
        if connector is None:
            connector = aiohttp.TCPConnector(
                limit=100,  # Max concurrent connections
                limit_per_host=10,  # Max connections per host
                ttl_dns_cache=300,  # DNS cache TTL
                use_dns_cache=True,
                keepalive_timeout=60,
                enable_cleanup_closed=True
            )

        self.http_session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30, connect=10)
        )
        logger.info("HTTP session with connection pooling initialized")

    async def init_redis_pool(self, host: str = 'localhost', port: int = 6379,
                             db: int = 0, minsize: int = 5, maxsize: int = 20):
        """Initialize Redis connection pool"""
        try:
            import aioredis
            self.redis_pool = aioredis.ConnectionPool(
                host=host,
                port=port,
                db=db,
                minsize=minsize,
                maxsize=maxsize,
                retry_on_timeout=True
            )
            logger.info(f"Redis connection pool initialized (min: {minsize}, max: {maxsize})")
        except ImportError:
            logger.warning("aioredis not available, Redis pooling disabled")
        except Exception as e:
            logger.error(f"Failed to initialize Redis pool: {e}")
            raise

    async def get_db_connection(self):
        """Get database connection from pool"""
        if not self.db_pool:
            raise RuntimeError("Database pool not initialized")
        return await self.db_pool.acquire()

    async def release_db_connection(self, conn):
        """Release database connection back to pool"""
        if self.db_pool:
            self.db_pool.release(conn)

    async def close_all(self):
        """Close all connection pools"""
        if self.db_pool:
            self.db_pool.close()
            await self.db_pool.wait_closed()

        if self.http_session:
            await self.http_session.close()

        if self.redis_pool:
            await self.redis_pool.disconnect()

        logger.info("All connection pools closed")

# Global connection pool manager instance
pool_manager = ConnectionPoolManager()

async def init_connection_pools():
    """Initialize all connection pools"""
    await pool_manager.init_db_pool()
    await pool_manager.init_http_session()
    await pool_manager.init_redis_pool()

async def cleanup_connection_pools():
    """Cleanup all connection pools"""
    await pool_manager.close_all()

# Context manager for database connections
class DatabaseConnection:
    """Context manager for database connections"""

    def __init__(self):
        self.conn = None

    async def __aenter__(self):
        self.conn = await pool_manager.get_db_connection()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            await pool_manager.release_db_connection(self.conn)

# Optimized query execution with connection pooling
async def execute_query(query: str, params: tuple = None) -> list:
    """Execute database query using connection pool"""
    async with DatabaseConnection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query, params or ())
            return await cursor.fetchall()

async def execute_query_single(query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
    """Execute query and return single result"""
    async with DatabaseConnection() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query, params or ())
            return await cursor.fetchone()
EOF

    print_success "Connection pooling configuration created"
}

# Create performance monitoring middleware
create_performance_monitoring() {
    print_status "Creating performance monitoring middleware..."

    cat > "$OPTIMIZATION_DIR/performance-monitor.py" << 'EOF'
"""
GhostLink Performance Monitoring Middleware
Monitors response times, cache hit ratios, and system performance
"""

import time
import logging
import psutil
from functools import wraps
from typing import Dict, Any, Optional
import asyncio
from collections import defaultdict, deque
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitors application performance metrics"""

    def __init__(self, max_samples: int = 1000):
        self.response_times = deque(maxlen=max_samples)
        self.cache_hits = 0
        self.cache_misses = 0
        self.request_count = 0
        self.error_count = 0
        self.start_time = time.time()
        self.endpoint_stats = defaultdict(lambda: {'count': 0, 'total_time': 0, 'errors': 0})

    def record_request(self, endpoint: str, response_time: float, status_code: int):
        """Record request metrics"""
        self.response_times.append(response_time)
        self.request_count += 1
        self.endpoint_stats[endpoint]['count'] += 1
        self.endpoint_stats[endpoint]['total_time'] += response_time

        if status_code >= 400:
            self.error_count += 1
            self.endpoint_stats[endpoint]['errors'] += 1

    def record_cache_hit(self):
        """Record cache hit"""
        self.cache_hits += 1

    def record_cache_miss(self):
        """Record cache miss"""
        self.cache_misses += 1

    @property
    def cache_hit_ratio(self) -> float:
        """Calculate cache hit ratio"""
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

    @property
    def average_response_time(self) -> float:
        """Calculate average response time"""
        return sum(self.response_times) / len(self.response_times) if self.response_times else 0.0

    @property
    def p95_response_time(self) -> float:
        """Calculate 95th percentile response time"""
        if not self.response_times:
            return 0.0
        sorted_times = sorted(self.response_times)
        index = int(len(sorted_times) * 0.95)
        return sorted_times[min(index, len(sorted_times) - 1)]

    @property
    def error_rate(self) -> float:
        """Calculate error rate"""
        return self.error_count / self.request_count if self.request_count > 0 else 0.0

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_connections': len(psutil.net_connections()),
            'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
        }

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        uptime = time.time() - self.start_time

        return {
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': uptime,
            'requests_total': self.request_count,
            'errors_total': self.error_count,
            'error_rate': self.error_rate,
            'average_response_time_ms': self.average_response_time * 1000,
            'p95_response_time_ms': self.p95_response_time * 1000,
            'cache_hit_ratio': self.cache_hit_ratio,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'endpoint_stats': dict(self.endpoint_stats),
            'system_metrics': self.get_system_metrics(),
            'requests_per_second': self.request_count / uptime if uptime > 0 else 0
        }

    def log_performance_report(self):
        """Log current performance metrics"""
        report = self.get_performance_report()
        logger.info(f"Performance Report: {json.dumps(report, indent=2)}")

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def monitor_performance(endpoint: str = None):
    """Decorator to monitor endpoint performance"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status_code = 200
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status_code = 500
                raise
            finally:
                response_time = time.time() - start_time
                actual_endpoint = endpoint or f"{func.__module__}.{func.__name__}"
                performance_monitor.record_request(actual_endpoint, response_time, status_code)

        return wrapper
    return decorator

def monitor_cache(operation: str):
    """Decorator to monitor cache operations"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                if operation == 'get' and result is not None:
                    performance_monitor.record_cache_hit()
                elif operation == 'get' and result is None:
                    performance_monitor.record_cache_miss()
                return result
            except Exception as e:
                logger.error(f"Cache {operation} error: {e}")
                raise

        return wrapper
    return decorator

# Background performance monitoring task
async def performance_monitoring_task(interval: int = 60):
    """Background task to periodically log performance metrics"""
    while True:
        try:
            performance_monitor.log_performance_report()

            # Check performance thresholds
            if performance_monitor.average_response_time * 1000 > 1000:  # 1 second
                logger.warning(".2f")

            if performance_monitor.error_rate > 0.05:  # 5% error rate
                logger.warning(".2%")

            if performance_monitor.cache_hit_ratio < 0.7:  # 70% cache hit ratio
                logger.warning(".2%")

        except Exception as e:
            logger.error(f"Performance monitoring error: {e}")

        await asyncio.sleep(interval)

# Performance optimization suggestions
def get_optimization_suggestions() -> list:
    """Generate performance optimization suggestions based on metrics"""
    suggestions = []

    if performance_monitor.average_response_time * 1000 > 500:
        suggestions.append("Consider implementing response caching for slow endpoints")

    if performance_monitor.cache_hit_ratio < 0.8:
        suggestions.append("Cache hit ratio is low, review caching strategy")

    if performance_monitor.error_rate > 0.01:
        suggestions.append("High error rate detected, investigate error sources")

    system_metrics = performance_monitor.get_system_metrics()
    if system_metrics['cpu_percent'] > 80:
        suggestions.append("High CPU usage, consider horizontal scaling")

    if system_metrics['memory_percent'] > 85:
        suggestions.append("High memory usage, optimize memory allocation")

    return suggestions
EOF

    print_success "Performance monitoring middleware created"
}

# Create optimized Docker configuration
create_optimized_docker_config() {
    print_status "Creating optimized Docker configuration..."

    cat > "$OPTIMIZATION_DIR/docker-compose-optimized.yml" << 'EOF'
version: '3.8'

services:
  # Redis caching layer
  redis:
    image: redis:7-alpine
    container_name: ghostlink-redis
    restart: unless-stopped
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./cache/redis:/data
      - ./performance/optimization/redis.conf:/etc/redis/redis.conf
      - ./logs/redis:/var/log/redis
    ports:
      - "6379:6379"
    networks:
      - ghostlink-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # Optimized API server with caching
  ghostlink-api-optimized:
    build: .
    container_name: ghostlink-api-opt
    restart: unless-stopped
    environment:
      - GHOSTLINK_ENV=production
      - REDIS_URL=redis://redis:6379
      - PYTHONPATH=/app
      - GUNICORN_WORKERS=4
      - GUNICORN_THREADS=2
      - GUNICORN_WORKER_TIMEOUT=30
      - GUNICORN_KEEP_ALIVE=10
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      - ./performance/optimization:/app/optimization
    ports:
      - "3000:3000"
    depends_on:
      redis:
        condition: service_healthy
    networks:
      - ghostlink-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G

  # Optimized AI orchestrator
  ghostlink-orchestrator-optimized:
    build: .
    command: ["python3", "optimized_ai_orchestrator.py"]
    container_name: ghostlink-orchestrator-opt
    restart: unless-stopped
    environment:
      - GHOSTLINK_ENV=production
      - REDIS_URL=redis://redis:6379
      - PYTHONPATH=/app
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      - ./performance/optimization:/app/optimization
    depends_on:
      ghostlink-api-optimized:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - ghostlink-network
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
        reservations:
          cpus: '2.0'
          memory: 4G

  # Nginx with caching
  nginx-optimized:
    image: nginx:alpine
    container_name: ghostlink-nginx-opt
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./performance/optimization/nginx-cache.conf:/etc/nginx/conf.d/default.conf
      - ./cache/nginx:/var/cache/nginx
      - ./logs/nginx:/var/log/nginx
      - ./nginx/ssl:/etc/nginx/ssl
    restart: unless-stopped
    depends_on:
      - ghostlink-api-optimized
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

    print_success "Optimized Docker configuration created"
}

# Create optimization management script
create_optimization_manager() {
    print_status "Creating optimization management script..."

    cat > "$OPTIMIZATION_DIR/manage-optimization.sh" << 'EOF'
#!/bin/bash

# GhostLink Performance Optimization Manager
# Manages caching, connection pooling, and performance optimizations

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

# Check system performance
check_performance() {
    print_status "Checking current system performance..."

    # CPU usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    echo "CPU Usage: ${cpu_usage}%"

    # Memory usage
    mem_usage=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')
    echo "Memory Usage: ${mem_usage}%"

    # Disk usage
    disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    echo "Disk Usage: ${disk_usage}%"

    # Network connections
    net_connections=$(netstat -tun | grep ESTABLISHED | wc -l)
    echo "Network Connections: ${net_connections}"

    # Check if services are running
    if command -v docker &> /dev/null && docker ps | grep -q ghostlink; then
        echo "Docker Services: Running"
    else
        echo "Docker Services: Not running or not accessible"
    fi

    if pgrep -f "redis-server" > /dev/null; then
        echo "Redis: Running"
    else
        echo "Redis: Not running"
    fi
}

# Optimize system settings
optimize_system() {
    print_status "Optimizing system settings..."

    # Increase file descriptors
    if [ "$(ulimit -n)" -lt 65536 ]; then
        ulimit -n 65536 2>/dev/null || print_warning "Could not increase file descriptors (need root)"
    fi

    # Optimize kernel parameters (requires root)
    if [ "$EUID" -eq 0 ]; then
        # Network optimizations
        sysctl -w net.core.somaxconn=65536 >/dev/null 2>&1
        sysctl -w net.ipv4.tcp_max_syn_backlog=65536 >/dev/null 2>&1
        sysctl -w net.ipv4.ip_local_port_range="1024 65535" >/dev/null 2>&1

        # Memory optimizations
        sysctl -w vm.swappiness=10 >/dev/null 2>&1
        sysctl -w vm.dirty_ratio=60 >/dev/null 2>&1
        sysctl -w vm.dirty_background_ratio=2 >/dev/null 2>&1

        print_success "System optimizations applied"
    else
        print_warning "System optimizations require root privileges"
    fi
}

# Clear caches
clear_caches() {
    print_status "Clearing performance caches..."

    # Clear system cache (requires root)
    if [ "$EUID" -eq 0 ]; then
        sync
        echo 3 > /proc/sys/vm/drop_caches
        print_success "System caches cleared"
    else
        print_warning "System cache clearing requires root privileges"
    fi

    # Clear Redis cache
    if command -v redis-cli &> /dev/null; then
        redis-cli FLUSHALL >/dev/null 2>&1 && print_success "Redis cache cleared" || print_warning "Could not clear Redis cache"
    fi

    # Clear Nginx cache
    if [ -d "./cache/nginx" ]; then
        rm -rf ./cache/nginx/* && print_success "Nginx cache cleared" || print_warning "Could not clear Nginx cache"
    fi
}

# Monitor performance in real-time
monitor_performance() {
    print_status "Starting real-time performance monitoring (Ctrl+C to stop)..."

    while true; do
        echo "=== Performance Snapshot $(date) ==="
        echo "CPU: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')%"
        echo "Memory: $(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')%"
        echo "Load: $(uptime | awk -F'load average:' '{ print $2 }')"
        echo "Connections: $(netstat -tun | grep ESTABLISHED | wc -l)"
        echo ""

        if command -v docker &> /dev/null; then
            echo "Docker Containers:"
            docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "No containers running"
            echo ""
        fi

        sleep 5
    done
}

# Generate performance report
generate_report() {
    print_status "Generating performance optimization report..."

    report_file="./logs/performance/optimization-report-$(date +%Y%m%d-%H%M%S).txt"

    {
        echo "GhostLink Performance Optimization Report"
        echo "Generated: $(date)"
        echo "=========================================="
        echo ""

        echo "System Information:"
        echo "-------------------"
        uname -a
        echo "CPU Cores: $(nproc)"
        echo "Total Memory: $(free -h | grep Mem | awk '{print $2}')"
        echo ""

        echo "Current Performance Metrics:"
        echo "----------------------------"
        echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')%"
        echo "Memory Usage: $(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')%"
        echo "Disk Usage: $(df / | tail -1 | awk '{print $5}')"
        echo "Network Connections: $(netstat -tun | grep ESTABLISHED | wc -l)"
        echo ""

        if command -v docker &> /dev/null; then
            echo "Docker Performance:"
            echo "-------------------"
            docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}" 2>/dev/null || echo "No containers accessible"
            echo ""
        fi

        echo "Optimization Recommendations:"
        echo "----------------------------"

        cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
        if (( $(echo "$cpu_usage > 80" | bc -l) )); then
            echo "- High CPU usage detected. Consider horizontal scaling or optimizing CPU-intensive operations."
        fi

        mem_usage=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')
        if (( $(echo "$mem_usage > 85" | bc -l) )); then
            echo "- High memory usage detected. Consider increasing memory limits or optimizing memory usage."
        fi

        disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
        if [ "$disk_usage" -gt 90 ]; then
            echo "- High disk usage detected. Consider cleanup or increasing disk space."
        fi

        echo "- Ensure Redis caching is enabled and properly configured."
        echo "- Verify Nginx caching is active and cache hit ratios are monitored."
        echo "- Check connection pooling is implemented for database connections."
        echo "- Monitor application logs for performance bottlenecks."

    } > "$report_file"

    print_success "Performance report generated: $report_file"
}

# Main function
main() {
    case "${1:-status}" in
        "status")
            check_performance
            ;;
        "optimize")
            optimize_system
            ;;
        "clear-cache")
            clear_caches
            ;;
        "monitor")
            monitor_performance
            ;;
        "report")
            generate_report
            ;;
        "all")
            check_performance
            echo ""
            optimize_system
            echo ""
            clear_caches
            echo ""
            generate_report
            ;;
        *)
            echo "Usage: $0 [status|optimize|clear-cache|monitor|report|all]"
            echo "  status      - Check current performance status"
            echo "  optimize    - Apply system optimizations"
            echo "  clear-cache - Clear all caches"
            echo "  monitor     - Real-time performance monitoring"
            echo "  report      - Generate performance report"
            echo "  all         - Run all optimization tasks"
            exit 1
            ;;
    esac
}

main "$@"
EOF

    chmod +x "$OPTIMIZATION_DIR/manage-optimization.sh"

    print_success "Optimization management script created"
}

# Create optimization documentation
create_optimization_docs() {
    print_status "Creating optimization documentation..."

    cat > "$OPTIMIZATION_DIR/README.md" << 'EOF'
# GhostLink Performance Optimization

This directory contains performance optimization configurations including caching, connection pooling, and system optimizations.

## Optimization Components

### Caching Layer
- **Redis**: In-memory caching for API responses and session data
- **Nginx**: HTTP caching for static content and API responses
- **Application Cache**: In-memory caching within the application

### Connection Pooling
- **Database Connections**: Pooled MySQL connections with aiomysql
- **HTTP Clients**: Pooled HTTP connections with aiohttp
- **Redis Connections**: Pooled Redis connections with aioredis

### Performance Monitoring
- **Response Time Tracking**: Monitor API response times
- **Cache Hit Ratios**: Track caching effectiveness
- **System Metrics**: CPU, memory, disk, and network monitoring
- **Error Rate Monitoring**: Track application errors

## Configuration Files

### Redis Configuration (`redis.conf`)
- Memory management with LRU eviction
- Connection pooling settings
- Security hardening (disabled dangerous commands)
- Performance optimizations

### Nginx Caching (`nginx-cache.conf`)
- Proxy caching for API responses
- Static content caching with long expiry
- Cache bypass for dynamic content
- Cache status headers for debugging

### Connection Pooling (`connection-pool.py`)
- Database connection pool management
- HTTP client session pooling
- Redis connection pooling
- Context managers for safe connection handling

### Performance Monitoring (`performance-monitor.py`)
- Request/response time tracking
- Cache hit/miss monitoring
- System resource monitoring
- Performance report generation

## Docker Optimization

### Optimized Compose File (`docker-compose-optimized.yml`)
- Redis caching service
- Optimized API server with Gunicorn tuning
- Resource limits and reservations
- Health checks and dependencies

## Management Scripts

### Optimization Manager (`manage-optimization.sh`)
```bash
# Check performance status
./manage-optimization.sh status

# Apply system optimizations
./manage-optimization.sh optimize

# Clear all caches
./manage-optimization.sh clear-cache

# Real-time monitoring
./manage-optimization.sh monitor

# Generate performance report
./manage-optimization.sh report

# Run all optimizations
./manage-optimization.sh all
```

## Performance Metrics

### Key Metrics to Monitor
- **Response Time**: Average and 95th percentile
- **Cache Hit Ratio**: Should be > 80%
- **Error Rate**: Should be < 1%
- **CPU Usage**: Should be < 80%
- **Memory Usage**: Should be < 85%
- **Requests per Second**: Application throughput

### Monitoring Commands
```bash
# Check Redis cache stats
redis-cli info stats

# Check Nginx cache status
curl -I http://localhost/api/v1/health

# Monitor application performance
python3 -c "from optimization.performance_monitor import performance_monitor; performance_monitor.log_performance_report()"

# Docker performance stats
docker stats
```

## Optimization Strategies

### Caching Strategy
1. **API Response Caching**: Cache frequently accessed data
2. **Static Content**: Long-term caching for assets
3. **Session Data**: Redis for user sessions
4. **Database Query Results**: Cache expensive queries

### Connection Pooling
1. **Database**: Maintain persistent connections
2. **HTTP**: Reuse connections for external APIs
3. **Redis**: Pooled connections for caching operations

### System Optimizations
1. **File Descriptors**: Increase limits for high concurrency
2. **Kernel Parameters**: Optimize network and memory settings
3. **Resource Limits**: Set appropriate CPU and memory limits

## Deployment Instructions

### 1. Deploy Optimized Configuration
```bash
# Use the optimized docker-compose file
docker-compose -f performance/optimization/docker-compose-optimized.yml up -d

# Or update existing deployment
docker-compose down
cp performance/optimization/docker-compose-optimized.yml docker-compose.yml
docker-compose up -d
```

### 2. Initialize Connection Pools
```bash
# In your application startup
from optimization.connection_pool import init_connection_pools
await init_connection_pools()
```

### 3. Enable Performance Monitoring
```bash
# Add to your application
from optimization.performance_monitor import performance_monitor, monitor_performance

@app.middleware("http")
async def performance_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response_time = time.time() - start_time
    performance_monitor.record_request(request.url.path, response_time, response.status_code)
    return response
```

### 4. Configure Caching
```bash
# Start Redis
docker-compose up -d redis

# Configure Nginx caching
cp performance/optimization/nginx-cache.conf nginx/nginx.conf
docker-compose restart nginx-optimized
```

## Performance Tuning

### Gunicorn Tuning
- **Workers**: (2 * CPU cores) + 1
- **Threads**: 2-4 per worker
- **Worker Timeout**: 30 seconds
- **Keep Alive**: 10 seconds

### Database Optimization
- **Connection Pool Size**: 5-20 connections
- **Query Optimization**: Use indexes and EXPLAIN
- **Connection Recycling**: Recycle every hour

### Cache Tuning
- **Redis Memory**: 256MB - 1GB depending on data size
- **Cache TTL**: 5 minutes - 1 hour for API responses
- **Cache Strategy**: LRU for memory efficiency

## Troubleshooting

### Common Performance Issues

1. **High Response Times**
   - Check database query performance
   - Verify cache hit ratios
   - Monitor system resources

2. **Memory Issues**
   - Check for memory leaks in application
   - Adjust Redis memory limits
   - Monitor connection pool usage

3. **Cache Problems**
   - Verify Redis connectivity
   - Check cache key patterns
   - Monitor cache hit/miss ratios

4. **Connection Pool Exhaustion**
   - Increase pool sizes
   - Check for connection leaks
   - Monitor pool usage metrics

### Debugging Commands
```bash
# Check Redis connections
redis-cli client list

# Monitor Redis performance
redis-cli info

# Check application logs
docker-compose logs ghostlink-api-optimized

# Profile Python performance
python3 -m cProfile -s time your_script.py
```

## Best Practices

### Monitoring
- Set up alerts for performance thresholds
- Regularly review performance reports
- Monitor trends over time

### Maintenance
- Clear caches periodically
- Update connection pool configurations
- Review and optimize slow queries

### Scaling
- Use horizontal scaling for increased load
- Implement auto-scaling based on metrics
- Monitor resource usage patterns

## Advanced Optimizations

### Query Optimization
- Use database indexes effectively
- Implement query result caching
- Optimize complex queries

### Async Processing
- Use async/await for I/O operations
- Implement background task processing
- Use connection pooling for external services

### Memory Management
- Monitor memory usage patterns
- Implement memory-efficient data structures
- Use streaming for large data processing

## Support

For performance issues:
- Check application logs: `docker-compose logs`
- Monitor metrics: Grafana dashboards
- Review performance reports: `./manage-optimization.sh report`
- Analyze system resources: `top`, `htop`, `free`
- Profile application: Python profilers
EOF

    print_success "Optimization documentation created"
}

# Main optimization function
main() {
    echo "🚀 GhostLink Performance Optimization"
    echo "===================================="

    setup_optimization_dirs

    print_status "Creating comprehensive performance optimizations..."

    create_redis_config
    create_nginx_cache_config
    create_connection_pool_config
    create_performance_monitoring
    create_optimized_docker_config
    create_optimization_manager
    create_optimization_docs

    print_success "🎯 Performance optimization configurations completed!"
    print_status "📁 Optimization files created in: $OPTIMIZATION_DIR"
    print_status "🚀 Deploy optimized configuration:"
    echo "   docker-compose -f $OPTIMIZATION_DIR/docker-compose-optimized.yml up -d"
    print_status "📊 Monitor performance:"
    echo "   ./$OPTIMIZATION_DIR/manage-optimization.sh status"
    print_status "📚 Documentation: $OPTIMIZATION_DIR/README.md"
}

# Run main function
main "$@"
EOF

    chmod +x "$OPTIMIZATION_DIR/setup-optimization.sh"

    print_success "Performance optimization script created"
}

# Main optimization function
main() {
    echo "🚀 GhostLink Performance Optimization"
    echo "===================================="

    setup_optimization_dirs

    print_status "Creating comprehensive performance optimizations..."

    create_redis_config
    create_nginx_cache_config
    create_connection_pool_config
    create_performance_monitoring
    create_optimized_docker_config
    create_optimization_manager
    create_optimization_docs

    print_success "🎯 Performance optimization configurations completed!"
    print_status "📁 Optimization files created in: $OPTIMIZATION_DIR"
    print_status "🚀 Deploy optimized configuration:"
    echo "   docker-compose -f $OPTIMIZATION_DIR/docker-compose-optimized.yml up -d"
    print_status "📊 Monitor performance:"
    echo "   ./$OPTIMIZATION_DIR/manage-optimization.sh status"
    print_status "📚 Documentation: $OPTIMIZATION_DIR/README.md"
}

# Run main function
main "$@"
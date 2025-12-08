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

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

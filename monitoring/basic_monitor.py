#!/usr/bin/env python3
"""
GhostLink Basic Monitoring Server
Provides Prometheus metrics for AI system monitoring
"""

import time
import psutil
from prometheus_client import start_http_server, Gauge, Counter, Histogram
import threading
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Prometheus metrics
CPU_USAGE = Gauge('ghostlink_cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('ghostlink_memory_usage_mb', 'Memory usage in MB')
DISK_USAGE = Gauge('ghostlink_disk_usage_percent', 'Disk usage percentage')

# AI System metrics
AGENTS_ACTIVE = Gauge('ghostlink_agents_active', 'Number of active AI agents')
TASKS_COMPLETED = Counter('ghostlink_tasks_completed_total', 'Total tasks completed')
CONSCIOUSNESS_LEVEL = Gauge('ghostlink_consciousness_level', 'Current consciousness level', ['level'])

# System health metrics
SYSTEM_UPTIME = Gauge('ghostlink_system_uptime_seconds', 'System uptime in seconds')
ERROR_COUNT = Counter('ghostlink_errors_total', 'Total errors encountered')

def update_system_metrics():
    """Update basic system metrics"""
    while True:
        try:
            # CPU and Memory
            CPU_USAGE.set(psutil.cpu_percent(interval=1))
            memory = psutil.virtual_memory()
            MEMORY_USAGE.set(memory.used / 1024 / 1024)  # Convert to MB

            # Disk usage
            disk = psutil.disk_usage('/')
            DISK_USAGE.set(disk.percent)

            # System uptime
            SYSTEM_UPTIME.set(time.time() - psutil.boot_time())

            time.sleep(5)  # Update every 5 seconds
        except Exception as e:
            ERROR_COUNT.inc()
            print(f"Error updating system metrics: {e}")
            time.sleep(5)

def update_ai_metrics():
    """Update AI system metrics"""
    while True:
        try:
            # For now, set basic AI metrics
            # These would be updated by the actual AI systems
            AGENTS_ACTIVE.set(6)  # From multi-agent engine
            CONSCIOUSNESS_LEVEL.labels(level='moderate_awareness').set(1)

            time.sleep(10)  # Update every 10 seconds
        except Exception as e:
            ERROR_COUNT.inc()
            print(f"Error updating AI metrics: {e}")
            time.sleep(10)

def main():
    """Start the monitoring server"""
    print("🚀 Starting GhostLink Basic Monitoring Server...")

    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    print("📊 Metrics server started on http://localhost:8000")

    # Start metric update threads
    system_thread = threading.Thread(target=update_system_metrics, daemon=True)
    ai_thread = threading.Thread(target=update_ai_metrics, daemon=True)

    system_thread.start()
    ai_thread.start()

    print("✅ Monitoring server active")
    print("📈 View metrics at: http://localhost:8000")

    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring server stopped")

if __name__ == "__main__":
    main()

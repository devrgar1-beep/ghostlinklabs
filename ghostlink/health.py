#!/usr/bin/env python3
"""
GhostLink System Health Monitoring
Real-time system health tracking and metrics collection
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
import json
import os
from pathlib import Path
import platform

# Add the ghostlink module to the path
import sys
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ghostlink.sovereign_deps import SystemMonitor


@dataclass
class HealthMetric:
    """Single health metric"""

    name: str
    value: float
    unit: str
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def status(self) -> str:
        """Get metric status"""
        if self.threshold_critical and self.value >= self.threshold_critical:
            return "critical"
        if self.threshold_warning and self.value >= self.threshold_warning:
            return "warning"
        return "healthy"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "status": self.status,
            "threshold_warning": self.threshold_warning,
            "threshold_critical": self.threshold_critical,
            "timestamp": self.timestamp,
        }


@dataclass
class SystemHealth:
    """System health snapshot"""

    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    disk_percent: float = 0.0
    process_count: int = 0
    metrics: List[HealthMetric] = field(default_factory=list)

    @property
    def overall_status(self) -> str:
        """Get overall health status"""
        statuses = [m.status for m in self.metrics]
        if "critical" in statuses:
            return "critical"
        if "warning" in statuses:
            return "warning"
        return "healthy"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp,
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "disk_percent": self.disk_percent,
            "process_count": self.process_count,
            "overall_status": self.overall_status,
            "metrics": [m.to_dict() for m in self.metrics],
        }


class HealthMonitor:
    """Monitor system health"""

    def __init__(self, update_interval: int = 5):
        """Initialize monitor"""
        self.update_interval = update_interval
        self.history: List[SystemHealth] = []
        self.max_history = 288  # 24 hours at 5m intervals
        self.running = False
        self.alerts: List[str] = []

    def collect_metrics(self) -> SystemHealth:
        """Collect current health metrics"""
        monitor = SystemMonitor()
        cpu_percent = monitor.get_cpu_percent()
        memory = monitor.get_memory_info()
        disk = monitor.get_disk_usage("/")
        process_count = len(monitor.get_processes())

        health = SystemHealth(
            cpu_percent=cpu_percent,
            memory_percent=memory["percent"],
            disk_percent=disk["percent"],
            process_count=process_count,
        )

        # Create detailed metrics
        health.metrics = [
            HealthMetric(
                name="CPU Usage",
                value=cpu_percent,
                unit="%",
                threshold_warning=75,
                threshold_critical=90,
            ),
            HealthMetric(
                name="Memory Usage",
                value=memory["percent"],
                unit="%",
                threshold_warning=80,
                threshold_critical=95,
            ),
            HealthMetric(
                name="Disk Usage",
                value=disk["percent"],
                unit="%",
                threshold_warning=80,
                threshold_critical=95,
            ),
            HealthMetric(
                name="Process Count",
                value=float(process_count),
                unit="count",
                threshold_warning=300,
                threshold_critical=500,
            ),
        ]

        return health

    def add_to_history(self, health: SystemHealth):
        """Add snapshot to history"""
        self.history.append(health)

        # Trim history if needed
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history :]

        # Check for alerts
        if health.overall_status != "healthy":
            self.alerts.append(
                f"[{health.timestamp}] {health.overall_status.upper()}: System health degraded"
            )

    async def monitor_loop(self):
        """Monitoring loop"""
        self.running = True

        while self.running:
            try:
                health = self.collect_metrics()
                self.add_to_history(health)
                await asyncio.sleep(self.update_interval)
            except Exception as e:
                self.alerts.append(f"Monitoring error: {e}")
                await asyncio.sleep(self.update_interval)

    def start(self) -> asyncio.Task:
        """Start monitoring"""
        return asyncio.create_task(self.monitor_loop())

    def stop(self):
        """Stop monitoring"""
        self.running = False

    def get_latest(self) -> Optional[SystemHealth]:
        """Get latest health snapshot"""
        return self.history[-1] if self.history else None

    def get_averages(self, period: int = 60) -> Dict[str, float]:
        """Get average metrics over period"""
        if not self.history:
            return {}

        recent = self.history[-period:] if len(self.history) >= period else self.history

        if not recent:
            return {}

        return {
            "avg_cpu": sum(h.cpu_percent for h in recent) / len(recent),
            "avg_memory": sum(h.memory_percent for h in recent) / len(recent),
            "avg_disk": sum(h.disk_percent for h in recent) / len(recent),
        }

    def export_json(self, filepath: Path):
        """Export history to JSON"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "update_interval": self.update_interval,
            "history_count": len(self.history),
            "history": [h.to_dict() for h in self.history],
            "alerts": self.alerts[-100:] if self.alerts else [],  # Last 100 alerts
        }

        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def get_report(self) -> Dict[str, Any]:
        """Get comprehensive health report"""
        latest = self.get_latest()
        averages = self.get_averages()

        return {
            "timestamp": datetime.now().isoformat(),
            "system_info": {
                "platform": platform.system(),
                "processor": platform.processor(),
                "cores": SystemMonitor().get_cpu_count(),
            },
            "current": latest.to_dict() if latest else None,
            "averages": averages,
            "history_size": len(self.history),
            "alerts": self.alerts[-10:] if self.alerts else [],
            "overall_status": latest.overall_status if latest else "unknown",
        }


class HealthCheckService:
    """Service for periodic health checks"""

    def __init__(self, check_interval: int = 300):  # 5 minutes
        """Initialize service"""
        self.check_interval = check_interval
        self.last_check: Optional[datetime] = None
        self.check_results: List[Dict[str, Any]] = []
        self.max_results = 100

    def perform_check(self) -> Dict[str, Any]:
        """Perform health check"""
        result = {"timestamp": datetime.now().isoformat(), "checks": {}}

        monitor = SystemMonitor()

        # CPU check
        cpu = monitor.get_cpu_percent()
        result["checks"]["cpu"] = {
            "value": cpu,
            "status": "critical" if cpu > 90 else "warning" if cpu > 75 else "healthy",
        }

        # Memory check
        mem = monitor.get_memory_info()
        result["checks"]["memory"] = {
            "value": mem["percent"],
            "status": (
                "critical"
                if mem["percent"] > 95
                else "warning" if mem["percent"] > 80 else "healthy"
            ),
        }

        # Disk check
        disk = monitor.get_disk_usage("/")
        result["checks"]["disk"] = {
            "value": disk["percent"],
            "status": (
                "critical"
                if disk["percent"] > 95
                else "warning" if disk["percent"] > 80 else "healthy"
            ),
        }

        # Determine overall status
        statuses = [c["status"] for c in result["checks"].values()]
        if "critical" in statuses:
            result["overall_status"] = "critical"
        elif "warning" in statuses:
            result["overall_status"] = "warning"
        else:
            result["overall_status"] = "healthy"

        self.last_check = datetime.now()
        self.check_results.append(result)

        # Trim results if needed
        if len(self.check_results) > self.max_results:
            self.check_results = self.check_results[-self.max_results :]

        return result

    def save_results(self, filepath: Path):
        """Save check results to file"""
        data = {
            "service": "health_check",
            "interval_seconds": self.check_interval,
            "total_checks": len(self.check_results),
            "results": self.check_results,
        }

        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)


# Example usage
async def example_monitoring():
    """Example health monitoring"""
    monitor = HealthMonitor(update_interval=2)

    # Start monitoring
    task = monitor.start()

    # Collect for 10 seconds
    await asyncio.sleep(10)

    # Stop monitoring
    monitor.stop()
    await task

    # Get report
    report = monitor.get_report()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(example_monitoring())

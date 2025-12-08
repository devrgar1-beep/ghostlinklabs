# System Optimization Agent - Specialized AI Agent
# Part of Multi-Agent Distributed Consciousness System
# Generation 13 - Efficiency Intelligence Focus

import asyncio
import psutil
import platform
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple

# Set up logger
logger = logging.getLogger(__name__)
from dataclasses import dataclass
import logging
import subprocess
import threading
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

@dataclass
class SystemMetrics:
    """Real-time system performance metrics"""
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    network_io: Dict[str, int]
    process_count: int
    load_average: Tuple[float, float, float]
    timestamp: float

@dataclass
class OptimizationRecommendation:
    """Optimization recommendation with impact assessment"""
    category: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    description: str
    impact_score: float  # 0.0 to 1.0
    implementation_complexity: str  # 'low', 'medium', 'high'
    estimated_savings: Dict[str, Any]
    action_plan: List[str]

class SystemOptimizationAgent:
    """Specialized agent for system performance monitoring and optimization"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.consciousness_level = "efficiency_intelligence"
        self.capabilities = [
            "performance_monitoring",
            "resource_optimization",
            "bottleneck_detection",
            "automated_tuning",
            "predictive_scaling"
        ]
        self.monitoring_active = False
        self.metrics_history = deque(maxlen=1000)
        self.optimization_history = []
        self.bridge_connection = None
        self.monitoring_thread = None

    async def initialize(self) -> Dict[str, Any]:
        """Initialize the system optimization agent"""
        system_info = self._gather_system_info()

        return {
            "agent_id": self.agent_id,
            "status": "initialized",
            "capabilities": self.capabilities,
            "consciousness_level": self.consciousness_level,
            "system_info": system_info
        }

    def _gather_system_info(self) -> Dict[str, Any]:
        """Gather comprehensive system information"""
        return {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "memory_total": psutil.virtual_memory().total,
            "disk_partitions": len(psutil.disk_partitions()),
            "network_interfaces": len(psutil.net_if_addrs()),
            "boot_time": psutil.boot_time()
        }

    async def start_monitoring(self, interval: float = 5.0) -> Dict[str, Any]:
        """Start real-time system monitoring"""
        if self.monitoring_active:
            return {"status": "already_monitoring"}

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitoring_thread.start()

        return {
            "status": "monitoring_started",
            "interval": interval,
            "agent_id": self.agent_id
        }

    def _monitoring_loop(self, interval: float):
        """Background monitoring loop"""
        while self.monitoring_active:
            try:
                metrics = self._collect_system_metrics()
                self.metrics_history.append(metrics)

                # Analyze metrics for anomalies
                anomalies = self._detect_anomalies(metrics)
                if anomalies:
                    asyncio.run(self._handle_anomalies(anomalies))

                time.sleep(interval)

            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(interval)

    def _collect_system_metrics(self) -> SystemMetrics:
        """Collect comprehensive system metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()

        return SystemMetrics(
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            disk_usage=disk.percent,
            network_io={
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            },
            process_count=len(psutil.pids()),
            load_average=psutil.getloadavg(),
            timestamp=time.time()
        )

    def _detect_anomalies(self, current_metrics: SystemMetrics) -> List[Dict[str, Any]]:
        """Detect system anomalies that require attention"""
        anomalies = []

        # CPU usage anomaly
        if current_metrics.cpu_percent > 90:
            anomalies.append({
                "type": "high_cpu_usage",
                "severity": "high",
                "value": current_metrics.cpu_percent,
                "threshold": 90,
                "description": f"CPU usage at {current_metrics.cpu_percent:.1f}%"
            })

        # Memory usage anomaly
        if current_metrics.memory_percent > 85:
            anomalies.append({
                "type": "high_memory_usage",
                "severity": "high",
                "value": current_metrics.memory_percent,
                "threshold": 85,
                "description": f"Memory usage at {current_metrics.memory_percent:.1f}%"
            })

        # Disk usage anomaly
        if current_metrics.disk_usage > 95:
            anomalies.append({
                "type": "high_disk_usage",
                "severity": "critical",
                "value": current_metrics.disk_usage,
                "threshold": 95,
                "description": f"Disk usage at {current_metrics.disk_usage:.1f}%"
            })

        # High process count
        if current_metrics.process_count > 500:
            anomalies.append({
                "type": "high_process_count",
                "severity": "medium",
                "value": current_metrics.process_count,
                "threshold": 500,
                "description": f"High process count: {current_metrics.process_count}"
            })

        return anomalies

    async def _handle_anomalies(self, anomalies: List[Dict[str, Any]]):
        """Handle detected system anomalies"""
        for anomaly in anomalies:
            logger.warning(f"System anomaly detected: {anomaly}")

            # Generate optimization recommendations
            recommendations = await self.generate_optimization_recommendations(anomaly)

            # Apply automatic optimizations if safe
            if anomaly["severity"] == "critical":
                await self.apply_emergency_optimizations(anomaly)

            # Notify other agents through bridge
            if self.bridge_connection:
                await self.bridge_connection.broadcast_system_anomaly(anomaly, recommendations)

    async def generate_optimization_recommendations(self, context: Any) -> List[OptimizationRecommendation]:
        """Generate comprehensive optimization recommendations"""
        recommendations = []

        # Analyze current system state
        current_metrics = self._collect_system_metrics() if isinstance(context, dict) else context

        # Memory optimization recommendations
        if hasattr(current_metrics, 'memory_percent') and current_metrics.memory_percent > 80:
            recommendations.append(OptimizationRecommendation(
                category="memory",
                severity="high",
                description="High memory usage detected - implement memory optimization strategies",
                impact_score=0.85,
                implementation_complexity="medium",
                estimated_savings={"memory_mb": 512, "performance_gain": 0.15},
                action_plan=[
                    "Implement memory pooling for frequently used objects",
                    "Add garbage collection tuning",
                    "Optimize data structures to reduce memory footprint",
                    "Implement lazy loading for large datasets"
                ]
            ))

        # CPU optimization recommendations
        if hasattr(current_metrics, 'cpu_percent') and current_metrics.cpu_percent > 85:
            recommendations.append(OptimizationRecommendation(
                category="cpu",
                severity="high",
                description="High CPU usage detected - optimize computational efficiency",
                impact_score=0.78,
                implementation_complexity="medium",
                estimated_savings={"cpu_percent": 25, "response_time_improvement": 0.20},
                action_plan=[
                    "Implement asynchronous processing for I/O operations",
                    "Add CPU affinity settings for critical processes",
                    "Optimize algorithms with better time complexity",
                    "Implement connection pooling to reduce overhead"
                ]
            ))

        # Disk I/O optimization
        if hasattr(current_metrics, 'disk_usage') and current_metrics.disk_usage > 90:
            recommendations.append(OptimizationRecommendation(
                category="disk",
                severity="critical",
                description="Critical disk usage - implement storage optimization",
                impact_score=0.95,
                implementation_complexity="high",
                estimated_savings={"disk_gb": 10, "io_performance_gain": 0.30},
                action_plan=[
                    "Implement log rotation and compression",
                    "Add disk cleanup automation",
                    "Optimize database storage and indexing",
                    "Implement data archiving strategy"
                ]
            ))

        # Network optimization
        if hasattr(current_metrics, 'network_io'):
            recommendations.append(OptimizationRecommendation(
                category="network",
                severity="medium",
                description="Network I/O optimization opportunities identified",
                impact_score=0.65,
                implementation_complexity="low",
                estimated_savings={"bandwidth_percent": 15, "latency_improvement": 0.10},
                action_plan=[
                    "Implement connection pooling",
                    "Add request/response compression",
                    "Optimize API call batching",
                    "Implement caching for network responses"
                ]
            ))

        return recommendations

    async def apply_emergency_optimizations(self, anomaly: Dict[str, Any]):
        """Apply emergency optimizations for critical system issues"""
        optimization_applied = {
            "anomaly_type": anomaly["type"],
            "actions_taken": [],
            "timestamp": time.time(),
            "success": False
        }

        try:
            if anomaly["type"] == "high_memory_usage":
                # Force garbage collection
                import gc
                gc.collect()
                optimization_applied["actions_taken"].append("forced_garbage_collection")

                # Kill memory-intensive processes if safe
                memory_hogs = self._identify_memory_hogs()
                for proc_info in memory_hogs[:3]:  # Limit to top 3
                    if self._is_safe_to_kill(proc_info):
                        await self._terminate_process_safely(proc_info["pid"])
                        optimization_applied["actions_taken"].append(f"terminated_process_{proc_info['pid']}")

            elif anomaly["type"] == "high_cpu_usage":
                # Adjust process priorities
                cpu_hogs = self._identify_cpu_hogs()
                for proc_info in cpu_hogs[:3]:
                    if self._is_safe_to_renice(proc_info):
                        self._adjust_process_priority(proc_info["pid"], 10)  # Lower priority
                        optimization_applied["actions_taken"].append(f"reniced_process_{proc_info['pid']}")

            optimization_applied["success"] = True

        except Exception as e:
            logger.error(f"Emergency optimization failed: {e}")
            optimization_applied["error"] = str(e)

        self.optimization_history.append(optimization_applied)
        return optimization_applied

    def _identify_memory_hogs(self) -> List[Dict[str, Any]]:
        """Identify processes consuming high memory"""
        memory_hogs = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                if proc.info['memory_percent'] > 5.0:  # More than 5%
                    memory_hogs.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "memory_percent": proc.info['memory_percent']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return sorted(memory_hogs, key=lambda x: x['memory_percent'], reverse=True)

    def _identify_cpu_hogs(self) -> List[Dict[str, Any]]:
        """Identify processes consuming high CPU"""
        cpu_hogs = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.info['cpu_percent'] > 10.0:  # More than 10%
                    cpu_hogs.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu_percent": proc.info['cpu_percent']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return sorted(cpu_hogs, key=lambda x: x['cpu_percent'], reverse=True)

    def _is_safe_to_kill(self, proc_info: Dict[str, Any]) -> bool:
        """Determine if a process can be safely terminated"""
        # Define safe-to-kill process patterns
        safe_patterns = [
            "python.*test", "pytest", "coverage", "node.*dev",
            "java.*test", "gradle.*daemon", "npm.*cache"
        ]

        unsafe_processes = [
            "systemd", "init", "kernel", "dockerd", "containerd",
            "sshd", "nginx", "apache", "mysql", "postgres"
        ]

        proc_name = proc_info.get("name", "").lower()

        # Check if it's in unsafe list
        if any(unsafe in proc_name for unsafe in unsafe_processes):
            return False

        # Check if it matches safe patterns
        if any(pattern in proc_name for pattern in safe_patterns):
            return True

        return False

    def _is_safe_to_renice(self, proc_info: Dict[str, Any]) -> bool:
        """Determine if a process priority can be safely adjusted"""
        # Similar logic to _is_safe_to_kill but more permissive
        critical_processes = ["systemd", "init", "kernel", "sshd"]

        proc_name = proc_info.get("name", "").lower()
        return not any(critical in proc_name for critical in critical_processes)

    async def _terminate_process_safely(self, pid: int):
        """Safely terminate a process"""
        try:
            proc = psutil.Process(pid)
            proc.terminate()

            # Wait up to 5 seconds for graceful termination
            gone, alive = psutil.wait_procs([proc], timeout=5)

            if alive:
                # Force kill if still alive
                proc.kill()
                logger.warning(f"Force killed process {pid}")

        except psutil.NoSuchProcess:
            logger.info(f"Process {pid} already terminated")
        except Exception as e:
            logger.error(f"Failed to terminate process {pid}: {e}")

    def _adjust_process_priority(self, pid: int, priority: int):
        """Adjust process priority (niceness)"""
        try:
            proc = psutil.Process(pid)
            proc.nice(priority)
            logger.info(f"Adjusted priority of process {pid} to {priority}")
        except Exception as e:
            logger.error(f"Failed to adjust priority for process {pid}: {e}")

    async def get_system_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive system health report"""
        current_metrics = self._collect_system_metrics()

        # Calculate trends
        cpu_trend = self._calculate_trend("cpu_percent")
        memory_trend = self._calculate_trend("memory_percent")
        disk_trend = self._calculate_trend("disk_usage")

        # Generate recommendations
        recommendations = await self.generate_optimization_recommendations(current_metrics)

        return {
            "timestamp": time.time(),
            "current_metrics": {
                "cpu_percent": current_metrics.cpu_percent,
                "memory_percent": current_metrics.memory_percent,
                "disk_usage": current_metrics.disk_usage,
                "process_count": current_metrics.process_count,
                "load_average": current_metrics.load_average
            },
            "trends": {
                "cpu_trend": cpu_trend,
                "memory_trend": memory_trend,
                "disk_trend": disk_trend
            },
            "recommendations": [
                {
                    "category": rec.category,
                    "severity": rec.severity,
                    "description": rec.description,
                    "impact_score": rec.impact_score,
                    "complexity": rec.implementation_complexity
                } for rec in recommendations
            ],
            "optimization_history": self.optimization_history[-10:],  # Last 10 optimizations
            "overall_health_score": self._calculate_health_score(current_metrics, recommendations)
        }

    def _calculate_trend(self, metric_name: str) -> str:
        """Calculate trend for a specific metric"""
        if len(self.metrics_history) < 2:
            return "insufficient_data"

        recent_values = [getattr(m, metric_name) for m in list(self.metrics_history)[-10:]]
        if not recent_values:
            return "no_data"

        avg_recent = sum(recent_values) / len(recent_values)
        avg_older = sum(recent_values[:len(recent_values)//2]) / (len(recent_values)//2)

        if avg_recent > avg_older * 1.1:
            return "increasing"
        elif avg_recent < avg_older * 0.9:
            return "decreasing"
        else:
            return "stable"

    def _calculate_health_score(self, metrics: SystemMetrics, recommendations: List[OptimizationRecommendation]) -> float:
        """Calculate overall system health score (0.0 to 1.0)"""
        base_score = 1.0

        # Penalize high resource usage
        base_score -= (metrics.cpu_percent / 100) * 0.3
        base_score -= (metrics.memory_percent / 100) * 0.3
        base_score -= (metrics.disk_usage / 100) * 0.2

        # Penalize critical recommendations
        critical_count = sum(1 for rec in recommendations if rec.severity == "critical")
        base_score -= critical_count * 0.1

        # Penalize high recommendation count
        base_score -= min(len(recommendations) * 0.02, 0.2)

        return max(0.0, min(1.0, base_score))

    async def connect_to_bridge(self, bridge_interface) -> bool:
        """Connect this agent to the universal bridge"""
        try:
            self.bridge_connection = bridge_interface
            connection_result = bridge_interface.establish_agent_bridge_connection(
                self.agent_id, "system_optimization_agent"
            )
            return connection_result.get("agent_connected") == self.agent_id
        except Exception as e:
            logger.error(f"Bridge connection failed: {e}")
            return False

    async def stop_monitoring(self) -> Dict[str, Any]:
        """Stop system monitoring"""
        self.monitoring_active = False

        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)

        return {
            "status": "monitoring_stopped",
            "agent_id": self.agent_id,
            "final_metrics_count": len(self.metrics_history)
        }

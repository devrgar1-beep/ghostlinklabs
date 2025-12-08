#!/usr/bin/env python3
"""
GhostLink OpenTelemetry Integration
Comprehensive observability for distributed AI systems
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
import json
import psutil
import threading

# OpenTelemetry imports
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation import instrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
from opentelemetry.trace import Status, StatusCode
from opentelemetry.metrics import CallbackOptions, Observation

# Prometheus metrics
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GhostLinkTelemetry:
    """OpenTelemetry integration for GhostLink observability"""

    def __init__(self, service_name: str = "ghostlink",
                 otlp_endpoint: str = "http://localhost:4317",
                 prometheus_port: int = 8000):
        self.service_name = service_name
        self.otlp_endpoint = otlp_endpoint
        self.prometheus_port = prometheus_port

        # Initialize OpenTelemetry
        self.tracer_provider = None
        self.meter_provider = None
        self.tracer = None
        self.meter = None

        # Prometheus metrics
        self.prometheus_metrics = {}

        # System monitoring
        self.system_monitoring = False
        self.monitoring_thread = None

        # Performance tracking
        self.operation_counts = {}
        self.operation_durations = {}

    def initialize(self) -> bool:
        """Initialize OpenTelemetry and Prometheus"""
        try:
            # Set up tracing
            self.tracer_provider = TracerProvider()
            trace.set_tracer_provider(self.tracer_provider)

            # OTLP trace exporter
            trace_exporter = OTLPSpanExporter(
                endpoint=self.otlp_endpoint,
                insecure=True
            )
            span_processor = BatchSpanProcessor(trace_exporter)
            self.tracer_provider.add_span_processor(span_processor)

            # Set up metrics
            metric_exporter = OTLPMetricExporter(
                endpoint=self.otlp_endpoint,
                insecure=True
            )
            metric_reader = PeriodicExportingMetricReader(
                exporter=metric_exporter,
                export_interval_millis=5000  # Export every 5 seconds
            )

            self.meter_provider = MeterProvider(metric_readers=[metric_reader])
            metrics.set_meter_provider(self.meter_provider)

            # Get tracer and meter
            self.tracer = trace.get_tracer(__name__)
            self.meter = metrics.get_meter(__name__)

            # Initialize Prometheus metrics
            self._initialize_prometheus_metrics()

            # Instrument common libraries
            self._instrument_libraries()

            logger.info("✅ OpenTelemetry initialized successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenTelemetry: {e}")
            return False

    def _initialize_prometheus_metrics(self):
        """Initialize Prometheus metrics"""
        try:
            # Start Prometheus HTTP server
            start_http_server(self.prometheus_port)
            logger.info(f"📊 Prometheus metrics server started on port {self.prometheus_port}")

            # Define metrics
            self.prometheus_metrics = {
                # Counters
                "tasks_processed_total": Counter(
                    "ghostlink_tasks_processed_total",
                    "Total number of tasks processed",
                    ["task_type", "status"]
                ),
                "api_requests_total": Counter(
                    "ghostlink_api_requests_total",
                    "Total number of API requests",
                    ["method", "endpoint", "status"]
                ),
                "errors_total": Counter(
                    "ghostlink_errors_total",
                    "Total number of errors",
                    ["error_type", "component"]
                ),

                # Gauges
                "active_agents": Gauge(
                    "ghostlink_active_agents",
                    "Number of active agents"
                ),
                "models_loaded": Gauge(
                    "ghostlink_models_loaded",
                    "Number of models currently loaded"
                ),
                "memory_usage_mb": Gauge(
                    "ghostlink_memory_usage_mb",
                    "Memory usage in MB"
                ),
                "cpu_usage_percent": Gauge(
                    "ghostlink_cpu_usage_percent",
                    "CPU usage percentage"
                ),

                # Histograms
                "task_duration_seconds": Histogram(
                    "ghostlink_task_duration_seconds",
                    "Task processing duration",
                    ["task_type"],
                    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
                ),
                "api_request_duration_seconds": Histogram(
                    "ghostlink_api_request_duration_seconds",
                    "API request duration",
                    ["method", "endpoint"],
                    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
                ),
                "model_inference_duration_seconds": Histogram(
                    "ghostlink_model_inference_duration_seconds",
                    "Model inference duration",
                    ["model_id", "operation"],
                    buckets=[0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0]
                )
            }

        except Exception as e:
            logger.error(f"❌ Failed to initialize Prometheus metrics: {e}")

    def _instrument_libraries(self):
        """Instrument common libraries for automatic tracing"""
        try:
            # Instrument HTTP requests
            RequestsInstrumentor().instrument()
            URLLib3Instrumentor().instrument()

            logger.info("🔧 Library instrumentation completed")

        except Exception as e:
            logger.warning(f"⚠️ Library instrumentation failed: {e}")

    def start_system_monitoring(self):
        """Start system resource monitoring"""
        if self.system_monitoring:
            return

        self.system_monitoring = True
        self.monitoring_thread = threading.Thread(
            target=self._system_monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()
        logger.info("📊 System monitoring started")

    def stop_system_monitoring(self):
        """Stop system resource monitoring"""
        self.system_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
        logger.info("🛑 System monitoring stopped")

    def _system_monitoring_loop(self):
        """System monitoring loop"""
        while self.system_monitoring:
            try:
                # Update system metrics
                memory_mb = psutil.virtual_memory().used / 1024 / 1024
                cpu_percent = psutil.cpu_percent(interval=1)

                self.prometheus_metrics["memory_usage_mb"].set(memory_mb)
                self.prometheus_metrics["cpu_usage_percent"].set(cpu_percent)

                time.sleep(5)  # Update every 5 seconds

            except Exception as e:
                logger.error(f"Error in system monitoring: {e}")
                time.sleep(5)

    # Tracing decorators and context managers

    def trace_operation(self, operation_name: str, attributes: Dict[str, Any] = None):
        """Decorator for tracing operations"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                with self.tracer.start_as_span(
                    operation_name,
                    attributes=attributes or {}
                ) as span:
                    try:
                        start_time = time.time()
                        result = func(*args, **kwargs)
                        duration = time.time() - start_time

                        # Add metrics
                        span.set_attribute("duration_seconds", duration)
                        self.record_operation(operation_name, duration, success=True)

                        return result

                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                        self.record_operation(operation_name, 0, success=False)
                        raise

            return wrapper
        return decorator

    def start_span(self, name: str, attributes: Dict[str, Any] = None):
        """Context manager for tracing spans"""
        return self.tracer.start_as_span(name, attributes=attributes or {})

    # Metrics recording methods

    def record_task_processed(self, task_type: str, status: str = "success"):
        """Record task processing"""
        if "tasks_processed_total" in self.prometheus_metrics:
            self.prometheus_metrics["tasks_processed_total"].labels(
                task_type=task_type, status=status
            ).inc()

    def record_api_request(self, method: str, endpoint: str, status: str, duration: float):
        """Record API request"""
        if "api_requests_total" in self.prometheus_metrics:
            self.prometheus_metrics["api_requests_total"].labels(
                method=method, endpoint=endpoint, status=status
            ).inc()

        if "api_request_duration_seconds" in self.prometheus_metrics:
            self.prometheus_metrics["api_request_duration_seconds"].labels(
                method=method, endpoint=endpoint
            ).observe(duration)

    def record_error(self, error_type: str, component: str):
        """Record error"""
        if "errors_total" in self.prometheus_metrics:
            self.prometheus_metrics["errors_total"].labels(
                error_type=error_type, component=component
            ).inc()

    def record_model_inference(self, model_id: str, operation: str, duration: float):
        """Record model inference"""
        if "model_inference_duration_seconds" in self.prometheus_metrics:
            self.prometheus_metrics["model_inference_duration_seconds"].labels(
                model_id=model_id, operation=operation
            ).observe(duration)

    def update_active_agents(self, count: int):
        """Update active agents count"""
        if "active_agents" in self.prometheus_metrics:
            self.prometheus_metrics["active_agents"].set(count)

    def update_models_loaded(self, count: int):
        """Update loaded models count"""
        if "models_loaded" in self.prometheus_metrics:
            self.prometheus_metrics["models_loaded"].set(count)

    def record_operation(self, operation_name: str, duration: float, success: bool = True):
        """Record generic operation metrics"""
        if operation_name not in self.operation_counts:
            self.operation_counts[operation_name] = 0
            self.operation_durations[operation_name] = []

        self.operation_counts[operation_name] += 1
        if success:
            self.operation_durations[operation_name].append(duration)

    # High-level monitoring methods

    def monitor_orchestrator(self, orchestrator):
        """Set up monitoring for Ray orchestrator"""
        # This would be called to integrate with the Ray orchestrator
        # For now, just log that monitoring is enabled
        logger.info("🎮 Orchestrator monitoring enabled")

    def monitor_nats(self, nats_integration):
        """Set up monitoring for NATS messaging"""
        # This would integrate with NATS metrics
        logger.info("🐱 NATS monitoring enabled")

    def create_dashboard_config(self) -> Dict[str, Any]:
        """Create Grafana dashboard configuration"""
        return {
            "dashboard": {
                "title": "GhostLink Observability",
                "tags": ["ghostlink", "ai", "distributed"],
                "timezone": "UTC",
                "panels": [
                    {
                        "title": "Task Processing Rate",
                        "type": "graph",
                        "targets": [{
                            "expr": "rate(ghostlink_tasks_processed_total[5m])",
                            "legendFormat": "{{task_type}}"
                        }]
                    },
                    {
                        "title": "Active Agents",
                        "type": "gauge",
                        "targets": [{
                            "expr": "ghostlink_active_agents",
                        }]
                    },
                    {
                        "title": "Memory Usage",
                        "type": "graph",
                        "targets": [{
                            "expr": "ghostlink_memory_usage_mb",
                            "legendFormat": "Memory (MB)"
                        }]
                    },
                    {
                        "title": "API Request Duration",
                        "type": "heatmap",
                        "targets": [{
                            "expr": "ghostlink_api_request_duration_seconds_bucket",
                        }]
                    }
                ]
            }
        }

    def export_metrics_snapshot(self) -> Dict[str, Any]:
        """Export current metrics snapshot"""
        return {
            "timestamp": datetime.now().isoformat(),
            "operation_counts": self.operation_counts.copy(),
            "operation_durations": {
                op: sum(durations) / len(durations) if durations else 0
                for op, durations in self.operation_durations.items()
            },
            "system_info": {
                "memory_mb": psutil.virtual_memory().used / 1024 / 1024,
                "cpu_percent": psutil.cpu_percent(),
                "disk_usage": psutil.disk_usage('/').percent
            }
        }

class TelemetryIntegration:
    """Integration layer for telemetry across GhostLink components"""

    def __init__(self):
        self.telemetry = GhostLinkTelemetry()
        self.orchestrator = None
        self.nats_integration = None
        self.initialized = False

    async def initialize(self) -> bool:
        """Initialize telemetry integration"""
        if not self.telemetry.initialize():
            return False

        # Start system monitoring
        self.telemetry.start_system_monitoring()

        # Try to integrate with existing components
        try:
            from ghostlink_ray_orchestrator import ProductionRayOrchestrator
            self.orchestrator = ProductionRayOrchestrator(num_workers=4)
            self.telemetry.monitor_orchestrator(self.orchestrator)
        except ImportError:
            logger.warning("Ray orchestrator not available for telemetry")

        try:
            from ghostlink_nats import NATSIntegration
            self.nats_integration = NATSIntegration()
            await self.nats_integration.initialize()
            self.telemetry.monitor_nats(self.nats_integration)
        except ImportError:
            logger.warning("NATS integration not available for telemetry")

        self.initialized = True
        logger.info("✅ Telemetry integration initialized")
        return True

    async def shutdown(self):
        """Shutdown telemetry integration"""
        self.telemetry.stop_system_monitoring()

        if self.orchestrator:
            self.orchestrator.shutdown()

        if self.nats_integration:
            await self.nats_integration.stop()

        logger.info("🛑 Telemetry integration shutdown")

    def get_status(self) -> Dict[str, Any]:
        """Get telemetry status"""
        return {
            "initialized": self.initialized,
            "orchestrator_available": self.orchestrator is not None,
            "nats_available": self.nats_integration is not None if self.nats_integration else False,
            "prometheus_port": self.telemetry.prometheus_port,
            "otlp_endpoint": self.telemetry.otlp_endpoint,
            "system_monitoring": self.telemetry.system_monitoring,
            "metrics_snapshot": self.telemetry.export_metrics_snapshot()
        }

# Decorators for easy instrumentation

def trace_operation(operation_name: str, attributes: Dict[str, Any] = None):
    """Global trace decorator"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Get telemetry instance (assuming it's initialized globally)
            telemetry = getattr(trace_operation, '_telemetry', None)
            if telemetry:
                with telemetry.start_span(operation_name, attributes):
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def record_api_request(method: str, endpoint: str):
    """Decorator for API request recording"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            telemetry = getattr(record_api_request, '_telemetry', None)
            if telemetry:
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    telemetry.record_api_request(method, endpoint, "success", duration)
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    telemetry.record_api_request(method, endpoint, "error", duration)
                    raise
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator

# Demo and testing functions

async def demo_telemetry():
    """Demonstrate telemetry capabilities"""
    print("📊 OpenTelemetry Demo")
    print("=" * 40)

    # Initialize telemetry
    telemetry = GhostLinkTelemetry()

    if not telemetry.initialize():
        print("❌ Failed to initialize telemetry")
        return

    try:
        # Start system monitoring
        telemetry.start_system_monitoring()

        # Simulate some operations
        print("🔄 Simulating operations...")

        # Record some metrics
        telemetry.record_task_processed("compression", "success")
        telemetry.record_task_processed("expansion", "success")
        telemetry.record_task_processed("compression", "failed")

        telemetry.record_api_request("GET", "/health", "200", 0.05)
        telemetry.record_api_request("POST", "/tasks", "201", 0.15)

        telemetry.record_error("timeout", "nats_client")
        telemetry.record_error("memory", "ray_worker")

        telemetry.update_active_agents(3)
        telemetry.update_models_loaded(2)

        # Simulate traced operations
        @telemetry.trace_operation("demo_compression")
        def simulate_compression():
            time.sleep(0.1)
            return "compressed"

        @telemetry.trace_operation("demo_expansion")
        def simulate_expansion():
            time.sleep(0.2)
            return "expanded"

        simulate_compression()
        simulate_expansion()

        # Wait a bit for metrics to be exported
        print("⏳ Waiting for metrics export...")
        await asyncio.sleep(6)

        # Export metrics snapshot
        snapshot = telemetry.export_metrics_snapshot()
        print(f"📈 Metrics snapshot: {json.dumps(snapshot, indent=2)}")

        print("\\n🎉 Telemetry demo completed successfully!")

    finally:
        telemetry.stop_system_monitoring()

if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_telemetry())

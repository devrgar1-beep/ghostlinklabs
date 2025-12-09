#!/usr/bin/env python3
"""
GhostLink Phase 2 Integration
Unified system with NATS messaging, OpenTelemetry observability, and Ray orchestration
"""

import asyncio
import logging
import signal
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GhostLinkPhase2:
    """Phase 2 integrated system with messaging, observability, and orchestration"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.running = False

        # Core components
        self.telemetry = None
        self.nats_integration = None
        self.orchestrator = None

        # Component status
        self.component_status = {
            "telemetry": False,
            "nats": False,
            "orchestrator": False,
            "system_health": "initializing"
        }

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            "nats": {
                "servers": ["nats://localhost:4222"],
                "client_id": f"ghostlink-phase2-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            },
            "telemetry": {
                "service_name": "ghostlink-phase2",
                "otlp_endpoint": "http://localhost:4317",
                "prometheus_port": 8000
            },
            "orchestrator": {
                "num_workers": 4,
                "enable_serve": False
            },
            "system": {
                "shutdown_timeout": 10.0,
                "health_check_interval": 30.0
            }
        }

    async def initialize(self) -> bool:
        """Initialize all Phase 2 components"""
        logger.info("🚀 Initializing GhostLink Phase 2")

        try:
            # Initialize telemetry first (for observability of initialization)
            logger.info("📊 Initializing telemetry...")
            from ghostlink_telemetry import TelemetryIntegration
            self.telemetry = TelemetryIntegration()
            if await self.telemetry.initialize():
                self.component_status["telemetry"] = True
                logger.info("✅ Telemetry initialized")
            else:
                logger.error("❌ Telemetry initialization failed")
                return False

            # Initialize NATS messaging
            logger.info("🐱 Initializing NATS messaging...")
            from ghostlink_nats import NATSIntegration
            self.nats_integration = NATSIntegration(
                nats_servers=self.config["nats"]["servers"]
            )
            if await self.nats_integration.initialize():
                self.component_status["nats"] = True
                logger.info("✅ NATS messaging initialized")
            else:
                logger.error("❌ NATS messaging initialization failed")
                return False

            # Initialize Ray orchestrator
            logger.info("🎮 Initializing Ray orchestrator...")
            try:
                from ghostlink_ray_orchestrator import ProductionRayOrchestrator
                self.orchestrator = ProductionRayOrchestrator(
                    num_workers=self.config["orchestrator"]["num_workers"],
                    enable_serve=self.config["orchestrator"]["enable_serve"]
                )
                self.component_status["orchestrator"] = True
                logger.info("✅ Ray orchestrator initialized")
            except ImportError as e:
                logger.warning(f"⚠️ Ray orchestrator not available: {e}")
                self.orchestrator = None

            # Set up cross-component integration
            await self._setup_component_integration()

            # Mark system as healthy
            self.component_status["system_health"] = "healthy"
            logger.info("✅ GhostLink Phase 2 initialization completed")

            # Record successful initialization
            if self.telemetry and self.telemetry.initialized:
                self.telemetry.telemetry.record_task_processed("system_initialization", "success")

            return True

        except Exception as e:
            logger.error(f"❌ Phase 2 initialization failed: {e}")
            self.component_status["system_health"] = "failed"
            if self.telemetry and self.telemetry.initialized:
                self.telemetry.telemetry.record_error("initialization", "system")
            return False

    async def _setup_component_integration(self):
        """Set up integration between components"""
        logger.info("🔗 Setting up component integration...")

        # Connect telemetry to other components
        if self.telemetry and self.orchestrator:
            self.telemetry.telemetry.monitor_orchestrator(self.orchestrator)

        if self.telemetry and self.nats_integration:
            self.telemetry.telemetry.monitor_nats(self.nats_integration)

        # Set up NATS message handlers that integrate with orchestrator
        if self.nats_integration and self.orchestrator:
            await self._setup_nats_orchestrator_integration()

        logger.info("✅ Component integration completed")

    async def _setup_nats_orchestrator_integration(self):
        """Set up NATS handlers that communicate with Ray orchestrator"""

        async def handle_orchestrator_command(message):
            """Handle orchestrator commands from NATS"""
            from ghostlink_nats import Message

            command = message.payload.get("command")
            parameters = message.payload.get("parameters", {})

            logger.info(f"🎮 Processing orchestrator command: {command}")

            try:
                if command == "submit_compression_task":
                    from ghostlink_ray_orchestrator import CompressionType
                    task_id = self.orchestrator.submit_compression_task(
                        parameters["model_id"],
                        CompressionType(parameters["compression_type"]),
                        parameters.get("task_params", {})
                    )
                    # Send confirmation via NATS
                    await self.nats_integration.nats.publish("ghostlink.orchestrator.responses", {
                        "task_id": task_id,
                        "status": "submitted",
                        "command": command
                    })

                elif command == "submit_expansion_task":
                    from ghostlink_ray_orchestrator import ExpansionType
                    task_id = self.orchestrator.submit_expansion_task(
                        parameters["model_id"],
                        ExpansionType(parameters["expansion_type"]),
                        parameters.get("task_params", {})
                    )
                    await self.nats_integration.nats.publish("ghostlink.orchestrator.responses", {
                        "task_id": task_id,
                        "status": "submitted",
                        "command": command
                    })

                elif command == "submit_consciousness_task":
                    task_id = self.orchestrator.submit_consciousness_task(parameters)
                    await self.nats_integration.nats.publish("ghostlink.orchestrator.responses", {
                        "task_id": task_id,
                        "status": "submitted",
                        "command": command
                    })

                elif command == "process_tasks":
                    # Process tasks asynchronously
                    asyncio.create_task(self.orchestrator.process_tasks())
                    await self.nats_integration.nats.publish("ghostlink.orchestrator.responses", {
                        "status": "processing_started",
                        "command": command
                    })

                elif command == "get_status":
                    status = self.orchestrator.get_status()
                    await self.nats_integration.nats.publish("ghostlink.orchestrator.status", status)

                # Record telemetry
                if self.telemetry and self.telemetry.initialized:
                    self.telemetry.telemetry.record_task_processed("orchestrator_command", "success")

            except Exception as e:
                logger.error(f"❌ Error processing orchestrator command: {e}")
                await self.nats_integration.nats.publish("ghostlink.orchestrator.errors", {
                    "command": command,
                    "error": str(e)
                })
                if self.telemetry and self.telemetry.initialized:
                    self.telemetry.telemetry.record_error("orchestrator_command", "nats_handler")

        # Subscribe to orchestrator commands
        await self.nats_integration.nats.subscribe(
            "ghostlink.orchestrator.commands",
            handle_orchestrator_command
        )

        # Set up agent response handler
        async def handle_agent_response(message):
            """Handle agent responses"""
            logger.info(f"📥 Agent response received: {message.payload}")

            # Forward to telemetry
            if self.telemetry and self.telemetry.initialized:
                self.telemetry.telemetry.record_task_processed("agent_response", "received")

        await self.nats_integration.nats.subscribe(
            "ghostlink.agent.responses.>",
            handle_agent_response
        )

    async def start(self):
        """Start the Phase 2 system"""
        self.running = True
        logger.info("🚀 Starting GhostLink Phase 2 system")

        # Publish system startup event
        if self.nats_integration:
            await self.nats_integration.nats.publish_event(
                "system_startup",
                {
                    "phase": "phase2",
                    "components": self.component_status,
                    "config": self.config
                },
                source="phase2_system"
            )

        # Start background tasks
        health_check_task = asyncio.create_task(self._health_check_loop())
        nats_task = asyncio.create_task(self.nats_integration.start()) if self.nats_integration else None

        # Set up signal handlers
        def signal_handler(signum, frame):
            logger.info(f"🛑 Received signal {signum}, initiating shutdown...")
            asyncio.create_task(self.stop())

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            # Wait for shutdown signal
            while self.running:
                await asyncio.sleep(1)

                # Send periodic heartbeats
                if self.nats_integration:
                    await self.nats_integration.nats.send_heartbeat(
                        "phase2_system",
                        {
                            "status": self.component_status["system_health"],
                            "uptime": asyncio.get_event_loop().time(),
                            "active_components": sum(1 for v in self.component_status.values() if v is True)
                        }
                    )

        except Exception as e:
            logger.error(f"❌ Error in main loop: {e}")
        finally:
            # Cancel background tasks
            health_check_task.cancel()
            if nats_task:
                nats_task.cancel()

            await self.stop()

    async def stop(self):
        """Stop the Phase 2 system"""
        if not self.running:
            return

        logger.info("🛑 Stopping GhostLink Phase 2 system")
        self.running = False
        self.component_status["system_health"] = "shutting_down"

        # Publish shutdown event
        if self.nats_integration:
            await self.nats_integration.nats.publish_event(
                "system_shutdown",
                {
                    "phase": "phase2",
                    "shutdown_time": datetime.now().isoformat()
                },
                source="phase2_system"
            )

        # Shutdown components in reverse order
        if self.orchestrator:
            self.orchestrator.shutdown()

        if self.nats_integration:
            await self.nats_integration.stop()

        if self.telemetry:
            await self.telemetry.shutdown()

        logger.info("✅ GhostLink Phase 2 system shutdown complete")

    async def _health_check_loop(self):
        """Periodic health check loop"""
        while self.running:
            try:
                await asyncio.sleep(self.config["system"]["health_check_interval"])

                # Perform health checks
                health_status = await self._perform_health_checks()

                # Update system health
                if all(health_status.values()):
                    self.component_status["system_health"] = "healthy"
                else:
                    self.component_status["system_health"] = "degraded"

                # Publish health status
                if self.nats_integration:
                    await self.nats_integration.nats.publish_event(
                        "health_check",
                        {
                            "status": self.component_status["system_health"],
                            "component_health": health_status,
                            "timestamp": datetime.now().isoformat()
                        },
                        source="health_monitor"
                    )

                logger.debug(f"💓 Health check completed: {self.component_status['system_health']}")

            except Exception as e:
                logger.error(f"❌ Error in health check loop: {e}")

    async def _perform_health_checks(self) -> Dict[str, bool]:
        """Perform health checks on all components"""
        health_status = {}

        # Check NATS connectivity
        if self.nats_integration:
            health_status["nats"] = self.nats_integration.nats.connected
        else:
            health_status["nats"] = False

        # Check orchestrator
        if self.orchestrator:
            try:
                status = self.orchestrator.get_status()
                health_status["orchestrator"] = status.get("ray_initialized", False)
            except Exception:
                health_status["orchestrator"] = False
        else:
            health_status["orchestrator"] = False

        # Check telemetry
        if self.telemetry:
            health_status["telemetry"] = self.telemetry.initialized
        else:
            health_status["telemetry"] = False

        return health_status

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            "phase": "phase2",
            "running": self.running,
            "component_status": self.component_status.copy(),
            "config": self.config.copy(),
            "timestamp": datetime.now().isoformat()
        }

        # Add component-specific status
        if self.orchestrator:
            status["orchestrator_status"] = self.orchestrator.get_status()

        if self.telemetry:
            status["telemetry_status"] = self.telemetry.get_status()

        if self.nats_integration:
            status["nats_status"] = {
                "connected": self.nats_integration.nats.connected,
                "client_id": self.nats_integration.nats.client_id,
                "subscriptions": len(self.nats_integration.nats.subscriptions)
            }

        return status

    async def execute_command(self, command: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a system command"""
        parameters = parameters or {}

        try:
            if command == "submit_task":
                task_type = parameters.get("task_type")
                if not self.orchestrator:
                    return {"error": "Orchestrator not available"}

                if task_type == "compression":
                    from ghostlink_ray_orchestrator import CompressionType
                    task_id = self.orchestrator.submit_compression_task(
                        parameters["model_id"],
                        CompressionType(parameters["compression_type"]),
                        parameters.get("task_params", {})
                    )
                    return {"task_id": task_id, "status": "submitted"}

                elif task_type == "expansion":
                    from ghostlink_ray_orchestrator import ExpansionType
                    task_id = self.orchestrator.submit_expansion_task(
                        parameters["model_id"],
                        ExpansionType(parameters["expansion_type"]),
                        parameters.get("task_params", {})
                    )
                    return {"task_id": task_id, "status": "submitted"}

            elif command == "process_tasks":
                if self.orchestrator:
                    await self.orchestrator.process_tasks()
                    return {"status": "processed"}
                else:
                    return {"error": "Orchestrator not available"}

            elif command == "get_status":
                return self.get_status()

            elif command == "send_nats_message":
                if self.nats_integration:
                    success = await self.nats_integration.nats.publish(
                        parameters["subject"],
                        parameters["payload"]
                    )
                    return {"success": success}
                else:
                    return {"error": "NATS not available"}

            else:
                return {"error": f"Unknown command: {command}"}

        except Exception as e:
            logger.error(f"❌ Error executing command {command}: {e}")
            return {"error": str(e)}

        # Fallback return (should not be reached)
        return {"error": "Unexpected execution path"}

# CLI interface

async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="GhostLink Phase 2 System")
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--nats-servers", type=str, nargs="+", help="NATS servers")
    parser.add_argument("--otlp-endpoint", type=str, help="OTLP endpoint")
    parser.add_argument("--prometheus-port", type=int, help="Prometheus port")
    parser.add_argument("--command", type=str, help="Execute single command and exit")
    parser.add_argument("--command-params", type=str, help="JSON parameters for command")

    args = parser.parse_args()

    # Load configuration
    config = GhostLinkPhase2()._default_config()

    if args.config:
        try:
            with open(args.config, 'r') as f:
                config.update(json.load(f))
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return 1

    # Override with command line args
    if args.nats_servers:
        config["nats"]["servers"] = args.nats_servers
    if args.otlp_endpoint:
        config["telemetry"]["otlp_endpoint"] = args.otlp_endpoint
    if args.prometheus_port:
        config["telemetry"]["prometheus_port"] = args.prometheus_port

    # Create and initialize system
    system = GhostLinkPhase2(config)

    if not await system.initialize():
        logger.error("❌ Failed to initialize GhostLink Phase 2")
        return 1

    # Execute single command if requested
    if args.command:
        params = {}
        if args.command_params:
            try:
                params = json.loads(args.command_params)
            except Exception as e:
                logger.error(f"Failed to parse command params: {e}")
                return 1

        result = await system.execute_command(args.command, params)
        print(json.dumps(result, indent=2))
        await system.stop()
        return 0

    # Start the system
    try:
        await system.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    finally:
        await system.stop()

    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

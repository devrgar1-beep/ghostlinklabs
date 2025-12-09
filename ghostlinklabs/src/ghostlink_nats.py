#!/usr/bin/env python3
"""
GhostLink NATS Messaging Integration
High-performance messaging system for distributed AI orchestration
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Set
from dataclasses import dataclass, field
import time

import nats
from nats.aio.client import Client as NATSClient
from nats.aio.errors import ErrTimeout, ErrNoServers

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Message:
    """NATS message structure"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    subject: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    reply_to: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    headers: Dict[str, str] = field(default_factory=dict)

    def to_json(self) -> str:
        """Convert message to JSON string"""
        data = {
            "id": self.id,
            "subject": self.subject,
            "payload": self.payload,
            "reply_to": self.reply_to,
            "timestamp": self.timestamp.isoformat(),
            "headers": self.headers
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        """Create message from JSON string"""
        data = json.loads(json_str)
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)

class NATSMessaging:
    """NATS messaging system for GhostLink"""

    def __init__(self, servers: List[str] = None, client_id: str = None):
        self.servers = servers or ["nats://localhost:4222"]
        self.client_id = client_id or f"ghostlink-{uuid.uuid4().hex[:8]}"
        self.nc: Optional[NATSClient] = None
        self.subscriptions: Dict[str, str] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self.request_handlers: Dict[str, Callable] = {}
        self.connected = False

        # Message queues
        self.agent_tasks_queue = "ghostlink.agent.tasks"
        self.agent_responses_queue = "ghostlink.agent.responses"
        self.events_stream = "ghostlink.events"
        self.heartbeats_subject = "ghostlink.heartbeats"
        self.model_updates_subject = "ghostlink.model.updates"
        self.orchestrator_commands = "ghostlink.orchestrator.commands"

    async def connect(self) -> bool:
        """Connect to NATS servers"""
        try:
            self.nc = NATSClient()

            # Connect with reconnection settings
            await self.nc.connect(
                servers=self.servers,
                name=self.client_id,
                reconnect_time_wait=2,
                max_reconnect_attempts=10,
                ping_interval=20,
                max_outstanding_pings=5,
            )

            self.connected = True
            logger.info(f"✅ Connected to NATS as {self.client_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to connect to NATS: {e}")
            return False

    async def disconnect(self):
        """Disconnect from NATS"""
        if self.nc and self.connected:
            # Unsubscribe from all subjects
            for sid in self.subscriptions.values():
                try:
                    await self.nc.unsubscribe(sid)
                except Exception as e:
                    logger.warning(f"Error unsubscribing {sid}: {e}")

            await self.nc.close()
            self.connected = False
            logger.info("✅ Disconnected from NATS")

    async def publish(self, subject: str, payload: Dict[str, Any],
                     headers: Dict[str, str] = None) -> bool:
        """Publish a message to a subject"""
        if not self.connected:
            logger.warning("Not connected to NATS")
            return False

        try:
            message = Message(subject=subject, payload=payload, headers=headers or {})
            data = message.to_json()

            await self.nc.publish(subject, data.encode())
            logger.debug(f"📤 Published to {subject}: {len(data)} bytes")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to publish to {subject}: {e}")
            return False

    async def request(self, subject: str, payload: Dict[str, Any],
                     timeout: float = 5.0) -> Optional[Dict[str, Any]]:
        """Send a request and wait for response"""
        if not self.connected:
            logger.warning("Not connected to NATS")
            return None

        try:
            message = Message(subject=subject, payload=payload)
            data = message.to_json()

            response = await self.nc.request(subject, data.encode(), timeout=timeout)
            if response.data:
                response_msg = Message.from_json(response.data.decode())
                return response_msg.payload
            return None

        except ErrTimeout:
            logger.warning(f"Request to {subject} timed out")
            return None
        except Exception as e:
            logger.error(f"❌ Request failed: {e}")
            return None

    async def subscribe(self, subject: str, handler: Callable,
                       queue_group: str = None) -> Optional[str]:
        """Subscribe to a subject"""
        if not self.connected:
            logger.warning("Not connected to NATS")
            return None

        try:
            async def message_handler(msg):
                try:
                    message = Message.from_json(msg.data.decode())
                    await handler(message)
                except Exception as e:
                    logger.error(f"Error handling message on {subject}: {e}")

            sid = await self.nc.subscribe(subject, queue_group=queue_group, cb=message_handler)
            self.subscriptions[subject] = sid
            logger.info(f"📡 Subscribed to {subject} (sid: {sid})")
            return sid

        except Exception as e:
            logger.error(f"❌ Failed to subscribe to {subject}: {e}")
            return None

    async def unsubscribe(self, subject: str) -> bool:
        """Unsubscribe from a subject"""
        if subject in self.subscriptions:
            try:
                await self.nc.unsubscribe(self.subscriptions[subject])
                del self.subscriptions[subject]
                logger.info(f"📡 Unsubscribed from {subject}")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to unsubscribe from {subject}: {e}")
        return False

    # High-level messaging methods for GhostLink

    async def send_agent_task(self, agent_id: str, task_type: str,
                             task_data: Dict[str, Any]) -> bool:
        """Send a task to a specific agent"""
        subject = f"{self.agent_tasks_queue}.{agent_id}"
        payload = {
            "task_type": task_type,
            "task_data": task_data,
            "timestamp": datetime.now().isoformat()
        }
        return await self.publish(subject, payload)

    async def send_broadcast_task(self, task_type: str, task_data: Dict[str, Any],
                                 agent_filter: List[str] = None) -> bool:
        """Broadcast a task to all agents (or filtered list)"""
        payload = {
            "task_type": task_type,
            "task_data": task_data,
            "agent_filter": agent_filter,
            "broadcast": True,
            "timestamp": datetime.now().isoformat()
        }
        return await self.publish(self.agent_tasks_queue, payload)

    async def send_agent_response(self, agent_id: str, task_id: str,
                                 response: Dict[str, Any]) -> bool:
        """Send agent response back to orchestrator"""
        subject = f"{self.agent_responses_queue}.{agent_id}"
        payload = {
            "task_id": task_id,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        return await self.publish(subject, payload)

    async def publish_event(self, event_type: str, event_data: Dict[str, Any],
                           source: str = "system") -> bool:
        """Publish a system event"""
        payload = {
            "event_type": event_type,
            "event_data": event_data,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        return await self.publish(f"{self.events_stream}.{event_type}", payload)

    async def send_heartbeat(self, component_id: str, status: Dict[str, Any]) -> bool:
        """Send heartbeat from a component"""
        payload = {
            "component_id": component_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        return await self.publish(f"{self.heartbeats_subject}.{component_id}", payload)

    async def publish_model_update(self, model_id: str, update_type: str,
                                  update_data: Dict[str, Any]) -> bool:
        """Publish model update event"""
        payload = {
            "model_id": model_id,
            "update_type": update_type,
            "update_data": update_data,
            "timestamp": datetime.now().isoformat()
        }
        return await self.publish(f"{self.model_updates_subject}.{model_id}", payload)

    async def send_orchestrator_command(self, command: str, parameters: Dict[str, Any],
                                       target_agents: List[str] = None) -> bool:
        """Send command to orchestrator"""
        payload = {
            "command": command,
            "parameters": parameters,
            "target_agents": target_agents,
            "timestamp": datetime.now().isoformat()
        }
        return await self.publish(self.orchestrator_commands, payload)

    # Request/Response patterns

    async def request_agent_status(self, agent_id: str, timeout: float = 3.0) -> Optional[Dict[str, Any]]:
        """Request status from a specific agent"""
        subject = f"ghostlink.agent.{agent_id}.status"
        return await self.request(subject, {"request": "status"}, timeout=timeout)

    async def request_model_info(self, model_id: str, timeout: float = 3.0) -> Optional[Dict[str, Any]]:
        """Request information about a model"""
        subject = f"ghostlink.model.{model_id}.info"
        return await self.request(subject, {"request": "info"}, timeout=timeout)

    async def request_system_health(self, timeout: float = 3.0) -> Optional[Dict[str, Any]]:
        """Request overall system health"""
        return await self.request("ghostlink.system.health", {"request": "health"}, timeout=timeout)

    # Setup methods for common subscriptions

    async def setup_agent_subscriptions(self, agent_id: str,
                                       task_handler: Callable,
                                       response_handler: Callable = None) -> bool:
        """Set up subscriptions for an agent"""
        try:
            # Subscribe to tasks for this agent
            await self.subscribe(f"{self.agent_tasks_queue}.{agent_id}", task_handler)

            # Subscribe to broadcast tasks
            await self.subscribe(self.agent_tasks_queue, task_handler, queue_group="agents")

            # Subscribe to events
            await self.subscribe(f"{self.events_stream}.>", self._default_event_handler)

            # Set up response handler if provided
            if response_handler:
                await self.subscribe(f"{self.agent_responses_queue}.{agent_id}", response_handler)

            logger.info(f"✅ Agent {agent_id} subscriptions set up")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to set up agent subscriptions: {e}")
            return False

    async def setup_orchestrator_subscriptions(self,
                                              response_handler: Callable,
                                              command_handler: Callable,
                                              event_handler: Callable = None) -> bool:
        """Set up subscriptions for the orchestrator"""
        try:
            # Subscribe to all agent responses
            await self.subscribe(f"{self.agent_responses_queue}.>", response_handler)

            # Subscribe to orchestrator commands
            await self.subscribe(self.orchestrator_commands, command_handler)

            # Subscribe to events
            if event_handler:
                await self.subscribe(f"{self.events_stream}.>", event_handler)
            else:
                await self.subscribe(f"{self.events_stream}.>", self._default_event_handler)

            # Subscribe to heartbeats
            await self.subscribe(f"{self.heartbeats_subject}.>", self._default_heartbeat_handler)

            logger.info("✅ Orchestrator subscriptions set up")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to set up orchestrator subscriptions: {e}")
            return False

    # Default handlers

    async def _default_event_handler(self, message: Message):
        """Default event handler"""
        logger.info(f"📢 Event: {message.subject} - {message.payload}")

    async def _default_heartbeat_handler(self, message: Message):
        """Default heartbeat handler"""
        component_id = message.subject.split('.')[-1]
        logger.debug(f"💓 Heartbeat from {component_id}: {message.payload.get('status', {})}")

class NATSIntegration:
    """Integration layer between NATS messaging and Ray orchestrator"""

    def __init__(self, nats_servers: List[str] = None):
        self.nats = NATSMessaging(servers=nats_servers)
        self.orchestrator = None
        self.agent_connections: Set[str] = set()
        self.running = False

    async def initialize(self) -> bool:
        """Initialize NATS integration"""
        if not await self.nats.connect():
            return False

        # Import here to avoid circular imports
        try:
            from ghostlink_ray_orchestrator import ProductionRayOrchestrator
            self.orchestrator = ProductionRayOrchestrator(num_workers=4)
        except ImportError:
            logger.warning("Ray orchestrator not available, running NATS-only mode")
            self.orchestrator = None

        # Set up orchestrator subscriptions
        await self.nats.setup_orchestrator_subscriptions(
            response_handler=self._handle_agent_response,
            command_handler=self._handle_orchestrator_command,
            event_handler=self._handle_system_event
        )

        logger.info("✅ NATS integration initialized")
        return True

    async def start(self):
        """Start the NATS integration"""
        self.running = True
        logger.info("🚀 NATS integration started")

        # Send startup event
        await self.nats.publish_event("system_startup", {
            "component": "nats_integration",
            "orchestrator_available": self.orchestrator is not None
        })

        # Keep running
        while self.running:
            await asyncio.sleep(1)

            # Send periodic health check
            await self.nats.send_heartbeat("nats_integration", {
                "status": "healthy",
                "connected_agents": len(self.agent_connections),
                "uptime": time.time()
            })

    async def stop(self):
        """Stop the NATS integration"""
        self.running = False

        # Send shutdown event
        await self.nats.publish_event("system_shutdown", {
            "component": "nats_integration"
        })

        await self.nats.disconnect()

        if self.orchestrator:
            self.orchestrator.shutdown()

        logger.info("🛑 NATS integration stopped")

    async def _handle_agent_response(self, message: Message):
        """Handle agent response messages"""
        subject_parts = message.subject.split('.')
        if len(subject_parts) >= 3:
            agent_id = subject_parts[2]

            if self.orchestrator:
                # Forward to Ray orchestrator for processing
                logger.info(f"📥 Agent {agent_id} response: {message.payload}")
            else:
                logger.info(f"📥 Agent {agent_id} response (no orchestrator): {message.payload}")

    async def _handle_orchestrator_command(self, message: Message):
        """Handle orchestrator command messages"""
        command = message.payload.get("command")
        parameters = message.payload.get("parameters", {})

        logger.info(f"🎮 Orchestrator command: {command}")

        if command == "submit_task" and self.orchestrator:
            # Submit task to Ray orchestrator
            task_type = parameters.get("task_type")
            if task_type == "compression":
                from ghostlink_ray_orchestrator import CompressionType
                self.orchestrator.submit_compression_task(
                    parameters["model_id"],
                    CompressionType(parameters["compression_type"]),
                    parameters.get("task_params", {})
                )
            elif task_type == "expansion":
                from ghostlink_ray_orchestrator import ExpansionType
                self.orchestrator.submit_expansion_task(
                    parameters["model_id"],
                    ExpansionType(parameters["expansion_type"]),
                    parameters.get("task_params", {})
                )

        elif command == "process_tasks" and self.orchestrator:
            # Process pending tasks
            asyncio.create_task(self.orchestrator.process_tasks())

        elif command == "get_status":
            # Return system status
            status = {
                "nats_connected": self.nats.connected,
                "orchestrator_available": self.orchestrator is not None,
                "connected_agents": len(self.agent_connections)
            }
            if self.orchestrator:
                status.update(self.orchestrator.get_status())

            await self.nats.publish("ghostlink.system.status", status)

    async def _handle_system_event(self, message: Message):
        """Handle system events"""
        event_type = message.subject.split('.')[-1]
        logger.info(f"🌟 System event: {event_type} from {message.payload.get('source', 'unknown')}")

# Standalone functions for easy use

async def create_nats_integration(servers: List[str] = None) -> NATSIntegration:
    """Create and initialize NATS integration"""
    integration = NATSIntegration(nats_servers=servers)
    if await integration.initialize():
        return integration
    return None

async def send_agent_task(nats_integration: NATSIntegration, agent_id: str,
                         task_type: str, task_data: Dict[str, Any]) -> bool:
    """Send a task to an agent via NATS"""
    return await nats_integration.nats.send_agent_task(agent_id, task_type, task_data)

async def publish_event(nats_integration: NATSIntegration, event_type: str,
                       event_data: Dict[str, Any], source: str = "system") -> bool:
    """Publish an event via NATS"""
    return await nats_integration.nats.publish_event(event_type, event_data, source)

# Test/demo functions

async def demo_nats_messaging():
    """Demonstrate NATS messaging capabilities"""
    print("🐱 NATS Messaging Demo")
    print("=" * 40)

    # Create integration
    integration = NATSIntegration()
    if not await integration.initialize():
        print("❌ Failed to initialize NATS integration")
        return

    try:
        # Send some demo messages
        print("📤 Sending demo messages...")

        # Send agent task
        await integration.nats.send_agent_task("demo_agent", "compression", {
            "model_id": "test_model",
            "compression_ratio": 0.3
        })
        print("✅ Sent agent task")

        # Send broadcast task
        await integration.nats.send_broadcast_task("heartbeat", {})
        print("✅ Sent broadcast task")

        # Publish event
        await integration.nats.publish_event("model_updated", {
            "model_id": "consciousness_v1",
            "update_type": "compression",
            "new_size_mb": 250.0
        })
        print("✅ Published event")

        # Send heartbeat
        await integration.nats.send_heartbeat("demo_component", {
            "status": "healthy",
            "cpu_usage": 45.2,
            "memory_usage": 67.8
        })
        print("✅ Sent heartbeat")

        print("\\n🎉 NATS messaging demo completed successfully!")

    finally:
        await integration.stop()

if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_nats_messaging())

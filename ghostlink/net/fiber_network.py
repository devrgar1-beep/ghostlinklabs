"""Internal Fiber Communication Network for GhostLink agents and components."""

import asyncio
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import time
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Set

from ..utils.logging import setup_logging

logger = setup_logging()


@dataclass
class FiberMessage:
    """Message structure for fiber communication."""

    message_id: str
    sender: str
    recipient: str
    channel: str
    payload: Dict[str, Any]
    priority: int = 1  # 1=low, 5=high
    timestamp: float = field(default_factory=time.time)
    ttl: int = 30  # Time to live in seconds
    reply_to: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization."""
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "channel": self.channel,
            "payload": self.payload,
            "priority": self.priority,
            "timestamp": self.timestamp,
            "ttl": self.ttl,
            "reply_to": self.reply_to,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FiberMessage":
        """Create message from dictionary."""
        return cls(
            message_id=data["message_id"],
            sender=data["sender"],
            recipient=data["recipient"],
            channel=data["channel"],
            payload=data["payload"],
            priority=data.get("priority", 1),
            timestamp=data.get("timestamp", time.time()),
            ttl=data.get("ttl", 30),
            reply_to=data.get("reply_to"),
        )

    def is_expired(self) -> bool:
        """Check if message has expired."""
        return time.time() - self.timestamp > self.ttl


@dataclass
class FiberChannel:
    """Communication channel within the fiber network."""

    name: str
    subscribers: Set[str] = field(default_factory=set)
    message_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    bandwidth_limit: int = 1000  # messages per second
    active: bool = True

    async def publish(self, message: FiberMessage) -> bool:
        """Publish a message to the channel."""
        if not self.active:
            return False

        try:
            await asyncio.wait_for(self.message_queue.put(message), timeout=1.0)
            return True
        except asyncio.TimeoutError:
            logger.warning(f"Channel {self.name} queue full, dropping message")
            return False

    async def subscribe(self, subscriber_id: str) -> AsyncGenerator[FiberMessage, None]:
        """Subscribe to channel messages."""
        self.subscribers.add(subscriber_id)
        try:
            while self.active:
                try:
                    message = await asyncio.wait_for(self.message_queue.get(), timeout=0.1)
                    if message.recipient in [subscriber_id, "*"]:
                        # * = broadcast
                        yield message
                    self.message_queue.task_done()
                except asyncio.TimeoutError:
                    continue
        finally:
            self.subscribers.discard(subscriber_id)


class FiberRouter:
    """Routes messages through the fiber network."""

    def __init__(self):
        self.channels: Dict[str, FiberChannel] = {}
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.routing_table: Dict[str, str] = {}  # agent -> channel
        self.message_history: deque = deque(maxlen=1000)
        self.executor = ThreadPoolExecutor(max_workers=4)

    def create_channel(self, name: str, bandwidth_limit: int = 1000) -> FiberChannel:
        """Create a new communication channel."""
        if name in self.channels:
            return self.channels[name]

        channel = FiberChannel(name=name, bandwidth_limit=bandwidth_limit)
        self.channels[name] = channel
        logger.info(f"Created fiber channel: {name}")
        return channel

    def register_agent(self, agent_id: str, agent_info: Dict[str, Any]) -> str:
        """Register an agent in the fiber network."""
        self.agent_registry[agent_id] = {
            **agent_info,
            "registered_at": time.time(),
            "status": "active",
        }

        # Auto-assign to appropriate channel based on agent role
        role = agent_info.get("role", "general")
        channel_name = f"fiber_{role}"

        if channel_name not in self.channels:
            self.create_channel(channel_name)

        self.routing_table[agent_id] = channel_name
        logger.info(f"Registered agent {agent_id} on channel {channel_name}")
        return channel_name

    def unregister_agent(self, agent_id: str):
        """Unregister an agent from the network."""
        if agent_id in self.agent_registry:
            del self.agent_registry[agent_id]
        if agent_id in self.routing_table:
            del self.routing_table[agent_id]
        logger.info(f"Unregistered agent {agent_id}")

    async def route_message(self, message: FiberMessage) -> bool:
        """Route a message through the fiber network."""
        # Record message in history
        self.message_history.append(message)

        # Find target channel
        if message.recipient in self.routing_table:
            channel_name = self.routing_table[message.recipient]
        elif message.channel in self.channels:
            channel_name = message.channel
        else:
            # Try general channel
            channel_name = "fiber_general"
            if channel_name not in self.channels:
                self.create_channel(channel_name)

        channel = self.channels[channel_name]

        # Publish message
        success = await channel.publish(message)
        if success:
            logger.debug(f"Routed message {message.message_id} to channel {channel_name}")
        else:
            logger.warning(f"Failed to route message {message.message_id}")

        return success

    def discover_agents(self, role_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Discover available agents in the network."""
        agents = []
        for agent_id, info in self.agent_registry.items():
            if info.get("status") == "active":
                if role_filter is None or info.get("role") == role_filter:
                    agents.append({"id": agent_id, **info})
        return agents

    def get_channel_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all channels."""
        stats = {}
        for name, channel in self.channels.items():
            stats[name] = {
                "subscribers": len(channel.subscribers),
                "queue_size": (
                    channel.message_queue.qsize() if hasattr(channel.message_queue, "qsize") else 0
                ),
                "active": channel.active,
                "bandwidth_limit": channel.bandwidth_limit,
            }
        return stats


class FiberNetwork:
    """Main fiber communication network coordinator."""

    def __init__(self):
        self.router = FiberRouter()
        self.message_handlers: Dict[str, Callable] = {}
        self.running = False
        self.network_task: Optional[asyncio.Task] = None

    async def start(self):
        """Start the fiber network."""
        if self.running:
            return

        self.running = True
        logger.info("Starting internal fiber communication network")

        # Create core channels
        self.router.create_channel("fiber_system")  # System messages
        self.router.create_channel("fiber_agents")  # Agent coordination
        self.router.create_channel("fiber_general")  # General communication

        # Start network monitoring
        self.network_task = asyncio.create_task(self._monitor_network())

        logger.info("Fiber communication network started")

    async def stop(self):
        """Stop the fiber network."""
        if not self.running:
            return

        self.running = False
        if self.network_task:
            self.network_task.cancel()
            try:
                await self.network_task
            except asyncio.CancelledError:
                pass

        logger.info("Fiber communication network stopped")

    async def send_message(
        self,
        sender: str,
        recipient: str,
        channel: str,
        payload: Dict[str, Any],
        priority: int = 1,
        reply_to: Optional[str] = None,
    ) -> str:
        """Send a message through the fiber network."""
        if not self.running:
            raise RuntimeError("Network not running. Call start() first.")

        message_id = f"msg_{int(time.time() * 1000000)}_{sender}"

        message = FiberMessage(
            message_id=message_id,
            sender=sender,
            recipient=recipient,
            channel=channel,
            payload=payload,
            priority=priority,
            reply_to=reply_to,
        )

        success = await self.router.route_message(message)
        return message_id if success else ""

    async def broadcast(
        self, sender: str, channel: str, payload: Dict[str, Any], priority: int = 1
    ) -> int:
        """Broadcast a message to all subscribers on a channel."""
        message = FiberMessage(
            message_id=f"broadcast_{int(time.time() * 1000000)}_{sender}",
            sender=sender,
            recipient="*",  # Broadcast
            channel=channel,
            payload=payload,
            priority=priority,
        )

        success = await self.router.route_message(message)
        return 1 if success else 0

    def register_message_handler(self, message_type: str, handler: Callable[[FiberMessage], Any]):
        """Register a handler for specific message types."""
        self.message_handlers[message_type] = handler

    async def listen_for_messages(
        self, agent_id: str, channel: str
    ) -> AsyncGenerator[FiberMessage, None]:
        """Listen for messages on a specific channel."""
        if channel not in self.router.channels:
            self.router.create_channel(channel)

        async for message in self.router.channels[channel].subscribe(agent_id):
            # Process message through handlers
            msg_type = message.payload.get("type", "unknown")
            if msg_type in self.message_handlers:
                try:
                    await self.message_handlers[msg_type](message)
                except Exception as e:
                    logger.error(f"Error in message handler for {msg_type}: {e}")

            yield message

    def register_agent(self, agent_id: str, agent_info: Dict[str, Any]) -> str:
        """Register an agent with the fiber network."""
        return self.router.register_agent(agent_id, agent_info)

    def unregister_agent(self, agent_id: str):
        """Unregister an agent from the network."""
        self.router.unregister_agent(agent_id)

    def discover_agents(self, role_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Discover available agents."""
        return self.router.discover_agents(role_filter)

    def get_network_stats(self) -> Dict[str, Any]:
        """Get comprehensive network statistics."""
        return {
            "channels": self.router.get_channel_stats(),
            "agents": len(self.router.agent_registry),
            "messages_routed": len(self.router.message_history),
            "running": self.running,
        }

    async def _monitor_network(self):
        """Monitor network health and performance."""
        while self.running:
            try:
                # Clean up expired messages
                expired_count = 0
                for message in list(self.router.message_history):
                    if hasattr(message, "is_expired") and message.is_expired():
                        self.router.message_history.remove(message)
                        expired_count += 1

                if expired_count > 0:
                    logger.debug(f"Cleaned up {expired_count} expired messages")

                # Log stats periodically
                stats = self.get_network_stats()
                logger.debug(f"Network stats: {stats}")

                await asyncio.sleep(60)  # Monitor every minute

            except Exception as e:
                logger.error(f"Error in network monitoring: {e}")
                await asyncio.sleep(10)


# Global fiber network instance
fiber_network = FiberNetwork()


# Integration with autonomous agents
async def send_agent_message(
    sender: str, recipient: str, message_type: str, payload: Dict[str, Any]
) -> str:
    """Send a message between agents through the fiber network."""
    return await fiber_network.send_message(
        sender=sender,
        recipient=recipient,
        channel="fiber_agents",
        payload={"type": message_type, **payload},
    )


async def broadcast_to_agents(sender: str, message_type: str, payload: Dict[str, Any]) -> int:
    """Broadcast a message to all agents."""
    return await fiber_network.broadcast(
        sender=sender, channel="fiber_agents", payload={"type": message_type, **payload}
    )


def register_agent_in_network(agent_id: str, role: str) -> str:
    """Register an agent with the fiber network."""
    return fiber_network.register_agent(agent_id, {"role": role, "type": "autonomous_agent"})


async def agent_listen_for_messages(agent_id: str) -> AsyncGenerator[FiberMessage, None]:
    """Listen for messages addressed to a specific agent."""
    async for message in fiber_network.listen_for_messages(agent_id, "fiber_agents"):
        yield message

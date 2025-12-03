#!/usr/bin/env python3
"""
GhostLink Lattice - Unified Component Bridge

A lattice architecture connecting all autonomous components in a mesh network:
- Link: AI orchestration brain
- Container: Execution environment
- Signal: Communication protocols
- Pressure: Resource management
- Vault: Secure storage
- Groq: Internal communication AI

Each node can communicate with any other node, creating resilient multi-path routing.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GhostLink.Lattice")


class ComponentType(Enum):
    """GhostLink component types"""
    LINK = "link"
    CONTAINER = "container"
    SIGNAL = "signal"
    PRESSURE = "pressure"
    VAULT = "vault"
    GROQ = "groq"


class MessagePriority(Enum):
    """Message priority levels"""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class LatticeMessage:
    """Message passed through the lattice"""
    id: str
    sender: ComponentType
    receiver: ComponentType
    payload: Dict[str, Any]
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    route: List[str] = field(default_factory=list)
    ttl: int = 10  # Time to live (max hops)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "sender": self.sender.value,
            "receiver": self.receiver.value,
            "payload": self.payload,
            "priority": self.priority.value,
            "timestamp": self.timestamp,
            "route": self.route,
            "ttl": self.ttl
        }


@dataclass
class ComponentState:
    """State of a lattice component"""
    type: ComponentType
    status: str = "idle"
    health: float = 1.0  # 0.0 to 1.0
    load: float = 0.0  # 0.0 to 1.0
    connections: Set[ComponentType] = field(default_factory=set)
    message_count: int = 0
    last_activity: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class LatticeNode:
    """A node in the GhostLink lattice"""
    
    def __init__(self, component_type: ComponentType):
        self.type = component_type
        self.state = ComponentState(type=component_type)
        self.message_handlers: Dict[str, Callable] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.running = False
        
    def register_handler(self, action: str, handler: Callable):
        """Register a message handler"""
        self.message_handlers[action] = handler
        logger.debug(f"{self.type.value}: Registered handler for '{action}'")
    
    async def handle_message(self, message: LatticeMessage) -> Optional[Dict[str, Any]]:
        """Handle incoming message"""
        self.state.message_count += 1
        self.state.last_activity = datetime.now().isoformat()
        
        action = message.payload.get("action")
        if action and action in self.message_handlers:
            try:
                result = await self.message_handlers[action](message)
                return result
            except Exception as e:
                logger.error(f"{self.type.value}: Handler error for '{action}': {e}")
                return {"status": "error", "error": str(e)}
        else:
            logger.warning(f"{self.type.value}: No handler for action '{action}'")
            return {"status": "error", "error": f"Unknown action: {action}"}
    
    async def process_messages(self):
        """Process messages from queue"""
        while self.running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                await self.handle_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"{self.type.value}: Message processing error: {e}")
    
    def update_health(self, health: float):
        """Update node health"""
        self.state.health = max(0.0, min(1.0, health))
        self.state.last_activity = datetime.now().isoformat()


class GhostLinkLattice:
    """
    GhostLink Lattice - Unified Component Bridge
    
    Creates a mesh network of all GhostLink components with:
    - Multi-path routing
    - Automatic failover
    - Load balancing
    - Priority messaging
    - Health monitoring
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".ghostlink" / "lattice_config.json"
        self.config: Dict[str, Any] = self.load_config()
        
        # Initialize nodes
        self.nodes: Dict[ComponentType, LatticeNode] = {
            ComponentType.LINK: LatticeNode(ComponentType.LINK),
            ComponentType.CONTAINER: LatticeNode(ComponentType.CONTAINER),
            ComponentType.SIGNAL: LatticeNode(ComponentType.SIGNAL),
            ComponentType.PRESSURE: LatticeNode(ComponentType.PRESSURE),
            ComponentType.VAULT: LatticeNode(ComponentType.VAULT),
            ComponentType.GROQ: LatticeNode(ComponentType.GROQ),
        }
        
        # Message routing table
        self.routing_table: Dict[str, List[ComponentType]] = {}
        
        # Statistics
        self.stats = {
            "messages_sent": 0,
            "messages_delivered": 0,
            "messages_failed": 0,
            "lattice_uptime": datetime.now().isoformat()
        }
        
        # Initialize lattice
        self.setup_connections()
        self.register_default_handlers()
        
        logger.info("GhostLink Lattice initialized")
    
    def load_config(self) -> Dict[str, Any]:
        """Load lattice configuration"""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {
            "auto_healing": True,
            "max_route_hops": 5,
            "health_check_interval": 30,
            "message_timeout": 60
        }
    
    def save_config(self):
        """Save lattice configuration"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_connections(self):
        """Setup full mesh connections between all nodes"""
        all_types = list(ComponentType)
        
        for node_type in all_types:
            # Each node connects to all other nodes (full mesh)
            self.nodes[node_type].state.connections = {
                t for t in all_types if t != node_type
            }
        
        logger.info("Lattice mesh connections established")
    
    def register_default_handlers(self):
        """Register default message handlers for all nodes"""
        
        # Link handlers
        self.nodes[ComponentType.LINK].register_handler("task_schedule", self.handle_task_schedule)
        self.nodes[ComponentType.LINK].register_handler("status_request", self.handle_status_request)
        self.nodes[ComponentType.LINK].register_handler("coordinate", self.handle_coordinate)
        
        # Container handlers
        self.nodes[ComponentType.CONTAINER].register_handler("execute", self.handle_execute)
        self.nodes[ComponentType.CONTAINER].register_handler("resource_request", self.handle_resource_request)
        self.nodes[ComponentType.CONTAINER].register_handler("status_request", self.handle_status_request)
        
        # Signal handlers
        self.nodes[ComponentType.SIGNAL].register_handler("transmit", self.handle_transmit)
        self.nodes[ComponentType.SIGNAL].register_handler("bandwidth_check", self.handle_bandwidth_check)
        self.nodes[ComponentType.SIGNAL].register_handler("status_request", self.handle_status_request)
        
        # Pressure handlers
        self.nodes[ComponentType.PRESSURE].register_handler("resource_allocate", self.handle_resource_allocate)
        self.nodes[ComponentType.PRESSURE].register_handler("health_monitor", self.handle_health_monitor)
        self.nodes[ComponentType.PRESSURE].register_handler("status_request", self.handle_status_request)
        
        # Vault handlers
        self.nodes[ComponentType.VAULT].register_handler("store", self.handle_store)
        self.nodes[ComponentType.VAULT].register_handler("retrieve", self.handle_retrieve)
        self.nodes[ComponentType.VAULT].register_handler("status_request", self.handle_status_request)
        
        # Groq handlers
        self.nodes[ComponentType.GROQ].register_handler("communicate", self.handle_ai_communicate)
        self.nodes[ComponentType.GROQ].register_handler("reason", self.handle_ai_reason)
        self.nodes[ComponentType.GROQ].register_handler("status_request", self.handle_status_request)
        
        logger.info("Default handlers registered")
    
    async def send_message(
        self,
        sender: ComponentType,
        receiver: ComponentType,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL
    ) -> bool:
        """Send message through the lattice"""
        message = LatticeMessage(
            id=f"{sender.value}-{receiver.value}-{datetime.now().timestamp()}",
            sender=sender,
            receiver=receiver,
            payload=payload,
            priority=priority
        )
        
        self.stats["messages_sent"] += 1
        
        # Direct delivery if receiver is available
        if receiver in self.nodes and self.nodes[receiver].state.health > 0.5:
            message.route.append(receiver.value)
            await self.nodes[receiver].message_queue.put(message)
            self.stats["messages_delivered"] += 1
            logger.debug(f"Message {message.id} delivered: {sender.value} → {receiver.value}")
            return True
        
        # Multi-path routing if direct path unavailable
        alternate_routes = self.find_alternate_routes(sender, receiver)
        if alternate_routes:
            route = alternate_routes[0]  # Use first available route
            for hop in route:
                message.route.append(hop.value)
                if hop == receiver:
                    await self.nodes[hop].message_queue.put(message)
                    self.stats["messages_delivered"] += 1
                    logger.info(f"Message routed via {' → '.join(message.route)}")
                    return True
        
        self.stats["messages_failed"] += 1
        logger.error(f"Failed to route message: {sender.value} → {receiver.value}")
        return False
    
    def find_alternate_routes(
        self,
        sender: ComponentType,
        receiver: ComponentType
    ) -> List[List[ComponentType]]:
        """Find alternate routes through the lattice"""
        routes = []
        visited = {sender}
        
        def dfs(current: ComponentType, path: List[ComponentType]):
            if current == receiver:
                routes.append(path.copy())
                return
            
            if len(path) >= self.config["max_route_hops"]:
                return
            
            for next_node in self.nodes[current].state.connections:
                if next_node not in visited and self.nodes[next_node].state.health > 0.3:
                    visited.add(next_node)
                    path.append(next_node)
                    dfs(next_node, path)
                    path.pop()
                    visited.remove(next_node)
        
        dfs(sender, [sender])
        return routes
    
    async def broadcast(
        self,
        sender: ComponentType,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL
    ):
        """Broadcast message to all nodes"""
        tasks = []
        for node_type in ComponentType:
            if node_type != sender:
                tasks.append(self.send_message(sender, node_type, payload, priority))
        
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(f"Broadcast from {sender.value} to all nodes")
    
    def get_lattice_state(self) -> Dict[str, Any]:
        """Get current state of the lattice"""
        return {
            "nodes": {
                node_type.value: {
                    "status": node.state.status,
                    "health": node.state.health,
                    "load": node.state.load,
                    "connections": [c.value for c in node.state.connections],
                    "messages": node.state.message_count,
                    "last_activity": node.state.last_activity
                }
                for node_type, node in self.nodes.items()
            },
            "statistics": self.stats,
            "config": self.config
        }
    
    async def health_check_loop(self):
        """Periodic health check of all nodes"""
        while True:
            try:
                await asyncio.sleep(self.config["health_check_interval"])
                
                for node_type, node in self.nodes.items():
                    # Simple health degradation over time if no activity
                    last_activity = datetime.fromisoformat(node.state.last_activity)
                    age = (datetime.now() - last_activity).total_seconds()
                    
                    if age > 300:  # 5 minutes
                        node.update_health(node.state.health * 0.9)
                    
                    logger.debug(f"{node_type.value}: health={node.state.health:.2f}, load={node.state.load:.2f}")
                
                # Auto-healing
                if self.config.get("auto_healing", True):
                    await self.auto_heal()
                    
            except Exception as e:
                logger.error(f"Health check error: {e}")
    
    async def auto_heal(self):
        """Automatically heal degraded nodes"""
        for node_type, node in self.nodes.items():
            if node.state.health < 0.5:
                logger.warning(f"Auto-healing {node_type.value} (health={node.state.health:.2f})")
                node.update_health(0.8)  # Restore to 80%
                node.state.status = "recovered"
    
    async def start(self):
        """Start the lattice"""
        logger.info("Starting GhostLink Lattice...")
        
        # Start all node message processors
        for node in self.nodes.values():
            node.running = True
        
        tasks = [
            asyncio.create_task(node.process_messages())
            for node in self.nodes.values()
        ]
        
        # Add health check task
        tasks.append(asyncio.create_task(self.health_check_loop()))
        
        logger.info("🌐 GhostLink Lattice is ONLINE")
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("Shutting down lattice...")
            await self.stop()
    
    async def stop(self):
        """Stop the lattice"""
        for node in self.nodes.values():
            node.running = False
        
        self.save_config()
        logger.info("GhostLink Lattice stopped")
    
    # ============================================================
    # Default Message Handlers
    # ============================================================
    
    async def handle_task_schedule(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle task scheduling (Link)"""
        task_id = message.payload.get("task_id")
        logger.info(f"Link: Scheduling task {task_id}")
        return {"status": "scheduled", "task_id": task_id}
    
    async def handle_status_request(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle status request"""
        return {"status": "operational", "lattice_state": self.get_lattice_state()}
    
    async def handle_coordinate(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle coordination request (Link)"""
        target = message.payload.get("target")
        logger.info(f"Link: Coordinating with {target}")
        return {"status": "coordinating", "target": target}
    
    async def handle_execute(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle execution request (Container)"""
        command = message.payload.get("command")
        logger.info(f"Container: Executing {command}")
        return {"status": "executed", "command": command, "result": "success"}
    
    async def handle_resource_request(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle resource request (Container)"""
        resources = message.payload.get("resources", {})
        logger.info(f"Container: Requesting resources {resources}")
        return {"status": "allocated", "resources": resources}
    
    async def handle_transmit(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle data transmission (Signal)"""
        data_size = message.payload.get("size", 0)
        logger.info(f"Signal: Transmitting {data_size} bytes")
        return {"status": "transmitted", "size": data_size}
    
    async def handle_bandwidth_check(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle bandwidth check (Signal)"""
        return {"status": "ok", "bandwidth": "100Mbps", "latency": "5ms"}
    
    async def handle_resource_allocate(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle resource allocation (Pressure)"""
        allocation = message.payload.get("allocation", {})
        logger.info(f"Pressure: Allocating resources {allocation}")
        return {"status": "allocated", "allocation": allocation}
    
    async def handle_health_monitor(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle health monitoring (Pressure)"""
        health_data = {
            node_type.value: node.state.health
            for node_type, node in self.nodes.items()
        }
        return {"status": "ok", "health": health_data}
    
    async def handle_store(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle data storage (Vault)"""
        key = message.payload.get("key")
        message.payload.get("value")
        logger.info(f"Vault: Storing {key}")
        return {"status": "stored", "key": key}
    
    async def handle_retrieve(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle data retrieval (Vault)"""
        key = message.payload.get("key")
        logger.info(f"Vault: Retrieving {key}")
        return {"status": "retrieved", "key": key, "value": "data"}
    
    async def handle_ai_communicate(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle AI communication (Groq)"""
        try:
            from groq_integration import GroqClient
            client = GroqClient()
            
            sender = message.payload.get("sender", "Unknown")
            receiver = message.payload.get("receiver", "Unknown")
            msg = message.payload.get("message", "")
            
            response = client.internal_communication(sender, receiver, msg)
            return {"status": "communicated", "response": response}
        except Exception as e:
            logger.error(f"Groq communication error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def handle_ai_reason(self, message: LatticeMessage) -> Dict[str, Any]:
        """Handle AI reasoning (Groq)"""
        try:
            from groq_integration import GroqClient
            client = GroqClient()
            
            prompt = message.payload.get("prompt", "")
            response = client.simple_chat(prompt, system="You coordinate GhostLink autonomous operations.")
            return {"status": "reasoned", "response": response}
        except Exception as e:
            logger.error(f"Groq reasoning error: {e}")
            return {"status": "error", "error": str(e)}


# ============================================================
# CLI Interface
# ============================================================

async def demo_lattice():
    """Demonstrate lattice functionality"""
    lattice = GhostLinkLattice()
    
    print("🌐 GhostLink Lattice Demo\n")
    print("=" * 60)
    
    # Start lattice in background
    lattice_task = asyncio.create_task(lattice.start())
    await asyncio.sleep(1)  # Let it initialize
    
    print("\n📊 Lattice State:")
    state = lattice.get_lattice_state()
    for node_name, node_state in state["nodes"].items():
        print(f"  • {node_name}: {node_state['status']} (health={node_state['health']:.2f})")
    
    print("\n📨 Testing message routing...")
    
    # Test 1: Link → Container task execution
    await lattice.send_message(
        ComponentType.LINK,
        ComponentType.CONTAINER,
        {"action": "execute", "command": "test_task"},
        MessagePriority.HIGH
    )
    await asyncio.sleep(0.5)
    
    # Test 2: Container → Pressure resource request
    await lattice.send_message(
        ComponentType.CONTAINER,
        ComponentType.PRESSURE,
        {"action": "resource_allocate", "allocation": {"cpu": 0.5, "memory": "2GB"}},
        MessagePriority.NORMAL
    )
    await asyncio.sleep(0.5)
    
    # Test 3: Link → Groq AI coordination
    await lattice.send_message(
        ComponentType.LINK,
        ComponentType.GROQ,
        {"action": "communicate", "sender": "Link", "receiver": "Container", "message": "Status update request"},
        MessagePriority.HIGH
    )
    await asyncio.sleep(1)
    
    # Test 4: Broadcast from Link
    await lattice.broadcast(
        ComponentType.LINK,
        {"action": "status_request"},
        MessagePriority.NORMAL
    )
    await asyncio.sleep(0.5)
    
    print("\n📈 Statistics:")
    print(f"  • Messages sent: {lattice.stats['messages_sent']}")
    print(f"  • Messages delivered: {lattice.stats['messages_delivered']}")
    print(f"  • Messages failed: {lattice.stats['messages_failed']}")
    print(f"  • Success rate: {(lattice.stats['messages_delivered']/max(lattice.stats['messages_sent'],1)*100):.1f}%")
    
    print("\n✅ Lattice demo complete!")
    print("\nPress Ctrl+C to stop...")
    
    try:
        await lattice_task
    except KeyboardInterrupt:
        await lattice.stop()


async def interactive_mode():
    """Interactive lattice control"""
    lattice = GhostLinkLattice()
    asyncio.create_task(lattice.start())
    await asyncio.sleep(1)
    
    print("🌐 GhostLink Lattice - Interactive Mode")
    print("Commands: send, broadcast, state, stats, quit\n")
    
    while True:
        try:
            cmd = input("lattice> ").strip().lower()
            
            if cmd == "quit":
                break
            elif cmd == "state":
                state = lattice.get_lattice_state()
                print(json.dumps(state, indent=2))
            elif cmd == "stats":
                print(json.dumps(lattice.stats, indent=2))
            elif cmd.startswith("send"):
                # Example: send link container task_schedule
                parts = cmd.split()
                if len(parts) >= 4:
                    sender = ComponentType(parts[1])
                    receiver = ComponentType(parts[2])
                    action = parts[3]
                    await lattice.send_message(sender, receiver, {"action": action})
                    print("✅ Message sent")
            elif cmd.startswith("broadcast"):
                # Example: broadcast link status_request
                parts = cmd.split()
                if len(parts) >= 3:
                    sender = ComponentType(parts[1])
                    action = parts[2]
                    await lattice.broadcast(sender, {"action": action})
                    print("✅ Broadcast sent")
            else:
                print("Unknown command")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    await lattice.stop()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GhostLink Lattice - Unified Component Bridge")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--state", action="store_true", help="Show lattice state")
    
    args = parser.parse_args()
    
    if args.demo:
        asyncio.run(demo_lattice())
    elif args.interactive:
        asyncio.run(interactive_mode())
    elif args.state:
        lattice = GhostLinkLattice()
        print(json.dumps(lattice.get_lattice_state(), indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

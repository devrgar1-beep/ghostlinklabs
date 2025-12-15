#!/usr/bin/env python3
"""
InterMesh Protocol - AI Service Coordination Layer
Enables structured communication between multiple AI services
"""

import asyncio
import json
import uuid
import time
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging

class MessageType(Enum):
    """InterMesh message types"""
    INSTRUCTION = "instruction"
    RESPONSE = "response"
    COORDINATION = "coordination"
    STATUS_UPDATE = "status_update"
    CAPABILITY_QUERY = "capability_query"
    CAPABILITY_RESPONSE = "capability_response"
    HANDSHAKE = "handshake"
    HEARTBEAT = "heartbeat"
    ERROR = "error"
    SHUTDOWN = "shutdown"

class MessagePriority(Enum):
    """Message priority levels"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4

@dataclass
class InterMeshMessage:
    """Standard InterMesh message format"""
    message_id: str
    message_type: MessageType
    sender_id: str
    recipient_id: Optional[str] = None  # None for broadcast
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    priority: MessagePriority = MessagePriority.NORMAL
    payload: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None  # For request/response correlation
    ttl: int = 300  # Time to live in seconds
    signature: Optional[str] = None  # For message integrity
    
    def __post_init__(self):
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        self._generate_signature()
    
    def _generate_signature(self):
        """Generate message signature for integrity verification"""
        content = f"{self.message_id}{self.sender_id}{self.timestamp.isoformat()}{json.dumps(self.payload, sort_keys=True)}"
        self.signature = hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def is_expired(self) -> bool:
        """Check if message has expired"""
        age = (datetime.now(timezone.utc) - self.timestamp).total_seconds()
        return age > self.ttl
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "payload": self.payload,
            "correlation_id": self.correlation_id,
            "ttl": self.ttl,
            "signature": self.signature
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InterMeshMessage":
        """Create from dictionary"""
        return cls(
            message_id=data["message_id"],
            message_type=MessageType(data["message_type"]),
            sender_id=data["sender_id"],
            recipient_id=data.get("recipient_id"),
            timestamp=datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00')),
            priority=MessagePriority(data["priority"]),
            payload=data.get("payload", {}),
            correlation_id=data.get("correlation_id"),
            ttl=data.get("ttl", 300),
            signature=data.get("signature")
        )

@dataclass
class ServiceCapability:
    """Represents a service capability"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    cost_estimate: float = 0.0  # Arbitrary cost units
    execution_time_estimate: float = 1.0  # Seconds
    reliability_score: float = 1.0  # 0.0 to 1.0

@dataclass
class ServiceNode:
    """Represents an AI service in the mesh"""
    node_id: str
    service_type: str
    capabilities: List[ServiceCapability] = field(default_factory=list)
    status: str = "offline"
    last_heartbeat: Optional[datetime] = None
    message_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    response_handlers: Dict[str, Callable] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.metrics:
            self.metrics = {
                "messages_sent": 0,
                "messages_received": 0,
                "errors": 0,
                "uptime": 0.0
            }

class InterMeshProtocol:
    """Core InterMesh protocol implementation"""
    
    def __init__(self, node_id: str, service_type: str = "coordinator"):
        self.node_id = node_id
        self.service_type = service_type
        self.nodes: Dict[str, ServiceNode] = {}
        self.message_handlers: Dict[MessageType, List[Callable]] = {}
        self.pending_responses: Dict[str, asyncio.Future] = {}
        self.message_history: List[InterMeshMessage] = []
        self.running = False
        
        # Protocol settings
        self.heartbeat_interval = 30.0  # seconds
        self.message_timeout = 30.0  # seconds
        self.max_history_size = 1000
        
        self.logger = logging.getLogger(f"intermesh.{node_id}")
        
        # Register default handlers
        self._register_default_handlers()
    
    async def start(self):
        """Start the InterMesh protocol"""
        self.running = True
        self.logger.info(f"Starting InterMesh node: {self.node_id}")
        
        # Start background tasks
        asyncio.create_task(self._heartbeat_loop())
        asyncio.create_task(self._message_processor())
        asyncio.create_task(self._cleanup_loop())
        
        # Send handshake to existing nodes
        await self._send_handshake()
    
    async def stop(self):
        """Stop the InterMesh protocol"""
        self.running = False
        
        # Send shutdown message
        await self.broadcast_message(
            MessageType.SHUTDOWN,
            {"reason": "Node shutting down"}
        )
        
        self.logger.info(f"InterMesh node stopped: {self.node_id}")
    
    def register_node(self, node: ServiceNode):
        """Register a service node"""
        self.nodes[node.node_id] = node
        self.logger.info(f"Registered node: {node.node_id} ({node.service_type})")
    
    def unregister_node(self, node_id: str):
        """Unregister a service node"""
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.logger.info(f"Unregistered node: {node_id}")
    
    def register_handler(self, message_type: MessageType, handler: Callable):
        """Register a message handler"""
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)
    
    async def send_message(self, message: InterMeshMessage) -> bool:
        """Send a message to a specific node or broadcast"""
        try:
            # Add to history
            self.message_history.append(message)
            if len(self.message_history) > self.max_history_size:
                self.message_history.pop(0)
            
            # Route message
            if message.recipient_id:
                # Direct message
                if message.recipient_id in self.nodes:
                    await self.nodes[message.recipient_id].message_queue.put(message)
                    self.logger.debug(f"Sent message {message.message_id} to {message.recipient_id}")
                    return True
                else:
                    self.logger.warning(f"Recipient not found: {message.recipient_id}")
                    return False
            else:
                # Broadcast message
                for node_id, node in self.nodes.items():
                    if node_id != self.node_id:  # Don't send to self
                        await node.message_queue.put(message)
                
                self.logger.debug(f"Broadcasted message {message.message_id}")
                return True
        
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False
    
    async def send_instruction(self, recipient_id: str, instruction: str, context: Dict[str, Any] = None) -> str:
        """Send an instruction to a specific service"""
        correlation_id = str(uuid.uuid4())
        
        message = InterMeshMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.INSTRUCTION,
            sender_id=self.node_id,
            recipient_id=recipient_id,
            correlation_id=correlation_id,
            payload={
                "instruction": instruction,
                "context": context or {}
            }
        )
        
        await self.send_message(message)
        return correlation_id
    
    async def send_response(self, correlation_id: str, recipient_id: str, response_data: Any, success: bool = True):
        """Send a response to a previous instruction"""
        message = InterMeshMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.RESPONSE,
            sender_id=self.node_id,
            recipient_id=recipient_id,
            correlation_id=correlation_id,
            payload={
                "success": success,
                "data": response_data,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
        
        await self.send_message(message)
    
    async def broadcast_message(self, message_type: MessageType, payload: Dict[str, Any]) -> str:
        """Broadcast a message to all nodes"""
        message = InterMeshMessage(
            message_id=str(uuid.uuid4()),
            message_type=message_type,
            sender_id=self.node_id,
            recipient_id=None,  # Broadcast
            payload=payload
        )
        
        await self.send_message(message)
        return message.message_id
    
    async def query_capabilities(self, node_id: Optional[str] = None) -> Dict[str, List[ServiceCapability]]:
        """Query capabilities of nodes"""
        correlation_id = str(uuid.uuid4())
        
        message = InterMeshMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.CAPABILITY_QUERY,
            sender_id=self.node_id,
            recipient_id=node_id,  # None for broadcast
            correlation_id=correlation_id,
            payload={"query_timestamp": datetime.now(timezone.utc).isoformat()}
        )
        
        # Set up response future
        response_future = asyncio.Future()
        self.pending_responses[correlation_id] = response_future
        
        await self.send_message(message)
        
        try:
            # Wait for responses
            responses = await asyncio.wait_for(response_future, timeout=self.message_timeout)
            return responses
        except asyncio.TimeoutError:
            self.logger.warning(f"Capability query timeout: {correlation_id}")
            return {}
        finally:
            self.pending_responses.pop(correlation_id, None)
    
    async def coordinate_multi_service_task(self, task_description: str, required_capabilities: List[str]) -> Dict[str, Any]:
        """Coordinate a task across multiple services"""
        # Query available capabilities
        all_capabilities = await self.query_capabilities()
        
        # Find services with required capabilities
        suitable_services = []
        for node_id, capabilities in all_capabilities.items():
            node_caps = [cap.name for cap in capabilities]
            if any(req_cap in node_caps for req_cap in required_capabilities):
                suitable_services.append(node_id)
        
        if not suitable_services:
            return {
                "success": False,
                "error": "No services found with required capabilities",
                "required_capabilities": required_capabilities
            }
        
        # Create coordination plan
        coordination_plan = {
            "task_id": str(uuid.uuid4()),
            "description": task_description,
            "services": suitable_services,
            "required_capabilities": required_capabilities,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Broadcast coordination message
        coordination_id = await self.broadcast_message(
            MessageType.COORDINATION,
            {
                "plan": coordination_plan,
                "action": "task_coordination"
            }
        )
        
        return {
            "success": True,
            "coordination_id": coordination_id,
            "plan": coordination_plan
        }
    
    async def wait_for_response(self, correlation_id: str, timeout: float = None) -> Any:
        """Wait for a response with specific correlation ID"""
        if timeout is None:
            timeout = self.message_timeout
        
        # Set up response future if not exists
        if correlation_id not in self.pending_responses:
            self.pending_responses[correlation_id] = asyncio.Future()
        
        try:
            response = await asyncio.wait_for(
                self.pending_responses[correlation_id],
                timeout=timeout
            )
            return response
        except asyncio.TimeoutError:
            self.logger.warning(f"Response timeout for correlation: {correlation_id}")
            return None
        finally:
            self.pending_responses.pop(correlation_id, None)
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeats"""
        while self.running:
            try:
                await self.broadcast_message(
                    MessageType.HEARTBEAT,
                    {
                        "node_id": self.node_id,
                        "service_type": self.service_type,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "metrics": {
                            "messages_processed": len(self.message_history),
                            "active_nodes": len(self.nodes)
                        }
                    }
                )
                
                await asyncio.sleep(self.heartbeat_interval)
                
            except Exception as e:
                self.logger.error(f"Heartbeat error: {e}")
    
    async def _message_processor(self):
        """Process incoming messages"""
        while self.running:
            try:
                # Process messages from all nodes
                for node_id, node in self.nodes.items():
                    try:
                        # Process messages with timeout
                        message = await asyncio.wait_for(
                            node.message_queue.get(),
                            timeout=0.1
                        )
                        
                        await self._handle_message(message, node)
                        
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        self.logger.error(f"Error processing message from {node_id}: {e}")
                
                # Small delay to prevent busy loop
                await asyncio.sleep(0.01)
                
            except Exception as e:
                self.logger.error(f"Message processor error: {e}")
    
    async def _handle_message(self, message: InterMeshMessage, sender_node: ServiceNode):
        """Handle a received message"""
        try:
            # Check if message is expired
            if message.is_expired():
                self.logger.warning(f"Received expired message: {message.message_id}")
                return
            
            # Update sender metrics
            sender_node.metrics["messages_received"] += 1
            sender_node.last_heartbeat = datetime.now(timezone.utc)
            
            # Handle based on message type
            handlers = self.message_handlers.get(message.message_type, [])
            
            for handler in handlers:
                try:
                    await handler(message, sender_node)
                except Exception as e:
                    self.logger.error(f"Handler error for {message.message_type}: {e}")
            
            # Handle responses
            if message.message_type == MessageType.RESPONSE and message.correlation_id:
                if message.correlation_id in self.pending_responses:
                    future = self.pending_responses[message.correlation_id]
                    if not future.done():
                        future.set_result(message.payload)
            
        except Exception as e:
            self.logger.error(f"Error handling message {message.message_id}: {e}")
    
    async def _cleanup_loop(self):
        """Clean up expired messages and inactive nodes"""
        while self.running:
            try:
                # Clean expired messages
                now = datetime.now(timezone.utc)
                self.message_history = [
                    msg for msg in self.message_history
                    if not msg.is_expired()
                ]
                
                # Check for inactive nodes
                inactive_nodes = []
                for node_id, node in self.nodes.items():
                    if node.last_heartbeat:
                        time_since_heartbeat = now - node.last_heartbeat
                        if time_since_heartbeat.total_seconds() > self.heartbeat_interval * 3:
                            inactive_nodes.append(node_id)
                            node.status = "inactive"
                
                for node_id in inactive_nodes:
                    self.logger.warning(f"Node appears inactive: {node_id}")
                
                await asyncio.sleep(60)  # Clean up every minute
                
            except Exception as e:
                self.logger.error(f"Cleanup error: {e}")
    
    def _register_default_handlers(self):
        """Register default message handlers"""
        self.register_handler(MessageType.HANDSHAKE, self._handle_handshake)
        self.register_handler(MessageType.HEARTBEAT, self._handle_heartbeat)
        self.register_handler(MessageType.CAPABILITY_QUERY, self._handle_capability_query)
        self.register_handler(MessageType.STATUS_UPDATE, self._handle_status_update)
    
    async def _handle_handshake(self, message: InterMeshMessage, sender_node: ServiceNode):
        """Handle handshake messages"""
        self.logger.info(f"Received handshake from {message.sender_id}")
        
        # Send handshake response
        await self.send_response(
            message.correlation_id or message.message_id,
            message.sender_id,
            {
                "node_id": self.node_id,
                "service_type": self.service_type,
                "capabilities": [cap.name for cap in getattr(self, 'capabilities', [])],
                "status": "online"
            }
        )
    
    async def _handle_heartbeat(self, message: InterMeshMessage, sender_node: ServiceNode):
        """Handle heartbeat messages"""
        sender_node.status = "online"
        sender_node.last_heartbeat = datetime.now(timezone.utc)
        
        # Update metrics from heartbeat
        if "metrics" in message.payload:
            sender_node.metrics.update(message.payload["metrics"])
    
    async def _handle_capability_query(self, message: InterMeshMessage, sender_node: ServiceNode):
        """Handle capability query messages"""
        capabilities_data = []
        
        # Get capabilities for this node (if any)
        if hasattr(self, 'capabilities'):
            capabilities_data = [asdict(cap) for cap in self.capabilities]
        
        await self.send_response(
            message.correlation_id or message.message_id,
            message.sender_id,
            {
                "node_id": self.node_id,
                "capabilities": capabilities_data
            }
        )
    
    async def _handle_status_update(self, message: InterMeshMessage, sender_node: ServiceNode):
        """Handle status update messages"""
        if "status" in message.payload:
            sender_node.status = message.payload["status"]
        
        if "metrics" in message.payload:
            sender_node.metrics.update(message.payload["metrics"])
    
    async def _send_handshake(self):
        """Send handshake to all known nodes"""
        handshake_id = await self.broadcast_message(
            MessageType.HANDSHAKE,
            {
                "node_id": self.node_id,
                "service_type": self.service_type,
                "capabilities": [cap.name for cap in getattr(self, 'capabilities', [])],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
        
        self.logger.info(f"Sent handshake: {handshake_id}")
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get current network status"""
        online_nodes = sum(1 for node in self.nodes.values() if node.status == "online")
        
        return {
            "node_id": self.node_id,
            "service_type": self.service_type,
            "total_nodes": len(self.nodes),
            "online_nodes": online_nodes,
            "message_history_size": len(self.message_history),
            "pending_responses": len(self.pending_responses),
            "nodes": {
                node_id: {
                    "service_type": node.service_type,
                    "status": node.status,
                    "capabilities": [cap.name for cap in node.capabilities],
                    "last_heartbeat": node.last_heartbeat.isoformat() if node.last_heartbeat else None,
                    "metrics": node.metrics
                }
                for node_id, node in self.nodes.items()
            }
        }

# Utility functions for creating common message types
def create_instruction_message(sender_id: str, recipient_id: str, instruction: str, context: Dict[str, Any] = None) -> InterMeshMessage:
    """Create an instruction message"""
    return InterMeshMessage(
        message_id=str(uuid.uuid4()),
        message_type=MessageType.INSTRUCTION,
        sender_id=sender_id,
        recipient_id=recipient_id,
        correlation_id=str(uuid.uuid4()),
        payload={
            "instruction": instruction,
            "context": context or {}
        }
    )

def create_capability(name: str, description: str, input_schema: Dict[str, Any], output_schema: Dict[str, Any]) -> ServiceCapability:
    """Create a service capability"""
    return ServiceCapability(
        name=name,
        description=description,
        input_schema=input_schema,
        output_schema=output_schema
    )
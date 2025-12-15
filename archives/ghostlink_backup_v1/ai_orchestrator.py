#!/usr/bin/env python3
"""
GhostLink AI Connector Orchestration System
Multi-AI Coordination with Sovereignty Controls
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from contextlib import asynccontextmanager

import aiohttp
import websockets
from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# GhostLink Core Imports
from .core.sovereignty_gate import SovereigntyGate
from .core.intermesh_protocol import InterMeshProtocol
from .core.coldstack import ColdStack
from .connectors.base_connector import BaseConnector
from .utils.logger import setup_logging

class AIServiceType(Enum):
    """Available AI service types"""
    CLAUDE_ANTHROPIC = "claude"
    CHATGPT_OPENAI = "chatgpt"
    CLAUDE_CODE = "claude_code"
    BROWSER_AI = "browser_ai"
    LOCAL_LLM = "local_llm"
    NEURAL_NODE = "neural_node"
    CUSTOM_API = "custom_api"

class ConnectorStatus(Enum):
    """Connector status states"""
    OFFLINE = "offline"
    CONNECTING = "connecting"
    ONLINE = "online"
    ERROR = "error"
    SOVEREIGNTY_BLOCKED = "sovereignty_blocked"

class TaskPriority(Enum):
    """Task execution priorities"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5

@dataclass
class AIConnector:
    """AI service connector configuration"""
    service_id: str
    service_type: AIServiceType
    endpoint: Optional[str] = None
    api_key: Optional[str] = None
    capabilities: List[str] = None
    status: ConnectorStatus = ConnectorStatus.OFFLINE
    last_ping: Optional[datetime] = None
    error_count: int = 0
    max_concurrent: int = 3
    rate_limit: float = 1.0  # requests per second
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []

@dataclass
class OrchestrationTask:
    """Task for AI orchestration"""
    task_id: str
    instruction: str
    context: Dict[str, Any]
    priority: TaskPriority = TaskPriority.NORMAL
    target_services: List[str] = None
    sovereignty_check: bool = True
    timeout: float = 30.0
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        if self.target_services is None:
            self.target_services = []

@dataclass
class OrchestrationResult:
    """Result from AI orchestration"""
    task_id: str
    service_id: str
    success: bool
    response: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

class AIOrchestrator:
    """Main AI orchestration controller"""
    
    def __init__(self, sovereignty_gate: SovereigntyGate):
        self.sovereignty_gate = sovereignty_gate
        self.intermesh = InterMeshProtocol()
        self.coldstack = ColdStack()
        
        # Connector registry
        self.connectors: Dict[str, AIConnector] = {}
        self.active_connections: Dict[str, Any] = {}
        
        # Task management
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.active_tasks: Dict[str, OrchestrationTask] = {}
        self.task_results: Dict[str, List[OrchestrationResult]] = {}
        
        # WebSocket connections for real-time updates
        self.websocket_connections: List[WebSocket] = []
        
        # Event handlers
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Metrics
        self.metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_execution_time": 0.0,
            "sovereignty_blocks": 0,
            "connector_errors": 0
        }
        
        self.logger = logging.getLogger("ghostlink.orchestrator")
        self.running = False

    async def start(self):
        """Start the orchestration system"""
        self.logger.info("Starting AI Orchestrator...")
        self.running = True
        
        # Initialize default connectors
        await self._initialize_default_connectors()
        
        # Start background tasks
        asyncio.create_task(self._task_processor())
        asyncio.create_task(self._health_monitor())
        asyncio.create_task(self._metrics_collector())
        
        self.logger.info("AI Orchestrator started successfully")

    async def stop(self):
        """Stop the orchestration system"""
        self.logger.info("Stopping AI Orchestrator...")
        self.running = False
        
        # Close all connections
        for service_id in list(self.active_connections.keys()):
            await self._disconnect_service(service_id)
        
        # Close WebSocket connections
        for ws in self.websocket_connections:
            try:
                await ws.close()
            except:
                pass
        
        self.logger.info("AI Orchestrator stopped")

    async def register_connector(self, connector: AIConnector) -> bool:
        """Register a new AI service connector"""
        try:
            # Sovereignty check
            check_result = await self.sovereignty_gate.check_action(
                "register_ai_connector",
                {"service_type": connector.service_type.value, "capabilities": connector.capabilities}
            )
            
            if not check_result.allowed:
                self.logger.warning(f"Sovereignty gate blocked connector registration: {check_result.reason}")
                self.metrics["sovereignty_blocks"] += 1
                return False
            
            self.connectors[connector.service_id] = connector
            self.logger.info(f"Registered AI connector: {connector.service_id} ({connector.service_type.value})")
            
            # Attempt to connect
            await self._connect_service(connector.service_id)
            
            # Emit event
            await self._emit_event("connector_registered", {"connector": connector})
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register connector {connector.service_id}: {e}")
            return False

    async def submit_task(self, task: OrchestrationTask) -> str:
        """Submit a task for orchestration"""
        try:
            # Sovereignty check if required
            if task.sovereignty_check:
                check_result = await self.sovereignty_gate.check_action(
                    "orchestrate_ai_task",
                    {
                        "instruction": task.instruction,
                        "target_services": task.target_services,
                        "priority": task.priority.name
                    }
                )
                
                if not check_result.allowed:
                    self.logger.warning(f"Sovereignty gate blocked task: {check_result.reason}")
                    self.metrics["sovereignty_blocks"] += 1
                    raise HTTPException(status_code=403, detail=check_result.reason)
            
            # Add to queue
            self.active_tasks[task.task_id] = task
            await self.task_queue.put(task)
            
            self.logger.info(f"Task submitted: {task.task_id} (priority: {task.priority.name})")
            
            # Emit event
            await self._emit_event("task_submitted", {"task": task})
            
            return task.task_id
            
        except Exception as e:
            self.logger.error(f"Failed to submit task {task.task_id}: {e}")
            raise

    async def get_task_results(self, task_id: str) -> List[OrchestrationResult]:
        """Get results for a specific task"""
        return self.task_results.get(task_id, [])

    async def orchestrate_instruction(self, instruction: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """High-level orchestration of a natural language instruction"""
        if context is None:
            context = {}
        
        # Parse instruction and determine best services
        target_services = await self._analyze_instruction(instruction, context)
        
        # Create orchestration task
        task = OrchestrationTask(
            task_id=f"orch_{int(time.time())}_{hash(instruction) % 1000}",
            instruction=instruction,
            context=context,
            target_services=target_services,
            priority=TaskPriority.NORMAL
        )
        
        # Submit and wait for completion
        task_id = await self.submit_task(task)
        
        # Wait for results (with timeout)
        timeout = 60.0
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            results = await self.get_task_results(task_id)
            if results and all(r.success or r.error for r in results):
                break
            await asyncio.sleep(0.5)
        
        # Compile results
        results = await self.get_task_results(task_id)
        
        return {
            "task_id": task_id,
            "instruction": instruction,
            "results": [asdict(r) for r in results],
            "summary": self._summarize_results(results)
        }

    async def broadcast_to_all(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Broadcast a message to all available AI services"""
        if context is None:
            context = {}
        
        # Get all online connectors
        online_services = [
            connector.service_id 
            for connector in self.connectors.values() 
            if connector.status == ConnectorStatus.ONLINE
        ]
        
        if not online_services:
            raise HTTPException(status_code=503, detail="No AI services available")
        
        # Create broadcast task
        task = OrchestrationTask(
            task_id=f"broadcast_{int(time.time())}",
            instruction=message,
            context=context,
            target_services=online_services,
            priority=TaskPriority.HIGH
        )
        
        return await self.orchestrate_instruction(message, context)

    async def _initialize_default_connectors(self):
        """Initialize default AI service connectors"""
        default_connectors = [
            AIConnector(
                service_id="claude_main",
                service_type=AIServiceType.CLAUDE_ANTHROPIC,
                capabilities=["text_generation", "code_analysis", "reasoning", "file_operations"],
                max_concurrent=5
            ),
            AIConnector(
                service_id="chatgpt_browser",
                service_type=AIServiceType.CHATGPT_OPENAI,
                capabilities=["text_generation", "web_search", "image_analysis"],
                max_concurrent=3
            ),
            AIConnector(
                service_id="local_neural",
                service_type=AIServiceType.NEURAL_NODE,
                endpoint="http://localhost:8081/neural/process",
                capabilities=["offline_processing", "privacy_preserving"],
                max_concurrent=2
            )
        ]
        
        for connector in default_connectors:
            await self.register_connector(connector)

    async def _connect_service(self, service_id: str):
        """Connect to an AI service"""
        connector = self.connectors.get(service_id)
        if not connector:
            return
        
        try:
            connector.status = ConnectorStatus.CONNECTING
            
            # Service-specific connection logic
            if connector.service_type == AIServiceType.NEURAL_NODE:
                # Connect to local neural node
                if connector.endpoint:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"{connector.endpoint}/health") as response:
                            if response.status == 200:
                                self.active_connections[service_id] = session
                                connector.status = ConnectorStatus.ONLINE
                                connector.last_ping = datetime.now(timezone.utc)
            
            elif connector.service_type in [AIServiceType.CLAUDE_ANTHROPIC, AIServiceType.CHATGPT_OPENAI]:
                # Browser-based AI services - simulate connection
                connector.status = ConnectorStatus.ONLINE
                connector.last_ping = datetime.now(timezone.utc)
                self.active_connections[service_id] = {"type": "browser_connection"}
            
            self.logger.info(f"Connected to AI service: {service_id}")
            
        except Exception as e:
            connector.status = ConnectorStatus.ERROR
            connector.error_count += 1
            self.metrics["connector_errors"] += 1
            self.logger.error(f"Failed to connect to {service_id}: {e}")

    async def _disconnect_service(self, service_id: str):
        """Disconnect from an AI service"""
        connector = self.connectors.get(service_id)
        connection = self.active_connections.get(service_id)
        
        if connection:
            try:
                if hasattr(connection, 'close'):
                    await connection.close()
                del self.active_connections[service_id]
            except Exception as e:
                self.logger.error(f"Error disconnecting {service_id}: {e}")
        
        if connector:
            connector.status = ConnectorStatus.OFFLINE
            self.logger.info(f"Disconnected from AI service: {service_id}")

    async def _task_processor(self):
        """Background task processor"""
        while self.running:
            try:
                # Get task from queue with timeout
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                # Process task
                await self._process_task(task)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"Task processor error: {e}")

    async def _process_task(self, task: OrchestrationTask):
        """Process a single orchestration task"""
        start_time = time.time()
        
        try:
            # Determine target services if not specified
            if not task.target_services:
                task.target_services = await self._select_best_services(task)
            
            # Execute task on target services
            results = []
            
            for service_id in task.target_services:
                connector = self.connectors.get(service_id)
                if not connector or connector.status != ConnectorStatus.ONLINE:
                    continue
                
                try:
                    # Execute on service
                    result = await self._execute_on_service(service_id, task)
                    results.append(result)
                    
                except Exception as e:
                    error_result = OrchestrationResult(
                        task_id=task.task_id,
                        service_id=service_id,
                        success=False,
                        error=str(e),
                        execution_time=time.time() - start_time
                    )
                    results.append(error_result)
            
            # Store results
            self.task_results[task.task_id] = results
            
            # Update metrics
            if any(r.success for r in results):
                self.metrics["tasks_completed"] += 1
            else:
                self.metrics["tasks_failed"] += 1
            
            self.metrics["total_execution_time"] += time.time() - start_time
            
            # Emit completion event
            await self._emit_event("task_completed", {
                "task": task,
                "results": results,
                "execution_time": time.time() - start_time
            })
            
        except Exception as e:
            self.logger.error(f"Failed to process task {task.task_id}: {e}")
            self.metrics["tasks_failed"] += 1
        finally:
            # Remove from active tasks
            self.active_tasks.pop(task.task_id, None)

    async def _execute_on_service(self, service_id: str, task: OrchestrationTask) -> OrchestrationResult:
        """Execute a task on a specific AI service"""
        start_time = time.time()
        connector = self.connectors[service_id]
        
        try:
            # Service-specific execution logic
            response = None
            
            if connector.service_type == AIServiceType.NEURAL_NODE:
                # Execute on local neural node
                async with aiohttp.ClientSession() as session:
                    payload = {
                        "prompt": task.instruction,
                        "context": task.context,
                        "parameters": {
                            "max_tokens": 2048,
                            "temperature": 0.7
                        }
                    }
                    
                    async with session.post(connector.endpoint, json=payload) as resp:
                        if resp.status == 200:
                            response = await resp.json()
                        else:
                            raise Exception(f"Neural node returned status {resp.status}")
            
            elif connector.service_type in [AIServiceType.CLAUDE_ANTHROPIC, AIServiceType.CHATGPT_OPENAI]:
                # For browser-based AI, create a structured response
                # In a real implementation, this would interface with browser automation
                response = {
                    "service": connector.service_type.value,
                    "instruction_received": task.instruction,
                    "context_processed": bool(task.context),
                    "response": f"[{connector.service_type.value}] Processing: {task.instruction[:100]}...",
                    "capabilities_used": connector.capabilities[:3],
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            
            return OrchestrationResult(
                task_id=task.task_id,
                service_id=service_id,
                success=True,
                response=response,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return OrchestrationResult(
                task_id=task.task_id,
                service_id=service_id,
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )

    async def _analyze_instruction(self, instruction: str, context: Dict[str, Any]) -> List[str]:
        """Analyze instruction to determine best AI services"""
        instruction_lower = instruction.lower()
        
        # Service selection logic based on instruction content
        services = []
        
        # Code-related tasks
        if any(keyword in instruction_lower for keyword in ["code", "python", "javascript", "debug", "programming"]):
            services.extend(["claude_main", "chatgpt_browser"])
        
        # Analysis tasks
        if any(keyword in instruction_lower for keyword in ["analyze", "summarize", "research", "compare"]):
            services.extend(["claude_main", "local_neural"])
        
        # Creative tasks
        if any(keyword in instruction_lower for keyword in ["write", "create", "generate", "story", "creative"]):
            services.extend(["chatgpt_browser", "claude_main"])
        
        # Privacy-sensitive tasks
        if any(keyword in instruction_lower for keyword in ["private", "confidential", "secure", "personal"]):
            services.append("local_neural")
        
        # Default to all available services if no specific match
        if not services:
            services = [
                connector.service_id 
                for connector in self.connectors.values() 
                if connector.status == ConnectorStatus.ONLINE
            ]
        
        # Remove duplicates and ensure services exist
        services = list(set(services))
        services = [s for s in services if s in self.connectors]
        
        return services

    async def _select_best_services(self, task: OrchestrationTask) -> List[str]:
        """Select the best services for a task"""
        return await self._analyze_instruction(task.instruction, task.context)

    async def _health_monitor(self):
        """Monitor health of all connectors"""
        while self.running:
            try:
                for service_id, connector in self.connectors.items():
                    if connector.status == ConnectorStatus.ONLINE:
                        # Check if service is still responsive
                        if connector.last_ping:
                            time_since_ping = datetime.now(timezone.utc) - connector.last_ping
                            if time_since_ping.total_seconds() > 300:  # 5 minutes
                                await self._connect_service(service_id)
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Health monitor error: {e}")

    async def _metrics_collector(self):
        """Collect and update system metrics"""
        while self.running:
            try:
                # Update connector metrics
                online_count = sum(1 for c in self.connectors.values() if c.status == ConnectorStatus.ONLINE)
                total_count = len(self.connectors)
                
                self.metrics.update({
                    "connectors_online": online_count,
                    "connectors_total": total_count,
                    "active_tasks": len(self.active_tasks),
                    "pending_tasks": self.task_queue.qsize(),
                    "uptime": time.time()  # Will be calculated from start time
                })
                
                # Broadcast metrics to WebSocket clients
                await self._broadcast_metrics()
                
                await asyncio.sleep(10)  # Update every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Metrics collector error: {e}")

    async def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit an event to registered handlers"""
        handlers = self.event_handlers.get(event_type, [])
        for handler in handlers:
            try:
                await handler(event_type, data)
            except Exception as e:
                self.logger.error(f"Event handler error for {event_type}: {e}")

    async def _broadcast_metrics(self):
        """Broadcast metrics to WebSocket connections"""
        if not self.websocket_connections:
            return
        
        metrics_message = {
            "type": "metrics_update",
            "data": self.metrics,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Send to all connected WebSocket clients
        disconnected = []
        for ws in self.websocket_connections:
            try:
                await ws.send_json(metrics_message)
            except:
                disconnected.append(ws)
        
        # Remove disconnected clients
        for ws in disconnected:
            self.websocket_connections.remove(ws)

    def _summarize_results(self, results: List[OrchestrationResult]) -> Dict[str, Any]:
        """Summarize orchestration results"""
        total = len(results)
        successful = sum(1 for r in results if r.success)
        
        return {
            "total_services": total,
            "successful_responses": successful,
            "failed_responses": total - successful,
            "success_rate": successful / total if total > 0 else 0,
            "average_execution_time": sum(r.execution_time for r in results) / total if total > 0 else 0,
            "services_used": [r.service_id for r in results]
        }

    def add_event_handler(self, event_type: str, handler: Callable):
        """Add an event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    def remove_event_handler(self, event_type: str, handler: Callable):
        """Remove an event handler"""
        if event_type in self.event_handlers:
            try:
                self.event_handlers[event_type].remove(handler)
            except ValueError:
                pass

    async def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status"""
        return {
            "running": self.running,
            "connectors": {
                service_id: {
                    "status": connector.status.value,
                    "service_type": connector.service_type.value,
                    "capabilities": connector.capabilities,
                    "error_count": connector.error_count,
                    "last_ping": connector.last_ping.isoformat() if connector.last_ping else None
                }
                for service_id, connector in self.connectors.items()
            },
            "metrics": self.metrics,
            "active_tasks": len(self.active_tasks),
            "pending_tasks": self.task_queue.qsize()
        }

# FastAPI integration
app = FastAPI(title="GhostLink AI Orchestrator", version="8.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator: Optional[AIOrchestrator] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global orchestrator
    
    # Startup
    from .core.sovereignty_gate import SovereigntyGate
    sovereignty_gate = SovereigntyGate(mode="audit")  # Start in audit mode
    
    orchestrator = AIOrchestrator(sovereignty_gate)
    await orchestrator.start()
    
    yield
    
    # Shutdown
    if orchestrator:
        await orchestrator.stop()

app.router.lifespan_context = lifespan

# API Models
class InstructionRequest(BaseModel):
    instruction: str
    context: Optional[Dict[str, Any]] = None
    priority: Optional[str] = "normal"
    target_services: Optional[List[str]] = None

class BroadcastRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

# API Routes
@app.post("/orchestrate")
async def orchestrate_instruction(request: InstructionRequest):
    """Orchestrate an instruction across AI services"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    return await orchestrator.orchestrate_instruction(
        request.instruction,
        request.context or {}
    )

@app.post("/broadcast")
async def broadcast_message(request: BroadcastRequest):
    """Broadcast a message to all AI services"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    return await orchestrator.broadcast_to_all(
        request.message,
        request.context or {}
    )

@app.get("/status")
async def get_status():
    """Get orchestrator status"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    return await orchestrator.get_status()

@app.get("/connectors")
async def list_connectors():
    """List all registered connectors"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    return {
        "connectors": [
            {
                "service_id": connector.service_id,
                "service_type": connector.service_type.value,
                "status": connector.status.value,
                "capabilities": connector.capabilities,
                "error_count": connector.error_count
            }
            for connector in orchestrator.connectors.values()
        ]
    }

@app.get("/tasks/{task_id}/results")
async def get_task_results(task_id: str):
    """Get results for a specific task"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    results = await orchestrator.get_task_results(task_id)
    return {
        "task_id": task_id,
        "results": [asdict(r) for r in results]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    
    if orchestrator:
        orchestrator.websocket_connections.append(websocket)
        
        try:
            while True:
                # Keep connection alive
                await websocket.receive_text()
        except:
            pass
        finally:
            if websocket in orchestrator.websocket_connections:
                orchestrator.websocket_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084)
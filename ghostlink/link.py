"""Link - Your AI orchestration brain.

Link is the autonomous orchestrator that coordinates all GhostLink operations,
manages tasks, routes workflows, and serves as your personal AI assistant brain.
"""
from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

from ..config import config
from ..automation import (
    TOOL_CHAIN_ORCHESTRATOR,
    AUTO_TRIGGER_ENGINE,
    SYMBOLIC_TASK_SCHEDULER,
    LATTICE_WATCHDOG,
)
from ..runtime import RUNTIME_STATE_MANAGER, SESSION_EXECUTOR
from ..core import SIGNAL, CONTAINER, LINK as CORE_LINK
from ..troubleshooter import get_troubleshooter, handle_error
from ..health_monitor import get_health_monitor

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """Represents a task for Link to execute."""
    id: str
    name: str
    description: str
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error,
            "metadata": self.metadata,
        }


@dataclass
class LinkMemory:
    """Link's persistent memory storage."""
    tasks: list[Task] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)
    
    def save(self, path: Path) -> None:
        """Save memory to disk."""
        data = {
            "tasks": [t.to_dict() for t in self.tasks],
            "context": self.context,
            "preferences": self.preferences,
            "history": self.history,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2))
    
    @classmethod
    def load(cls, path: Path) -> "LinkMemory":
        """Load memory from disk."""
        if not path.exists():
            return cls()
        
        data = json.loads(path.read_text())
        memory = cls(
            context=data.get("context", {}),
            preferences=data.get("preferences", {}),
            history=data.get("history", []),
        )
        
        # Reconstruct tasks
        for task_data in data.get("tasks", []):
            task = Task(
                id=task_data["id"],
                name=task_data["name"],
                description=task_data["description"],
                priority=TaskPriority(task_data["priority"]),
                status=TaskStatus(task_data["status"]),
                created_at=datetime.fromisoformat(task_data["created_at"]),
                result=task_data.get("result"),
                error=task_data.get("error"),
                metadata=task_data.get("metadata", {}),
            )
            if task_data.get("started_at"):
                task.started_at = datetime.fromisoformat(task_data["started_at"])
            if task_data.get("completed_at"):
                task.completed_at = datetime.fromisoformat(task_data["completed_at"])
            memory.tasks.append(task)
        
        return memory


class Link:
    """Link - Your autonomous AI orchestration brain.
    
    Link coordinates all GhostLink operations, manages tasks, learns your
    preferences, and serves as your personal AI assistant.
    
    Features:
    - Autonomous task orchestration
    - Priority-based task scheduling
    - Persistent memory and learning
    - Context-aware decision making
    - Integration with all GhostLink components
    - LLM integration for natural language interaction (optional)
    """
    
    def __init__(
        self,
        name: str = "Link",
        memory_path: Optional[Path] = None,
    ):
        """Initialize Link.
        
        Args:
            name: Link's display name
            memory_path: Path to persistent memory file
        """
        self.name = name
        self.memory_path = memory_path or Path.home() / ".ghostlink" / "link_memory.json"
        self.memory = LinkMemory.load(self.memory_path)
        self.active = False
        self.task_queue: list[Task] = []
        self._handlers: dict[str, Callable] = {}
        
        # Automatic troubleshooting and monitoring
        self.troubleshooter = get_troubleshooter()
        self.health_monitor = get_health_monitor()
        self.auto_fix_enabled = True
        self.proactive_monitoring = False
        
    async def start(self) -> None:
        """Start Link's autonomous operation."""
        if self.active:
            return
        
        self.active = True
        print(f"🧠 {self.name} is now active")
        
        # Start health monitoring if enabled
        if self.proactive_monitoring:
            await self.health_monitor.start_monitoring()
            logger.info("Proactive health monitoring started")
        
        # Run initial health check
        try:
            health_status = await self.health_monitor.check_health()
            if health_status.overall_status == "critical":
                logger.error(f"Critical issues detected: {', '.join(health_status.issues)}")
            elif health_status.warnings:
                logger.warning(f"Warnings: {', '.join(health_status.warnings)}")
        except Exception as e:
            logger.warning(f"Initial health check failed: {e}")
        
        # Load pending tasks from memory
        self.task_queue = [t for t in self.memory.tasks if t.status == TaskStatus.PENDING]
        
        # Start background task processing
        asyncio.create_task(self._process_tasks())
        
    async def stop(self) -> None:
        """Stop Link's operation."""
        self.active = False
        
        # Stop health monitoring
        if self.proactive_monitoring:
            await self.health_monitor.stop_monitoring()
        
        self.memory.save(self.memory_path)
        print(f"🧠 {self.name} is now offline")
        
    def add_task(
        self,
        name: str,
        description: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        **metadata: Any,
    ) -> Task:
        """Add a new task for Link to execute.
        
        Args:
            name: Task name
            description: Task description
            priority: Task priority level
            **metadata: Additional task metadata
            
        Returns:
            Created task
        """
        task = Task(
            id=f"task_{datetime.utcnow().timestamp()}",
            name=name,
            description=description,
            priority=priority,
            metadata=metadata,
        )
        
        self.task_queue.append(task)
        self.memory.tasks.append(task)
        
        # Sort by priority
        self.task_queue.sort(key=lambda t: t.priority.value, reverse=True)
        
        print(f"📋 Task added: {name} (Priority: {priority.name})")
        return task
        
    def register_handler(self, task_type: str, handler: Callable) -> None:
        """Register a handler for a specific task type.
        
        Args:
            task_type: Type of task to handle
            handler: Async function to handle the task
        """
        self._handlers[task_type] = handler
        
    async def _process_tasks(self) -> None:
        """Background task processing loop."""
        while self.active:
            if self.task_queue:
                task = self.task_queue.pop(0)
                await self._execute_task(task)
            else:
                await asyncio.sleep(1)
                
    async def _execute_task(self, task: Task) -> None:
        """Execute a single task.
        
        Args:
            task: Task to execute
        """
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        print(f"🔄 Executing: {task.name}")
        
        try:
            # Check for registered handler
            handler = self._handlers.get(task.metadata.get("type"))
            if handler:
                task.result = await handler(task)
            else:
                # Default orchestration using GhostLink components
                task.result = await self._orchestrate_default(task)
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            print(f"✅ Completed: {task.name}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.utcnow()
            print(f"❌ Failed: {task.name} - {e}")
            
            # Automatic error handling and troubleshooting
            if self.auto_fix_enabled:
                logger.error(f"Task {task.name} failed: {e}")
                try:
                    error_report = await handle_error(
                        e, 
                        context={
                            "task_id": task.id,
                            "task_name": task.name,
                            "task_description": task.description
                        },
                        auto_fix=True
                    )
                    
                    if error_report.fix_applied:
                        # Retry task after successful fix
                        logger.info(f"Auto-fixed error, retrying task {task.name}")
                        task.status = TaskStatus.PENDING
                        self.task_queue.insert(0, task)
                except Exception as fix_error:
                    logger.error(f"Auto-fix failed: {fix_error}")
        
        # Save memory after each task
        self.memory.save(self.memory_path)
        
        # Add to history
        self.memory.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "task": task.to_dict(),
        })
        
    async def _orchestrate_default(self, task: Task) -> Any:
        """Default task orchestration using GhostLink components.
        
        Args:
            task: Task to orchestrate
            
        Returns:
            Task execution result
        """
        # This is where Link coordinates with other GhostLink components
        # to accomplish tasks autonomously
        
        # For now, return a placeholder
        return {
            "status": "orchestrated",
            "components_used": [
                "TOOL_CHAIN_ORCHESTRATOR",
                "SYMBOLIC_TASK_SCHEDULER",
            ],
            "task_id": task.id,
        }
        
    def set_context(self, key: str, value: Any) -> None:
        """Set a context variable for Link to remember.
        
        Args:
            key: Context key
            value: Context value
        """
        self.memory.context[key] = value
        self.memory.save(self.memory_path)
        
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a context variable.
        
        Args:
            key: Context key
            default: Default value if key not found
            
        Returns:
            Context value
        """
        return self.memory.context.get(key, default)
        
    def learn_preference(self, key: str, value: Any) -> None:
        """Learn a user preference.
        
        Args:
            key: Preference key
            value: Preference value
        """
        self.memory.preferences[key] = value
        self.memory.save(self.memory_path)
        print(f"📚 Learned: {key} = {value}")
        
    def get_status(self) -> dict[str, Any]:
        """Get Link's current status.
        
        Returns:
            Status dictionary
        """
        return {
            "name": self.name,
            "active": self.active,
            "pending_tasks": len([t for t in self.memory.tasks if t.status == TaskStatus.PENDING]),
            "completed_tasks": len([t for t in self.memory.tasks if t.status == TaskStatus.COMPLETED]),
            "failed_tasks": len([t for t in self.memory.tasks if t.status == TaskStatus.FAILED]),
            "context_vars": len(self.memory.context),
            "preferences": len(self.memory.preferences),
            "history_size": len(self.memory.history),
        }


# Global Link instance
_link_instance: Optional[Link] = None


def get_link() -> Link:
    """Get the global Link instance."""
    global _link_instance
    if _link_instance is None:
        _link_instance = Link()
    return _link_instance


async def main():
    """Example usage of Link."""
    link = get_link()
    
    await link.start()
    
    # Add some tasks
    link.add_task(
        "Analyze codebase",
        "Scan and analyze the GhostLink codebase for improvements",
        priority=TaskPriority.HIGH,
        type="analysis",
    )
    
    link.add_task(
        "Check system health",
        "Monitor system metrics and report any issues",
        priority=TaskPriority.NORMAL,
        type="monitoring",
    )
    
    # Set some context
    link.set_context("user_name", "Ghost")
    link.learn_preference("output_format", "concise")
    
    # Wait a bit
    await asyncio.sleep(5)
    
    # Check status
    status = link.get_status()
    print(f"\n📊 Link Status: {json.dumps(status, indent=2)}")
    
    await link.stop()


if __name__ == "__main__":
    asyncio.run(main())

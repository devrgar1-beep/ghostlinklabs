#!/usr/bin/env python3
"""
GhostLink Pipeline Orchestration Engine
Comprehensive pipeline management and task orchestration
"""

import json
import asyncio
import uuid
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Callable, Coroutine
from datetime import datetime
from enum import Enum
import logging


class PipelineStatus(Enum):
    """Pipeline execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskStatus(Enum):
    """Task execution status"""
    IDLE = "idle"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    RETRY = "retry"
    SKIPPED = "skipped"


@dataclass
class TaskMetrics:
    """Task execution metrics"""
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    attempts: int = 0
    max_retries: int = 3
    timeout_seconds: int = 300

    @property
    def duration(self) -> Optional[float]:
        """Get task duration"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


@dataclass
class PipelineTask:
    """Single pipeline task"""
    name: str
    description: str
    handler: Optional[Callable] = None
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.IDLE
    metrics: TaskMetrics = field(default_factory=TaskMetrics)
    result: Optional[Any] = None
    error: Optional[str] = None
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "result": self.result,
            "error": self.error,
            "metrics": {
                "duration": self.metrics.duration,
                "attempts": self.metrics.attempts,
                "max_retries": self.metrics.max_retries
            }
        }


@dataclass
class PipelineStep:
    """A step in pipeline execution"""
    order: int
    tasks: List[str]  # Task names in this step
    parallel: bool = False
    condition: Optional[Callable] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "order": self.order,
            "tasks": self.tasks,
            "parallel": self.parallel
        }


class PipelineOrchestrator:
    """Orchestrate pipeline execution"""

    def __init__(self, name: str, description: str = ""):
        """Initialize orchestrator"""
        self.name = name
        self.description = description
        self.pipeline_id = str(uuid.uuid4())
        self.status = PipelineStatus.PENDING
        self.tasks: Dict[str, PipelineTask] = {}
        self.execution_plan: List[PipelineStep] = []
        self.results: Dict[str, Any] = {}
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

        # Setup logging
        self.logger = logging.getLogger(f"pipeline.{name}")

    def add_task(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        dependencies: Optional[List[str]] = None,
        max_retries: int = 3,
        timeout_seconds: int = 300
    ) -> PipelineTask:
        """Add a task to the pipeline"""
        task = PipelineTask(
            name=name,
            description=description or f"Task: {name}",
            handler=handler,
            dependencies=dependencies or []
        )
        task.metrics.max_retries = max_retries
        task.metrics.timeout_seconds = timeout_seconds

        self.tasks[name] = task
        self.logger.info(f"Added task: {name}")
        return task

    def build_execution_plan(self) -> List[PipelineStep]:
        """Build execution plan from task dependencies"""
        plan = []
        visited = set()
        current_order = 0

        while len(visited) < len(self.tasks):
            current_step_tasks = []

            for task_name, task in self.tasks.items():
                if task_name in visited:
                    continue

                # Check if all dependencies are satisfied
                deps_satisfied = all(
                    dep in visited for dep in task.dependencies
                )

                if deps_satisfied:
                    current_step_tasks.append(task_name)

            if not current_step_tasks:
                raise ValueError("Circular dependency detected in tasks")

            # Determine if can parallelize
            can_parallel = len(current_step_tasks) > 1

            step = PipelineStep(
                order=current_order,
                tasks=current_step_tasks,
                parallel=can_parallel
            )
            plan.append(step)

            visited.update(current_step_tasks)
            current_order += 1

        self.execution_plan = plan
        self.logger.info(f"Built execution plan with {len(plan)} steps")
        return plan

    async def execute_task(self, task_name: str) -> Any:
        """Execute a single task with retry logic"""
        task = self.tasks[task_name]
        task.status = TaskStatus.RUNNING
        task.metrics.attempts = 0

        while task.metrics.attempts < task.metrics.max_retries:
            try:
                task.metrics.attempts += 1
                import time
                task.metrics.start_time = time.time()

                self.logger.info(f"Executing task: {task_name} (attempt {task.metrics.attempts})")

                # Execute handler
                if asyncio.iscoroutinefunction(task.handler):
                    result = await asyncio.wait_for(
                        task.handler(),
                        timeout=task.metrics.timeout_seconds
                    )
                else:
                    result = await asyncio.get_event_loop().run_in_executor(
                        None,
                        task.handler
                    )

                task.metrics.end_time = time.time()
                task.status = TaskStatus.SUCCESS
                task.result = result

                self.logger.info(f"Task {task_name} completed successfully")
                return result

            except asyncio.TimeoutError:
                task.error = f"Task timeout after {task.metrics.timeout_seconds}s"
                task.status = TaskStatus.RETRY if task.metrics.attempts < task.metrics.max_retries else TaskStatus.FAILURE
                self.logger.warning(f"Task {task_name} timed out, retrying...")

            except Exception as e:
                task.error = str(e)
                task.status = TaskStatus.RETRY if task.metrics.attempts < task.metrics.max_retries else TaskStatus.FAILURE
                self.logger.warning(f"Task {task_name} failed: {e}")

        task.status = TaskStatus.FAILURE
        self.logger.error(f"Task {task_name} failed after {task.metrics.attempts} attempts")
        raise RuntimeError(f"Task '{task_name}' failed: {task.error}")

    async def execute_step(self, step: PipelineStep) -> Dict[str, Any]:
        """Execute a pipeline step"""
        self.logger.info(f"Executing step {step.order}: {len(step.tasks)} tasks")

        step_results = {}

        if step.parallel:
            # Execute tasks in parallel
            tasks = [
                asyncio.create_task(self.execute_task(name))
                for name in step.tasks
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for task_name, result in zip(step.tasks, results):
                if isinstance(result, Exception):
                    step_results[task_name] = {"error": str(result)}
                else:
                    step_results[task_name] = result
        else:
            # Execute tasks sequentially
            for task_name in step.tasks:
                try:
                    result = await self.execute_task(task_name)
                    step_results[task_name] = result
                except Exception as e:
                    step_results[task_name] = {"error": str(e)}
                    # Stop on first failure in sequential mode
                    raise

        return step_results

    async def execute(self) -> Dict[str, Any]:
        """Execute the complete pipeline"""
        self.status = PipelineStatus.RUNNING
        self.start_time = datetime.now()

        try:
            if not self.execution_plan:
                self.build_execution_plan()

            for step in self.execution_plan:
                step_results = await self.execute_step(step)
                self.results.update(step_results)

            self.status = PipelineStatus.SUCCESS

        except Exception as e:
            self.status = PipelineStatus.FAILURE
            self.logger.error(f"Pipeline execution failed: {e}")
            raise

        finally:
            self.end_time = datetime.now()

    def get_report(self) -> Dict[str, Any]:
        """Get pipeline execution report"""
        duration = None
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()

        return {
            "pipeline_id": self.pipeline_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": duration,
            "tasks": {name: task.to_dict() for name, task in self.tasks.items()},
            "execution_plan": [step.to_dict() for step in self.execution_plan],
            "results": self.results
        }

    def save_report(self, output_dir: Optional[Path] = None) -> Path:
        """Save report to file"""
        if output_dir is None:
            output_dir = Path.home() / ".local" / "share" / "ghostlink" / "pipelines"

        output_dir.mkdir(parents=True, exist_ok=True)

        report_file = output_dir / f"pipeline_{self.pipeline_id}.json"

        with open(report_file, 'w') as f:
            json.dump(self.get_report(), f, indent=2)

        return report_file


# Example usage
async def example_task_1():
    """Example task 1"""
    await asyncio.sleep(1)
    return {"status": "Task 1 completed"}


async def example_task_2():
    """Example task 2"""
    await asyncio.sleep(0.5)
    return {"status": "Task 2 completed"}


async def main_example():
    """Example pipeline execution"""
    orchestrator = PipelineOrchestrator(
        name="example_pipeline",
        description="Example pipeline for demonstration"
    )

    orchestrator.add_task("task_1", example_task_1)
    orchestrator.add_task("task_2", example_task_2, dependencies=["task_1"])

    await orchestrator.execute()

    report = orchestrator.get_report()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(main_example())

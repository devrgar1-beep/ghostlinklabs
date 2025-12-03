"""GhostLink Pure Pipeline Orchestration Matrix

Core orchestration system for coordinating all GhostLink components
in a pure, production-ready pipeline architecture.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)


class PipelineStage:
    """Represents a stage in the orchestration pipeline."""

    def __init__(self, name: str, processor: callable, dependencies: list[str] | None = None):
        self.name = name
        self.processor = processor
        self.dependencies = dependencies or []
        self.status = "idle"
        self.last_execution = None
        self.error_count = 0

    async def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute this pipeline stage."""
        try:
            self.status = "running"
            logger.info(f"Executing pipeline stage: {self.name}")

            result = await self.processor(context)

            self.status = "completed"
            self.last_execution = asyncio.get_event_loop().time()
            self.error_count = 0

            return result

        except Exception as e:
            self.status = "error"
            self.error_count += 1
            logger.error(f"Pipeline stage {self.name} failed: {e}")
            raise


class OrchestrationMatrix:
    """Pure pipeline orchestration matrix for GhostLink components."""

    def __init__(self):
        self.stages: dict[str, PipelineStage] = {}
        self.pipeline_order: list[str] = []
        self.context: dict[str, Any] = {}
        self.running = False

    def register_stage(self, stage: PipelineStage):
        """Register a pipeline stage."""
        self.stages[stage.name] = stage
        logger.info(f"Registered pipeline stage: {stage.name}")

    def set_pipeline_order(self, order: list[str]):
        """Set the execution order of pipeline stages."""
        # Validate that all stages exist and dependencies are satisfied
        for stage_name in order:
            if stage_name not in self.stages:
                raise ValueError(f"Stage {stage_name} not registered")

            stage = self.stages[stage_name]
            for dep in stage.dependencies:
                if dep not in order:
                    raise ValueError(
                        f"Dependency {dep} for stage {stage_name} not in pipeline order"
                    )

        self.pipeline_order = order
        logger.info(f"Set pipeline order: {order}")

    async def execute_pipeline(self) -> dict[str, Any]:
        """Execute the complete pipeline."""
        if not self.pipeline_order:
            raise RuntimeError("Pipeline order not set")

        logger.info("Starting pipeline execution...")

        for stage_name in self.pipeline_order:
            stage = self.stages[stage_name]

            # Check dependencies
            for dep in stage.dependencies:
                if self.stages[dep].status != "completed":
                    raise RuntimeError(f"Dependency {dep} not completed for stage {stage_name}")

            # Execute stage
            try:
                result = await stage.execute(self.context)
                self.context.update(result)
                logger.info(f"Stage {stage_name} completed successfully")

            except Exception as e:
                logger.error(f"Pipeline failed at stage {stage_name}: {e}")
                # Continue with error handling - don't stop the entire pipeline
                self.context[f"{stage_name}_error"] = str(e)

        logger.info("Pipeline execution completed")
        return self.context

    async def start_continuous_orchestration(self):
        """Start continuous pipeline orchestration."""
        self.running = True
        logger.info("Starting continuous pipeline orchestration...")

        try:
            while self.running:
                await self.execute_pipeline()
                await asyncio.sleep(1)  # Pipeline execution interval

        except KeyboardInterrupt:
            logger.info("Stopping continuous orchestration...")
        finally:
            self.running = False

    def stop_orchestration(self):
        """Stop continuous orchestration."""
        self.running = False
        logger.info("Orchestration stopped")

    def get_status(self) -> dict[str, Any]:
        """Get current orchestration status."""
        return {
            "running": self.running,
            "stages": {
                name: {
                    "status": stage.status,
                    "last_execution": stage.last_execution,
                    "error_count": stage.error_count,
                }
                for name, stage in self.stages.items()
            },
            "pipeline_order": self.pipeline_order,
            "context_keys": list(self.context.keys()),
        }


# Global orchestration matrix instance
_orchestration_matrix: OrchestrationMatrix | None = None


def get_orchestration_matrix() -> OrchestrationMatrix:
    """Get the global orchestration matrix instance."""
    global _orchestration_matrix
    if _orchestration_matrix is None:
        _orchestration_matrix = OrchestrationMatrix()
    return _orchestration_matrix


async def initialize_orchestration_matrix():
    """Initialize the pure pipeline orchestration matrix."""
    matrix = get_orchestration_matrix()

    # Import and register core components
    try:
        from . import network, obd

        # Network pipeline stage
        async def network_processor(context):
            try:
                # Initialize network components
                network_manager = await network.initialize_networks()
                context["network_manager"] = network_manager
                return {"network_initialized": True}
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as e:
                logger.warning("Network initialization failed: %s", e)
                return {"network_initialized": False, "network_error": str(e)}

        # OBD pipeline stage
        async def obd_processor(context):
            # Initialize OBD components
            obd_engine = obd.create_substrate_engine()
            context["obd_engine"] = obd_engine
            return {"obd_initialized": True}

        # Register stages
        matrix.register_stage(PipelineStage("network", network_processor))
        matrix.register_stage(PipelineStage("obd", obd_processor, ["network"]))

        # Set pipeline order
        matrix.set_pipeline_order(["network", "obd"])

        logger.info("Orchestration matrix initialized with core components")

    except ImportError as e:
        logger.error(f"Failed to import components: {e}")
        raise

    return matrix


async def main():
    """Main orchestration entry point."""
    matrix = await initialize_orchestration_matrix()

    # Start continuous orchestration
    await matrix.start_continuous_orchestration()


if __name__ == "__main__":
    # Pure pipeline orchestration matrix
    asyncio.run(main())

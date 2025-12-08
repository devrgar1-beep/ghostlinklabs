#!/usr/bin/env python3
"""
GhostLink Ray Migration Adapter
Provides backward compatibility during transition to Ray orchestrator
"""

import asyncio
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from ray_orchestrator import RayOrchestrator, ModelSize, ModelMetrics, CompressionType, ExpansionType
    RAY_AVAILABLE = True
except ImportError:
    RAY_AVAILABLE = False

class MigrationAdapter:
    """
    Adapter class that provides the old multi_agent_engine interface
    while delegating to the new Ray orchestrator
    """

    def __init__(self, use_ray: bool = True):
        self.use_ray = use_ray and RAY_AVAILABLE

        if self.use_ray:
            print("🚀 Using Ray orchestrator")
            self.orchestrator = RayOrchestrator(
                num_compression_agents=2,
                num_expansion_agents=2,
                num_consciousness_agents=1
            )
        else:
            print("⚠️  Ray not available, falling back to legacy engine")
            # Import legacy engine if Ray fails
            try:
                from multi_agent_engine import MultiAgentEngine
                self.orchestrator = MultiAgentEngine()
            except ImportError:
                raise RuntimeError("Neither Ray orchestrator nor legacy engine available")

        # Compatibility mappings
        self.model_registry = {}
        self.active_tasks = []

    def register_model(self, model_id: str, model_path: str, **kwargs):
        """Register a model (compatible with old interface)"""
        if self.use_ray:
            # Convert old format to new format
            size_category = ModelSize.MEDIUM  # Default
            if 'size' in kwargs:
                size_str = kwargs['size'].lower()
                if 'tiny' in size_str:
                    size_category = ModelSize.TINY
                elif 'small' in size_str:
                    size_category = ModelSize.SMALL
                elif 'large' in size_str:
                    size_category = ModelSize.LARGE
                elif 'huge' in size_str:
                    size_category = ModelSize.HUGE

            metrics = ModelMetrics(
                parameter_count=kwargs.get('parameter_count', 1000000),
                model_size_mb=kwargs.get('model_size_mb', 500.0),
                inference_time_ms=kwargs.get('inference_time_ms', 50.0),
                memory_usage_mb=kwargs.get('memory_usage_mb', 1000.0),
                accuracy_score=kwargs.get('accuracy_score', 0.85)
            )

            return self.orchestrator.register_model(model_id, model_path, size_category, metrics)
        else:
            # Legacy interface
            return self.orchestrator.register_model(model_id, model_path, **kwargs)

    def compress_model(self, model_id: str, compression_type: str = "pruning", **kwargs):
        """Compress a model (compatible with old interface)"""
        if self.use_ray:
            # Convert string to enum
            comp_type = CompressionType.PRUNING
            if compression_type.lower() == "quantization":
                comp_type = CompressionType.QUANTIZATION
            elif compression_type.lower() == "distillation":
                comp_type = CompressionType.DISTILLATION

            task_id = self.orchestrator.submit_compression_task(
                model_id, comp_type, kwargs
            )
            self.active_tasks.append(task_id)
            return task_id
        else:
            return self.orchestrator.compress_model(model_id, compression_type, **kwargs)

    def expand_model(self, model_id: str, expansion_type: str = "layer_expansion", **kwargs):
        """Expand a model (compatible with old interface)"""
        if self.use_ray:
            # Convert string to enum
            exp_type = ExpansionType.LAYER_EXPANSION
            if expansion_type.lower() == "width":
                exp_type = ExpansionType.WIDTH_EXPANSION
            elif expansion_type.lower() == "depth":
                exp_type = ExpansionType.DEPTH_EXPANSION

            task_id = self.orchestrator.submit_expansion_task(
                model_id, exp_type, kwargs
            )
            self.active_tasks.append(task_id)
            return task_id
        else:
            return self.orchestrator.expand_model(model_id, expansion_type, **kwargs)

    def evolve_consciousness(self, **kwargs):
        """Evolve consciousness (compatible with old interface)"""
        if self.use_ray:
            task_id = self.orchestrator.submit_consciousness_task(kwargs)
            self.active_tasks.append(task_id)
            return task_id
        else:
            return self.orchestrator.evolve_consciousness(**kwargs)

    async def process_tasks(self):
        """Process pending tasks"""
        if self.use_ray:
            await self.orchestrator.process_tasks()
        else:
            await self.orchestrator.process_tasks()

    def get_status(self):
        """Get orchestrator status"""
        if self.use_ray:
            return self.orchestrator.get_status()
        else:
            return self.orchestrator.get_status()

    def shutdown(self):
        """Shutdown the orchestrator"""
        if self.use_ray:
            self.orchestrator.shutdown()
        else:
            self.orchestrator.shutdown()

# Global instance for backward compatibility
migration_adapter = MigrationAdapter()

# Backward compatibility functions
def register_model(model_id: str, model_path: str, **kwargs):
    return migration_adapter.register_model(model_id, model_path, **kwargs)

def compress_model(model_id: str, compression_type: str = "pruning", **kwargs):
    return migration_adapter.compress_model(model_id, compression_type, **kwargs)

def expand_model(model_id: str, expansion_type: str = "layer_expansion", **kwargs):
    return migration_adapter.expand_model(model_id, expansion_type, **kwargs)

def evolve_consciousness(**kwargs):
    return migration_adapter.evolve_consciousness(**kwargs)

async def process_tasks():
    await migration_adapter.process_tasks()

def get_status():
    return migration_adapter.get_status()

def shutdown():
    migration_adapter.shutdown()

if __name__ == "__main__":
    print("🔄 GhostLink Ray Migration Adapter")
    print("This adapter provides backward compatibility during the transition to Ray")
    print(f"Ray Available: {RAY_AVAILABLE}")
    print(f"Using Ray: {migration_adapter.use_ray}")

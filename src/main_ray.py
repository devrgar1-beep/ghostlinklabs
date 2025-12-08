#!/usr/bin/env python3
"""
GhostLink Main Entry Point with Ray Orchestration
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

async def main():
    """Main GhostLink application with Ray orchestration"""

    print("🚀 GhostLink AI System with Ray Orchestration")
    print("=" * 50)

    try:
        # Import the production Ray orchestrator
        from ghostlink_ray_orchestrator import (
            ProductionRayOrchestrator, ModelSize, ModelMetrics,
            CompressionType, ExpansionType
        )

        # Initialize orchestrator
        orchestrator = ProductionRayOrchestrator(num_workers=4, enable_serve=False)

        print("✅ Ray orchestrator initialized")

        # Register initial models
        # These would be loaded from configuration in production
        sample_metrics = ModelMetrics(
            parameter_count=1000000,
            model_size_mb=500.0,
            inference_time_ms=50.0,
            memory_usage_mb=1000.0,
            accuracy_score=0.85
        )

        orchestrator.register_model(
            "consciousness_core",
            "/models/consciousness_core_v1",
            ModelSize.MEDIUM,
            sample_metrics
        )

        print("✅ Initial models registered")

        # Start background task processing
        print("🔄 Starting background task processing...")

        # In a real application, this would be an event loop
        # For demo purposes, we'll submit some sample tasks

        # Submit sample compression task
        compress_task = orchestrator.submit_compression_task(
            "consciousness_core",
            CompressionType.PRUNING,
            {"pruning_ratio": 0.2, "target_sparsity": 0.3}
        )

        # Submit sample expansion task
        expand_task = orchestrator.submit_expansion_task(
            "consciousness_core",
            ExpansionType.LAYER_EXPANSION,
            {"num_layers": 3, "expansion_factor": 1.5}
        )

        # Submit consciousness evolution
        consciousness_task = orchestrator.submit_consciousness_task({
            "target_level": "UltraGrok",
            "evolution_focus": "distributed_intelligence",
            "time_horizon": "2026"
        })

        # Process tasks
        await orchestrator.process_tasks()

        # Show results
        status = orchestrator.get_status()
        print("\n📊 System Status:")
        print(f"   Tasks Processed: {status['performance_stats']['tasks_processed']}")
        print(f"   Models Registered: {status['registered_models']}")
        print(f"   Ray Workers: {status['num_workers']}")

        # Keep running for monitoring (in real app, this would be a server)
        print("\n🔄 System running... (Press Ctrl+C to stop)")

        while True:
            await asyncio.sleep(10)
            # Periodic status check
            current_status = orchestrator.get_status()
            print(f"   Status check: {current_status['pending_tasks']} pending, {current_status['completed_tasks']} completed")

    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user")
    except Exception as e:
        print(f"❌ Error in main loop: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if 'orchestrator' in locals():
            orchestrator.shutdown()

        print("✅ GhostLink shutdown complete")

if __name__ == "__main__":
    # Set up environment
    os.environ.setdefault("RAY_DISABLE_IMPORT_WARNING", "1")

    # Run main application
    asyncio.run(main())

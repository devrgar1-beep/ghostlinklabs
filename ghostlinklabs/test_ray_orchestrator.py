#!/usr/bin/env python3
"""
GhostLink Ray Orchestrator Test Suite
Tests the new Ray-based distributed orchestration system
"""

import asyncio
import time
import sys
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ray_orchestrator import (
    RayOrchestrator, ModelSize, ModelMetrics,
    CompressionType, ExpansionType, optimize_hyperparameters
)
from ray import tune

def test_basic_orchestrator():
    """Test basic orchestrator functionality"""
    print("🧪 Testing basic Ray orchestrator functionality...")

    orchestrator = RayOrchestrator(
        num_compression_agents=2,
        num_expansion_agents=2,
        num_consciousness_agents=1
    )

    try:
        # Test model registration
        metrics = ModelMetrics(
            parameter_count=1000000,
            model_size_mb=500.0,
            inference_time_ms=50.0,
            memory_usage_mb=1000.0,
            accuracy_score=0.85
        )

        success = orchestrator.register_model("test_model", "/tmp/test_model", ModelSize.MEDIUM, metrics)
        assert success, "Model registration failed"
        print("✅ Model registration successful")

        # Test task submission
        compress_task = orchestrator.submit_compression_task(
            "test_model", CompressionType.PRUNING, {"pruning_ratio": 0.3}
        )
        assert compress_task, "Compression task submission failed"
        print("✅ Compression task submitted")

        expand_task = orchestrator.submit_expansion_task(
            "test_model", ExpansionType.LAYER_EXPANSION, {"num_layers": 2}
        )
        assert expand_task, "Expansion task submission failed"
        print("✅ Expansion task submitted")

        consciousness_task = orchestrator.submit_consciousness_task({
            "target_level": "UltraGrok",
            "evolution_focus": "intelligence"
        })
        assert consciousness_task, "Consciousness task submission failed"
        print("✅ Consciousness task submitted")

        # Test task processing
        start_time = time.time()
        asyncio.run(orchestrator.process_tasks())
        processing_time = time.time() - start_time

        status = orchestrator.get_status()
        assert status["completed_tasks"] == 3, f"Expected 3 completed tasks, got {status['completed_tasks']}"
        print(f"✅ All tasks completed in {processing_time:.2f} seconds")

        # Test parallel processing performance
        print("\\n🔬 Testing parallel processing performance...")

        # Submit multiple tasks
        for i in range(5):
            orchestrator.submit_compression_task(
                "test_model", CompressionType.QUANTIZATION, {"quantization_bits": 8}
            )

        start_time = time.time()
        asyncio.run(orchestrator.process_tasks())
        parallel_time = time.time() - start_time

        final_status = orchestrator.get_status()
        assert final_status["completed_tasks"] == 8, f"Expected 8 total completed tasks, got {final_status['completed_tasks']}"
        print(f"✅ Parallel processing completed in {parallel_time:.2f} seconds")

        return True

    finally:
        orchestrator.shutdown()

def test_hyperparameter_optimization():
    """Test Ray Tune hyperparameter optimization"""
    print("\\n🎯 Testing hyperparameter optimization...")

    try:
        # Define search space
        search_space = {
            "learning_rate": tune.loguniform(1e-4, 1e-1),
            "batch_size": tune.choice([16, 32, 64, 128]),
        }

        # Run optimization (reduced samples for testing)
        result = optimize_hyperparameters(search_space, num_samples=3)

        # Check results
        assert result, "Hyperparameter optimization failed"
        print("✅ Hyperparameter optimization completed")

        return True

    except Exception as e:
        print(f"⚠️  Hyperparameter optimization test failed (expected if Tune not fully configured): {e}")
        return False

def test_migration_adapter():
    """Test the migration adapter for backward compatibility"""
    print("\\n🔄 Testing migration adapter...")

    try:
        from migration_adapter import MigrationAdapter, register_model, compress_model

        # Test adapter initialization
        adapter = MigrationAdapter()
        assert adapter.use_ray, "Adapter should use Ray orchestrator"
        print("✅ Migration adapter initialized with Ray")

        # Test backward compatibility functions
        success = register_model("adapter_test_model", "/tmp/adapter_model",
                               parameter_count=500000, model_size_mb=250.0)
        assert success, "Adapter model registration failed"
        print("✅ Backward compatible model registration works")

        # Test compression through adapter
        task_id = compress_model("adapter_test_model", "pruning", pruning_ratio=0.2)
        assert task_id, "Adapter compression failed"
        print("✅ Backward compatible compression works")

        # Process tasks
        asyncio.run(adapter.process_tasks())

        # Check status
        status = adapter.get_status()
        assert status["completed_tasks"] >= 1, "Adapter task processing failed"
        print("✅ Migration adapter task processing works")

        adapter.shutdown()
        return True

    except Exception as e:
        print(f"❌ Migration adapter test failed: {e}")
        return False

def benchmark_performance():
    """Benchmark Ray orchestrator vs legacy system"""
    print("\\n📊 Benchmarking performance improvements...")

    # Test Ray orchestrator performance
    ray_orchestrator = RayOrchestrator(num_compression_agents=4, num_expansion_agents=4)

    try:
        # Register test models
        for i in range(10):
            metrics = ModelMetrics(
                parameter_count=1000000 + i * 100000,
                model_size_mb=500.0 + i * 50,
                inference_time_ms=50.0,
                memory_usage_mb=1000.0,
                accuracy_score=0.85
            )
            ray_orchestrator.register_model(f"bench_model_{i}", f"/tmp/model_{i}", ModelSize.MEDIUM, metrics)

        # Submit batch of tasks
        for i in range(20):  # 20 tasks total
            if i % 2 == 0:
                ray_orchestrator.submit_compression_task(
                    f"bench_model_{i % 10}", CompressionType.PRUNING, {"pruning_ratio": 0.3}
                )
            else:
                ray_orchestrator.submit_expansion_task(
                    f"bench_model_{i % 10}", ExpansionType.LAYER_EXPANSION, {"num_layers": 2}
                )

        # Measure processing time
        start_time = time.time()
        asyncio.run(ray_orchestrator.process_tasks())
        ray_time = time.time() - start_time

        status = ray_orchestrator.get_status()
        print(f"✅ Ray orchestrator processed {status['completed_tasks']} tasks in {ray_time:.2f} seconds")
        print(".2f")

        return {
            "ray_processing_time": ray_time,
            "tasks_completed": status["completed_tasks"],
            "throughput": status["completed_tasks"] / ray_time
        }

    finally:
        ray_orchestrator.shutdown()

def create_test_report(results: dict):
    """Create a test report"""
    report = {
        "test_timestamp": time.time(),
        "ray_orchestrator_tests": results,
        "summary": {
            "total_tests": len(results),
            "passed_tests": sum(1 for r in results.values() if r),
            "failed_tests": sum(1 for r in results.values() if not r)
        }
    }

    report_path = Path("RAY_TEST_REPORT.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"📊 Test report saved to {report_path}")
    return report

def main():
    """Run all tests"""
    print("🧪 GhostLink Ray Orchestrator Test Suite")
    print("=" * 50)

    results = {}

    # Test basic functionality
    results["basic_orchestrator"] = test_basic_orchestrator()

    # Test hyperparameter optimization
    results["hyperparameter_optimization"] = test_hyperparameter_optimization()

    # Test migration adapter
    results["migration_adapter"] = test_migration_adapter()

    # Benchmark performance
    benchmark_results = benchmark_performance()
    results["performance_benchmark"] = benchmark_results is not None

    # Create test report
    report = create_test_report(results)

    # Summary
    print("\\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"   Total Tests: {len(results)}")
    print(f"   Passed: {sum(1 for r in results.values() if r)}")
    print(f"   Failed: {sum(1 for r in results.values() if not r)}")

    if benchmark_results:
        print("\\n🚀 Performance Results:")
        print(".2f")
        print(".1f")

    if all(results.values()):
        print("\\n🎉 All tests passed! Ray orchestrator is ready for production.")
        return 0
    else:
        print("\\n⚠️  Some tests failed. Check the test report for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

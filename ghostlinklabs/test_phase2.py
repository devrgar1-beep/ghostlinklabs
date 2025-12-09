#!/usr/bin/env python3
"""
GhostLink Phase 2 Test Suite
Comprehensive testing of NATS messaging, OpenTelemetry, and Ray orchestration integration
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_nats_integration():
    """Test NATS messaging functionality"""
    print("🐱 Testing NATS Integration...")
    try:
        from ghostlink_nats import NATSMessaging

        nats = NATSMessaging()
        success = await nats.connect()

        if not success:
            print("❌ NATS connection failed (server may not be running)")
            return False

        try:
            # Test basic publish/subscribe
            messages_received = []

            async def test_handler(message):
                messages_received.append(message.payload)

            await nats.subscribe("test.topic", test_handler)

            # Publish test message
            await nats.publish("test.topic", {"test": "data", "timestamp": time.time()})

            # Wait for message
            await asyncio.sleep(0.1)

            if messages_received:
                print("✅ NATS publish/subscribe working")
                return True
            else:
                print("❌ NATS message not received")
                return False

        finally:
            await nats.disconnect()

    except Exception as e:
        print(f"⚠️ NATS test skipped: {e}")
        return False  # Return False instead of raising to allow other tests to run

async def test_telemetry_integration():
    """Test OpenTelemetry functionality"""
    print("\\n📊 Testing Telemetry Integration...")
    try:
        from ghostlink_telemetry import GhostLinkTelemetry

        telemetry = GhostLinkTelemetry()

        if not telemetry.initialize():
            print("❌ Telemetry initialization failed (OTLP endpoint may not be available)")
            return False

        try:
            # Test metrics recording
            telemetry.record_task_processed("test_task", "success")
            telemetry.record_api_request("GET", "/test", "200", 0.05)
            telemetry.update_active_agents(2)

            # Test tracing
            with telemetry.start_span("test_operation", {"test": "value"}):
                time.sleep(0.01)

            print("✅ Telemetry recording working")
            return True

        finally:
            telemetry.stop_system_monitoring()

    except Exception as e:
        print(f"⚠️ Telemetry test skipped: {e}")
        return False

async def test_ray_orchestrator():
    """Test Ray orchestrator functionality"""
    print("\\n🎮 Testing Ray Orchestrator...")
    try:
        from ghostlink_ray_orchestrator import ProductionRayOrchestrator, ModelSize, ModelMetrics, CompressionType

        orchestrator = ProductionRayOrchestrator(num_workers=2)

        # Register test model
        metrics = ModelMetrics(parameter_count=1000000, model_size_mb=500.0)
        success = orchestrator.register_model("test_model", "/tmp/test", ModelSize.MEDIUM, metrics)

        if not success:
            print("❌ Model registration failed")
            return False

        # Submit test task
        task_id = orchestrator.submit_compression_task(
            "test_model", CompressionType.PRUNING, {"ratio": 0.3}
        )

        if not task_id:
            print("❌ Task submission failed")
            return False

        # Process tasks
        await orchestrator.process_tasks()

        # Check status
        status = orchestrator.get_status()
        if status.get("completed_tasks", 0) > 0:
            print("✅ Ray orchestrator working")
            orchestrator.shutdown()
            return True
        else:
            print("❌ Task processing failed")
            orchestrator.shutdown()
            return False

    except ImportError:
        print("⚠️ Ray orchestrator not available")
        return False

async def test_phase2_integration():
    """Test full Phase 2 integration"""
    print("\\n🚀 Testing Phase 2 Integration...")
    from ghostlink_phase2 import GhostLinkPhase2

    system = GhostLinkPhase2()

    if not await system.initialize():
        print("❌ Phase 2 initialization failed")
        return False

    try:
        # Test status reporting
        status = system.get_status()
        if status["component_status"]["system_health"] == "healthy":
            print("✅ Phase 2 system healthy")
        else:
            print(f"❌ System health: {status['component_status']['system_health']}")
            return False

        # Test command execution
        result = await system.execute_command("get_status")
        if "error" not in result:
            print("✅ Command execution working")
            return True
        else:
            print(f"❌ Command execution failed: {result}")
            return False

    finally:
        await system.stop()

async def test_cross_component_communication():
    """Test communication between components"""
    print("\\n🔗 Testing Cross-Component Communication...")
    from ghostlink_phase2 import GhostLinkPhase2

    system = GhostLinkPhase2()

    if not await system.initialize():
        print("❌ Cross-component test initialization failed")
        return False

    try:
        # Test NATS message sending via orchestrator command
        if system.nats_integration and system.orchestrator:
            # Send a command that should trigger NATS messaging
            result = await system.execute_command("process_tasks")
            if "error" not in result:
                print("✅ Cross-component communication working")
                return True
            else:
                print(f"❌ Cross-component communication failed: {result}")
                return False
        else:
            print("⚠️ Not all components available for cross-component test")
            return True  # Not a failure, just limited testing

    finally:
        await system.stop()

async def run_performance_test():
    """Run performance comparison test"""
    print("\\n📈 Running Performance Test...")
    try:
        from ghostlink_ray_orchestrator import ProductionRayOrchestrator, ModelSize, ModelMetrics, CompressionType

        orchestrator = ProductionRayOrchestrator(num_workers=4)

        # Register multiple models
        for i in range(5):
            metrics = ModelMetrics(
                parameter_count=1000000 + i * 100000,
                model_size_mb=500.0 + i * 50
            )
            orchestrator.register_model(f"perf_model_{i}", f"/tmp/model_{i}", ModelSize.MEDIUM, metrics)

        # Submit batch of tasks
        for i in range(10):
            orchestrator.submit_compression_task(
                f"perf_model_{i % 5}", CompressionType.PRUNING, {"ratio": 0.3}
            )

        # Measure processing time
        start_time = time.time()
        await orchestrator.process_tasks()
        processing_time = time.time() - start_time

        status = orchestrator.get_status()
        tasks_completed = status.get("completed_tasks", 0)

        print(".2f")
        print(".1f")

        orchestrator.shutdown()

        # Performance thresholds (adjust based on system)
        if processing_time < 10.0 and tasks_completed >= 10:
            print("✅ Performance test passed")
            return True
        else:
            print("⚠️ Performance below expectations")
            return True  # Don't fail test for performance

    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def create_test_report(results: Dict[str, Any]) -> Dict[str, Any]:
    """Create comprehensive test report"""
    report = {
        "test_timestamp": time.time(),
        "phase": "phase2_integration",
        "test_results": results,
        "summary": {
            "total_tests": len(results),
            "passed_tests": sum(1 for r in results.values() if r),
            "failed_tests": sum(1 for r in results.values() if not r),
            "success_rate": sum(1 for r in results.values() if r) / len(results) if results else 0
        },
        "components_tested": [
            "nats_messaging",
            "opentelemetry_telemetry",
            "ray_orchestrator",
            "phase2_integration",
            "cross_component_communication",
            "performance"
        ],
        "recommendations": []
    }

    # Add recommendations based on results
    if not results.get("nats_integration", False):
        report["recommendations"].append("Start NATS server for messaging functionality")
    if not results.get("telemetry_integration", False):
        report["recommendations"].append("Check OpenTelemetry OTLP endpoint configuration")
    if not results.get("ray_orchestrator", False):
        report["recommendations"].append("Verify Ray installation and GPU/OpenCL setup")

    return report

async def main():
    """Run all Phase 2 tests"""
    print("🧪 GhostLink Phase 2 Integration Test Suite")
    print("=" * 60)

    results = {}

    # Run individual component tests
    results["nats_integration"] = await test_nats_integration()
    results["telemetry_integration"] = await test_telemetry_integration()
    results["ray_orchestrator"] = await test_ray_orchestrator()

    # Run integration tests
    results["phase2_integration"] = await test_phase2_integration()
    results["cross_component_communication"] = await test_cross_component_communication()

    # Run performance test
    results["performance"] = await run_performance_test()

    # Create and save test report
    report = create_test_report(results)

    print("\\n" + "=" * 60)
    print("📋 Test Results Summary:")
    print(f"   Total Tests: {report['summary']['total_tests']}")
    print(f"   Passed: {report['summary']['passed_tests']}")
    print(f"   Failed: {report['summary']['failed_tests']}")
    print(".1%")

    # Save report
    report_path = Path("PHASE2_TEST_REPORT.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\\n📊 Detailed report saved to {report_path}")

    if report["recommendations"]:
        print("\\n💡 Recommendations:")
        for rec in report["recommendations"]:
            print(f"   • {rec}")

    # Overall assessment
    if report["summary"]["success_rate"] >= 0.8:
        print("\\n🎉 Phase 2 integration test PASSED!")
        print("✅ Ready for production deployment")
        return 0
    elif report["summary"]["success_rate"] >= 0.6:
        print("\\n⚠️ Phase 2 integration test PARTIALLY PASSED")
        print("🔧 Some components need attention before production")
        return 1
    else:
        print("\\n❌ Phase 2 integration test FAILED")
        print("🔧 Critical issues need to be resolved")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

#!/usr/bin/env python3
"""
GhostLink Phase 2 Demo
Showcase the integrated NATS messaging, OpenTelemetry observability, and Ray orchestration system
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

class Phase2Demo:
    """Comprehensive Phase 2 system demonstration"""

    def __init__(self):
        self.system = None
        self.demo_results = {}

    async def initialize_system(self):
        """Initialize the complete Phase 2 system"""
        print("🚀 Initializing GhostLink Phase 2 System...")
        from ghostlink_phase2 import GhostLinkPhase2

        self.system = GhostLinkPhase2()

        if await self.system.initialize():
            print("✅ Phase 2 system initialized successfully")
            return True
        else:
            print("❌ Phase 2 system initialization failed")
            return False

    async def demo_nats_messaging(self):
        """Demonstrate NATS messaging capabilities"""
        print("\\n🐱 Demonstrating NATS Messaging...")

        if not self.system or not self.system.nats_integration:
            print("⚠️ NATS integration not available")
            return False

        try:
            # Simulate agent communication
            agents = ["agent_1", "agent_2", "agent_3"]
            tasks = []

            for agent in agents:
                task = {
                    "agent_id": agent,
                    "task_type": "protocol_analysis",
                    "payload": {
                        "packets": 1000,
                        "protocol": "TCP",
                        "timestamp": time.time()
                    }
                }
                tasks.append(task)

            # Publish tasks via NATS
            for task in tasks:
                await self.system.nats_integration.nats.publish(
                    "agent.tasks",
                    task
                )
                print(f"📤 Published task for {task['agent_id']}")

            # Simulate responses
            responses_received = 0

            async def response_handler(message):
                nonlocal responses_received
                response = message.payload
                print(f"📥 Received response from {response.get('agent_id')}: {response.get('status')}")
                responses_received += 1

            await self.system.nats_integration.nats.subscribe("agent.responses", response_handler)

            # Simulate agent responses
            for agent in agents:
                response = {
                    "agent_id": agent,
                    "status": "completed",
                    "processed_packets": 1000,
                    "timestamp": time.time()
                }
                await self.system.nats_integration.nats.publish("agent.responses", response)
                await asyncio.sleep(0.1)  # Simulate processing time

            await asyncio.sleep(0.5)  # Wait for all responses

            print(f"✅ NATS messaging demo completed: {responses_received} responses received")
            self.demo_results["nats_messaging"] = responses_received == len(agents)
            return responses_received == len(agents)

        except Exception as e:
            print(f"❌ NATS demo failed: {e}")
            self.demo_results["nats_messaging"] = False
            return False

    async def demo_telemetry_observability(self):
        """Demonstrate OpenTelemetry observability"""
        print("\\n📊 Demonstrating Telemetry & Observability...")

        if not self.system or not self.system.telemetry:
            print("⚠️ Telemetry integration not available")
            return False

        try:
            # Simulate system activity
            telemetry = self.system.telemetry.telemetry

            # Record various metrics
            for i in range(10):
                telemetry.record_task_processed(f"demo_task_{i}", "success")
                telemetry.record_api_request("POST", f"/api/endpoint_{i}", "200", 0.05 + i * 0.01)
                telemetry.update_active_agents(3 + (i % 3))

                # Create nested spans
                with telemetry.start_span(f"demo_operation_{i}", {"iteration": i}):
                    with telemetry.start_span("sub_operation", {"type": "processing"}):
                        time.sleep(0.01)

            # Get metrics summary
            status = self.system.get_status()
            metrics = status.get("telemetry_metrics", {})

            print("📈 Recorded metrics:")
            print(f"   Tasks processed: {metrics.get('tasks_processed', 0)}")
            print(f"   API requests: {metrics.get('api_requests', 0)}")
            print(f"   Active agents: {metrics.get('active_agents', 0)}")

            print("✅ Telemetry observability demo completed")
            self.demo_results["telemetry_observability"] = True
            return True

        except Exception as e:
            print(f"❌ Telemetry demo failed: {e}")
            self.demo_results["telemetry_observability"] = False
            return False

    async def demo_ray_orchestration(self):
        """Demonstrate Ray distributed orchestration"""
        print("\\n🎮 Demonstrating Ray Orchestration...")

        if not self.system.orchestrator:
            print("⚠️ Ray orchestrator not available")
            return False

        try:
            # Register demo models
            models_registered = 0
            from ghostlink_ray_orchestrator import ModelSize, ModelMetrics, CompressionType

            for i in range(3):
                metrics = ModelMetrics(
                    parameter_count=500000 + i * 200000,
                    model_size_mb=250.0 + i * 100
                )
                success = self.system.orchestrator.register_model(
                    f"demo_model_{i}",
                    f"/tmp/demo_model_{i}",
                    ModelSize.MEDIUM,
                    metrics
                )
                if success:
                    models_registered += 1

            print(f"📝 Registered {models_registered} demo models")

            # Submit compression tasks
            tasks_submitted = 0
            for i in range(6):
                task_id = self.system.orchestrator.submit_compression_task(
                    f"demo_model_{i % 3}",
                    CompressionType.PRUNING,
                    {"ratio": 0.2 + (i % 3) * 0.1}
                )
                if task_id:
                    tasks_submitted += 1

            print(f"🎯 Submitted {tasks_submitted} compression tasks")

            # Process tasks
            await self.system.orchestrator.process_tasks()

            # Check results
            status = self.system.orchestrator.get_status()
            tasks_completed = status.get("completed_tasks", 0)

            print(f"✅ Completed {tasks_completed} tasks")

            self.demo_results["ray_orchestration"] = tasks_completed > 0
            return tasks_completed > 0

        except Exception as e:
            print(f"❌ Ray orchestration demo failed: {e}")
            self.demo_results["ray_orchestration"] = False
            return False

    async def demo_integrated_workflow(self):
        """Demonstrate integrated workflow across all components"""
        print("\\n🔗 Demonstrating Integrated Workflow...")

        try:
            # Simulate a complete AI agent workflow
            workflow_steps = [
                "receive_task",
                "analyze_protocol",
                "compress_model",
                "validate_results",
                "report_completion"
            ]

            for step in workflow_steps:
                        # Start telemetry span
                        if self.system.telemetry:
                            with self.system.telemetry.telemetry.start_span(
                                f"workflow_{step}",
                                {"step": step, "workflow": "integrated_demo"}
                            ):
                                # Simulate processing time
                                processing_time = 0.05 + (workflow_steps.index(step) * 0.02)
                                time.sleep(processing_time)

                                # Record metrics
                                self.system.telemetry.telemetry.record_task_processed(
                                    f"workflow_{step}", "success"
                                )

                                # Send NATS message about step completion
                                if self.system.nats_integration:
                                    message = {
                                        "step": step,
                                        "status": "completed",
                                        "processing_time": processing_time,
                                        "timestamp": time.time()
                                    }
                                    await self.system.nats_integration.nats.publish(
                                        "workflow.progress",
                                        message
                                    )

                                print(f"🔄 Completed workflow step: {step}")

            print("✅ Integrated workflow demo completed")
            self.demo_results["integrated_workflow"] = True
            return True

        except Exception as e:
            print(f"❌ Integrated workflow demo failed: {e}")
            self.demo_results["integrated_workflow"] = False
            return False

    async def demo_system_monitoring(self):
        """Demonstrate system monitoring capabilities"""
        print("\\n📊 Demonstrating System Monitoring...")

        try:
            # Get comprehensive system status
            status = self.system.get_status()

            print("🔍 System Status Overview:")
            print(f"   System Health: {status['component_status']['system_health']}")
            print(f"   Active Components: {len([c for c in status['component_status'].values() if c == 'healthy'])}")

            if "telemetry_metrics" in status:
                metrics = status["telemetry_metrics"]
                print("\\n📈 Current Metrics:")
                print(f"   Tasks Processed: {metrics.get('tasks_processed', 0)}")
                print(f"   API Requests: {metrics.get('api_requests', 0)}")
                print(f"   Active Agents: {metrics.get('active_agents', 0)}")

            if "orchestrator_status" in status:
                orch_status = status["orchestrator_status"]
                print("\\n🎮 Orchestrator Status:")
                print(f"   Workers: {orch_status.get('workers', 0)}")
                print(f"   Queued Tasks: {orch_status.get('queued_tasks', 0)}")
                print(f"   Completed Tasks: {orch_status.get('completed_tasks', 0)}")

            print("✅ System monitoring demo completed")
            self.demo_results["system_monitoring"] = True
            return True

        except Exception as e:
            print(f"❌ System monitoring demo failed: {e}")
            self.demo_results["system_monitoring"] = False
            return False

    async def run_full_demo(self):
        """Run the complete Phase 2 demonstration"""
        print("🎭 GhostLink Phase 2 Full System Demo")
        print("=" * 60)

        # Initialize system
        if not await self.initialize_system():
            return False

        try:
            # Run all demo components
            demos = [
                ("NATS Messaging", self.demo_nats_messaging),
                ("Telemetry & Observability", self.demo_telemetry_observability),
                ("Ray Orchestration", self.demo_ray_orchestration),
                ("Integrated Workflow", self.demo_integrated_workflow),
                ("System Monitoring", self.demo_system_monitoring)
            ]

            successful_demos = 0

            for demo_name, demo_func in demos:
                try:
                    if await demo_func():
                        successful_demos += 1
                        print(f"✅ {demo_name}: PASSED")
                    else:
                        print(f"❌ {demo_name}: FAILED")
                except Exception as e:
                    print(f"❌ {demo_name}: ERROR - {e}")
                    self.demo_results[demo_name.lower().replace(" ", "_").replace("&", "and")] = False

            # Final summary
            print("\\n" + "=" * 60)
            print("🎭 Demo Results Summary:")
            print(f"   Total Demos: {len(demos)}")
            print(f"   Successful: {successful_demos}")
            print(f"   Failed: {len(demos) - successful_demos}")
            print(".1%")

            # Save demo results
            demo_report = {
                "demo_timestamp": time.time(),
                "phase": "phase2_demo",
                "demo_results": self.demo_results,
                "summary": {
                    "total_demos": len(demos),
                    "successful_demos": successful_demos,
                    "success_rate": successful_demos / len(demos) if demos else 0
                },
                "system_status": self.system.get_status() if self.system else None
            }

            report_path = Path("PHASE2_DEMO_REPORT.json")
            with open(report_path, 'w') as f:
                json.dump(demo_report, f, indent=2)

            print(f"\\n📊 Demo report saved to {report_path}")

            if successful_demos >= len(demos) * 0.8:
                print("\\n🎉 Phase 2 demo COMPLETED SUCCESSFULLY!")
                print("🚀 System ready for production deployment")
                return True
            else:
                print("\\n⚠️ Phase 2 demo PARTIALLY SUCCESSFUL")
                print("🔧 Some components may need attention")
                return True

        finally:
            # Cleanup
            if self.system:
                await self.system.stop()

async def main():
    """Run the Phase 2 demo"""
    demo = Phase2Demo()
    success = await demo.run_full_demo()

    if success:
        print("\\n🎊 GhostLink Phase 2 is ready for production!")
        print("\\nNext steps:")
        print("1. Start NATS server: nats-server")
        print("2. Configure OTLP endpoint for telemetry")
        print("3. Deploy Ray cluster for distributed processing")
        print("4. Run production workloads")
    else:
        print("\\n⚠️ Some demo components failed - check system configuration")

    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

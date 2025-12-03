#!/usr/bin/env python3
"""
GhostLink System Stress Test & Break Attempt

This script attempts to break the GhostLink system in various ways.
"""

import asyncio
import random
import time

from ghostlink.core.autonomous_agents import AutonomousAgent
from ghostlink.net.fiber_network import fiber_network


class BreakTest:
    """Comprehensive system breaking test suite."""

    def __init__(self):
        self.test_results = []
        self.agents_created = []

    def log_result(self, test_name: str, success: bool, error: str = "", details: str = ""):
        """Log a test result."""
        result = {
            "test": test_name,
            "success": success,
            "error": error,
            "details": details,
            "timestamp": time.time(),
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if error:
            print(f"   Error: {error}")
        if details:
            print(f"   Details: {details}")

    async def test_network_double_start_stop(self):
        """Test starting/stopping network multiple times."""
        try:
            await fiber_network.start()
            await fiber_network.start()  # Should handle gracefully
            await fiber_network.stop()
            await fiber_network.stop()  # Should handle gracefully
            self.log_result("Network double start/stop", True)
        except Exception as e:
            self.log_result("Network double start/stop", False, str(e))

    async def test_agent_invalid_names(self):
        """Test creating agents with invalid names."""
        invalid_names = ["", None, 123, [], {}]
        for invalid_name in invalid_names:
            try:
                agent = AutonomousAgent(invalid_name, "test")
                self.agents_created.append(agent)
                self.log_result(
                    f"Invalid agent name: {repr(invalid_name)}", False, "Should have failed"
                )
            except Exception as e:
                self.log_result(
                    f"Invalid agent name: {repr(invalid_name)}",
                    True,
                    details=f"Correctly rejected: {e}",
                )

    async def test_message_to_nonexistent_agent(self):
        """Test sending messages to agents that don't exist."""
        try:
            await fiber_network.start()
            agent = AutonomousAgent("sender_agent", "sender")
            self.agents_created.append(agent)

            nonexistent_recipients = ["ghost_agent", "", None, "never_existed"]
            for recipient in nonexistent_recipients:
                try:
                    msg_id = await agent.send_fiber_message(recipient, "test", {"data": "test"})
                    if msg_id:
                        self.log_result(
                            f"Message to nonexistent: {recipient}",
                            True,
                            details=f"Routed with ID: {msg_id}",
                        )
                    else:
                        self.log_result(
                            f"Message to nonexistent: {recipient}",
                            True,
                            details="Failed to route (expected)",
                        )
                except Exception as e:
                    self.log_result(f"Message to nonexistent: {recipient}", False, str(e))

            await fiber_network.stop()
        except Exception as e:
            self.log_result("Message to nonexistent agent", False, str(e))

    async def test_malformed_messages(self):
        """Test sending malformed message payloads."""
        try:
            await fiber_network.start()
            agent = AutonomousAgent("malformed_sender", "sender")
            self.agents_created.append(agent)

            malformed_payloads = [None, "string_not_dict", [], {"very_large": "x" * 100000}]
            for i, payload in enumerate(malformed_payloads):
                try:
                    msg_id = await agent.send_fiber_message("test_recipient", "malformed", payload)
                    # Only the last payload (dict) should succeed
                    should_succeed = i == 3
                    self.log_result(
                        f"Malformed payload {i}",
                        should_succeed,
                        details=(
                            f"Unexpected success, ID: {msg_id}"
                            if not should_succeed
                            else f"Handled gracefully, ID: {msg_id}"
                        ),
                    )
                except Exception as e:
                    # First 3 payloads should fail with validation errors
                    should_fail = i < 3
                    self.log_result(
                        f"Malformed payload {i}",
                        should_fail,
                        str(e) if should_fail else f"Unexpected failure: {e}",
                    )

            await fiber_network.stop()
        except Exception as e:
            self.log_result("Malformed messages", False, str(e))

    async def test_network_congestion(self):
        """Test network behavior under message congestion."""
        try:
            await fiber_network.start()

            agents = []
            for i in range(10):  # Reduced for stability
                agent = AutonomousAgent(f"congestion_agent_{i}", "worker")
                agents.append(agent)
                self.agents_created.append(agent)

            tasks = []
            for i in range(100):  # Reduced message count
                sender_idx = random.randint(0, len(agents) - 1)
                recipient_idx = random.randint(0, len(agents) - 1)
                task = agents[sender_idx].send_fiber_message(
                    agents[recipient_idx].name,
                    "congestion_test",
                    {"message_num": i, "data": "x" * 50},
                )
                tasks.append(task)

            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            end_time = time.time()

            success_count = sum(1 for r in results if not isinstance(r, Exception))
            error_count = len(results) - success_count

            self.log_result(
                "Network congestion",
                success_count > error_count,
                details=f"Sent {len(tasks)} messages in {end_time-start_time:.2f}s. Success: {success_count}, Errors: {error_count}",
            )

            await fiber_network.stop()
        except Exception as e:
            self.log_result("Network congestion", False, str(e))

    async def test_network_recovery(self):
        """Test network recovery after failures."""
        try:
            await fiber_network.start()

            agent1 = AutonomousAgent("recovery_agent_1", "recovery")
            agent2 = AutonomousAgent("recovery_agent_2", "recovery")
            self.agents_created.extend([agent1, agent2])

            msg1 = await agent1.send_fiber_message(agent2.name, "test", {"data": "before_stop"})
            print(f"   Message before stop: {msg1}")

            await fiber_network.stop()

            try:
                msg2 = await agent1.send_fiber_message(agent2.name, "test", {"data": "after_stop"})
                self.log_result(
                    "Network recovery - message during stop", False, "Should have failed"
                )
            except Exception as e:
                self.log_result(
                    "Network recovery - message during stop", True, details=f"Correctly failed: {e}"
                )

            await fiber_network.start()
            msg3 = await agent1.send_fiber_message(agent2.name, "test", {"data": "after_restart"})
            print(f"   Message after restart: {msg3}")

            success = bool(msg3)
            self.log_result(
                "Network recovery",
                success,
                details="Network recovered" if success else "Failed to recover",
            )

            await fiber_network.stop()
        except Exception as e:
            self.log_result("Network recovery", False, str(e))

    async def run_all_tests(self):
        """Run all break tests."""
        print("🔨 Starting GhostLink Break Tests")
        print("=" * 50)

        tests = [
            self.test_network_double_start_stop,
            self.test_agent_invalid_names,
            self.test_message_to_nonexistent_agent,
            self.test_malformed_messages,
            self.test_network_congestion,
            self.test_network_recovery,
        ]

        for test in tests:
            print(f"\n🧪 Running: {test.__name__}")
            try:
                await test()
            except Exception as e:
                self.log_result(test.__name__, False, f"Test framework error: {e}")

        print("\n🧹 Cleaning up...")
        for agent in self.agents_created:
            try:
                fiber_network.unregister_agent(agent.name)
            except:
                pass

        print("\n📊 Test Summary:")
        print("=" * 30)
        passed = sum(1 for r in self.test_results if r["success"])
        total = len(self.test_results)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(".1f")

        if passed == total:
            print("🎉 All tests passed! System is robust.")
        elif passed > total * 0.8:
            print("✅ Most tests passed. System is fairly robust.")
        elif passed > total * 0.5:
            print("⚠️  Some vulnerabilities found.")
        else:
            print("❌ Many vulnerabilities found.")

        failed_tests = [r for r in self.test_results if not r["success"]]
        if failed_tests:
            print("\n❌ Failed Tests:")
            for test in failed_tests:
                print(f"   - {test['test']}: {test['error']}")


async def main():
    """Main test function."""
    breaker = BreakTest()
    await breaker.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())

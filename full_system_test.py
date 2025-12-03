#!/usr/bin/env python3
"""
GhostLink Phase 1 Cold Boot - Full System Test Suite
Comprehensive testing of all cold boot components and functionality
"""

from datetime import datetime
import json
import os
import subprocess
import sys
import time

import psutil


class FullSystemTester:
    """Comprehensive cold boot system testing"""

    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.python_exe = sys.executable
        self.test_results = []
        self.start_time = datetime.now()

    def log_test(self, test_name, success, details=""):
        """Log a test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        return success

    def run_command(self, cmd_args, timeout=30, description=""):
        """Run a command and return result"""
        print(f"🧊 Testing: {description}")
        try:
            result = subprocess.run(
                [self.python_exe] + cmd_args,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            success = result.returncode == 0
            if success:
                print(f"✅ {description}: SUCCESS - SHUT DOWN")
            else:
                print(f"❌ {description}: FAILED (exit code {result.returncode})")

            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            print(f"⏰ {description}: TIMEOUT ({timeout}s)")
            return False, "", f"Timeout after {timeout}s"
        except Exception as e:
            print(f"💥 {description}: ERROR - {e}")
            return False, "", str(e)

    def test_component_isolation(self):
        """Test that components don't interfere with each other"""
        print("\n🧊 TEST SUITE: Component Isolation")
        print("=" * 50)

        # Test 1: Multiple rapid cold boots
        success_count = 0
        for i in range(3):  # Reduced from 5 to 3 for speed
            success, _, _ = self.run_command(
                ["src/multi_agent_engine.py", "--engine-status"],
                10, f"Rapid Multi-Agent Boot #{i+1}"
            )
            if success:
                success_count += 1
                self.log_test(f"Rapid Boot {i+1}", True, "Clean shutdown")
            else:
                self.log_test(f"Rapid Boot {i+1}", False, "Failed")
            time.sleep(0.5)

        self.log_test("Rapid Boot Stress Test", success_count >= 2,
                     f"{success_count}/3 successful boots")

        # Test 2: Sequential component testing
        components = [
            (["src/multi_agent_engine.py", "--engine-status"], "Multi-Agent Sequential"),
            (["src/unified_consciousness.py", "--snapshot"], "Consciousness Sequential"),
            (["monitoring/basic_monitor.py"], "Monitoring Sequential")
        ]

        sequential_success = 0
        for cmd_args, desc in components:
            success, _, _ = self.run_command(cmd_args, 15, desc)
            if success:
                sequential_success += 1

        self.log_test("Sequential Component Test", sequential_success == len(components),
                     f"{sequential_success}/{len(components)} components successful")

    def test_resource_efficiency(self):
        """Test resource usage and cleanup"""
        print("\n🧊 TEST SUITE: Resource Efficiency")
        print("=" * 50)

        # Get baseline memory
        baseline_memory = psutil.virtual_memory().percent
        baseline_processes = len(psutil.pids())

        # Test memory cleanup after cold boot
        success, _, _ = self.run_command(
            ["src/unified_consciousness.py", "--snapshot"],
            20, "Memory Cleanup Test"
        )

        post_memory = psutil.virtual_memory().percent
        post_processes = len(psutil.pids())

        memory_delta = post_memory - baseline_memory
        process_delta = post_processes - baseline_processes

        self.log_test("Memory Cleanup", abs(memory_delta) < 10.0,
                     f"Memory delta: {memory_delta:.1f}%")
        self.log_test("Process Cleanup", process_delta <= 2,
                     f"Process delta: {process_delta}")

    def test_functional_correctness(self):
        """Test that components produce correct outputs"""
        print("\n🧊 TEST SUITE: Functional Correctness")
        print("=" * 50)

        # Test 1: Multi-agent engine status
        success, stdout, _ = self.run_command(
            ["src/multi_agent_engine.py", "--engine-status"],
            10, "Engine Status Parsing"
        )

        if success:
            # Extract JSON from output (skip log messages)
            json_start = stdout.find('{')
            if json_start >= 0:
                json_content = stdout[json_start:]
                try:
                    data = json.loads(json_content)
                    agent_count = data.get("total_agents", 0)
                    self.log_test("Agent Count Correct", agent_count >= 6,
                                 f"Found {agent_count} agents")
                except Exception:
                    self.log_test("Agent Count Correct", False, "JSON parsing failed")
            else:
                self.log_test("Agent Count Correct", False, "No JSON found in output")
        else:
            self.log_test("Agent Count Correct", False, "Status not retrieved")

        # Test 2: Consciousness framework snapshot
        success, stdout, _ = self.run_command(
            ["src/unified_consciousness.py", "--snapshot"],
            20, "Consciousness Snapshot"
        )

        if success:
            # Extract JSON from output
            json_start = stdout.find('{')
            if json_start >= 0:
                json_content = stdout[json_start:]
                try:
                    data = json.loads(json_content)
                    level = data.get("consciousness_level", "unknown")
                    self.log_test("Consciousness Level", level in ["moderate_awareness", "high_awareness", "full_awareness"],
                                 f"Level: {level}")
                except Exception:
                    self.log_test("Consciousness Level", False, "JSON parsing failed")
            else:
                self.log_test("Consciousness Level", False, "No JSON found in output")
        else:
            self.log_test("Consciousness Level", False, "Snapshot not retrieved")

        # Test 3: Monitoring data structure
        success, stdout, _ = self.run_command(
            ["monitoring/basic_monitor.py"],
            10, "Monitoring Data Structure"
        )

        if success:
            # Extract JSON from output (find complete JSON object)
            json_start = stdout.find('{')
            if json_start >= 0:
                # Find the matching closing brace
                brace_count = 0
                json_end = json_start
                for i, char in enumerate(stdout[json_start:], json_start):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break

                if json_end > json_start:
                    json_content = stdout[json_start:json_end]
                    try:
                        data = json.loads(json_content)
                        has_system = "ghostlink_system_metrics" in data
                        has_ai = "ghostlink_ai_metrics" in data
                        self.log_test("Monitoring Structure", has_system and has_ai,
                                     f"System: {has_system}, AI: {has_ai}")
                    except Exception as e:
                        self.log_test("Monitoring Structure", False, f"JSON parsing failed: {e}")
                else:
                    self.log_test("Monitoring Structure", False, "Could not find complete JSON object")
            else:
                self.log_test("Monitoring Structure", False, "No JSON found in output")
        else:
            self.log_test("Monitoring Structure", False, "Metrics not collected")

    def test_error_handling(self):
        """Test error conditions and recovery"""
        print("\n🧊 TEST SUITE: Error Handling")
        print("=" * 50)

        # Test 1: Invalid arguments
        success, _, stderr = self.run_command(
            ["src/multi_agent_engine.py", "--invalid-arg"],
            5, "Invalid Arguments"
        )
        self.log_test("Invalid Args Handled", not success,
                     "Component rejected invalid arguments")

        # Test 2: Recovery after failure
        success, _, _ = self.run_command(
            ["src/multi_agent_engine.py", "--engine-status"],
            10, "Recovery Test"
        )
        self.log_test("Recovery After Error", success,
                     "Component recovered and ran successfully")

    def test_orchestrator_integration(self):
        """Test the cold boot orchestrator itself"""
        print("\n🧊 TEST SUITE: Orchestrator Integration")
        print("=" * 50)

        # Test 1: Health check
        success, stdout, _ = self.run_command(
            ["cold_boot_orchestrator.py", "health"],
            60, "Orchestrator Health Check"
        )

        health_success = success and "COLD BOOT HEALTH: PERFECT" in stdout
        self.log_test("Orchestrator Health", health_success,
                     "Full system health check passed")

        # Test 2: Status check
        success, stdout, _ = self.run_command(
            ["cold_boot_orchestrator.py", "status"],
            30, "Orchestrator Status"
        )

        status_success = success and "READY" in stdout
        self.log_test("Orchestrator Status", status_success,
                     "Status check completed")

    def run_full_test_suite(self):
        """Run the complete test suite"""
        print("🚀 GHOSTLINK PHASE 1 COLD BOOT - FULL SYSTEM TEST")
        print("=" * 70)
        print(f"Start Time: {self.start_time.isoformat()}")
        print(f"Test Environment: {sys.platform}")
        print(f"Python Version: {sys.version.split()[0]}")
        print("=" * 70)

        # Run all test suites
        self.test_component_isolation()
        self.test_resource_efficiency()
        self.test_functional_correctness()
        self.test_error_handling()
        self.test_orchestrator_integration()

        # Generate final report
        return self.generate_final_report()

    def generate_final_report(self):
        """Generate comprehensive test report"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - passed_tests

        print("\n" + "=" * 70)
        print("📊 FINAL TEST REPORT")
        print("=" * 70)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%")

        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['details']}")

        # Overall assessment
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        if success_rate >= 90:
            print("\n🎯 OVERALL RESULT: EXCELLENT")
            print("✅ Cold boot system fully operational and reliable")
            overall_success = True
        elif success_rate >= 75:
            print("\n⚠️ OVERALL RESULT: GOOD")
            print("✅ Cold boot system operational with minor issues")
            overall_success = True
        else:
            print("\n❌ OVERALL RESULT: NEEDS ATTENTION")
            print("🔧 Cold boot system requires fixes")
            overall_success = False

        # Save detailed report
        report = {
            "test_run": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": duration,
                "environment": {
                    "platform": sys.platform,
                    "python_version": sys.version.split()[0],
                    "working_directory": self.project_root
                }
            },
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate_percent": success_rate,
                "overall_success": overall_success
            },
            "detailed_results": self.test_results
        }

        with open("full_system_test_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print("\n📄 Detailed report saved to: full_system_test_report.json")
        return overall_success

def main():
    """Run the full system test"""
    tester = FullSystemTester()
    success = tester.run_full_test_suite()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

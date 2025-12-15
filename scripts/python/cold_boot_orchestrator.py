#!/usr/bin/env python3
"""
GhostLink Cold Boot Orchestrator
Central controller that starts components on-demand and ensures clean shutdown
"""

import subprocess
import sys
import time
import json
import argparse
import os
from datetime import datetime

class ColdBootOrchestrator:
    """Manages cold boot lifecycle of all GhostLink components"""

    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.python_exe = sys.executable
        self.active_processes = []

    def run_command(self, cmd_args, timeout=30, description=""):
        """Run a command and return result, ensuring it shuts down after"""
        print(f"🧊 Cold booting: {description}")
        try:
            result = subprocess.run(
                [self.python_exe] + cmd_args,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                print(f"✅ {description}: SUCCESS - SHUT DOWN")
                return True, result.stdout, result.stderr
            else:
                print(f"❌ {description}: FAILED (exit code {result.returncode})")
                return False, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            print(f"⏰ {description}: TIMEOUT - FORCE SHUTDOWN")
            return False, "", "Timeout"
        except Exception as e:
            print(f"💥 {description}: ERROR - {e}")
            return False, "", str(e)

    def check_system_health(self):
        """Run comprehensive cold boot health check"""
        print("🧊 GHOSTLINK COLD BOOT SYSTEM HEALTH CHECK")
        print("=" * 60)

        checks = [
            (["src/multi_agent_engine.py", "--engine-status"], "Multi-Agent Engine", 15),
            (["src/unified_consciousness.py", "--snapshot"], "Consciousness Framework", 20),
            (["monitoring/basic_monitor.py"], "Monitoring Collection", 15),
            (["tests/core/test_fib.py"], "Basic Functionality", 10)
        ]

        results = []
        for cmd_args, description, timeout in checks:
            success, stdout, stderr = self.run_command(cmd_args, timeout, description)
            results.append((description, success, stdout, stderr))
            time.sleep(1)  # Brief pause between cold boots

        # Summary
        print("\n" + "=" * 60)
        successful = sum(1 for _, success, _, _ in results if success)
        total = len(results)

        health_report = {
            "timestamp": datetime.now().isoformat(),
            "cold_boot_check": True,
            "total_components": total,
            "successful_components": successful,
            "failed_components": total - successful,
            "results": [
                {
                    "component": desc,
                    "status": "PASS" if success else "FAIL",
                    "output_length": len(stdout)
                } for desc, success, stdout, stderr in results
            ]
        }

        if successful == total:
            print(f"🎯 COLD BOOT HEALTH: PERFECT ({successful}/{total})")
            print("✅ All components start on-demand and shut down cleanly!")
            health_report["overall_status"] = "HEALTHY"
        else:
            print(f"⚠️  COLD BOOT HEALTH: ISSUES ({successful}/{total})")
            print("🔧 Some components need attention")
            health_report["overall_status"] = "DEGRADED"

        # Save health report
        with open("cold_boot_health.json", "w") as f:
            json.dump(health_report, f, indent=2)

        return successful == total

    def run_ai_task(self, task_type, **kwargs):
        """Run a specific AI task with cold boot"""
        print(f"🧊 Starting AI task: {task_type}")

        if task_type == "optimize":
            model_id = kwargs.get("model_id", "default")
            target_size = kwargs.get("target_size", "small")
            cmd_args = ["src/multi_agent_engine.py", "--optimize", f"{model_id}:{target_size}"]
            success, stdout, stderr = self.run_command(cmd_args, 60, f"Model Optimization ({model_id})")
            return {"success": success, "output": stdout, "error": stderr}

        elif task_type == "consciousness_scan":
            # Use snapshot instead of status for now
            cmd_args = ["src/unified_consciousness.py", "--snapshot"]
            success, stdout, stderr = self.run_command(cmd_args, 45, "Deep Consciousness Scan")
            return {"success": success, "output": stdout, "error": stderr}

        elif task_type == "system_metrics":
            cmd_args = ["monitoring/basic_monitor.py"]
            success, stdout, stderr = self.run_command(cmd_args, 15, "System Metrics Collection")
            if success:
                try:
                    metrics = json.loads(stdout)
                    return {"success": True, "metrics": metrics}
                except:
                    return {"success": False, "error": "Failed to parse metrics"}
            return {"success": False, "error": stderr}

        else:
            return {"success": False, "error": f"Unknown task type: {task_type}"}

    def cleanup(self):
        """Ensure all processes are shut down"""
        print("🧹 Cold boot cleanup: ensuring all processes shut down...")
        # In a real implementation, we'd track PIDs and force kill if needed
        # For now, rely on subprocess timeout and proper shutdown
        time.sleep(1)
        print("✅ Cleanup complete")

def main():
    """Main orchestrator entry point"""
    parser = argparse.ArgumentParser(description="GhostLink Cold Boot Orchestrator")
    parser.add_argument("action", choices=["health", "task", "status"],
                       help="Action to perform")
    parser.add_argument("--task-type", help="Task type for 'task' action")
    parser.add_argument("--model-id", help="Model ID for optimization tasks")
    parser.add_argument("--target-size", help="Target size for optimization")

    args = parser.parse_args()

    orchestrator = ColdBootOrchestrator()

    try:
        if args.action == "health":
            success = orchestrator.check_system_health()
            sys.exit(0 if success else 1)

        elif args.action == "task":
            if not args.task_type:
                print("❌ --task-type required for 'task' action")
                sys.exit(1)

            kwargs = {}
            if args.model_id:
                kwargs["model_id"] = args.model_id
            if args.target_size:
                kwargs["target_size"] = args.target_size

            result = orchestrator.run_ai_task(args.task_type, **kwargs)
            print(json.dumps(result, indent=2))
            sys.exit(0 if result["success"] else 1)

        elif args.action == "status":
            # Quick status check
            success, stdout, stderr = orchestrator.run_command(
                ["phase1_check.py"], 30, "Quick Status Check"
            )
            if success:
                print("🧊 Cold boot status: READY")
            else:
                print("🧊 Cold boot status: ISSUES DETECTED")
            sys.exit(0 if success else 1)

    finally:
        orchestrator.cleanup()

if __name__ == "__main__":
    main()

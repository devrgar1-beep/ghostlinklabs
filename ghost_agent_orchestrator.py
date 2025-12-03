#!/usr/bin/env python3
"""
Ghost Agent - Master Orchestrator Integration
Real-time interface between VS Code and GhostLink AI ecosystem
"""

import subprocess
import json
import sys
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional

class GhostAgentOrchestrator:
    """Master orchestrator interface for VS Code Ghost agent"""

    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.python_exe = sys.executable
        self.last_health_check = None
        self.system_status = {}

    def execute_cold_boot_command(self, command: str, *args, timeout: int = 30) -> Dict[str, Any]:
        """Execute a command through the cold boot orchestrator"""
        try:
            cmd_args = [self.python_exe, "cold_boot_orchestrator.py", command] + list(args)
            result = subprocess.run(
                cmd_args,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "command": " ".join(cmd_args)
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out",
                "timeout": timeout
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health status"""
        result = self.execute_cold_boot_command("health", timeout=60)

        if result["success"]:
            # Parse health check output for structured data
            health_data = {
                "timestamp": datetime.now().isoformat(),
                "overall_status": "healthy" if "PERFECT" in result["stdout"] else "degraded",
                "components_checked": 4,  # Multi-agent, consciousness, monitoring, basic
                "last_check": datetime.now().isoformat()
            }

            # Extract component status from output
            if "Multi-Agent Engine: SUCCESS" in result["stdout"]:
                health_data["multi_agent_engine"] = "operational"
            if "Consciousness Framework: SUCCESS" in result["stdout"]:
                health_data["consciousness_framework"] = "operational"
            if "Monitoring Collection: SUCCESS" in result["stdout"]:
                health_data["monitoring"] = "operational"

            self.last_health_check = health_data
            return health_data
        else:
            return {
                "overall_status": "unhealthy",
                "error": result.get("error", "Health check failed"),
                "timestamp": datetime.now().isoformat()
            }

    def execute_ai_task(self, task_type: str, **kwargs) -> Dict[str, Any]:
        """Execute an AI task through the orchestrator"""
        args = ["--task-type", task_type]

        if task_type == "optimize" and "model_id" in kwargs:
            args.extend(["--model-id", kwargs["model_id"]])
            if "target_size" in kwargs:
                args.extend(["--target-size", kwargs["target_size"]])

        result = self.execute_cold_boot_command("task", *args, timeout=120)

        if result["success"]:
            try:
                # Try to parse JSON response
                task_output = json.loads(result["stdout"])
                return task_output
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "output": result["stdout"],
                    "task_type": task_type
                }
        else:
            return {
                "success": False,
                "error": result.get("stderr", "Task execution failed"),
                "task_type": task_type
            }

    def get_component_status(self, component: str) -> Dict[str, Any]:
        """Get status of a specific component"""
        component_commands = {
            "multi_agent": ["src/multi_agent_engine.py", "--engine-status"],
            "consciousness": ["src/unified_consciousness.py", "--snapshot"],
            "monitoring": ["monitoring/basic_monitor.py"]
        }

        if component not in component_commands:
            return {"error": f"Unknown component: {component}"}

        try:
            result = subprocess.run(
                [self.python_exe] + component_commands[component],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=15
            )

            return {
                "component": component,
                "status": "operational" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "component": component,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def run_system_demo(self) -> Dict[str, Any]:
        """Run the full system demo"""
        try:
            result = subprocess.run(
                ["./full_system_demo.sh"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )

            return {
                "success": result.returncode == 0,
                "demo_output": result.stdout,
                "demo_errors": result.stderr,
                "duration": "completed",
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Demo timed out after 5 minutes",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics"""
        return self.execute_ai_task("system_metrics")

    def analyze_consciousness(self) -> Dict[str, Any]:
        """Analyze current consciousness state"""
        return self.execute_ai_task("consciousness_scan")

def main():
    """Command-line interface for Ghost agent orchestration"""
    if len(sys.argv) < 2:
        print("Usage: python3 ghost_agent_orchestrator.py <command> [args...]")
        print("Commands: health, status, task, component, demo, metrics, consciousness")
        sys.exit(1)

    orchestrator = GhostAgentOrchestrator()
    command = sys.argv[1]

    try:
        if command == "health":
            result = orchestrator.get_system_health()
            print(json.dumps(result, indent=2))

        elif command == "status":
            result = orchestrator.execute_cold_boot_command("status")
            print(json.dumps(result, indent=2))

        elif command == "task":
            if len(sys.argv) < 3:
                print("Usage: python3 ghost_agent_orchestrator.py task <task_type> [kwargs...]")
                sys.exit(1)
            task_type = sys.argv[2]
            kwargs = {}
            if len(sys.argv) > 3:
                # Parse additional arguments as key=value pairs
                for arg in sys.argv[3:]:
                    if "=" in arg:
                        key, value = arg.split("=", 1)
                        kwargs[key] = value
            result = orchestrator.execute_ai_task(task_type, **kwargs)
            print(json.dumps(result, indent=2))

        elif command == "component":
            if len(sys.argv) < 3:
                print("Usage: python3 ghost_agent_orchestrator.py component <component_name>")
                print("Components: multi_agent, consciousness, monitoring")
                sys.exit(1)
            component = sys.argv[2]
            result = orchestrator.get_component_status(component)
            print(json.dumps(result, indent=2))

        elif command == "demo":
            print("Running full system demo... This may take a few minutes.")
            result = orchestrator.run_system_demo()
            print(json.dumps(result, indent=2))

        elif command == "metrics":
            result = orchestrator.get_system_metrics()
            print(json.dumps(result, indent=2))

        elif command == "consciousness":
            result = orchestrator.analyze_consciousness()
            print(json.dumps(result, indent=2))

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

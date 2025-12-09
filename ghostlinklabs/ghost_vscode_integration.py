#!/usr/bin/env python3
"""
GhostLink VS Code Integration
Links the Ghost Agent (Brain of AI) with VS Code HTTP API
"""

import requests
import json
import subprocess
import sys
import os
import time
from typing import Dict, Any, Optional, List

class GhostVSCodeIntegration:
    """Integration between Ghost Agent and VS Code HTTP API"""

    def __init__(self, vscode_api_url: str = "http://localhost:3000"):
        self.vscode_api_url = vscode_api_url
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.python_exe = sys.executable
        self.session_id = None

    def check_vscode_api(self) -> bool:
        """Check if VS Code HTTP API is running"""
        try:
            response = requests.get(f"{self.vscode_api_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def start_vscode_api(self) -> bool:
        """Attempt to start VS Code HTTP API"""
        try:
            # This would require VS Code to be running with the extension
            # For now, we'll assume it's started manually
            print("VS Code HTTP API should be started manually via VS Code command palette")
            print("Run: 'VSCode HTTP API: Start' in VS Code")
            return False
        except Exception as e:
            print(f"Failed to start VS Code API: {e}")
            return False

    def execute_vscode_command(self, command: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a command through VS Code HTTP API"""
        if not self.check_vscode_api():
            return {"error": "VS Code HTTP API not available"}

        try:
            payload = {"command": command}
            if params:
                payload.update(params)

            response = requests.post(
                f"{self.vscode_api_url}/command",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"VS Code API error: {response.status_code}", "response": response.text}
        except Exception as e:
            return {"error": str(e)}

    def open_file_in_vscode(self, file_path: str, line: int = None, column: int = None) -> Dict[str, Any]:
        """Open a file in VS Code"""
        params = {"file": os.path.abspath(file_path)}
        if line is not None:
            params["line"] = line
        if column is not None:
            params["column"] = column

        return self.execute_vscode_command("openFile", params)

    def edit_file_in_vscode(self, file_path: str, edits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Edit a file through VS Code"""
        params = {
            "file": os.path.abspath(file_path),
            "edits": edits
        }
        return self.execute_vscode_command("editFile", params)

    def run_terminal_command_in_vscode(self, command: str, cwd: str = None) -> Dict[str, Any]:
        """Run a terminal command through VS Code"""
        params = {"command": command}
        if cwd:
            params["cwd"] = os.path.abspath(cwd)

        return self.execute_vscode_command("runTerminalCommand", params)

    def git_commit_in_vscode(self, message: str, files: List[str] = None) -> Dict[str, Any]:
        """Commit changes through VS Code"""
        params = {"message": message}
        if files:
            params["files"] = [os.path.abspath(f) for f in files]

        return self.execute_vscode_command("gitCommit", params)

    # GhostLink System Integration Methods

    def execute_ghost_command(self, command: str, *args) -> Dict[str, Any]:
        """Execute a Ghost agent orchestrator command"""
        try:
            cmd_args = [self.python_exe, "ghost_agent_orchestrator.py", command] + list(args)
            result = subprocess.run(
                cmd_args,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "command": " ".join(cmd_args)
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status for VS Code display"""
        # Get health from Ghost system
        health_result = self.execute_ghost_command("health")

        # Get VS Code API status
        vscode_status = self.check_vscode_api()

        status = {
            "timestamp": time.time(),
            "ghostlink_system": {
                "healthy": health_result.get("success", False),
                "last_check": time.time()
            },
            "vscode_integration": {
                "api_available": vscode_status,
                "api_url": self.vscode_api_url
            }
        }

        return status

    def orchestrate_ai_task(self, task_type: str, show_in_vscode: bool = True) -> Dict[str, Any]:
        """Orchestrate an AI task and optionally display results in VS Code"""
        # Execute the AI task
        result = self.execute_ghost_command("task", f"--task-type={task_type}")

        if show_in_vscode and self.check_vscode_api():
            # Create a temporary file with results and open it in VS Code
            result_file = f"/tmp/ghostlink_{task_type}_{int(time.time())}.json"
            with open(result_file, 'w') as f:
                json.dump(result, f, indent=2)

            self.open_file_in_vscode(result_file)

        return result

    def show_system_health_in_vscode(self) -> Dict[str, Any]:
        """Display system health in VS Code"""
        health_data = self.get_system_status()

        # Create health report file
        health_file = f"/tmp/ghostlink_health_{int(time.time())}.md"

        with open(health_file, 'w') as f:
            f.write("# GhostLink System Health Report\n\n")
            f.write(f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(health_data['timestamp']))}\n\n")

            f.write("## GhostLink AI System\n")
            f.write(f"- **Status:** {'✅ Healthy' if health_data['ghostlink_system']['healthy'] else '❌ Issues'}\n")
            f.write(f"- **Last Check:** {time.strftime('%H:%M:%S', time.localtime(health_data['ghostlink_system']['last_check']))}\n\n")

            f.write("## VS Code Integration\n")
            f.write(f"- **API Available:** {'✅ Yes' if health_data['vscode_integration']['api_available'] else '❌ No'}\n")
            f.write(f"- **API URL:** {health_data['vscode_integration']['api_url']}\n\n")

            if health_data['ghostlink_system']['healthy']:
                f.write("## Quick Actions\n\n")
                f.write("```bash\n")
                f.write("# Run consciousness analysis\n")
                f.write("python3 ghost_agent_orchestrator.py consciousness\n\n")
                f.write("# Check multi-agent status\n")
                f.write("python3 ghost_agent_orchestrator.py component multi_agent\n\n")
                f.write("# Deploy infrastructure\n")
                f.write("./deploy/deploy.sh development core\n")
                f.write("```\n")

        if self.check_vscode_api():
            self.open_file_in_vscode(health_file)

        return {"health_file": health_file, "opened_in_vscode": self.check_vscode_api()}

def main():
    """Command-line interface for Ghost VS Code integration"""
    if len(sys.argv) < 2:
        print("Usage: python3 ghost_vscode_integration.py <command> [args...]")
        print("Commands: status, health, task, open, edit, terminal, git")
        sys.exit(1)

    integration = GhostVSCodeIntegration()

    command = sys.argv[1]

    try:
        if command == "status":
            result = integration.get_system_status()
            print(json.dumps(result, indent=2))

        elif command == "health":
            result = integration.show_system_health_in_vscode()
            print(json.dumps(result, indent=2))

        elif command == "task":
            if len(sys.argv) < 3:
                print("Usage: python3 ghost_vscode_integration.py task <task_type>")
                sys.exit(1)
            task_type = sys.argv[2]
            result = integration.orchestrate_ai_task(task_type)
            print(json.dumps(result, indent=2))

        elif command == "open":
            if len(sys.argv) < 3:
                print("Usage: python3 ghost_vscode_integration.py open <file_path>")
                sys.exit(1)
            file_path = sys.argv[2]
            result = integration.open_file_in_vscode(file_path)
            print(json.dumps(result, indent=2))

        elif command == "edit":
            if len(sys.argv) < 4:
                print("Usage: python3 ghost_vscode_integration.py edit <file_path> <old_string> <new_string>")
                sys.exit(1)
            file_path = sys.argv[2]
            old_string = sys.argv[3]
            new_string = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
            edits = [{"oldString": old_string, "newString": new_string}]
            result = integration.edit_file_in_vscode(file_path, edits)
            print(json.dumps(result, indent=2))

        elif command == "terminal":
            if len(sys.argv) < 3:
                print("Usage: python3 ghost_vscode_integration.py terminal <command>")
                sys.exit(1)
            cmd = " ".join(sys.argv[2:])
            result = integration.run_terminal_command_in_vscode(cmd)
            print(json.dumps(result, indent=2))

        elif command == "git":
            if len(sys.argv) < 3:
                print("Usage: python3 ghost_vscode_integration.py git <commit_message>")
                sys.exit(1)
            message = " ".join(sys.argv[2:])
            result = integration.git_commit_in_vscode(message)
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

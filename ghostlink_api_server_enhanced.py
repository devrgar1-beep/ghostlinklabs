#!/usr/bin/env python3
"""
Enhanced GhostLink API Server with YOLO Mode Support
Provides HTTP endpoints for VS Code integration with full experimental autonomy
"""

import http.server
import json
import os
import socketserver
import subprocess
import sys
import threading
import time
from urllib.parse import urlparse


class EnhancedGhostLinkAPIHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, project_root=None, **kwargs):
        self.project_root = project_root or os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests with enhanced endpoints"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "Enhanced GhostLink VS Code API",
                "yolo_mode": True,
                "experimental_mode": True,
                "auto_approve": True,
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(response).encode())

        elif path == "/status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "vscode_api": "running",
                "ghostlink_integration": "active",
                "enhanced_features": ["yolo_mode", "experimental", "auto_approve", "scheduling", "auditing"],
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(response).encode())

        elif path == "/system-health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = self.get_enhanced_system_health()
            self.wfile.write(json.dumps(response).encode())

        elif path == "/scheduler-status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = self.get_scheduler_status()
            self.wfile.write(json.dumps(response).encode())

        elif path == "/audit-status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = self.get_audit_status()
            self.wfile.write(json.dumps(response).encode())

        elif path == "/test-status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = self.get_testing_status()
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handle POST requests with enhanced functionality"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/command":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            command = data.get('command', '')
            params = data.get('params', {})

            # Execute the command with enhanced processing
            result = self.execute_enhanced_command(command, params)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        elif path == "/experimental-task":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            task_type = data.get('task_type', 'consciousness')
            params = data.get('params', {})

            result = self.execute_experimental_task(task_type, params)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        elif path == "/yolo-task":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            task_type = data.get('task_type', 'chaos_test')
            params = data.get('params', {})

            result = self.execute_yolo_task(task_type, params)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        elif path == "/schedule-task":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            task_type = data.get('task_type', 'health_check')
            priority = data.get('priority', 'medium')

            result = self.schedule_autonomous_task(task_type, priority)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        elif path == "/sync-protocols":
            result = self.sync_all_protocols()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        elif path == "/run-audit":
            result = self.run_system_audit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        elif path == "/run-tests":
            suite = data.get('suite', 'full') if 'data' in locals() and data else 'full'
            result = self.run_automated_tests(suite)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())

    def execute_enhanced_command(self, command, params):
        """Execute command with enhanced processing"""
        try:
            # Use enhanced orchestrator
            if command == "health":
                result = subprocess.run(
                    [sys.executable, "ghost_agent_orchestrator_enhanced.py", "health"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                    "enhanced": True,
                    "yolo_mode": True
                }

            elif command == "status":
                result = subprocess.run(
                    [sys.executable, "ghost_vscode_integration.py", "status"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                    "enhanced": True
                }

            elif command == "task":
                task_type = params.get('task_type', 'consciousness')
                result = subprocess.run(
                    [sys.executable, "ghost_agent_orchestrator_enhanced.py", "task", f"--task-type={task_type}"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                    "task_type": task_type,
                    "enhanced": True
                }

            else:
                return {"error": f"Unknown command: {command}"}

        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": str(e)}

    def execute_experimental_task(self, task_type, params):
        """Execute experimental task"""
        try:
            result = subprocess.run(
                [sys.executable, "ghost_agent_orchestrator_enhanced.py", "experimental-task", task_type],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120
            )

            response = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "task_type": task_type,
                "experimental": True,
                "risk_level": "high"
            }

            # Parse JSON output if available
            try:
                if result.stdout.strip():
                    parsed_output = json.loads(result.stdout)
                    response.update(parsed_output)
            except json.JSONDecodeError:
                pass

            return response

        except Exception as e:
            return {"success": False, "error": str(e), "experimental": True}

    def execute_yolo_task(self, task_type, params):
        """Execute YOLO task"""
        try:
            result = subprocess.run(
                [sys.executable, "ghost_agent_orchestrator_enhanced.py", "yolo-task", task_type],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=180  # Longer timeout for YOLO tasks
            )

            response = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "task_type": task_type,
                "yolo_mode": True,
                "risk_level": "maximum",
                "learning_experience": True
            }

            # Parse JSON output if available
            try:
                if result.stdout.strip():
                    parsed_output = json.loads(result.stdout)
                    response.update(parsed_output)
            except json.JSONDecodeError:
                pass

            return response

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "yolo_mode": True,
                "learning_experience": True,
                "yolo_insight": f"Exception transformed into learning: {str(e)}"
            }

    def schedule_autonomous_task(self, task_type, priority):
        """Schedule autonomous task"""
        try:
            result = subprocess.run(
                [sys.executable, "ghost_agent_orchestrator_enhanced.py", "auto-schedule", task_type, priority],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )

            response = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "task_type": task_type,
                "priority": priority,
                "autonomous": True
            }

            # Parse JSON output if available
            try:
                if result.stdout.strip():
                    parsed_output = json.loads(result.stdout)
                    response.update(parsed_output)
            except json.JSONDecodeError:
                pass

            return response

        except Exception as e:
            return {"success": False, "error": str(e), "autonomous": True}

    def sync_all_protocols(self):
        """Sync all protocols"""
        try:
            result = subprocess.run(
                [sys.executable, "ghost_agent_orchestrator_enhanced.py", "sync-protocols"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )

            response = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "operation": "protocol_sync"
            }

            # Parse JSON output if available
            try:
                if result.stdout.strip():
                    parsed_output = json.loads(result.stdout)
                    response.update(parsed_output)
            except json.JSONDecodeError:
                pass

            return response

        except Exception as e:
            return {"success": False, "error": str(e), "operation": "protocol_sync"}

    def run_system_audit(self):
        """Run system audit"""
        try:
            result = subprocess.run(
                [sys.executable, "ghost_agent_orchestrator_enhanced.py", "audit"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120
            )

            response = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "audit_type": "comprehensive"
            }

            # Parse JSON output if available
            try:
                if result.stdout.strip():
                    parsed_output = json.loads(result.stdout)
                    response.update(parsed_output)
            except json.JSONDecodeError:
                pass

            return response

        except Exception as e:
            return {"success": False, "error": str(e), "audit_type": "comprehensive"}

    def run_automated_tests(self, suite):
        """Run automated tests"""
        try:
            result = subprocess.run(
                [sys.executable, "ghostlink_auto_tester.py", "run-tests", "--suite", suite],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )

            response = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "test_suite": suite,
                "automated": True
            }

            # Parse JSON output if available
            try:
                if result.stdout.strip():
                    parsed_output = json.loads(result.stdout)
                    response.update(parsed_output)
            except json.JSONDecodeError:
                pass

            return response

        except Exception as e:
            return {"success": False, "error": str(e), "test_suite": suite, "automated": True}

    def get_enhanced_system_health(self):
        """Get enhanced system health"""
        try:
            result = subprocess.run(
                [sys.executable, "ghost_agent_orchestrator_enhanced.py", "health"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0 and result.stdout.strip():
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    pass

            return {
                "status": "enhanced_health_check",
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "timestamp": time.time()
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "timestamp": time.time()}

    def get_scheduler_status(self):
        """Get scheduler status"""
        try:
            result = subprocess.run(
                [sys.executable, "ghostlink_scheduler.py", "status"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0 and result.stdout.strip():
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    pass

            return {
                "scheduler_status": "unknown",
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }

        except Exception as e:
            return {"scheduler_status": "error", "error": str(e)}

    def get_audit_status(self):
        """Get audit status"""
        try:
            result = subprocess.run(
                [sys.executable, "ghostlink_auto_tester.py", "status"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0 and result.stdout.strip():
                try:
                    status_data = json.loads(result.stdout)
                    return {
                        "audit_status": "active",
                        "details": status_data
                    }
                except json.JSONDecodeError:
                    pass

            return {
                "audit_status": "unknown",
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }

        except Exception as e:
            return {"audit_status": "error", "error": str(e)}

    def get_testing_status(self):
        """Get testing status"""
        try:
            result = subprocess.run(
                [sys.executable, "ghostlink_auto_tester.py", "status"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0 and result.stdout.strip():
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    pass

            return {
                "testing_status": "unknown",
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }

        except Exception as e:
            return {"testing_status": "error", "error": str(e)}

    def log_message(self, format, *args):
        """Override to reduce noise"""
        pass

class EnhancedGhostLinkAPIServer:
    def __init__(self, port=3000, project_root=None):
        self.port = port
        self.project_root = project_root
        self.server = None
        self.thread = None

    def start(self):
        """Start the enhanced HTTP API server"""
        def run_server():
            with socketserver.TCPServer(("", self.port), lambda *args: EnhancedGhostLinkAPIHandler(*args, project_root=self.project_root)) as httpd:
                self.server = httpd
                print(f"🚀 Enhanced GhostLink API Server running on port {self.port}")
                print("🎲 YOLO Mode: ACTIVE | 🧪 Experimental Mode: ACTIVE | ✅ Auto-approve: ENABLED")
                httpd.serve_forever()

        self.thread = threading.Thread(target=run_server, daemon=True)
        self.thread.start()
        time.sleep(1)  # Give server time to start

    def stop(self):
        """Stop the HTTP API server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join(timeout=5)

def main():
    """Main function to run the enhanced API server"""
    import argparse

    parser = argparse.ArgumentParser(description='Enhanced GhostLink VS Code API Server')
    parser.add_argument('--port', type=int, default=3000, help='Port to run server on')
    parser.add_argument('--project-root', help='Path to GhostLink project root')

    args = parser.parse_args()

    project_root = args.project_root or os.path.dirname(os.path.abspath(__file__))

    print("🧠 Starting Enhanced GhostLink VS Code API Server...")
    print(f"📁 Project Root: {project_root}")
    print(f"🌐 Port: {args.port}")
    print("🎯 Features: YOLO Mode, Experimental Tasks, Auto-scheduling, Auditing, Testing")

    server = EnhancedGhostLinkAPIServer(port=args.port, project_root=project_root)
    server.start()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Enhanced GhostLink API Server...")
        server.stop()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()

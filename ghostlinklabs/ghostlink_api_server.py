#!/usr/bin/env python3
"""
Simple HTTP API Server for VS Code Integration
Provides basic HTTP endpoints for testing GhostLink integration
"""

import http.server
import socketserver
import json
import threading
import time
import subprocess
import sys
import os
from urllib.parse import urlparse, parse_qs

class GhostLinkAPIHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, project_root=None, **kwargs):
        self.project_root = project_root or os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "healthy", "service": "GhostLink VS Code API"}
            self.wfile.write(json.dumps(response).encode())

        elif path == "/status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "vscode_api": "running",
                "ghostlink_integration": "active",
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/command":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            command = data.get('command', '')
            params = data.get('params', {})

            # Execute the command
            result = self.execute_ghost_command(command, params)

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

    def execute_ghost_command(self, command, params):
        """Execute a GhostLink command"""
        try:
            # Map commands to actual scripts
            if command == "health":
                result = subprocess.run(
                    [sys.executable, "ghost_agent_orchestrator.py", "health"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr
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
                    "error": result.stderr
                }

            elif command == "task":
                task_type = params.get('task_type', 'consciousness')
                result = subprocess.run(
                    [sys.executable, "ghost_agent_orchestrator.py", "task", f"--task-type={task_type}"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                    "task_type": task_type
                }

            else:
                return {"error": f"Unknown command: {command}"}

        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": str(e)}

    def log_message(self, format, *args):
        """Override to reduce noise"""
        pass

class GhostLinkAPIServer:
    def __init__(self, port=3000, project_root=None):
        self.port = port
        self.project_root = project_root
        self.server = None
        self.thread = None

    def start(self):
        """Start the HTTP API server"""
        def run_server():
            with socketserver.TCPServer(("", self.port), lambda *args: GhostLinkAPIHandler(*args, project_root=self.project_root)) as httpd:
                self.server = httpd
                print(f"🚀 GhostLink API Server running on port {self.port}")
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
    """Main function to run the API server"""
    import argparse

    parser = argparse.ArgumentParser(description='GhostLink VS Code API Server')
    parser.add_argument('--port', type=int, default=3000, help='Port to run server on')
    parser.add_argument('--project-root', help='Path to GhostLink project root')

    args = parser.parse_args()

    project_root = args.project_root or os.path.dirname(os.path.abspath(__file__))

    print("🧠 Starting GhostLink VS Code API Server...")
    print(f"📁 Project Root: {project_root}")
    print(f"🌐 Port: {args.port}")

    server = GhostLinkAPIServer(port=args.port, project_root=project_root)
    server.start()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down GhostLink API Server...")
        server.stop()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()
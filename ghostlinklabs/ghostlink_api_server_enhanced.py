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

# Performance monitoring integration
try:
    import importlib.util
    import os
    import sys

    # Add the performance directory to path
    performance_path = os.path.join(os.path.dirname(__file__), 'performance', 'optimization')
    if performance_path not in sys.path:
        sys.path.insert(0, performance_path)

    # Import performance monitor
    perf_monitor_spec = importlib.util.spec_from_file_location(
        "performance_monitor",
        os.path.join(performance_path, "performance-monitor.py")
    )
    perf_monitor_module = importlib.util.module_from_spec(perf_monitor_spec)
    perf_monitor_spec.loader.exec_module(perf_monitor_module)
    performance_monitor = perf_monitor_module.PerformanceMonitor()

    # Import connection pool
    conn_pool_spec = importlib.util.spec_from_file_location(
        "connection_pool",
        os.path.join(performance_path, "connection-pool.py")
    )
    conn_pool_module = importlib.util.module_from_spec(conn_pool_spec)
    conn_pool_spec.loader.exec_module(conn_pool_module)
    init_connection_pools = conn_pool_module.init_connection_pools

    PERFORMANCE_INTEGRATION = True
    print("✅ Performance integration loaded successfully")
except ImportError as e:
    print(f"⚠️  Performance integration not available: {e}")
    PERFORMANCE_INTEGRATION = False
    performance_monitor = None
    init_connection_pools = None

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

        elif path == "/ide" or path == "/":
            self.serve_web_interface()

        elif path == "/ai-status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = self.get_ai_system_status()
            self.wfile.write(json.dumps(response).encode())

        elif path == "/orchestrator-control":
            self.handle_orchestrator_control()

        elif path == "/monitoring":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = self.get_system_monitoring_data()
            self.wfile.write(json.dumps(response).encode())

        elif path == "/performance":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = self.get_performance_metrics()
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

        elif path == "/metrics":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            result = self.receive_system_metrics(data)

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

    def serve_web_interface(self):
        """Serve the GhostLink IDE web interface"""
        try:
            # Path to the web interface file
            web_interface_path = os.path.join(self.project_root, "ghostlink-ide.html")

            if os.path.exists(web_interface_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                with open(web_interface_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html_content = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>GhostLink IDE - Interface Not Found</title>
                    <style>
                        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                        .error { color: #ff4444; }
                    </style>
                </head>
                <body>
                    <h1>GhostLink IDE</h1>
                    <p class="error">Web interface file not found. Please ensure ghostlink-ide.html exists in the project root.</p>
                </body>
                </html>
                """
                self.wfile.write(html_content.encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": f"Failed to serve web interface: {str(e)}"}
            self.wfile.write(json.dumps(response).encode())

    def get_ai_system_status(self):
        """Get AI system status for web interface"""
        try:
            result = subprocess.run(
                [sys.executable, "optimized_ai_orchestrator.py", "status"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                # Parse the status output
                lines = result.stdout.strip().split('\n')
                status_info = {}
                for line in lines:
                    if 'Total Systems:' in line:
                        status_info['total_systems'] = int(line.split(':')[1].strip())
                    elif 'Active Systems:' in line:
                        status_info['active_systems'] = int(line.split(':')[1].strip())
                    elif 'CPU Usage:' in line:
                        status_info['cpu_usage'] = float(line.split(':')[1].strip().replace('%', ''))
                    elif 'Memory Usage:' in line:
                        status_info['memory_usage'] = float(line.split(':')[1].strip().replace('%', ''))

                return {
                    "status": "success",
                    "ai_systems": status_info,
                    "timestamp": time.time()
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr,
                    "timestamp": time.time()
                }

        except Exception as e:
            return {"status": "error", "error": str(e), "timestamp": time.time()}

    def handle_orchestrator_control(self):
        """Handle orchestrator control commands from web interface"""
        if self.command == "POST":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            action = data.get('action', '')

            try:
                if action == "start":
                    result = subprocess.run(
                        [sys.executable, "optimized_ai_orchestrator.py", "start"],
                        cwd=self.project_root,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                elif action == "stop":
                    result = subprocess.run(
                        [sys.executable, "optimized_ai_orchestrator.py", "stop"],
                        cwd=self.project_root,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"error": f"Unknown action: {action}"}
                    self.wfile.write(json.dumps(response).encode())
                    return

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "success": result.returncode == 0,
                    "action": action,
                    "output": result.stdout,
                    "error": result.stderr,
                    "timestamp": time.time()
                }
                self.wfile.write(json.dumps(response).encode())

            except subprocess.TimeoutExpired:
                self.send_response(408)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "Command timed out", "action": action}
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": str(e), "action": action}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(405)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Method not allowed. Use POST."}
            self.wfile.write(json.dumps(response).encode())

    def get_system_monitoring_data(self):
        """Get comprehensive system monitoring data"""
        try:
            import platform

            import psutil

            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Network info
            net_io = psutil.net_io_counters()

            # Process info
            current_process = psutil.Process()
            process_memory = current_process.memory_info()

            # AI system status
            ai_status = self.get_ai_system_status()

            monitoring_data = {
                "timestamp": time.time(),
                "system": {
                    "platform": platform.system(),
                    "platform_version": platform.version(),
                    "architecture": platform.machine(),
                    "cpu_count": psutil.cpu_count(),
                    "cpu_percent": cpu_percent,
                    "memory_total": memory.total,
                    "memory_used": memory.used,
                    "memory_percent": memory.percent,
                    "disk_total": disk.total,
                    "disk_used": disk.used,
                    "disk_percent": disk.percent,
                    "network_bytes_sent": net_io.bytes_sent,
                    "network_bytes_recv": net_io.bytes_recv
                },
                "process": {
                    "pid": current_process.pid,
                    "memory_rss": process_memory.rss,
                    "memory_vms": process_memory.vms,
                    "cpu_percent": current_process.cpu_percent(),
                    "threads": len(current_process.threads())
                },
                "ai_systems": ai_status,
                "uptime": time.time() - psutil.boot_time()
            }

            # Add application usage data if available
            if hasattr(EnhancedGhostLinkAPIServer, 'latest_system_metrics') and EnhancedGhostLinkAPIServer.latest_system_metrics:
                monitoring_data["application_usage"] = {
                    "cpu_percent": EnhancedGhostLinkAPIServer.latest_system_metrics.get("cpu", 0),
                    "memory_percent": EnhancedGhostLinkAPIServer.latest_system_metrics.get("memory", 0),
                    "disk_percent": EnhancedGhostLinkAPIServer.latest_system_metrics.get("disk", 0),
                    "applications": EnhancedGhostLinkAPIServer.latest_system_metrics.get("applications", ""),
                    "top_processes": EnhancedGhostLinkAPIServer.latest_system_metrics.get("top_processes", ""),
                    "last_updated": EnhancedGhostLinkAPIServer.latest_system_metrics.get("timestamp", time.time())
                }

            return monitoring_data

        except ImportError:
            return {
                "error": "psutil not available for detailed monitoring",
                "basic_info": {
                    "timestamp": time.time(),
                    "server_running": True
                }
            }
        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_performance_metrics(self):
        """Get performance monitoring metrics"""
        try:
            if PERFORMANCE_INTEGRATION and performance_monitor:
                return {
                    "performance_integration": True,
                    "metrics": performance_monitor.get_performance_report(),
                    "timestamp": time.time()
                }
            else:
                return {
                    "performance_integration": False,
                    "error": "Performance monitoring not available",
                    "timestamp": time.time()
                }
        except Exception as e:
            return {
                "performance_integration": False,
                "error": str(e),
                "timestamp": time.time()
            }

    def receive_system_metrics(self, metrics_data):
        """Receive and process system metrics from monitoring script"""
        try:
            # Store the metrics globally for access by other endpoints
            self.latest_metrics = {
                "cpu": metrics_data.get("cpu", 0),
                "memory": metrics_data.get("memory", 0),
                "disk": metrics_data.get("disk", 0),
                "applications": metrics_data.get("applications", ""),
                "top_processes": metrics_data.get("top_processes", ""),
                "timestamp": metrics_data.get("timestamp", time.time()),
                "source": "ghostlink-monitor"
            }

            # Store in class variable for persistence
            EnhancedGhostLinkAPIServer.latest_system_metrics = self.latest_metrics

            print(f"📊 Received metrics: CPU={self.latest_metrics['cpu']}%, MEM={self.latest_metrics['memory']}%, DISK={self.latest_metrics['disk']}%")
            if self.latest_metrics.get('applications'):
                print(f"🖥️  Applications: {self.latest_metrics['applications'][:100]}...")
            if self.latest_metrics.get('top_processes'):
                print(f"⚙️  Top Processes: {self.latest_metrics['top_processes'][:100]}...")

            return {
                "success": True,
                "message": "Enhanced metrics received successfully",
                "applications_tracked": len(str(self.latest_metrics.get('applications', '')).split(';')) if self.latest_metrics.get('applications') else 0,
                "processes_tracked": len(str(self.latest_metrics.get('top_processes', '')).split(';')) if self.latest_metrics.get('top_processes') else 0,
                "timestamp": time.time()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }

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
        # Initialize performance monitoring
        if PERFORMANCE_INTEGRATION and init_connection_pools:
            try:
                print("⚡ Initializing performance monitoring and connection pools...")
                import asyncio
                asyncio.run(init_connection_pools())
                print("✅ Performance monitoring initialized")
            except Exception as e:
                print(f"⚠️  Failed to initialize performance monitoring: {e}")

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

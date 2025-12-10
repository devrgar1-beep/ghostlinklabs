#!/usr/bin/env python3
"""
GhostLink Universal API Server
Platform-agnostic HTTP API server for system monitoring
Works on Windows, macOS, and Linux
"""

import http.server
import json
import os
import platform
import socketserver
import sys
import threading
import time
from urllib.parse import urlparse

# Database integration
try:
    from ghostlink_database import (
        Alert,
        Backup,
        Configuration,
        Dashboard,
        LogEntry,
        NetworkDevice,
        PerformanceBaseline,
        SecurityEvent,
        SystemMetrics,
        User,
        func,
        get_db,
        init_database,
    )

    DATABASE_SUPPORT = True
    print("✅ Database integration loaded successfully")
except ImportError as e:
    DATABASE_SUPPORT = False
    print(f"⚠️  Database integration not available: {e}")

# Alerting system
try:
    from ghostlink_alerts import alert_manager, check_alerts

    ALERTING_SUPPORT = True
    print("✅ Alerting system loaded successfully")
except ImportError as e:
    ALERTING_SUPPORT = False
    print(f"⚠️  Alerting system not available: {e}")

# USB drive harvesting
try:
    from usb_drive_harvester import USBDriveHarvester

    USB_HARVEST_SUPPORT = True
    print("✅ USB drive harvesting loaded successfully")
except ImportError as e:
    USB_HARVEST_SUPPORT = False
    print(f"⚠️  USB drive harvesting not available: {e}")

# Platform-specific imports
PLATFORM = platform.system().lower()
print(f"🖥️  Detected platform: {PLATFORM}")

# Raspberry Pi detection
IS_RASPBERRY_PI = False
try:
    if PLATFORM == "linux":
        with open("/proc/cpuinfo") as f:
            cpuinfo = f.read()
            if "Raspberry Pi" in cpuinfo:
                IS_RASPBERRY_PI = True
                print("🍓 Raspberry Pi detected")
except:
    pass

# Arduino support
try:
    import serial

    ARDUINO_SUPPORT = True
    print("✅ Arduino serial support loaded")
except ImportError:
    ARDUINO_SUPPORT = False
    print("⚠️  pyserial not available - Arduino support disabled")

# Windows-specific imports
if PLATFORM == "windows":
    try:
        import wmi

        WINDOWS_WMI = True
        print("✅ Windows WMI support loaded")
    except ImportError:
        WINDOWS_WMI = False
        print("⚠️  WMI not available - Windows features limited")

# Performance monitoring integration (from enhanced server)
try:
    import importlib.util
    import os
    import sys

    # Add the performance directory to path
    performance_path = os.path.join(os.path.dirname(__file__), "performance", "optimization")
    if performance_path not in sys.path:
        sys.path.insert(0, performance_path)

    # Import performance monitor
    perf_monitor_spec = importlib.util.spec_from_file_location(
        "performance_monitor", os.path.join(performance_path, "performance-monitor.py")
    )
    perf_monitor_module = importlib.util.module_from_spec(perf_monitor_spec)
    perf_monitor_spec.loader.exec_module(perf_monitor_module)
    performance_monitor = perf_monitor_module.PerformanceMonitor()

    # Import connection pool
    conn_pool_spec = importlib.util.spec_from_file_location(
        "connection_pool", os.path.join(performance_path, "connection-pool.py")
    )
    conn_pool_module = importlib.util.module_from_spec(conn_pool_spec)
    conn_pool_spec.loader.exec_module(conn_pool_module)
    init_connection_pools = conn_pool_module.init_connection_pools

    PERFORMANCE_OPTIMIZATION = True
    print("✅ Performance optimization loaded successfully")
except ImportError as e:
    print(f"⚠️  Performance optimization not available: {e}")
    PERFORMANCE_OPTIMIZATION = False

# Performance integration (psutil)
try:
    import psutil

    PERFORMANCE_INTEGRATION = True
    print("✅ Performance integration loaded successfully")
except ImportError as e:
    PERFORMANCE_INTEGRATION = False
    print(f"⚠️  Performance integration not available: {e}")


class GhostLinkAPIHandler(http.server.BaseHTTPRequestHandler):
    """Universal HTTP request handler for GhostLink API"""

    def __init__(self, *args, project_root=None, **kwargs):
        self.project_root = project_root or os.getcwd()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests with comprehensive error handling"""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path

            # Log request for debugging
            print(f"🔗 Processing request: {path}", flush=True)

            if path == "/health":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = {
                        "status": "healthy",
                        "platform": platform.system(),
                        "version": platform.version(),
                        "performance_integration": PERFORMANCE_INTEGRATION,
                        "performance_optimization": PERFORMANCE_OPTIMIZATION,
                        "wmi_support": WINDOWS_WMI if PLATFORM == "windows" else None,
                        "raspberry_pi_detected": (
                            IS_RASPBERRY_PI if "IS_RASPBERRY_PI" in globals() else False
                        ),
                        "arduino_support": (
                            ARDUINO_SUPPORT if "ARDUINO_SUPPORT" in globals() else False
                        ),
                        "usb_harvest_support": USB_HARVEST_SUPPORT,
                        "database_support": DATABASE_SUPPORT,
                        "alerting_support": ALERTING_SUPPORT,
                        "timestamp": time.time(),
                    }
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Health check successful", flush=True)
                except Exception as e:
                    print(f"❌ Health check error: {e}", flush=True)
                    self.send_error(500, f"Health check failed: {str(e)}")

            elif path == "/status":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_system_status()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Status check successful", flush=True)
                except Exception as e:
                    print(f"❌ Status check error: {e}", flush=True)
                    self.send_error(500, f"Status check failed: {str(e)}")

            elif path == "/monitoring":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_monitoring_data()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Monitoring data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ Monitoring error: {e}", flush=True)
                    self.send_error(500, f"Monitoring failed: {str(e)}")

            elif path == "/analytics":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_analytics()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Analytics data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ Analytics error: {e}", flush=True)
                    self.send_error(500, f"Analytics failed: {str(e)}")

            elif path == "/usb-drives":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_usb_drives()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ USB drives data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ USB drives error: {e}", flush=True)
                    self.send_error(500, f"USB drives failed: {str(e)}")

            elif path == "/services":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_services()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Services data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ Services error: {e}", flush=True)
                    self.send_error(500, f"Services failed: {str(e)}")

            elif path == "/processes":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_processes()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Processes data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ Processes error: {e}", flush=True)
                    self.send_error(500, f"Processes failed: {str(e)}")

            elif path == "/applications":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_applications()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Applications data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ Applications error: {e}", flush=True)
                    self.send_error(500, f"Applications failed: {str(e)}")

            elif path == "/raspberry-pi":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_raspberry_pi_data()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Raspberry Pi data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ Raspberry Pi error: {e}", flush=True)
                    self.send_error(500, f"Raspberry Pi failed: {str(e)}")

            elif path == "/arduino":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_arduino_data()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Arduino data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ Arduino error: {e}", flush=True)
                    self.send_error(500, f"Arduino failed: {str(e)}")

            elif path == "/history":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_historical_metrics()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ History data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ History error: {e}", flush=True)
                    self.send_error(500, f"History failed: {str(e)}")

            elif path == "/alerts":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_alerts()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Alerts data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ Alerts error: {e}", flush=True)
                    self.send_error(500, f"Alerts failed: {str(e)}")

            elif path == "/network":
                try:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = self.get_network_devices()
                    self.wfile.write(json.dumps(response).encode())
                    print("✅ Network data retrieved", flush=True)
                except Exception as e:
                    print(f"❌ Network error: {e}", flush=True)
                    self.send_error(500, f"Network failed: {str(e)}")

            elif path.startswith("/api/files/"):
                try:
                    if path == "/api/files/tree":
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.end_headers()
                        response = self.get_file_tree()
                        self.wfile.write(json.dumps(response).encode())
                        print("✅ File tree retrieved", flush=True)
                    elif path.startswith("/api/files/content"):
                        query = parsed_path.query
                        params = {}
                        if query:
                            for param in query.split("&"):
                                key, value = param.split("=")
                                params[key] = value

                        file_path = params.get("path", "")
                        if file_path:
                            self.send_response(200)
                            self.send_header("Content-type", "text/plain")
                            self.send_header("Access-Control-Allow-Origin", "*")
                            self.end_headers()
                            content = self.get_file_content(file_path)
                            self.wfile.write(content.encode())
                            print(f"✅ File content retrieved: {file_path}", flush=True)
                        else:
                            self.send_error(400, "Missing path parameter")
                    else:
                        self.send_error(404, "File endpoint not found")
                except Exception as e:
                    print(f"❌ File operation error: {e}", flush=True)
                    self.send_error(500, f"File operation failed: {str(e)}")

            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                response = {
                    "error": "Endpoint not found",
                    "available_endpoints": [
                        "/health",
                        "/status",
                        "/monitoring",
                        "/services",
                        "/processes",
                        "/applications",
                        "/raspberry-pi",
                        "/arduino",
                        "/history",
                        "/analytics",
                        "/alerts",
                        "/network",
                        "/usb-drives",
                        "/api/files/tree",
                        "/api/files/content",
                        "/api/files/save",
                        "/api/terminal/execute",
                    ],
                }
                self.wfile.write(json.dumps(response).encode())
                print(f"❌ Unknown endpoint: {path}", flush=True)

        except Exception as e:
            print(f"❌ Critical GET request error: {e}", flush=True)
            try:
                self.send_error(500, f"Internal server error: {str(e)}")
            except:
                # If we can't even send an error response, log it
                print(f"❌ Could not send error response: {e}", flush=True)

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/metrics":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            result = self.receive_metrics(data)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        elif path == "/command":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            command = data.get("command", "")
            params = data.get("params", {})

            # Execute the command
            result = self.execute_ghost_command(command, params)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        elif path == "/api/files/save":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            file_path = data.get("path", "")
            content = data.get("content", "")

            if file_path:
                result = self.save_file_content(file_path, content)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            else:
                self.send_error(400, "Missing path parameter")

        elif path == "/api/terminal/execute":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            command = data.get("command", "")

            if command:
                result = self.execute_terminal_command(command)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            else:
                self.send_error(400, "Missing command parameter")

        elif path == "/api/ecosystem/ai-systems":
            try:
                systems = self.get_ai_systems_status()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(systems).encode())
            except Exception as e:
                self.send_error(500, f"AI systems status failed: {str(e)}")

        elif path == "/api/ecosystem/control":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            system_name = data.get("system_name", "")
            action = data.get("action", "")  # start, stop, restart

            if system_name and action:
                result = self.control_ai_system(system_name, action)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            else:
                self.send_error(400, "Missing system_name or action parameter")

        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())

    def get_system_status(self):
        """Get comprehensive system status (platform-agnostic)"""
        try:
            status = {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "hostname": platform.node(),
                "python_version": sys.version,
                "timestamp": time.time(),
                "performance_integration": PERFORMANCE_INTEGRATION,
                "performance_optimization": PERFORMANCE_OPTIMIZATION,
            }

            # Platform-specific information
            if PLATFORM == "windows" and WINDOWS_WMI:
                try:
                    c = wmi.WMI()
                    for os_info in c.Win32_OperatingSystem():
                        status.update(
                            {
                                "os_caption": os_info.Caption,
                                "os_version": os_info.Version,
                                "os_build": os_info.BuildNumber,
                                "os_serial": os_info.SerialNumber,
                                "total_memory": int(os_info.TotalVisibleMemorySize)
                                * 1024,  # Convert to bytes
                                "free_memory": int(os_info.FreePhysicalMemory) * 1024,
                            }
                        )
                        break
                except Exception as e:
                    status["wmi_error"] = str(e)

            elif PLATFORM == "darwin":  # macOS
                try:
                    import subprocess

                    # Get macOS version
                    result = subprocess.run(
                        ["sw_vers", "-productVersion"], capture_output=True, text=True
                    )
                    if result.returncode == 0:
                        status["macos_version"] = result.stdout.strip()

                    # Get hardware info
                    result = subprocess.run(
                        ["sysctl", "-n", "hw.memsize"], capture_output=True, text=True
                    )
                    if result.returncode == 0:
                        status["total_memory"] = int(result.stdout.strip())
                except Exception as e:
                    status["macos_error"] = str(e)

            elif PLATFORM == "linux":
                try:
                    import subprocess

                    # Get Linux distribution
                    result = subprocess.run(["lsb_release", "-d"], capture_output=True, text=True)
                    if result.returncode == 0:
                        status["linux_distribution"] = (
                            result.stdout.strip().replace("Description:", "").strip()
                        )

                    # Get system info from /proc/meminfo
                    with open("/proc/meminfo") as f:
                        for line in f:
                            if line.startswith("MemTotal:"):
                                status["total_memory"] = (
                                    int(line.split()[1]) * 1024
                                )  # Convert to bytes
                                break
                except Exception as e:
                    status["linux_error"] = str(e)

            return status

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_monitoring_data(self):
        """Get comprehensive monitoring data (platform-agnostic)"""
        try:
            monitoring_data = {
                "timestamp": time.time(),
                "platform": platform.system(),
                "hostname": platform.node(),
                "performance_integration": PERFORMANCE_INTEGRATION,
            }

            if PERFORMANCE_INTEGRATION:
                # CPU information
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()

                # Memory information
                memory = psutil.virtual_memory()

                # Disk information (try common mount points)
                disk_percent = 0
                disk_total = 0
                disk_used = 0
                try:
                    if PLATFORM == "windows":
                        disk = psutil.disk_usage("C:")
                    else:
                        disk = psutil.disk_usage("/")
                    disk_percent = disk.percent
                    disk_total = disk.total
                    disk_used = disk.used
                except:
                    pass

                # Network information
                net_io = psutil.net_io_counters()

                monitoring_data.update(
                    {
                        "system": {
                            "cpu_percent": cpu_percent,
                            "cpu_count": cpu_count,
                            "memory_total": memory.total,
                            "memory_used": memory.used,
                            "memory_percent": memory.percent,
                            "disk_total": disk_total,
                            "disk_used": disk_used,
                            "disk_percent": disk_percent,
                            "network_bytes_sent": net_io.bytes_sent,
                            "network_bytes_recv": net_io.bytes_recv,
                        },
                        "process": {
                            "current_pid": os.getpid(),
                            "current_memory": psutil.Process().memory_info().rss,
                        },
                    }
                )

            # Add application usage data if available
            if hasattr(self, "latest_metrics") and self.latest_metrics:
                monitoring_data["application_usage"] = {
                    "cpu_percent": self.latest_metrics.get("cpu", 0),
                    "memory_percent": self.latest_metrics.get("memory", 0),
                    "disk_percent": self.latest_metrics.get("disk", 0),
                    "applications": self.latest_metrics.get("applications", ""),
                    "top_processes": self.latest_metrics.get("top_processes", ""),
                    "platform": self.latest_metrics.get("platform", "Unknown"),
                    "last_updated": self.latest_metrics.get("timestamp", time.time()),
                }

            # Add Raspberry Pi data if available
            if (
                hasattr(self, "latest_metrics")
                and self.latest_metrics
                and "raspberry_pi" in self.latest_metrics
            ):
                monitoring_data["raspberry_pi"] = self.latest_metrics["raspberry_pi"]

            # Add Arduino data if available
            if (
                hasattr(self, "latest_metrics")
                and self.latest_metrics
                and "arduino_devices" in self.latest_metrics
            ):
                monitoring_data["arduino_devices"] = self.latest_metrics["arduino_devices"]

            return monitoring_data

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_services(self):
        """Get system services (platform-agnostic)"""
        try:
            services = []

            if PLATFORM == "windows" and WINDOWS_WMI:
                try:
                    c = wmi.WMI()
                    for service in c.Win32_Service():
                        services.append(
                            {
                                "name": service.Name,
                                "display_name": service.DisplayName,
                                "status": service.State,
                                "start_mode": service.StartMode,
                                "path": service.PathName,
                            }
                        )
                except Exception as e:
                    return {"error": f"WMI service query failed: {str(e)}"}

            elif PLATFORM == "darwin":  # macOS
                try:
                    import subprocess

                    result = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split("\n")[1:]  # Skip header
                        for line in lines[:20]:  # Limit to 20 services
                            parts = line.split()
                            if len(parts) >= 3:
                                services.append(
                                    {
                                        "name": parts[2],
                                        "pid": parts[0] if parts[0] != "-" else None,
                                        "status": "running" if parts[0] != "-" else "stopped",
                                    }
                                )
                except Exception as e:
                    return {"error": f"macOS service query failed: {str(e)}"}

            elif PLATFORM == "linux":
                try:
                    import subprocess

                    result = subprocess.run(
                        ["systemctl", "list-units", "--type=service", "--no-pager"],
                        capture_output=True,
                        text=True,
                    )
                    if result.returncode == 0:
                        lines = result.stdout.strip().split("\n")
                        for line in lines[1:-7]:  # Skip header and footer
                            if line.strip() and not line.startswith("●"):
                                parts = line.split()
                                if len(parts) >= 4:
                                    services.append(
                                        {
                                            "name": parts[0],
                                            "status": parts[3],
                                            "description": (
                                                " ".join(parts[4:]) if len(parts) > 4 else ""
                                            ),
                                        }
                                    )
                            if len(services) >= 20:  # Limit to 20 services
                                break
                except Exception as e:
                    return {"error": f"Linux service query failed: {str(e)}"}

            return {
                "services": services,
                "total_services": len(services),
                "platform": PLATFORM,
                "timestamp": time.time(),
            }

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_processes(self):
        """Get running processes (cross-platform)"""
        try:
            if not PERFORMANCE_INTEGRATION:
                return {"error": "Performance integration not available"}

            processes = []
            for proc in psutil.process_iter(
                ["pid", "name", "cpu_percent", "memory_percent", "status"]
            ):
                try:
                    processes.append(
                        {
                            "pid": proc.info["pid"],
                            "name": proc.info["name"],
                            "cpu_percent": round(proc.info["cpu_percent"], 2),
                            "memory_percent": round(proc.info["memory_percent"], 2),
                            "status": proc.info["status"],
                        }
                    )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Sort by CPU usage
            processes.sort(key=lambda x: x["cpu_percent"], reverse=True)

            return {
                "processes": processes[:20],  # Top 20 processes
                "total_processes": len(processes),
                "timestamp": time.time(),
            }

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_applications(self):
        """Get running applications (platform-agnostic)"""
        try:
            applications = []

            if PLATFORM == "windows" and WINDOWS_WMI:
                try:
                    c = wmi.WMI()
                    for process in c.Win32_Process():
                        try:
                            if (
                                process.Caption
                                and not process.Caption.lower().startswith(
                                    ("system", "svchost", "csrss", "winlogon", "lsass")
                                )
                                and not any(
                                    x in process.Caption.lower()
                                    for x in ["exe", "dll", "sys", "com"]
                                )
                            ):
                                applications.append(
                                    {
                                        "name": process.Caption,
                                        "pid": process.ProcessId,
                                        "command_line": process.CommandLine or "",
                                    }
                                )
                        except Exception:
                            continue
                except Exception as e:
                    return {"error": f"WMI application query failed: {str(e)}"}

            elif PLATFORM == "darwin":  # macOS
                try:
                    import subprocess

                    result = subprocess.run(
                        [
                            "osascript",
                            "-e",
                            'tell application "System Events" to get {name, unix id} of every process where background only is false',
                        ],
                        capture_output=True,
                        text=True,
                        timeout=10,
                    )

                    if result.returncode == 0:
                        app_list = result.stdout.strip()
                        # Parse the AppleScript result
                        if app_list:
                            # This is a simplified parser - in production you'd want more robust parsing
                            parts = app_list.split(", ")
                            for i in range(0, len(parts), 2):
                                if i + 1 < len(parts):
                                    name = parts[i]
                                    try:
                                        pid = int(parts[i + 1])
                                        applications.append({"name": name, "pid": pid})
                                    except:
                                        continue
                except Exception as e:
                    return {"error": f"macOS application query failed: {str(e)}"}

            elif PLATFORM == "linux":
                try:
                    import subprocess

                    # Try wmctrl first for GUI applications
                    result = subprocess.run(
                        ["wmctrl", "-l"], capture_output=True, text=True, timeout=5
                    )
                    if result.returncode == 0:
                        lines = result.stdout.strip().split("\n")
                        for line in lines[:15]:  # Limit to 15 applications
                            parts = line.split(None, 3)
                            if len(parts) >= 4:
                                try:
                                    pid = int(parts[2])
                                    applications.append(
                                        {
                                            "name": parts[3].split(" - ")[0],
                                            "window_id": parts[0],
                                            "pid": pid,
                                        }
                                    )
                                except:
                                    continue
                    else:
                        # Fallback to ps
                        for proc in psutil.process_iter(["pid", "name"]):
                            try:
                                if (
                                    proc.info["name"]
                                    and len(proc.info["name"]) > 3
                                    and not any(
                                        sys in proc.info["name"].lower()
                                        for sys in ["system", "kernel", "init", "bash", "sh"]
                                    )
                                ):
                                    applications.append(
                                        {"name": proc.info["name"], "pid": proc.info["pid"]}
                                    )
                                    if len(applications) >= 15:
                                        break
                            except Exception:
                                continue
                except Exception as e:
                    return {"error": f"Linux application query failed: {str(e)}"}

            return {
                "applications": applications,
                "total_applications": len(applications),
                "platform": PLATFORM,
                "timestamp": time.time(),
            }

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def receive_metrics(self, metrics_data):
        """Receive and process metrics from monitoring script"""
        try:
            # Store the metrics globally for access by other endpoints
            self.latest_metrics = {
                "cpu": metrics_data.get("cpu", 0),
                "memory": metrics_data.get("memory", 0),
                "disk": metrics_data.get("disk", 0),
                "applications": metrics_data.get("applications", ""),
                "top_processes": metrics_data.get("top_processes", ""),
                "platform": metrics_data.get("platform", "Unknown"),
                "timestamp": metrics_data.get("timestamp", time.time()),
                "source": "ghostlink-monitor",
                "is_raspberry_pi": metrics_data.get("is_raspberry_pi", False),
            }

            # Add Raspberry Pi specific metrics
            if metrics_data.get("is_raspberry_pi"):
                rpi_metrics = {}
                if "cpu_temp" in metrics_data:
                    rpi_metrics["cpu_temp"] = metrics_data["cpu_temp"]
                if "gpu_memory_mb" in metrics_data:
                    rpi_metrics["gpu_memory_mb"] = metrics_data["gpu_memory_mb"]
                if "throttled" in metrics_data:
                    rpi_metrics["throttled"] = metrics_data["throttled"]
                if rpi_metrics:
                    self.latest_metrics["raspberry_pi"] = rpi_metrics

            # Add Arduino device data
            if "arduino_devices" in metrics_data:
                self.latest_metrics["arduino_devices"] = metrics_data["arduino_devices"]

            # Store in class variable for persistence
            GhostLinkAPIHandler.latest_system_metrics = self.latest_metrics

            # Store in database if available
            if DATABASE_SUPPORT:
                try:
                    db = get_db()
                    system_metrics = SystemMetrics(
                        platform=metrics_data.get("platform", "Unknown"),
                        hostname=platform.node(),
                        cpu_percent=metrics_data.get("cpu", 0),
                        cpu_count=psutil.cpu_count() if PERFORMANCE_INTEGRATION else None,
                        memory_total=(
                            psutil.virtual_memory().total if PERFORMANCE_INTEGRATION else None
                        ),
                        memory_used=(
                            psutil.virtual_memory().used if PERFORMANCE_INTEGRATION else None
                        ),
                        memory_percent=metrics_data.get("memory", 0),
                        disk_total=(
                            psutil.disk_usage("/").total if PERFORMANCE_INTEGRATION else None
                        ),
                        disk_used=psutil.disk_usage("/").used if PERFORMANCE_INTEGRATION else None,
                        disk_percent=metrics_data.get("disk", 0),
                        network_bytes_sent=(
                            psutil.net_io_counters().bytes_sent if PERFORMANCE_INTEGRATION else None
                        ),
                        network_bytes_recv=(
                            psutil.net_io_counters().bytes_recv if PERFORMANCE_INTEGRATION else None
                        ),
                        is_raspberry_pi=metrics_data.get("is_raspberry_pi", False),
                        raspberry_pi_data=self.latest_metrics.get("raspberry_pi"),
                        arduino_devices=metrics_data.get("arduino_devices"),
                        applications=metrics_data.get("applications", ""),
                        top_processes=metrics_data.get("top_processes", ""),
                    )
                    db.add(system_metrics)
                    db.commit()
                    print(f"💾 Metrics stored in database (ID: {system_metrics.id})")
                except Exception as db_error:
                    print(f"⚠️  Database storage failed: {db_error}")

            # Check for alerts
            if ALERTING_SUPPORT:
                try:
                    alerts = check_alerts(metrics_data)
                    if alerts:
                        print(f"🚨 {len(alerts)} alert(s) triggered")
                        for alert in alerts:
                            print(f"  - {alert['severity'].upper()}: {alert['message']}")
                except Exception as alert_error:
                    print(f"⚠️  Alert checking failed: {alert_error}")

            print(
                f"📊 Universal metrics received: CPU={self.latest_metrics['cpu']}%, MEM={self.latest_metrics['memory']}%, DISK={self.latest_metrics['disk']}%"
            )
            if self.latest_metrics.get("applications"):
                app_count = (
                    len(str(self.latest_metrics["applications"]).split(","))
                    if self.latest_metrics["applications"]
                    else 0
                )
                print(f"🖥️  Applications running: {app_count}")
            if self.latest_metrics.get("top_processes"):
                proc_count = (
                    len(str(self.latest_metrics["top_processes"]).split(","))
                    if self.latest_metrics["top_processes"]
                    else 0
                )
                print(f"⚙️  Processes tracked: {proc_count}")
            if self.latest_metrics.get("raspberry_pi"):
                rpi = self.latest_metrics["raspberry_pi"]
                temp = rpi.get("cpu_temp", "N/A")
                print(f"🍓 Raspberry Pi: CPU Temp={temp}°C")
            if self.latest_metrics.get("arduino_devices"):
                arduino_count = len(self.latest_metrics["arduino_devices"])
                print(f"📡 Arduino devices: {arduino_count} connected")

            return {
                "success": True,
                "message": "Universal metrics received successfully",
                "applications_tracked": (
                    len(str(self.latest_metrics.get("applications", "")).split(","))
                    if self.latest_metrics.get("applications")
                    else 0
                ),
                "processes_tracked": (
                    len(str(self.latest_metrics.get("top_processes", "")).split(","))
                    if self.latest_metrics.get("top_processes")
                    else 0
                ),
                "platform": self.latest_metrics.get("platform", "Unknown"),
                "is_raspberry_pi": self.latest_metrics.get("is_raspberry_pi", False),
                "arduino_devices": len(self.latest_metrics.get("arduino_devices", {})),
                "database_stored": DATABASE_SUPPORT,
                "timestamp": time.time(),
            }

        except Exception as e:
            return {"success": False, "error": str(e), "timestamp": time.time()}

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
                    timeout=30,
                )
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                }

            elif command == "status":
                result = subprocess.run(
                    [sys.executable, "ghost_vscode_integration.py", "status"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                }

            elif command == "task":
                task_type = params.get("task_type", "consciousness")
                result = subprocess.run(
                    [
                        sys.executable,
                        "ghost_agent_orchestrator.py",
                        "task",
                        f"--task-type={task_type}",
                    ],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr,
                    "task_type": task_type,
                }

            else:
                return {"error": f"Unknown command: {command}"}

        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": str(e)}

    def get_raspberry_pi_data(self):
        """Get Raspberry Pi specific data"""
        try:
            if not IS_RASPBERRY_PI:
                return {
                    "error": "Not running on Raspberry Pi",
                    "platform": PLATFORM,
                    "timestamp": time.time(),
                }

            rpi_data = {"platform": "raspberry_pi", "detected": True, "timestamp": time.time()}

            # Get Raspberry Pi specific metrics from latest metrics
            if (
                hasattr(self, "latest_metrics")
                and self.latest_metrics
                and "raspberry_pi" in self.latest_metrics
            ):
                rpi_data.update(self.latest_metrics["raspberry_pi"])

            # Get additional Raspberry Pi info
            try:
                import subprocess

                # Get Raspberry Pi model
                result = subprocess.run(
                    ["cat", "/proc/device-tree/model"], capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    rpi_data["model"] = result.stdout.strip()

                # Get current CPU frequency
                result = subprocess.run(
                    ["vcgencmd", "measure_clock", "arm"], capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    freq_str = result.stdout.strip()
                    # Extract frequency value (format: frequency(48)=600000000)
                    freq_value = int(freq_str.split("=")[1])
                    rpi_data["cpu_frequency_hz"] = freq_value

                # Get voltage
                result = subprocess.run(
                    ["vcgencmd", "measure_volts", "core"], capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    volt_str = result.stdout.strip()
                    # Extract voltage value (format: volt=1.20V)
                    volt_value = float(volt_str.split("=")[1].rstrip("V"))
                    rpi_data["core_voltage_v"] = volt_value

            except Exception as e:
                rpi_data["system_info_error"] = str(e)

            return rpi_data

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_arduino_data(self):
        """Get Arduino device data"""
        try:
            arduino_data = {"arduino_support": ARDUINO_SUPPORT, "timestamp": time.time()}

            if not ARDUINO_SUPPORT:
                arduino_data["error"] = (
                    "Arduino serial support not available (pyserial not installed)"
                )
                return arduino_data

            # Get Arduino data from latest metrics
            if (
                hasattr(self, "latest_metrics")
                and self.latest_metrics
                and "arduino_devices" in self.latest_metrics
            ):
                arduino_data["devices"] = self.latest_metrics["arduino_devices"]
                arduino_data["connected_devices"] = len(self.latest_metrics["arduino_devices"])
            else:
                arduino_data["devices"] = {}
                arduino_data["connected_devices"] = 0

            # Add Arduino-specific information
            arduino_data["serial_ports"] = self.scan_arduino_ports()

            return arduino_data

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def scan_arduino_ports(self):
        """Scan for available Arduino serial ports"""
        try:
            if not ARDUINO_SUPPORT:
                return []

            import serial.tools.list_ports

            ports = []

            for port in serial.tools.list_ports.comports():
                port_info = {
                    "device": port.device,
                    "name": port.name or "",
                    "description": port.description or "",
                    "manufacturer": port.manufacturer or "",
                    "serial_number": port.serial_number or "",
                }

                # Check if it looks like an Arduino
                if any(
                    keyword in (port.description or "").lower()
                    for keyword in ["arduino", "usb serial", "ch340", "ftdi"]
                ):
                    port_info["likely_arduino"] = True
                else:
                    port_info["likely_arduino"] = False

                ports.append(port_info)

            return ports

        except Exception as e:
            return [{"error": f"Port scanning failed: {str(e)}"}]

    def get_historical_metrics(self):
        """Get historical system metrics from database"""
        try:
            if not DATABASE_SUPPORT:
                return {"error": "Database not available", "timestamp": time.time()}

            db = get_db()
            # Get last 100 metrics entries
            metrics = (
                db.query(SystemMetrics).order_by(SystemMetrics.timestamp.desc()).limit(100).all()
            )

            historical_data = []
            for metric in metrics:
                data = {
                    "id": metric.id,
                    "timestamp": metric.timestamp.isoformat(),
                    "platform": metric.platform,
                    "hostname": metric.hostname,
                    "cpu_percent": metric.cpu_percent,
                    "memory_percent": metric.memory_percent,
                    "disk_percent": metric.disk_percent,
                    "is_raspberry_pi": metric.is_raspberry_pi,
                }

                if metric.raspberry_pi_data:
                    data["raspberry_pi"] = metric.raspberry_pi_data

                if metric.arduino_devices:
                    data["arduino_devices"] = metric.arduino_devices

                historical_data.append(data)

            return {
                "historical_metrics": historical_data,
                "total_records": len(historical_data),
                "database_available": True,
                "timestamp": time.time(),
            }

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_analytics(self):
        """Get system analytics and insights"""
        try:
            analytics = {"timestamp": time.time(), "database_available": DATABASE_SUPPORT}

            if DATABASE_SUPPORT:
                db = get_db()

                # CPU usage statistics
                cpu_stats = (
                    db.query(SystemMetrics.cpu_percent)
                    .filter(SystemMetrics.cpu_percent.isnot(None))
                    .all()
                )

                if cpu_stats:
                    cpu_values = [stat[0] for stat in cpu_stats]
                    analytics["cpu"] = {
                        "average": round(sum(cpu_values) / len(cpu_values), 2),
                        "max": max(cpu_values),
                        "min": min(cpu_values),
                        "samples": len(cpu_values),
                    }

                # Memory usage statistics
                mem_stats = (
                    db.query(SystemMetrics.memory_percent)
                    .filter(SystemMetrics.memory_percent.isnot(None))
                    .all()
                )

                if mem_stats:
                    mem_values = [stat[0] for stat in mem_stats]
                    analytics["memory"] = {
                        "average": round(sum(mem_values) / len(mem_values), 2),
                        "max": max(mem_values),
                        "min": min(mem_values),
                        "samples": len(mem_values),
                    }

                # Platform distribution
                platform_stats = (
                    db.query(SystemMetrics.platform, func.count(SystemMetrics.id))
                    .group_by(SystemMetrics.platform)
                    .all()
                )

                analytics["platforms"] = {platform: count for platform, count in platform_stats}

                # Raspberry Pi statistics
                rpi_count = (
                    db.query(SystemMetrics).filter(SystemMetrics.is_raspberry_pi == True).count()
                )
                analytics["raspberry_pi_devices"] = rpi_count

                # Recent alerts
                recent_alerts = db.query(Alert).order_by(Alert.timestamp.desc()).limit(10).all()
                analytics["recent_alerts"] = [
                    {
                        "id": alert.id,
                        "timestamp": alert.timestamp.isoformat(),
                        "type": alert.alert_type,
                        "severity": alert.severity,
                        "message": alert.message,
                        "resolved": alert.resolved,
                    }
                    for alert in recent_alerts
                ]

            return analytics

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_alerts(self):
        """Get system alerts"""
        try:
            if not DATABASE_SUPPORT:
                return {"error": "Database not available", "timestamp": time.time()}

            db = get_db()
            alerts = db.query(Alert).order_by(Alert.timestamp.desc()).limit(50).all()

            alert_data = []
            for alert in alerts:
                alert_data.append(
                    {
                        "id": alert.id,
                        "timestamp": alert.timestamp.isoformat(),
                        "type": alert.alert_type,
                        "severity": alert.severity,
                        "message": alert.message,
                        "resolved": alert.resolved,
                        "resolved_at": alert.resolved_at.isoformat() if alert.resolved_at else None,
                        "metadata": alert.metadata,
                    }
                )

            # Alert statistics
            total_alerts = db.query(Alert).count()
            resolved_alerts = db.query(Alert).filter(Alert.resolved == True).count()
            critical_alerts = db.query(Alert).filter(Alert.severity == "critical").count()

            return {
                "alerts": alert_data,
                "statistics": {
                    "total": total_alerts,
                    "resolved": resolved_alerts,
                    "unresolved": total_alerts - resolved_alerts,
                    "critical": critical_alerts,
                },
                "timestamp": time.time(),
            }

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_network_devices(self):
        """Get network device information"""
        try:
            network_info = {"timestamp": time.time(), "database_available": DATABASE_SUPPORT}

            if DATABASE_SUPPORT:
                db = get_db()
                devices = db.query(NetworkDevice).order_by(NetworkDevice.last_seen.desc()).all()

                network_info["devices"] = [
                    {
                        "id": device.id,
                        "ip_address": device.ip_address,
                        "mac_address": device.mac_address,
                        "hostname": device.hostname,
                        "device_type": device.device_type,
                        "vendor": device.vendor,
                        "status": device.status,
                        "last_seen": device.last_seen.isoformat(),
                        "first_discovered": device.first_discovered.isoformat(),
                    }
                    for device in devices
                ]

            # Current network interfaces
            if PERFORMANCE_INTEGRATION:
                network_info["interfaces"] = []
                for interface, addrs in psutil.net_if_addrs().items():
                    interface_info = {"name": interface, "addresses": []}
                    for addr in addrs:
                        interface_info["addresses"].append(
                            {
                                "family": str(addr.family),
                                "address": addr.address,
                                "netmask": addr.netmask,
                                "broadcast": addr.broadcast,
                            }
                        )
                    network_info["interfaces"].append(interface_info)

            return network_info

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_usb_drives(self):
        """Get USB drive information and harvested data"""
        try:
            usb_info = {"timestamp": time.time(), "usb_harvest_support": USB_HARVEST_SUPPORT}

            if USB_HARVEST_SUPPORT:
                harvester = USBDriveHarvester()
                usb_info.update(harvester.get_drive_info())
            else:
                usb_info["error"] = "USB harvesting not available"

            return usb_info

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_file_tree(self):
        """Get file tree structure for IDE"""
        try:
            import os

            def build_tree(path, max_depth=3, current_depth=0):
                if current_depth > max_depth:
                    return []

                items = []
                try:
                    entries = os.listdir(path)
                except (PermissionError, OSError):
                    return []

                for entry in sorted(entries):
                    if entry.startswith("."):  # Skip hidden files
                        continue

                    full_path = os.path.join(path, entry)
                    rel_path = os.path.relpath(full_path, self.project_root or os.getcwd())

                    try:
                        is_dir = os.path.isdir(full_path)
                        item = {
                            "name": entry,
                            "path": rel_path,
                            "type": "directory" if is_dir else "file",
                        }

                        if is_dir and current_depth < max_depth:
                            item["children"] = build_tree(full_path, max_depth, current_depth + 1)

                        items.append(item)
                    except (PermissionError, OSError):
                        continue

                return items

            root_path = self.project_root or os.getcwd()
            return build_tree(root_path)

        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def get_file_content(self, file_path):
        """Get file content for IDE"""
        try:
            import os

            # Security: ensure path is within project root
            if self.project_root:
                full_path = os.path.join(self.project_root, file_path)
                if not os.path.abspath(full_path).startswith(os.path.abspath(self.project_root)):
                    return "Access denied: Path outside project root"
            else:
                full_path = file_path

            if not os.path.exists(full_path):
                return "File not found"

            if os.path.isdir(full_path):
                return "Cannot read directory content"

            with open(full_path, encoding="utf-8", errors="ignore") as f:
                return f.read()

        except Exception as e:
            return f"Error reading file: {str(e)}"

    def save_file_content(self, file_path, content):
        """Save file content from IDE"""
        try:
            import os

            # Security: ensure path is within project root
            if self.project_root:
                full_path = os.path.join(self.project_root, file_path)
                if not os.path.abspath(full_path).startswith(os.path.abspath(self.project_root)):
                    return {"error": "Access denied: Path outside project root"}
            else:
                full_path = file_path

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

            return {"success": True, "message": "File saved successfully"}

        except Exception as e:
            return {"error": str(e)}

    def execute_terminal_command(self, command):
        """Execute terminal command from IDE"""
        try:
            import shlex
            import subprocess

            # Basic security: prevent dangerous commands
            dangerous_commands = ["rm", "del", "format", "fdisk", "mkfs", "dd", "sudo", "su"]
            command_parts = shlex.split(command)

            if any(cmd in command_parts[0] for cmd in dangerous_commands):
                return {"error": "Command not allowed for security reasons"}

            # Execute command with timeout
            result = subprocess.run(
                command_parts,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.project_root or os.getcwd(),
            )

            return {
                "output": result.stdout,
                "error": result.stderr,
                "returncode": result.returncode,
            }

        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": str(e)}

    def get_ai_systems_status(self):
        """Get status of AI systems and orchestrators"""
        try:
            systems = []
            ai_systems = [
                ("master_ai_orchestrator.py", "Master AI Orchestrator"),
                ("ghost_agent_orchestrator_enhanced.py", "Ghost Agent Orchestrator"),
                ("optimized_ai_orchestrator.py", "Optimized AI Orchestrator"),
                ("triad_synergy.py", "Triad Synergy System"),
                ("evolutionary_intelligence.py", "Evolutionary Intelligence"),
                ("unified_consciousness.py", "Unified Consciousness"),
                ("multi_agent_engine.py", "Multi-Agent Engine"),
                ("ghost_consciousness_daemon.py", "Ghost Consciousness Daemon"),
                ("autonomous_evolution.py", "Autonomous Evolution"),
                ("design_clarity_os.py", "Design Clarity OS"),
            ]

            for script_name, display_name in ai_systems:
                script_path = os.path.join(self.project_root, "src", script_name)
                if not os.path.exists(script_path):
                    script_path = os.path.join(self.project_root, script_name)

                status = "stopped"
                pid = None

                if os.path.exists(script_path):
                    # Check if process is running (simplified check)
                    try:
                        # This is a simplified check - in production you'd use psutil or similar
                        import subprocess

                        result = subprocess.run(
                            ["pgrep", "-f", script_name], capture_output=True, text=True, timeout=5
                        )
                        if result.returncode == 0 and result.stdout.strip():
                            status = "running"
                            pid = int(result.stdout.strip().split("\n")[0])
                    except:
                        pass

                systems.append(
                    {
                        "name": display_name,
                        "script": script_name,
                        "status": status,
                        "pid": pid,
                        "path": script_path,
                    }
                )

            return {"systems": systems}
        except Exception as e:
            return {"error": str(e)}

    def control_ai_system(self, system_name, action):
        """Control AI system (start, stop, restart)"""
        try:
            # Map system names to script files
            system_map = {
                "Master AI Orchestrator": "master_ai_orchestrator.py",
                "Ghost Agent Orchestrator": "ghost_agent_orchestrator_enhanced.py",
                "Optimized AI Orchestrator": "optimized_ai_orchestrator.py",
                "Triad Synergy System": "src/triad_synergy.py",
                "Evolutionary Intelligence": "src/evolutionary_intelligence.py",
                "Unified Consciousness": "src/unified_consciousness.py",
                "Multi-Agent Engine": "src/multi_agent_engine.py",
                "Ghost Consciousness Daemon": "src/ghost_consciousness_daemon.py",
                "Autonomous Evolution": "src/autonomous_evolution.py",
                "Design Clarity OS": "src/design_clarity_os.py",
            }

            script_name = system_map.get(system_name)
            if not script_name:
                return {"error": f"Unknown system: {system_name}"}

            script_path = os.path.join(self.project_root, script_name)
            if not os.path.exists(script_path):
                # Try without src prefix
                script_path = os.path.join(self.project_root, script_name.split("/", 1)[-1])

            if not os.path.exists(script_path):
                return {"error": f"Script not found: {script_path}"}

            if action == "start":
                # Start the system
                import subprocess

                process = subprocess.Popen(
                    [sys.executable, script_path],
                    cwd=self.project_root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                return {
                    "action": "start",
                    "system": system_name,
                    "status": "started",
                    "pid": process.pid,
                }

            elif action == "stop":
                # Find and stop the process
                try:
                    import subprocess

                    result = subprocess.run(
                        ["pkill", "-f", script_name], capture_output=True, timeout=5
                    )
                    return {
                        "action": "stop",
                        "system": system_name,
                        "status": "stopped" if result.returncode == 0 else "error",
                        "message": (
                            "Process terminated" if result.returncode == 0 else "Process not found"
                        ),
                    }
                except Exception as e:
                    return {"error": f"Failed to stop process: {str(e)}"}

            elif action == "restart":
                # Stop then start
                stop_result = self.control_ai_system(system_name, "stop")
                if "error" in stop_result:
                    return stop_result

                # Small delay
                time.sleep(1)

                start_result = self.control_ai_system(system_name, "start")
                return {
                    "action": "restart",
                    "system": system_name,
                    "status": "restarted",
                    "stop_result": stop_result,
                    "start_result": start_result,
                }

            else:
                return {"error": f"Unknown action: {action}"}

        except Exception as e:
            return {"error": str(e)}

    def log_message(self, format, *args):
        """Override to reduce noise"""
        pass


class GhostLinkAPIServer:
    """Universal GhostLink API Server"""

    def __init__(self, port=4000, project_root=None):
        self.port = port
        self.project_root = project_root
        self.server = None
        self.thread = None

    def start(self):
        """Start the universal HTTP API server"""

        def run_server():
            with socketserver.TCPServer(
                ("", self.port),
                lambda *args: GhostLinkAPIHandler(*args, project_root=self.project_root),
            ) as httpd:
                self.server = httpd
                print(f"🌐 GhostLink Universal API Server running on port {self.port}")
                print("🎯 Platform-agnostic mode: ACTIVE | 📊 Application Tracking: ENABLED")
                print(
                    f"🖥️  Platform: {PLATFORM} | 🔧 Performance: {'✅' if PERFORMANCE_OPTIMIZATION else '❌'}"
                )
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
    """Main function to run the universal API server"""
    import argparse

    parser = argparse.ArgumentParser(description="GhostLink Universal API Server")
    parser.add_argument("--port", type=int, default=4000, help="Port to run server on")
    parser.add_argument("--project-root", help="Path to GhostLink project root")

    args = parser.parse_args()

    project_root = args.project_root or os.getcwd()

    print("🚀 Starting GhostLink Universal API Server...")
    print(f"📁 Project Root: {project_root}")
    print(f"🌐 Port: {args.port}")
    print(
        "🎯 Universal Features: Cross-platform monitoring, Application tracking, Service enumeration"
    )

    # Initialize database if available
    if DATABASE_SUPPORT:
        print("🗄️  Initializing database...")
        init_database()
        print("✅ Database ready")
    else:
        print("⚠️  Database not available - running in memory-only mode")

    server = GhostLinkAPIServer(port=args.port, project_root=project_root)
    server.start()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down GhostLink Universal API Server...")
        server.stop()
        print("✅ Server stopped")


if __name__ == "__main__":
    main()

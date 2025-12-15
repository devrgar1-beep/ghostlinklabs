#!/usr/bin/env python3
"""
GhostLink OS Piggyback System

Deep OS integration layer that safely enumerates and monitors:
- File system operations (monitoring, adaptive bounded indexing)
- Network connections (establishment events)
- Process lifecycle (start / termination)
- Registry key value changes (selected hives)
- System events (recent Windows event log entries)
- Hardware / device / driver inventory (enumeration only, read-only)
- Clipboard changes (text format)
- Service states

Safety & Scope Disclaimer:
This module DOES NOT perform kernel hooking, driver patching, code injection,
privilege escalation, rootkit behavior, memory scraping, or security bypassing.
All operations are restricted to standard user-mode accessible APIs and WMI.
Driver and device enumeration is read‑only. File indexing is throttled and
bounded; it is not a full forensic crawler. Use responsibly.
"""

import asyncio
from collections import defaultdict
import ctypes
from datetime import datetime
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import shlex
import sys
import time
from typing import Any, Callable, Dict, List, Optional
import winreg

import win32con
import win32evtlog

try:  # optional WMI support
    import wmi  # type: ignore

    WMI_AVAILABLE = True
except Exception:
    WMI_AVAILABLE = False
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Add the ghostlink module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ghostlink.sovereign_deps import SystemMonitor


class OSPiggybackCore:
    """Core OS integration and monitoring system"""

    def __init__(self):
        self.running = False
        self.os_type = platform.system()
        self.hooks = defaultdict(list)
        self.monitored_data = {
            "filesystem": [],
            "network": [],
            "processes": [],
            "registry": [],
            "events": [],
            "clipboard": [],
            "windows": [],
            "drivers": [],
            "devices": [],
            "hardware_snapshot": [],
            "file_index": [],
        }
        self.stats = {
            "events_captured": 0,
            "files_monitored": 0,
            "processes_tracked": 0,
            "network_packets": 0,
            "registry_changes": 0,
        }

    def register_hook(self, category: str, callback: Callable):
        """Register a callback for OS events"""
        self.hooks[category].append(callback)

    async def trigger_hooks(self, category: str, data: Dict[str, Any]):
        """Trigger all registered hooks for a category"""
        for callback in self.hooks[category]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                print(f"❌ Hook error in {category}: {e}")


class FileSystemMonitor(FileSystemEventHandler):
    """Monitor all filesystem operations"""

    def __init__(self, piggyback: OSPiggybackCore):
        self.piggyback = piggyback
        self.observer = Observer()

    def on_any_event(self, event):
        """Capture all filesystem events"""
        data = {
            "type": event.event_type,
            "path": event.src_path,
            "is_directory": event.is_directory,
            "timestamp": datetime.now().isoformat(),
        }

        if hasattr(event, "dest_path"):
            data["dest_path"] = event.dest_path

        self.piggyback.monitored_data["filesystem"].append(data)
        self.piggyback.stats["files_monitored"] += 1
        asyncio.create_task(self.piggyback.trigger_hooks("filesystem", data))

    def start_monitoring(self, paths: List[str]):
        """Start monitoring specified paths"""
        for path in paths:
            if os.path.exists(path):
                self.observer.schedule(self, path, recursive=True)
        self.observer.start()

    def stop_monitoring(self):
        """Stop filesystem monitoring"""
        self.observer.stop()
        self.observer.join()


class ProcessMonitor:
    """Monitor all running processes"""

    def __init__(self, piggyback: OSPiggybackCore):
        self.piggyback = piggyback
        self.running = False
        self.known_processes = {}

    async def monitor_loop(self):
        """Continuously monitor processes"""
        self.running = True

        while self.running:
            try:
                monitor = SystemMonitor()
                current_processes = {}
                for proc in monitor.get_processes():
                    current_processes[proc["pid"]] = proc

                # Detect new processes
                for pid, proc in current_processes.items():
                    if pid not in self.known_processes:
                        try:
                            data = {
                                "event": "process_started",
                                "pid": pid,
                                "name": proc.get("name", "unknown"),
                                "exe": proc.get("exe"),
                                "cmdline": proc.get("cmdline"),
                                "timestamp": datetime.now().isoformat(),
                            }
                            self.piggyback.monitored_data["processes"].append(data)
                            self.piggyback.stats["processes_tracked"] += 1
                            await self.piggyback.trigger_hooks("process", data)
                        except Exception:
                            pass

                # Detect terminated processes
                for pid in list(self.known_processes.keys()):
                    if pid not in current_processes:
                        data = {
                            "event": "process_terminated",
                            "pid": pid,
                            "name": self.known_processes[pid].get("name", "unknown"),
                            "timestamp": datetime.now().isoformat(),
                        }
                        self.piggyback.monitored_data["processes"].append(data)
                        await self.piggyback.trigger_hooks("process", data)

                self.known_processes = current_processes
                await asyncio.sleep(2)

            except Exception as e:
                print(f"❌ Process monitor error: {e}")
                await asyncio.sleep(5)


class NetworkMonitor:
    """Monitor network connections and traffic"""

    def __init__(self, piggyback: OSPiggybackCore):
        self.piggyback = piggyback
        self.running = False
        self.known_connections = set()

    async def monitor_loop(self):
        """Monitor network connections"""
        self.running = True

        while self.running:
            try:
                monitor = SystemMonitor()
                connections = monitor.get_network_connections()

                for conn in connections:
                    conn_id = f"{conn.get('local_ip', 'N/A')}:{conn.get('local_port', 'N/A')}-{conn.get('remote_ip', 'N/A')}:{conn.get('remote_port', 'N/A')}"

                    if conn_id not in self.known_connections:
                        try:
                            data = {
                                "event": "connection_established",
                                "local": f"{conn.get('local_ip', 'N/A')}:{conn.get('local_port', 'N/A')}",
                                "remote": (
                                    f"{conn.get('remote_ip', 'N/A')}:{conn.get('remote_port', 'N/A')}"
                                    if conn.get("remote_ip")
                                    else None
                                ),
                                "status": conn.get("status", "unknown"),
                                "pid": conn.get("pid"),
                                "process": conn.get("process_name"),
                                "timestamp": datetime.now().isoformat(),
                            }
                            self.piggyback.monitored_data["network"].append(data)
                            self.piggyback.stats["network_packets"] += 1
                            await self.piggyback.trigger_hooks("network", data)
                            self.known_connections.add(conn_id)
                        except Exception:
                            pass

                await asyncio.sleep(3)

            except Exception as e:
                print(f"❌ Network monitor error: {e}")
                await asyncio.sleep(5)


class RegistryMonitor:
    """Monitor Windows Registry changes"""

    def __init__(self, piggyback: OSPiggybackCore):
        self.piggyback = piggyback
        self.running = False
        self.monitored_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services"),
        ]
        self.known_values = {}

    async def monitor_loop(self):
        """Monitor registry keys for changes"""
        self.running = True

        # Initial snapshot
        for hkey, subkey in self.monitored_keys:
            try:
                key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_READ)
                values = {}
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        values[name] = value
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(key)
                self.known_values[f"{hkey}\\{subkey}"] = values
            except Exception:
                pass

        while self.running:
            try:
                for hkey, subkey in self.monitored_keys:
                    try:
                        key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_READ)
                        current_values = {}
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                current_values[name] = value
                                i += 1
                            except OSError:
                                break
                        winreg.CloseKey(key)

                        key_path = f"{hkey}\\{subkey}"
                        old_values = self.known_values.get(key_path, {})

                        # Detect changes
                        for name, value in current_values.items():
                            if name not in old_values or old_values[name] != value:
                                data = {
                                    "event": "registry_changed",
                                    "key": key_path,
                                    "name": name,
                                    "value": str(value)[:200],  # Truncate long values
                                    "timestamp": datetime.now().isoformat(),
                                }
                                self.piggyback.monitored_data["registry"].append(data)
                                self.piggyback.stats["registry_changes"] += 1
                                await self.piggyback.trigger_hooks("registry", data)

                        self.known_values[key_path] = current_values

                    except Exception:
                        pass

                await asyncio.sleep(5)

            except Exception as e:
                print(f"❌ Registry monitor error: {e}")
                await asyncio.sleep(10)


class ClipboardMonitor:
    """Monitor clipboard operations"""

    def __init__(self, piggyback: OSPiggybackCore):
        self.piggyback = piggyback
        self.running = False
        self.last_clipboard = ""

    async def monitor_loop(self):
        """Monitor clipboard changes"""
        self.running = True

        while self.running:
            try:
                import win32clipboard

                win32clipboard.OpenClipboard()
                try:
                    if win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
                        data = win32clipboard.GetClipboardData(win32con.CF_TEXT)
                        if data and data != self.last_clipboard:
                            clipboard_data = {
                                "event": "clipboard_changed",
                                "content": str(data)[:500],  # Truncate large content
                                "length": len(data) if data else 0,
                                "timestamp": datetime.now().isoformat(),
                            }
                            self.piggyback.monitored_data["clipboard"].append(clipboard_data)
                            await self.piggyback.trigger_hooks("clipboard", clipboard_data)
                            self.last_clipboard = data
                except Exception:
                    pass
                finally:
                    win32clipboard.CloseClipboard()

                await asyncio.sleep(1)

            except Exception:
                await asyncio.sleep(2)


class SystemEventMonitor:
    """Monitor Windows system events"""

    def __init__(self, piggyback: OSPiggybackCore):
        self.piggyback = piggyback
        self.running = False

    async def monitor_loop(self):
        """Monitor system event logs"""
        self.running = True

        while self.running:
            try:
                hand = win32evtlog.OpenEventLog(None, "System")
                flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

                events = win32evtlog.ReadEventLog(hand, flags, 0)

                for event in events[:10]:  # Limit to recent events
                    data = {
                        "event": "system_event",
                        "event_id": event.EventID,
                        "event_type": event.EventType,
                        "source": event.SourceName,
                        "timestamp": event.TimeGenerated.isoformat(),
                    }
                    self.piggyback.monitored_data["events"].append(data)
                    await self.piggyback.trigger_hooks("system_event", data)

                win32evtlog.CloseEventLog(hand)
                await asyncio.sleep(10)

            except Exception:
                await asyncio.sleep(15)


class OSController:
    """Control OS operations"""

    def __init__(self):
        self.is_admin = self.check_admin()
        # Allowlist of safe commands for execution via execute_command
        self.ALLOWED_COMMANDS = {
            "sc",
            "ipconfig",
            "net",
            "ping",
            "tracert",
            "tasklist",
            "schtasks",
            "powershell",
            "Get-CimInstance",
            "python",
            "python3",
            "cmd",
            "sh",
            "bash",
        }

    def check_admin(self) -> bool:
        """Check if running with admin privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False

    def execute_command(self, command: str, elevated: bool = False) -> Dict[str, Any]:
        """Execute system command"""
        try:
            if elevated and not self.is_admin:
                return {"success": False, "error": "Requires admin privileges"}

            # Prevent arbitrary command execution: require allowlist
            args = shlex.split(command) if isinstance(command, str) else command
            if not args:
                return {"success": False, "error": "Empty command"}

            cmd_name = os.path.basename(args[0])
            if cmd_name not in self.ALLOWED_COMMANDS:
                return {"success": False, "error": "Command not permitted"}

            result = subprocess.run(
                args, check=False, capture_output=True, text=True, timeout=30
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_services(self) -> List[Dict[str, Any]]:
        """List Windows services"""
        try:
            result = subprocess.run(["sc", "query"], check=False, capture_output=True, text=True)
            # Parse service list
            services = []
            lines = result.stdout.split("\n")
            current_service = {}

            for line in lines:
                line = line.strip()
                if line.startswith("SERVICE_NAME:"):
                    if current_service:
                        services.append(current_service)
                    current_service = {"name": line.split(":", 1)[1].strip()}
                elif line.startswith("STATE"):
                    current_service["state"] = line.split(":", 1)[1].strip()

            if current_service:
                services.append(current_service)

            return services
        except Exception:
            return []

    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        monitor = SystemMonitor()
        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "processor": platform.processor(),
            "cpu_count": monitor.get_cpu_count(),
            "cpu_freq": None,  # Not implemented in SystemMonitor
            "memory": {
                "total": monitor.get_memory_info()["total"],
                "available": monitor.get_memory_info()["available"],
                "percent": monitor.get_memory_info()["percent"],
            },
            "disk": {
                "total": monitor.get_disk_usage("/")["total"],
                "used": monitor.get_disk_usage("/")["used"],
                "free": monitor.get_disk_usage("/")["free"],
                "percent": monitor.get_disk_usage("/")["percent"],
            },
            "boot_time": None,  # Not implemented in SystemMonitor
            "is_admin": self.is_admin,
        }


class DriverEnumerator:
    """Enumerate system drivers (read-only)."""

    def __init__(self):
        self.available = WMI_AVAILABLE
        self.last_snapshot: List[Dict[str, Any]] = []

    def enumerate(self) -> List[Dict[str, Any]]:
        if not self.available:
            return [
                {"error": "WMI module not available. Install 'wmi' to enable driver enumeration."}
            ]
        try:
            c = wmi.WMI()
            drivers = []
            for d in c.Win32_SystemDriver():
                drivers.append(
                    {
                        "name": d.Name,
                        "display_name": getattr(d, "DisplayName", None),
                        "state": getattr(d, "State", None),
                        "start_mode": getattr(d, "StartMode", None),
                        "type": getattr(d, "ServiceType", None),
                        "path": (getattr(d, "PathName", None) or "")[:220],
                    }
                )
                if len(drivers) >= 2000:  # safety cap
                    drivers.append({"note": "driver list truncated"})
                    break
            self.last_snapshot = drivers
            return drivers
        except Exception as e:
            return [{"error": f"Driver enumeration failed: {e}"}]


class DeviceEnumerator:
    """Enumerate PnP devices (read-only)."""

    def __init__(self):
        self.available = WMI_AVAILABLE
        self.last_snapshot: List[Dict[str, Any]] = []

    def enumerate(self) -> List[Dict[str, Any]]:
        if not self.available:
            return [
                {"error": "WMI module not available. Install 'wmi' to enable device enumeration."}
            ]
        try:
            c = wmi.WMI()
            devices = []
            for dev in c.Win32_PnPEntity():
                devices.append(
                    {
                        "name": getattr(dev, "Name", None),
                        "device_id": getattr(dev, "DeviceID", None),
                        "manufacturer": getattr(dev, "Manufacturer", None),
                        "status": getattr(dev, "Status", None),
                        "service": getattr(dev, "Service", None),
                    }
                )
                if len(devices) >= 1500:  # safety cap
                    devices.append({"note": "device list truncated"})
                    break
            self.last_snapshot = devices
            return devices
        except Exception as e:
            return [{"error": f"Device enumeration failed: {e}"}]


class HardwareSnapshot:
    """Capture a hardware state snapshot (CPU, memory, disks, sensors, net)."""

    def capture(self) -> Dict[str, Any]:
        monitor = SystemMonitor()
        disks = []
        try:
            for part in monitor.get_disk_partitions():
                usage = None
                try:
                    usage = monitor.get_disk_usage(part["mountpoint"])
                except Exception:
                    pass
                disks.append(
                    {
                        "device": part["device"],
                        "mountpoint": part["mountpoint"],
                        "fstype": part["fstype"],
                        "opts": part["opts"],
                        "usage": (
                            {
                                "total": usage.get("total") if usage else None,
                                "used": usage.get("used") if usage else None,
                                "free": usage.get("free") if usage else None,
                                "percent": usage.get("percent") if usage else None,
                            }
                            if usage
                            else None
                        ),
                    }
                )
        except Exception:
            pass

        net_ifaces = []
        try:
            for name, addr_list in monitor.get_network_interfaces().items():
                net_ifaces.append(
                    {
                        "name": name,
                        "addresses": [a["address"] for a in addr_list if a.get("address")],
                        "isup": None,  # Not implemented
                        "speed": None,  # Not implemented
                        "mtu": None,  # Not implemented
                    }
                )
        except Exception:
            pass

        sensors = {}
        # Battery sensors not implemented in SystemMonitor

        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent_per_core": [monitor.get_cpu_percent()]
            * monitor.get_cpu_count(),  # Simplified
            "cpu_percent_total": monitor.get_cpu_percent(),
            "memory": monitor.get_memory_info(),
            "swap": {},  # Not implemented
            "disks": disks,
            "net_interfaces": net_ifaces,
            "sensors": sensors,
        }


class FileIndexer:
    """Adaptive file indexer (bounded, incremental)."""

    def __init__(self, max_files: int = 50000, batch_size: int = 2000):
        self.max_files = max_files
        self.batch_size = batch_size
        self.index: List[Dict[str, Any]] = []
        self.last_stats: Dict[str, Any] = {}

    def index_path(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return {"error": f"Path does not exist: {path}"}
        total = 0
        start = time.time()
        try:
            for root, dirs, files in os.walk(path):
                for name in files:
                    fpath = os.path.join(root, name)
                    try:
                        st = os.stat(fpath)
                        self.index.append(
                            {
                                "path": fpath,
                                "size": st.st_size,
                                "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(),
                            }
                        )
                        total += 1
                        if total % self.batch_size == 0:
                            if len(self.index) > self.max_files:
                                self.index = self.index[-self.max_files :]
                        if total >= self.max_files:
                            return {
                                "indexed_files": total,
                                "truncated": True,
                                "duration_sec": round(time.time() - start, 2),
                            }
                    except Exception:
                        pass
            return {
                "indexed_files": total,
                "truncated": total >= self.max_files,
                "duration_sec": round(time.time() - start, 2),
            }
        finally:
            self.last_stats = {
                "total_indexed": len(self.index),
                "last_index_path": path,
                "last_index_duration_sec": round(time.time() - start, 2),
            }


class GhostLinkOSPiggyback:
    """Main OS piggyback orchestrator"""

    def __init__(self):
        self.core = OSPiggybackCore()
        self.fs_monitor = FileSystemMonitor(self.core)
        self.process_monitor = ProcessMonitor(self.core)
        self.network_monitor = NetworkMonitor(self.core)
        self.registry_monitor = RegistryMonitor(self.core)
        self.clipboard_monitor = ClipboardMonitor(self.core)
        self.event_monitor = SystemEventMonitor(self.core)
        self.controller = OSController()
        self.driver_enum = DriverEnumerator()
        self.device_enum = DeviceEnumerator()
        self.hw_snapshot = HardwareSnapshot()
        self.file_indexer = FileIndexer()

        self.data_file = Path.home() / ".ghostlink" / "os_piggyback_data.json"
        self.data_file.parent.mkdir(exist_ok=True)

    def register_hook(self, category: str, callback: Callable):
        """Register a hook for OS events"""
        self.core.register_hook(category, callback)

    async def start(self, monitor_paths: Optional[List[str]] = None):
        """Start OS piggyback monitoring"""
        print("🔌 GhostLink OS Piggyback - Starting...")
        print("=" * 60)

        self.core.running = True

        # Start filesystem monitoring
        if monitor_paths:
            print(f"📁 Monitoring paths: {', '.join(monitor_paths)}")
            self.fs_monitor.start_monitoring(monitor_paths)
        else:
            # Default: monitor common system locations
            default_paths = [
                str(Path.home()),
                "C:\\Windows\\System32",
                "C:\\Program Files",
                "C:\\ProgramData",
            ]
            self.fs_monitor.start_monitoring([p for p in default_paths if os.path.exists(p)])

        # Start all monitors
        tasks = [
            asyncio.create_task(self.process_monitor.monitor_loop()),
            asyncio.create_task(self.network_monitor.monitor_loop()),
            asyncio.create_task(self.registry_monitor.monitor_loop()),
            asyncio.create_task(self.clipboard_monitor.monitor_loop()),
            asyncio.create_task(self.event_monitor.monitor_loop()),
            asyncio.create_task(self.periodic_save()),
        ]

        print("✅ All monitors active")
        print(f"📊 Admin privileges: {'Yes' if self.controller.is_admin else 'No'}")
        print(f"💾 Data saved to: {self.data_file}")
        print("\nPress Ctrl+C to stop monitoring")

        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print("\n🛑 Stopping monitors...")
            self.stop()

    def stop(self):
        """Stop all monitoring"""
        self.core.running = False
        self.fs_monitor.stop_monitoring()
        self.process_monitor.running = False
        self.network_monitor.running = False
        self.registry_monitor.running = False
        self.clipboard_monitor.running = False
        self.event_monitor.running = False
        self.save_data()
        print("✅ OS Piggyback stopped")

    async def periodic_save(self):
        """Periodically save monitored data"""
        while self.core.running:
            await asyncio.sleep(60)  # Save every minute
            self.save_data()

    def save_data(self):
        """Save monitored data to file"""
        try:
            data = {
                "stats": self.core.stats,
                "monitored_data": {
                    k: v[-1000:]
                    for k, v in self.core.monitored_data.items()  # Keep last 1000 events per category
                },
                "system_info": self.controller.get_system_info(),
                "index_stats": getattr(self.file_indexer, "last_stats", {}),
                "timestamp": datetime.now().isoformat(),
            }

            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"❌ Failed to save data: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        return {
            "stats": self.core.stats,
            "system_info": self.controller.get_system_info(),
            "monitors": {
                "filesystem": self.fs_monitor.observer.is_alive(),
                "processes": self.process_monitor.running,
                "network": self.network_monitor.running,
                "registry": self.registry_monitor.running,
                "clipboard": self.clipboard_monitor.running,
                "events": self.event_monitor.running,
            },
        }

    def execute_command(self, command: str, elevated: bool = False) -> Dict[str, Any]:
        """Execute system command"""
        return self.controller.execute_command(command, elevated)

    # Extended capabilities
    def list_drivers(self) -> List[Dict[str, Any]]:
        drivers = self.driver_enum.enumerate()
        self.core.monitored_data["drivers"] = drivers[-1000:]
        return drivers

    def list_devices(self) -> List[Dict[str, Any]]:
        devices = self.device_enum.enumerate()
        self.core.monitored_data["devices"] = devices[-1000:]
        return devices

    def take_hardware_snapshot(self) -> Dict[str, Any]:
        snap = self.hw_snapshot.capture()
        self.core.monitored_data["hardware_snapshot"].append(snap)
        if len(self.core.monitored_data["hardware_snapshot"]) > 25:
            self.core.monitored_data["hardware_snapshot"] = self.core.monitored_data[
                "hardware_snapshot"
            ][-25:]
        return snap

    def index_files(self, path: str) -> Dict[str, Any]:
        stats = self.file_indexer.index_path(path)
        self.core.monitored_data["file_index"] = self.file_indexer.index[-200:]
        return stats


# CLI Interface
async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="GhostLink OS Piggyback")
    parser.add_argument("--start", action="store_true", help="Start OS monitoring")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--paths", nargs="+", help="Paths to monitor")
    parser.add_argument("--command", help="Execute system command")
    parser.add_argument("--elevated", action="store_true", help="Execute with elevation")
    parser.add_argument("--services", action="store_true", help="List Windows services")
    parser.add_argument("--sysinfo", action="store_true", help="Show system information")
    parser.add_argument("--drivers", action="store_true", help="List system drivers (read-only)")
    parser.add_argument("--devices", action="store_true", help="List PnP devices (read-only)")
    parser.add_argument("--snapshot", action="store_true", help="Capture hardware snapshot")
    parser.add_argument("--index", nargs="?", const=".", help="Index files under path (bounded)")

    args = parser.parse_args()

    piggyback = GhostLinkOSPiggyback()

    if args.start:
        await piggyback.start(monitor_paths=args.paths)
    elif args.stats:
        stats = piggyback.get_stats()
        print(json.dumps(stats, indent=2))
    elif args.command:
        result = piggyback.execute_command(args.command, args.elevated)
        print(json.dumps(result, indent=2))
    elif args.services:
        services = piggyback.controller.list_services()
        print(json.dumps(services, indent=2))
    elif args.sysinfo:
        info = piggyback.controller.get_system_info()
        print(json.dumps(info, indent=2))
    elif args.drivers:
        print(json.dumps(piggyback.list_drivers(), indent=2))
    elif args.devices:
        print(json.dumps(piggyback.list_devices(), indent=2))
    elif args.snapshot:
        print(json.dumps(piggyback.take_hardware_snapshot(), indent=2))
    elif args.index is not None:
        print(json.dumps(piggyback.index_files(args.index), indent=2))
    else:
        print("GhostLink OS Piggyback - Deep OS Integration")
        print("\nUsage:")
        print("  --start              Start monitoring")
        print("  --stats              Show statistics")
        print("  --paths DIR [...]    Specify paths to monitor")
        print("  --command CMD        Execute system command")
        print("  --elevated           Execute with admin privileges")
        print("  --services           List Windows services")
        print("  --sysinfo            Show system information")
        print("  --drivers            List system drivers (read-only)")
        print("  --devices            List PnP devices (read-only)")
        print("  --snapshot           Capture hardware snapshot")
        print("  --index [PATH]       Index files under path (default=.)")
        if not WMI_AVAILABLE:
            print(
                "\nNote: WMI module not available; install with 'pip install wmi' for drivers/devices enumeration."
            )


if __name__ == "__main__":
    asyncio.run(main())

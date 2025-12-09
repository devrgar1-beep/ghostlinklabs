#!/usr/bin/env python3
"""
Link Universal Bridge Integration
Allows Link to communicate with and control the Universal System Bridge
"""

import os
import sys
import json
import time
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("LinkBridgeIntegration")

class LinkBridgeIntegration:
    """Integration layer between Link and Universal System Bridge"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.bridge_process: Optional[subprocess.Popen] = None
        self.bridge_status = "stopped"
        self.last_bridge_check = 0
        self.bridge_check_interval = 30  # seconds

        # Link CLI interface
        self.link_cli = [str(self.project_root / ".venv" / "bin" / "python3"), "-m", "ghostlink.link_cli"]

    def start_bridge(self) -> bool:
        """Start the Universal System Bridge"""
        try:
            logger.info("🚀 Starting Universal System Bridge...")

            # Start bridge in background
            self.bridge_process = subprocess.Popen([
                str(self.project_root / ".venv" / "bin" / "python3"),
                str(self.project_root / "src" / "universal_system_bridge.py")
            ], cwd=self.project_root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait for bridge to start
            time.sleep(3)

            # Check if bridge is running
            if self.bridge_process.poll() is None:
                self.bridge_status = "running"
                logger.info("✅ Universal System Bridge started")
                return True
            else:
                stdout, stderr = self.bridge_process.communicate()
                logger.error(f"❌ Bridge failed to start: {stderr.decode()}")
                return False

        except Exception as e:
            logger.error(f"❌ Bridge start failed: {e}")
            return False

    def stop_bridge(self) -> bool:
        """Stop the Universal System Bridge"""
        try:
            if self.bridge_process and self.bridge_process.poll() is None:
                logger.info("🛑 Stopping Universal System Bridge...")
                self.bridge_process.terminate()

                # Wait for graceful shutdown
                try:
                    self.bridge_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.bridge_process.kill()
                    self.bridge_process.wait()

                self.bridge_status = "stopped"
                logger.info("✅ Universal System Bridge stopped")
                return True
            else:
                logger.info("ℹ️  Bridge not running")
                return True

        except Exception as e:
            logger.error(f"❌ Bridge stop failed: {e}")
            return False

    def get_bridge_status(self) -> Dict[str, Any]:
        """Get comprehensive bridge status"""
        status = {
            "bridge_status": self.bridge_status,
            "process_running": False,
            "components": {},
            "health_score": 0.0,
            "last_check": self.last_bridge_check
        }

        # Check if bridge process is still running
        if self.bridge_process and self.bridge_process.poll() is None:
            status["process_running"] = True

            # Try to get detailed status (this would need bridge API)
            # For now, return basic status
            status["components"] = {
                "hardware": 2,  # CPU, Memory
                "software": 2,  # API, Link
                "firmware": 1,  # Firmware Manager
                "application": 2,  # VS Code, Wireshark
                "network": 1,  # Network Monitor
                "storage": 1,  # Storage Monitor
                "service": 1,  # Task Scheduler
                "device": 1   # SD Card
            }
            status["health_score"] = 0.95
        else:
            status["bridge_status"] = "stopped"

        self.last_bridge_check = time.time()
        return status

    def send_bridge_command(self, command: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command to the bridge"""
        if not payload:
            payload = {}

        bridge_command = {
            "command": command,
            "payload": payload,
            "timestamp": time.time(),
            "source": "link_integration"
        }

        try:
            # For now, simulate bridge communication
            # In a full implementation, this would use the bridge's API
            result = self._simulate_bridge_command(bridge_command)
            return result

        except Exception as e:
            logger.error(f"Bridge command failed: {e}")
            return {"success": False, "error": str(e)}

    def _simulate_bridge_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate bridge command execution"""
        cmd = command["command"]
        payload = command["payload"]

        if cmd == "get_components":
            return {
                "success": True,
                "components": [
                    {"id": "cpu_monitor", "type": "hardware", "status": "online"},
                    {"id": "memory_monitor", "type": "hardware", "status": "online"},
                    {"id": "ghostlink_api", "type": "software", "status": "online"},
                    {"id": "link_orchestrator", "type": "software", "status": "online"},
                    {"id": "firmware_manager", "type": "firmware", "status": "online"},
                    {"id": "vscode_integration", "type": "application", "status": "online"},
                    {"id": "wireshark_analyzer", "type": "application", "status": "online"},
                    {"id": "network_monitor", "type": "network", "status": "online"},
                    {"id": "storage_monitor", "type": "storage", "status": "online"},
                    {"id": "task_scheduler", "type": "service", "status": "online"},
                    {"id": "sd_card_device", "type": "device", "status": "online"}
                ]
            }

        elif cmd == "get_component_status":
            component_id = payload.get("component_id", "")
            return {
                "success": True,
                "component_id": component_id,
                "status": "online",
                "health_score": 0.95,
                "last_seen": time.time()
            }

        elif cmd == "execute_hardware_action":
            action = payload.get("action", "")
            component = payload.get("component", "")
            logger.info(f"Executing hardware action: {action} on {component}")
            return {"success": True, "action": action, "component": component}

        elif cmd == "execute_software_action":
            action = payload.get("action", "")
            component = payload.get("component", "")
            logger.info(f"Executing software action: {action} on {component}")
            return {"success": True, "action": action, "component": component}

        elif cmd == "execute_firmware_action":
            action = payload.get("action", "")
            component = payload.get("component", "")
            logger.info(f"Executing firmware action: {action} on {component}")
            return {"success": True, "action": action, "component": component}

        elif cmd == "execute_application_action":
            action = payload.get("action", "")
            component = payload.get("component", "")
            logger.info(f"Executing application action: {action} on {component}")
            return {"success": True, "action": action, "component": component}

        else:
            return {"success": False, "error": f"Unknown command: {cmd}"}

    def get_system_overview(self) -> Dict[str, Any]:
        """Get comprehensive system overview through bridge"""
        overview = {
            "timestamp": time.time(),
            "bridge_status": self.get_bridge_status(),
            "system_components": {},
            "active_integrations": [],
            "health_summary": {}
        }

        # Get component information
        components_result = self.send_bridge_command("get_components")
        if components_result["success"]:
            for comp in components_result["components"]:
                comp_type = comp["type"]
                if comp_type not in overview["system_components"]:
                    overview["system_components"][comp_type] = []
                overview["system_components"][comp_type].append(comp)

        # Active integrations
        overview["active_integrations"] = [
            "Link AI Orchestrator",
            "Shell Command Interception",
            "VS Code Integration",
            "Wireshark Packet Analysis",
            "Hardware Monitoring",
            "Firmware Management",
            "Network Monitoring",
            "Storage Management"
        ]

        # Health summary
        bridge_status = overview["bridge_status"]
        overview["health_summary"] = {
            "overall_score": bridge_status.get("health_score", 0.0),
            "components_online": sum(len(comps) for comps in overview["system_components"].values()),
            "bridge_running": bridge_status.get("process_running", False),
            "last_check": bridge_status.get("last_check", 0)
        }

        return overview

    def create_link_task_for_bridge_action(self, action: str, component: str, description: str = "") -> bool:
        """Create a Link task for a bridge action"""
        try:
            task_desc = f"Bridge Action: {action} on {component}"
            if description:
                task_desc += f" - {description}"

            # Determine priority
            priority = "normal"
            if "firmware" in action.lower() or "update" in action.lower():
                priority = "high"
            elif "monitor" in action.lower() or "check" in action.lower():
                priority = "low"

            # Add task via Link CLI
            result = subprocess.run(
                self.link_cli + ["task", "add", task_desc, "--priority", priority],
                capture_output=True, text=True, cwd=self.project_root
            )

            return result.returncode == 0

        except Exception as e:
            logger.error(f"Failed to create Link task: {e}")
            return False

    def execute_system_command_via_bridge(self, command: str, component_type: str = "system") -> Dict[str, Any]:
        """Execute a system command through the bridge"""
        try:
            # Analyze command and route through appropriate component
            if "git" in command.lower():
                result = self.send_bridge_command("execute_software_action", {
                    "action": "git_command",
                    "command": command,
                    "component": "version_control"
                })
            elif "python" in command.lower() or "pip" in command.lower():
                result = self.send_bridge_command("execute_software_action", {
                    "action": "python_command",
                    "command": command,
                    "component": "python_runtime"
                })
            elif "disk" in command.lower() or "storage" in command.lower():
                result = self.send_bridge_command("execute_hardware_action", {
                    "action": "storage_command",
                    "command": command,
                    "component": "storage_monitor"
                })
            elif "network" in command.lower() or "net" in command.lower():
                result = self.send_bridge_command("execute_hardware_action", {
                    "action": "network_command",
                    "command": command,
                    "component": "network_monitor"
                })
            else:
                result = self.send_bridge_command("execute_system_action", {
                    "action": "system_command",
                    "command": command,
                    "component": component_type
                })

            # Create Link task for tracking
            self.create_link_task_for_bridge_action(
                "execute_command",
                component_type,
                f"Executed: {command[:50]}..."
            )

            return result

        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return {"success": False, "error": str(e)}

    def get_component_details(self, component_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific component"""
        return self.send_bridge_command("get_component_status", {"component_id": component_id})

    def perform_system_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive system health check through bridge"""
        health_check = {
            "timestamp": time.time(),
            "bridge_health": self.get_bridge_status(),
            "component_health": {},
            "system_metrics": {},
            "recommendations": []
        }

        # Check key components
        key_components = [
            "cpu_monitor", "memory_monitor", "ghostlink_api",
            "link_orchestrator", "firmware_manager", "network_monitor"
        ]

        for comp_id in key_components:
            comp_health = self.get_component_details(comp_id)
            health_check["component_health"][comp_id] = comp_health

        # Get system metrics
        health_check["system_metrics"] = {
            "cpu_usage": self._get_cpu_usage(),
            "memory_usage": self._get_memory_usage(),
            "disk_usage": self._get_disk_usage(),
            "network_status": self._get_network_status()
        }

        # Generate recommendations
        health_check["recommendations"] = self._generate_recommendations(health_check)

        return health_check

    def _get_cpu_usage(self) -> float:
        """Get current CPU usage"""
        try:
            result = subprocess.run(
                ["ps", "-A", "-o", "%cpu"],
                capture_output=True, text=True
            )
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            total_cpu = sum(float(line.strip()) for line in lines if line.strip())
            return min(100.0, total_cpu)  # Cap at 100%
        except:
            return 0.0

    def _get_memory_usage(self) -> float:
        """Get current memory usage"""
        try:
            result = subprocess.run(
                ["vm_stat"],
                capture_output=True, text=True
            )
            # Parse vm_stat output for memory usage
            lines = result.stdout.split('\n')
            free_pages = 0
            active_pages = 0

            for line in lines:
                if 'Pages free:' in line:
                    free_pages = int(line.split(':')[1].strip().replace('.', ''))
                elif 'Pages active:' in line:
                    active_pages = int(line.split(':')[1].strip().replace('.', ''))

            if free_pages + active_pages > 0:
                return (active_pages / (active_pages + free_pages)) * 100
            return 0.0
        except:
            return 0.0

    def _get_disk_usage(self) -> float:
        """Get current disk usage"""
        try:
            result = subprocess.run(
                ["df", "/"],
                capture_output=True, text=True
            )
            lines = result.stdout.split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 5:
                    usage_str = parts[4].rstrip('%')
                    return float(usage_str)
            return 0.0
        except:
            return 0.0

    def _get_network_status(self) -> str:
        """Get network status"""
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "1", "8.8.8.8"],
                capture_output=True
            )
            return "online" if result.returncode == 0 else "offline"
        except:
            return "unknown"

    def _generate_recommendations(self, health_check: Dict[str, Any]) -> List[str]:
        """Generate health recommendations"""
        recommendations = []

        # CPU recommendations
        cpu_usage = health_check["system_metrics"].get("cpu_usage", 0)
        if cpu_usage > 80:
            recommendations.append("High CPU usage detected - consider optimizing running processes")
        elif cpu_usage > 50:
            recommendations.append("Moderate CPU usage - monitor for performance issues")

        # Memory recommendations
        mem_usage = health_check["system_metrics"].get("memory_usage", 0)
        if mem_usage > 80:
            recommendations.append("High memory usage - consider freeing up memory or adding more RAM")
        elif mem_usage > 60:
            recommendations.append("Moderate memory usage - monitor memory-intensive applications")

        # Disk recommendations
        disk_usage = health_check["system_metrics"].get("disk_usage", 0)
        if disk_usage > 90:
            recommendations.append("Critical disk usage - free up disk space immediately")
        elif disk_usage > 75:
            recommendations.append("High disk usage - consider cleaning up old files")

        # Network recommendations
        network_status = health_check["system_metrics"].get("network_status", "unknown")
        if network_status != "online":
            recommendations.append("Network connectivity issues detected - check network configuration")

        # Component health recommendations
        for comp_id, comp_health in health_check["component_health"].items():
            health_score = comp_health.get("health_score", 1.0)
            if health_score < 0.5:
                recommendations.append(f"Component {comp_id} health is critical - requires immediate attention")
            elif health_score < 0.8:
                recommendations.append(f"Component {comp_id} health is degraded - monitor closely")

        if not recommendations:
            recommendations.append("System health is good - no immediate actions required")

        return recommendations


# Global integration instance
link_bridge = LinkBridgeIntegration()


def main():
    """Main Link Bridge Integration application"""
    import argparse

    parser = argparse.ArgumentParser(description="Link Universal Bridge Integration")
    parser.add_argument("command", choices=[
        "start", "stop", "status", "overview", "health-check",
        "execute", "component-info", "create-task"
    ], help="Command to execute")

    parser.add_argument("--component", help="Component ID for component-info command")
    parser.add_argument("--action", help="Action for execute command")
    parser.add_argument("--payload", help="JSON payload for execute command")
    parser.add_argument("--description", help="Description for create-task command")

    args = parser.parse_args()

    if args.command == "start":
        success = link_bridge.start_bridge()
        if success:
            print("✅ Universal System Bridge started")
        else:
            print("❌ Failed to start Universal System Bridge")
            sys.exit(1)

    elif args.command == "stop":
        success = link_bridge.stop_bridge()
        if success:
            print("✅ Universal System Bridge stopped")
        else:
            print("❌ Failed to stop Universal System Bridge")
            sys.exit(1)

    elif args.command == "status":
        status = link_bridge.get_bridge_status()
        print("🔗 Universal System Bridge Status:")
        print(json.dumps(status, indent=2))

    elif args.command == "overview":
        overview = link_bridge.get_system_overview()
        print("🌐 System Overview:")
        print(json.dumps(overview, indent=2))

    elif args.command == "health-check":
        health = link_bridge.perform_system_health_check()
        print("🏥 System Health Check:")
        print(json.dumps(health, indent=2))

    elif args.command == "execute":
        if not args.action:
            print("❌ --action required for execute command")
            sys.exit(1)

        payload = {}
        if args.payload:
            try:
                payload = json.loads(args.payload)
            except json.JSONDecodeError:
                print("❌ Invalid JSON payload")
                sys.exit(1)

        result = link_bridge.send_bridge_command(args.action, payload)
        print("⚡ Command Execution Result:")
        print(json.dumps(result, indent=2))

    elif args.command == "component-info":
        if not args.component:
            print("❌ --component required for component-info command")
            sys.exit(1)

        info = link_bridge.get_component_details(args.component)
        print(f"📋 Component Information for {args.component}:")
        print(json.dumps(info, indent=2))

    elif args.command == "create-task":
        if not args.action or not args.description:
            print("❌ --action and --description required for create-task command")
            sys.exit(1)

        success = link_bridge.create_link_task_for_bridge_action(
            args.action, "system", args.description
        )
        if success:
            print("✅ Link task created successfully")
        else:
            print("❌ Failed to create Link task")
            sys.exit(1)


if __name__ == "__main__":
    main()

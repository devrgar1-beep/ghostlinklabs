#!/usr/bin/env python3
"""
GhostLink Debug System
Interactive debugging tools for node failures and system issues
"""

import json
import time
import subprocess
import psutil
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class GhostLinkDebugger:
    """Core debugging utilities"""
    
    def __init__(self, log_dir="./logs", trace_dir="./traces"):
        self.log_dir = Path(log_dir)
        self.trace_dir = Path(trace_dir)
        self.debug_history = []
    
    def debug_node(self, node_name: str) -> Dict:
        """Deep debug a specific node"""
        report = {
            "node": node_name,
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # 1. Process check
        proc = self._check_process(node_name)
        report["checks"]["process"] = proc
        
        # 2. Log analysis
        logs = self._analyze_logs(node_name)
        report["checks"]["logs"] = logs
        
        # 3. Port/socket check
        ports = self._check_ports(node_name)
        report["checks"]["ports"] = ports
        
        # 4. Resource usage
        resources = self._check_resources(node_name)
        report["checks"]["resources"] = resources
        
        # 5. Trace analysis
        traces = self._analyze_traces(node_name)
        report["checks"]["traces"] = traces
        
        # 6. Heartbeat verification
        heartbeat = self._verify_heartbeat(node_name)
        report["checks"]["heartbeat"] = heartbeat
        
        # Generate diagnosis
        report["diagnosis"] = self._diagnose(report["checks"])
        report["fix_actions"] = self._suggest_fixes(report["diagnosis"])
        
        self.debug_history.append(report)
        return report
    
    def _check_process(self, node_name: str) -> Dict:
        """Check if process is running"""
        result = {"running": False, "pid": None, "details": {}}
        
        search_patterns = {
            "ColdStack": "coldstack.py",
            "HardwareDaemon": "hardware_daemon.py",
            "DriftGuard": "driftguard.py",
            "ToolHarvester": "toolharvester.py",
            "ResourceSearch": "resourcesearch.py",
            "Manager": "ghostlink_manager.py"
        }
        
        pattern = search_patterns.get(node_name, node_name.lower())
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'status']):
                if proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    if pattern in cmdline:
                        result["running"] = True
                        result["pid"] = proc.info['pid']
                        result["details"] = {
                            "status": proc.info['status'],
                            "cpu_percent": proc.cpu_percent(),
                            "memory_mb": proc.memory_info().rss / 1024 / 1024,
                            "threads": proc.num_threads(),
                            "open_files": len(proc.open_files())
                        }
                        break
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _analyze_logs(self, node_name: str) -> Dict:
        """Analyze recent logs for errors"""
        result = {
            "last_entry": None,
            "errors": [],
            "warnings": [],
            "patterns": {}
        }
        
        log_file = self.log_dir / f"{node_name.lower()}.log"
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()[-100:]  # Last 100 lines
                
                for line in lines:
                    if "ERROR" in line:
                        result["errors"].append(line.strip())
                    elif "WARNING" in line:
                        result["warnings"].append(line.strip())
                    
                    # Pattern detection
                    if "heartbeat" in line.lower():
                        result["patterns"]["heartbeat"] = result["patterns"].get("heartbeat", 0) + 1
                    if "timeout" in line.lower():
                        result["patterns"]["timeout"] = result["patterns"].get("timeout", 0) + 1
                    if "refused" in line.lower() or "connection" in line.lower():
                        result["patterns"]["connection"] = result["patterns"].get("connection", 0) + 1
                
                if lines:
                    result["last_entry"] = lines[-1].strip()
                    # Parse timestamp from last entry
                    try:
                        timestamp_str = lines[-1].split(']')[0][1:]
                        result["last_entry_age_s"] = time.time() - datetime.fromisoformat(timestamp_str).timestamp()
                    except:
                        pass
                        
            except Exception as e:
                result["error"] = str(e)
        else:
            result["error"] = "Log file not found"
        
        return result
    
    def _check_ports(self, node_name: str) -> Dict:
        """Check expected ports/sockets"""
        result = {"listening": [], "established": []}
        
        # Expected ports per node
        expected_ports = {
            "Manager": [8080],  # API port
            "ColdStack": [],    # Uses IPC
            "HardwareDaemon": [9001],  # Hardware monitoring
        }
        
        if node_name in expected_ports:
            for port in expected_ports[node_name]:
                for conn in psutil.net_connections():
                    if conn.laddr.port == port:
                        result["listening" if conn.status == "LISTEN" else "established"].append({
                            "port": port,
                            "status": conn.status,
                            "pid": conn.pid
                        })
        
        return result
    
    def _check_resources(self, node_name: str) -> Dict:
        """Check system resources"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_available_mb": psutil.virtual_memory().available / 1024 / 1024,
            "disk_free_gb": psutil.disk_usage('/').free / 1024 / 1024 / 1024,
            "load_avg": psutil.getloadavg()
        }
    
    def _analyze_traces(self, node_name: str) -> Dict:
        """Analyze trace files for issues"""
        result = {
            "total_events": 0,
            "errors": 0,
            "last_event": None,
            "message_flow": {}
        }
        
        try:
            trace_files = sorted(self.trace_dir.glob("trace_*.jsonl"))
            if trace_files:
                # Check last trace file
                with open(trace_files[-1], 'r') as f:
                    for line in f:
                        event = json.loads(line)
                        if event.get("src") == node_name or event.get("tgt") == node_name:
                            result["total_events"] += 1
                            if event.get("act") == "error":
                                result["errors"] += 1
                            result["last_event"] = event
                            
                            # Track message flow
                            flow_key = f"{event.get('src')}→{event.get('tgt')}"
                            result["message_flow"][flow_key] = result["message_flow"].get(flow_key, 0) + 1
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _verify_heartbeat(self, node_name: str) -> Dict:
        """Verify heartbeat mechanism"""
        result = {
            "expected_interval": None,
            "last_seen": None,
            "missed_count": 0
        }
        
        intervals = {
            "Manager": 30,
            "ColdStack": 5,
            "HardwareDaemon": 6,
            "DriftGuard": 7,
            "ToolHarvester": 8,
            "ResourceSearch": 9
        }
        
        result["expected_interval"] = intervals.get(node_name)
        
        # Check for heartbeat in recent traces
        traces = self._analyze_traces(node_name)
        if traces.get("last_event"):
            if traces["last_event"].get("act") == "heartbeat":
                result["last_seen"] = traces["last_event"].get("ts", 0)
                age = time.time() - result["last_seen"]
                if result["expected_interval"]:
                    result["missed_count"] = int(age / result["expected_interval"])
        
        return result
    
    def _diagnose(self, checks: Dict) -> Dict:
        """Generate diagnosis from checks"""
        diagnosis = {
            "status": "unknown",
            "issues": [],
            "root_cause": None
        }
        
        # Process not running
        if not checks["process"]["running"]:
            diagnosis["status"] = "dead"
            diagnosis["issues"].append("Process not running")
            diagnosis["root_cause"] = "process_dead"
        
        # High resource usage
        elif checks["process"].get("details", {}).get("cpu_percent", 0) > 80:
            diagnosis["status"] = "overloaded"
            diagnosis["issues"].append("High CPU usage")
            diagnosis["root_cause"] = "resource_exhaustion"
        
        # Log errors
        elif len(checks["logs"].get("errors", [])) > 0:
            diagnosis["status"] = "error"
            diagnosis["issues"].extend(checks["logs"]["errors"][:3])
            diagnosis["root_cause"] = "application_error"
        
        # Stale heartbeat
        elif checks["heartbeat"].get("missed_count", 0) > 3:
            diagnosis["status"] = "stale"
            diagnosis["issues"].append(f"Missed {checks['heartbeat']['missed_count']} heartbeats")
            diagnosis["root_cause"] = "heartbeat_failure"
        
        # Connection issues
        elif checks["logs"].get("patterns", {}).get("connection", 0) > 5:
            diagnosis["status"] = "disconnected"
            diagnosis["issues"].append("Multiple connection errors")
            diagnosis["root_cause"] = "network_issue"
        
        else:
            diagnosis["status"] = "healthy"
        
        return diagnosis
    
    def _suggest_fixes(self, diagnosis: Dict) -> List[str]:
        """Suggest fix actions based on diagnosis"""
        fixes = []
        
        if diagnosis["root_cause"] == "process_dead":
            fixes.append("restart_node")
            fixes.append("check_startup_logs")
            fixes.append("verify_dependencies")
        
        elif diagnosis["root_cause"] == "resource_exhaustion":
            fixes.append("increase_resources")
            fixes.append("check_memory_leaks")
            fixes.append("scale_horizontally")
        
        elif diagnosis["root_cause"] == "application_error":
            fixes.append("review_error_logs")
            fixes.append("check_configuration")
            fixes.append("rollback_recent_changes")
        
        elif diagnosis["root_cause"] == "heartbeat_failure":
            fixes.append("restart_heartbeat_thread")
            fixes.append("check_event_loop")
            fixes.append("verify_timing_config")
        
        elif diagnosis["root_cause"] == "network_issue":
            fixes.append("check_network_connectivity")
            fixes.append("verify_firewall_rules")
            fixes.append("test_intermesh_bus")
        
        return fixes
    
    def fix_node(self, node_name: str, action: str) -> Dict:
        """Attempt to fix a node issue"""
        result = {"action": action, "success": False, "output": None}
        
        try:
            if action == "restart_node":
                # Kill existing process
                proc_check = self._check_process(node_name)
                if proc_check["pid"]:
                    psutil.Process(proc_check["pid"]).terminate()
                    time.sleep(1)
                
                # Start new process
                script_map = {
                    "ColdStack": "modules/coldstack.py",
                    "HardwareDaemon": "modules/hardware_daemon.py",
                    "DriftGuard": "modules/driftguard.py",
                    "ToolHarvester": "modules/toolharvester.py",
                    "ResourceSearch": "modules/resourcesearch.py"
                }
                
                if node_name in script_map:
                    subprocess.Popen(["python3", script_map[node_name]], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
                    result["success"] = True
                    result["output"] = f"Restarted {node_name}"
            
            elif action == "clear_logs":
                log_file = self.log_dir / f"{node_name.lower()}.log"
                if log_file.exists():
                    log_file.rename(log_file.with_suffix(f".log.{int(time.time())}"))
                    result["success"] = True
                    result["output"] = "Logs rotated"
            
            elif action == "reset_heartbeat":
                # Send manual heartbeat
                from core.intermesh_protocol import heartbeat
                msg = heartbeat(node_name)
                result["success"] = True
                result["output"] = f"Sent heartbeat: {msg.to_json()}"
            
        except Exception as e:
            result["error"] = str(e)
            result["traceback"] = traceback.format_exc()
        
        return result

class DebugConsole:
    """Interactive debug console"""
    
    def __init__(self):
        self.debugger = GhostLinkDebugger()
        self.commands = {
            "status": self.show_status,
            "debug": self.debug_node,
            "fix": self.fix_node,
            "history": self.show_history,
            "monitor": self.monitor_live,
            "trace": self.show_traces,
            "help": self.show_help
        }
    
    def show_status(self, args=None):
        """Show all node status"""
        from node_status_monitor import StatusMonitor
        monitor = StatusMonitor()
        # Simulate real status collection here
        print(monitor.get_status_table())
    
    def debug_node(self, args):
        """Debug specific node"""
        if not args:
            print("Usage: debug <node_name>")
            return
        
        node = args[0]
        report = self.debugger.debug_node(node)
        
        print(f"\n{'='*60}")
        print(f"DEBUG REPORT: {node}")
        print(f"{'='*60}")
        print(f"Status: {report['diagnosis']['status'].upper()}")
        
        if report['diagnosis']['issues']:
            print(f"\nIssues Found:")
            for issue in report['diagnosis']['issues']:
                print(f"  • {issue}")
        
        if report['diagnosis']['root_cause']:
            print(f"\nRoot Cause: {report['diagnosis']['root_cause']}")
        
        if report['fix_actions']:
            print(f"\nSuggested Fixes:")
            for fix in report['fix_actions']:
                print(f"  → {fix}")
        
        print(f"\nDetailed Checks:")
        for check, data in report['checks'].items():
            print(f"  [{check}]: {json.dumps(data, indent=2)}")
    
    def fix_node(self, args):
        """Apply fix to node"""
        if len(args) < 2:
            print("Usage: fix <node_name> <action>")
            print("Actions: restart_node, clear_logs, reset_heartbeat")
            return
        
        node, action = args[0], args[1]
        result = self.debugger.fix_node(node, action)
        
        if result["success"]:
            print(f"✅ Fix applied: {result['output']}")
        else:
            print(f"❌ Fix failed: {result.get('error', 'Unknown error')}")
    
    def show_history(self, args=None):
        """Show debug history"""
        for i, report in enumerate(self.debugger.debug_history):
            print(f"{i}: {report['node']} @ {report['timestamp']} - {report['diagnosis']['status']}")
    
    def monitor_live(self, args=None):
        """Live monitoring mode"""
        print("Starting live monitor... (Ctrl+C to stop)")
        try:
            while True:
                # Clear screen
                print("\033[2J\033[H")
                self.show_status()
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nMonitor stopped")
    
    def show_traces(self, args=None):
        """Show recent traces"""
        traces = self.debugger._analyze_traces(args[0] if args else "Manager")
        print(json.dumps(traces, indent=2))
    
    def show_help(self, args=None):
        """Show help"""
        print("GhostLink Debug Console")
        print("Commands:")
        print("  status           - Show all node status")
        print("  debug <node>     - Debug specific node")
        print("  fix <node> <act> - Apply fix to node")
        print("  history          - Show debug history")
        print("  monitor          - Live monitoring mode")
        print("  trace [node]     - Show trace analysis")
        print("  help             - Show this help")
        print("  quit             - Exit console")
    
    def run(self):
        """Run interactive console"""
        print("GhostLink Debug Console v1.0")
        print("Type 'help' for commands")
        
        while True:
            try:
                cmd_line = input("\n[debug]> ").strip()
                if not cmd_line:
                    continue
                
                if cmd_line == "quit":
                    break
                
                parts = cmd_line.split()
                cmd, args = parts[0], parts[1:] if len(parts) > 1 else []
                
                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    print(f"Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    # Launch debug console
    console = DebugConsole()
    console.run()
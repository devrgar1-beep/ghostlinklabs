#!/usr/bin/env python3
"""
GhostLink Node Status Monitor
Real-time node health and status reporting
"""

import time
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class NodeStatus:
    name: str
    state: str  # running|stopped|error|unknown
    last_heartbeat: float
    heartbeat_interval: int
    messages_sent: int
    messages_received: int
    errors: int
    uptime: float
    capabilities: list
    
    @property
    def health(self) -> str:
        """Calculate health status"""
        if self.state == "error":
            return "❌ CRITICAL"
        
        time_since_heartbeat = time.time() - self.last_heartbeat
        if time_since_heartbeat > self.heartbeat_interval * 3:
            return "⚠️  STALE"
        elif time_since_heartbeat > self.heartbeat_interval * 1.5:
            return "⚡ DELAYED"
        return "✅ HEALTHY"
    
    @property
    def heartbeat_age(self) -> str:
        """Human readable heartbeat age"""
        age = time.time() - self.last_heartbeat
        if age < 1:
            return "now"
        elif age < 60:
            return f"{int(age)}s ago"
        elif age < 3600:
            return f"{int(age/60)}m ago"
        return f"{int(age/3600)}h ago"

class StatusMonitor:
    """Monitor all GhostLink nodes"""
    
    def __init__(self):
        self.nodes: Dict[str, NodeStatus] = {}
        self.start_time = time.time()
        
        # Initialize expected nodes
        self._init_nodes()
    
    def _init_nodes(self):
        """Initialize node configurations"""
        config = {
            "Manager": {"interval": 30, "caps": ["orchestrate", "monitor"]},
            "ColdStack": {"interval": 5, "caps": ["spawn", "stop", "event", "read_state", "write_state"]},
            "HardwareDaemon": {"interval": 6, "caps": ["event", "read_hw"]},
            "DriftGuard": {"interval": 7, "caps": ["event", "analyze"]},
            "ToolHarvester": {"interval": 8, "caps": ["event", "harvest_local"]},
            "ResourceSearch": {"interval": 9, "caps": ["event", "search_local"]}
        }
        
        for name, cfg in config.items():
            self.nodes[name] = NodeStatus(
                name=name,
                state="unknown",
                last_heartbeat=0,
                heartbeat_interval=cfg["interval"],
                messages_sent=0,
                messages_received=0,
                errors=0,
                uptime=0,
                capabilities=cfg["caps"]
            )
    
    def update_heartbeat(self, node: str):
        """Update node heartbeat"""
        if node in self.nodes:
            self.nodes[node].last_heartbeat = time.time()
            if self.nodes[node].state == "unknown":
                self.nodes[node].state = "running"
    
    def update_state(self, node: str, state: str):
        """Update node state"""
        if node in self.nodes:
            self.nodes[node].state = state
            if state == "running":
                self.nodes[node].uptime = time.time()
    
    def record_message(self, src: str, dst: str):
        """Record message between nodes"""
        if src in self.nodes:
            self.nodes[src].messages_sent += 1
        if dst in self.nodes:
            self.nodes[dst].messages_received += 1
    
    def record_error(self, node: str):
        """Record node error"""
        if node in self.nodes:
            self.nodes[node].errors += 1
            self.nodes[node].state = "error"
    
    def get_status_table(self) -> str:
        """Generate status table"""
        lines = []
        lines.append("=" * 80)
        lines.append("GHOSTLINK NODE STATUS")
        lines.append(f"System Uptime: {int(time.time() - self.start_time)}s")
        lines.append(f"Timestamp: {datetime.now().isoformat()}")
        lines.append("=" * 80)
        lines.append("")
        
        # Header
        lines.append(f"{'Node':<15} {'State':<10} {'Health':<12} {'Last HB':<12} {'Msgs↑':<8} {'Msgs↓':<8} {'Errors':<8}")
        lines.append("-" * 80)
        
        # Nodes
        for name, node in self.nodes.items():
            lines.append(
                f"{name:<15} {node.state:<10} {node.health:<12} {node.heartbeat_age:<12} "
                f"{node.messages_sent:<8} {node.messages_received:<8} {node.errors:<8}"
            )
        
        lines.append("")
        
        # Summary
        running = sum(1 for n in self.nodes.values() if n.state == "running")
        errors = sum(1 for n in self.nodes.values() if n.state == "error")
        unknown = sum(1 for n in self.nodes.values() if n.state == "unknown")
        
        lines.append(f"Summary: {running} running | {errors} errors | {unknown} unknown")
        
        # Alerts
        alerts = []
        for name, node in self.nodes.items():
            if node.state == "error":
                alerts.append(f"ERROR: {name} in error state")
            elif node.health == "⚠️  STALE":
                alerts.append(f"WARNING: {name} heartbeat stale")
        
        if alerts:
            lines.append("")
            lines.append("ALERTS:")
            for alert in alerts:
                lines.append(f"  - {alert}")
        
        lines.append("=" * 80)
        return "\n".join(lines)
    
    def get_json_status(self) -> Dict:
        """Get status as JSON"""
        return {
            "timestamp": time.time(),
            "uptime": time.time() - self.start_time,
            "nodes": {
                name: {
                    "state": node.state,
                    "health": node.health,
                    "last_heartbeat": node.last_heartbeat,
                    "heartbeat_age_s": time.time() - node.last_heartbeat,
                    "messages": {
                        "sent": node.messages_sent,
                        "received": node.messages_received
                    },
                    "errors": node.errors,
                    "capabilities": node.capabilities
                }
                for name, node in self.nodes.items()
            },
            "summary": {
                "total": len(self.nodes),
                "running": sum(1 for n in self.nodes.values() if n.state == "running"),
                "errors": sum(1 for n in self.nodes.values() if n.state == "error"),
                "healthy": sum(1 for n in self.nodes.values() if n.health == "✅ HEALTHY")
            }
        }

# Demo simulation
if __name__ == "__main__":
    monitor = StatusMonitor()
    
    # Simulate some activity
    monitor.update_state("Manager", "running")
    monitor.update_heartbeat("Manager")
    
    monitor.update_state("ColdStack", "running")
    monitor.update_heartbeat("ColdStack")
    monitor.record_message("Manager", "ColdStack")
    
    monitor.update_state("HardwareDaemon", "running")
    monitor.update_heartbeat("HardwareDaemon")
    
    monitor.update_state("DriftGuard", "running")
    # Simulate stale heartbeat
    monitor.nodes["DriftGuard"].last_heartbeat = time.time() - 30
    
    monitor.update_state("ToolHarvester", "error")
    monitor.record_error("ToolHarvester")
    
    # ResourceSearch remains unknown (never started)
    
    # Display status
    print(monitor.get_status_table())
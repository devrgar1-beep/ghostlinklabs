#!/usr/bin/env python3
"""GhostLink Network Integration Status

Displays the current state of GhostLink mesh integration with discovered neighbors.
"""
import json
import os
import socket
import subprocess
import time
from datetime import datetime


def get_local_ip() -> str:
    """Get primary local IP address."""
    try:
        result = subprocess.run(
            ["ip", "-br", "addr", "show", "enp0s31f6"],
            capture_output=True,
            text=True,
            timeout=2
        )
        for line in result.stdout.split("\n"):
            if "UP" in line:
                parts = line.split()
                for part in parts:
                    if "/" in part and "." in part:
                        return part.split("/")[0]
    except Exception:
        pass
    return "127.0.0.1"


def check_controller() -> dict:
    """Check if controller is running."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(("127.0.0.1", 7420))
        sock.close()
        return {"active": result == 0, "port": 7420}
    except Exception:
        return {"active": False, "port": 7420}


def check_metrics() -> dict:
    """Check if metrics endpoint is active."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(("127.0.0.1", 9108))
        sock.close()
        
        # Try to fetch a metric sample
        if result == 0:
            import urllib.request
            try:
                response = urllib.request.urlopen("http://127.0.0.1:9108/metrics", timeout=2)
                data = response.read().decode("utf-8")
                # Count metrics
                lines = [l for l in data.split("\n") if l and not l.startswith("#")]
                return {"active": True, "port": 9108, "metric_count": len(lines)}
            except Exception:
                pass
                
        return {"active": result == 0, "port": 9108}
    except Exception:
        return {"active": False, "port": 9108}


def probe_neighbor(ip: str, port: int = 7422, timeout: float = 0.5) -> dict:
    """Probe a neighbor for GhostLink service."""
    result = {"ip": ip, "port": port, "reachable": False, "ghostlink": False, "hostname": None}
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        if sock.connect_ex((ip, port)) == 0:
            result["reachable"] = True
            
            # Try GhostLink protocol
            try:
                sock.sendall(b'{"type":"ping","proto":"glp/0"}\n')
                sock.settimeout(timeout)
                response = sock.recv(1024)
                
                if response:
                    data = json.loads(response.decode("utf-8").strip())
                    if data.get("type") == "pong":
                        result["ghostlink"] = True
                        result["hostname"] = data.get("hostname", "unknown")
            except Exception:
                pass
                
        sock.close()
        
    except Exception:
        pass
        
    return result


def main():
    """Display integration status."""
    print("═" * 70)
    print("   GHOSTLINK NETWORK INTEGRATION STATUS")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 70)
    print()
    
    # Local system
    local_ip = get_local_ip()
    print("[LOCAL SYSTEM]")
    print(f"  IP Address: {local_ip}")
    print(f"  Hostname: {socket.gethostname()}")
    print()
    
    # Controller status
    controller = check_controller()
    print("[CONTROLLER]")
    status = "✓ ACTIVE" if controller["active"] else "✗ OFFLINE"
    print(f"  Status: {status}")
    print(f"  Port: {controller['port']}")
    print()
    
    # Metrics status
    metrics = check_metrics()
    print("[METRICS ENDPOINT]")
    status = "✓ ACTIVE" if metrics["active"] else "✗ OFFLINE"
    print(f"  Status: {status}")
    print(f"  Port: {metrics['port']}")
    if "metric_count" in metrics:
        print(f"  Metrics: {metrics['metric_count']} series")
    print()
    
    # Network neighbors
    neighbors = [
        "192.168.4.1",   # Gateway
        "192.168.4.2",
        "192.168.4.22",
        "192.168.4.23",
        "192.168.4.24",
        "192.168.4.42",
        "192.168.4.45",
        "192.168.4.46",
    ]
    
    print("[NEIGHBOR SCAN]")
    print(f"  Scanning {len(neighbors)} discovered hosts...")
    print()
    
    results = []
    for ip in neighbors:
        if ip == local_ip:
            continue
        result = probe_neighbor(ip)
        results.append(result)
        
    # Display results
    print("[INTEGRATION STATUS]")
    print()
    
    active_peers = 0
    reachable_hosts = 0
    
    for result in results:
        reachable_hosts += 1 if result["reachable"] else 0
        active_peers += 1 if result["ghostlink"] else 0
        
        ip = result["ip"]
        
        if result["ghostlink"]:
            status = "✓ GHOSTLINK PEER"
            hostname = result.get("hostname", "unknown")
            print(f"  {ip:16s} | {status:20s} | {hostname}")
        elif result["reachable"]:
            print(f"  {ip:16s} | ⚠ Port open (no GL) | Potential host")
        else:
            print(f"  {ip:16s} | • Not responding     | Offline/filtered")
    
    print()
    print("─" * 70)
    print(f"  Total Neighbors: {len(neighbors)}")
    print(f"  Reachable: {reachable_hosts}")
    print(f"  GhostLink Peers: {active_peers}")
    print()
    
    if active_peers > 0:
        print("  ✓ Mesh network active with {active_peers} peer(s)")
    else:
        print("  ℹ No GhostLink peers detected")
        print("    Deploy gl_peer_responder.py to neighbors to enable mesh")
    
    print("═" * 70)
    print()


if __name__ == "__main__":
    main()

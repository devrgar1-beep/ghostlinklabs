#!/usr/bin/env python3
"""GhostLink iDRAC Health Monitor - Continuous polling daemon for backbone R630s.

Polls Dell R630 iDRACs via Redfish for:
- Thermal sensors (CPU, ambient, exhaust temps + fan RPMs)
- Power supply status and wattage
- System health and SEL errors
- Firmware versions

Pushes aggregated metrics to GhostLink controller as special "idrac.health" samples.

Usage:
  python3 gl_idrac_monitor.py

Environment:
  CONTROLLER_HOST         Controller IP (default: 127.0.0.1)
  CONTROLLER_PORT         Controller port (default: 7420)
  IDRAC_INVENTORY         Path to inventory file (default: ./idrac_inventory.txt)
  IDRAC_CREDS_FILE        Path to credentials JSON (default: ./creds/idrac_creds.json)
  POLL_INTERVAL           Seconds between polls (default: 30)
  IDRAC_TIMEOUT           iDRAC request timeout (default: 5)
  MAX_WORKERS             Parallel iDRAC polls (default: 16)
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import socket
import sys
import time
from typing import Any

try:
    from gl_idrac import IDRACClient, load_credentials
except ImportError:
    print("[idrac_monitor] Error: gl_idrac.py not found. Run from project root.", file=sys.stderr)
    sys.exit(1)

CONTROLLER_HOST = os.getenv("CONTROLLER_HOST", "127.0.0.1")
CONTROLLER_PORT = int(os.getenv("CONTROLLER_PORT", "7420"))
INVENTORY_FILE = os.getenv("IDRAC_INVENTORY", "idrac_inventory.txt")
CREDS_FILE = os.getenv("IDRAC_CREDS_FILE", "creds/idrac_creds.json")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "30"))
IDRAC_TIMEOUT = int(os.getenv("IDRAC_TIMEOUT", "5"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "16"))


def load_inventory(path: str) -> list[dict[str, str]]:
    """Load iDRAC inventory. Returns list of dicts with hostname, data_ip, idrac_ip, user, location."""
    if not os.path.exists(path):
        return []
    hosts = []
    with open(path) as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            parts = [p.strip() for p in stripped.split(",")]
            if len(parts) >= 3:
                hosts.append({
                    "hostname": parts[0],
                    "data_ip": parts[1] if len(parts) > 1 else "",
                    "idrac_ip": parts[2] if len(parts) > 2 else "",
                    "user": parts[3] if len(parts) > 3 else "root",
                    "location": parts[4] if len(parts) > 4 else "",
                })
    return hosts


def poll_idrac(host_info: dict[str, str], creds: dict[str, dict[str, str]]) -> dict[str, Any]:
    """Poll a single iDRAC and return aggregated health metrics."""
    idrac_ip = host_info["idrac_ip"]
    hostname = host_info["hostname"]
    
    if idrac_ip not in creds:
        return {"error": f"No credentials for {idrac_ip}", "hostname": hostname, "idrac_ip": idrac_ip}
    
    try:
        c = creds[idrac_ip]
        client = IDRACClient(idrac_ip, c["username"], c["password"])
        
        # Gather data
        power_state = client.get_power_state()
        health = client.get_health_status()
        temps = client.get_temperatures()
        fans = client.get_fans()
        psus = client.get_power_supplies()
        
        # Aggregate
        temp_readings = [t["reading_c"] for t in temps if t["reading_c"] is not None]
        fan_rpms = [f["reading_rpm"] for f in fans if f["reading_rpm"] is not None]
        psu_ok = all(p["status"] == "OK" for p in psus)
        total_power_w = sum(p.get("power_output_watts", 0) or 0 for p in psus)
        
        return {
            "hostname": hostname,
            "idrac_ip": idrac_ip,
            "location": host_info.get("location", ""),
            "power_state": power_state,
            "health": health["health"],
            "temp_avg_c": sum(temp_readings) / len(temp_readings) if temp_readings else None,
            "temp_max_c": max(temp_readings) if temp_readings else None,
            "fan_avg_rpm": sum(fan_rpms) / len(fan_rpms) if fan_rpms else None,
            "psu_ok": psu_ok,
            "psu_count": len(psus),
            "total_power_w": total_power_w,
            "poll_time": time.time(),
        }
    except Exception as e:
        return {"error": str(e), "hostname": hostname, "idrac_ip": idrac_ip}


def send_to_controller(samples: list[dict[str, Any]]):
    """Send aggregated iDRAC health samples to controller."""
    if not samples:
        return
    
    payload = {
        "type": "idrac_health",
        "proto": "glp/0",
        "timestamp": time.time(),
        "host_count": len(samples),
        "samples": samples,
    }
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((CONTROLLER_HOST, CONTROLLER_PORT))
            msg = json.dumps(payload, separators=(",", ":")).encode("utf-8") + b"\n"
            s.sendall(msg)
            print(f"[idrac_monitor] Sent {len(samples)} host samples to controller")
    except Exception as e:
        print(f"[idrac_monitor] Failed to send to controller: {e}", file=sys.stderr)


def main():
    """Main monitoring loop."""
    print("[idrac_monitor] GhostLink iDRAC Health Monitor")
    print(f"[idrac_monitor] Controller: {CONTROLLER_HOST}:{CONTROLLER_PORT}")
    print(f"[idrac_monitor] Inventory: {INVENTORY_FILE}")
    print(f"[idrac_monitor] Poll interval: {POLL_INTERVAL}s")
    
    if not os.path.exists(INVENTORY_FILE):
        print(f"[idrac_monitor] Error: Inventory file not found: {INVENTORY_FILE}", file=sys.stderr)
        return 1
    
    if not os.path.exists(CREDS_FILE):
        print(f"[idrac_monitor] Error: Credentials file not found: {CREDS_FILE}", file=sys.stderr)
        return 1
    
    hosts = load_inventory(INVENTORY_FILE)
    if not hosts:
        print(f"[idrac_monitor] No hosts in inventory: {INVENTORY_FILE}", file=sys.stderr)
        return 1
    
    print(f"[idrac_monitor] Monitoring {len(hosts)} iDRAC(s)")
    for h in hosts:
        print(f"  - {h['hostname']} ({h['idrac_ip']}) @ {h['location']}")
    
    creds = load_credentials(CREDS_FILE)
    print(f"[idrac_monitor] Loaded credentials for {len(creds)} host(s)")
    
    try:
        while True:
            start = time.time()
            print(f"[idrac_monitor] Polling {len(hosts)} iDRACs...")
            
            results = []
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
                futs = [ex.submit(poll_idrac, h, creds) for h in hosts]
                for fut in as_completed(futs):
                    result = fut.result()
                    results.append(result)
                    if "error" in result:
                        print(f"  ⚠ {result['hostname']}: {result['error']}")
                    else:
                        health_mark = "✓" if result["health"] == "OK" else "⚠"
                        print(f"  {health_mark} {result['hostname']}: {result['health']}, "
                              f"{result['temp_max_c']:.1f}°C, {result['total_power_w']}W")
            
            # Send to controller
            send_to_controller(results)
            
            elapsed = time.time() - start
            sleep_time = max(0, POLL_INTERVAL - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    except KeyboardInterrupt:
        print("\n[idrac_monitor] Shutting down...")
        return 0


if __name__ == "__main__":
    sys.exit(main())

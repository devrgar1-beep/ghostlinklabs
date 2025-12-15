#!/usr/bin/env python3
import glob
import json
import os
import socket
import sys
import time

# Add the ghostlink module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ghostlink.sovereign_deps import SystemMonitor

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "7420"))


def read_temp_c():
    try:
        monitor = SystemMonitor()
        temps = monitor.get_temperatures(fahrenheit=False)
        if temps:
            vals = [t["current"] for t in temps.values() if t.get("current") is not None]
            if vals:
                return float(sum(vals) / len(vals))
    except Exception:
        pass
    vals = []
    for p in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
        try:
            with open(p) as f:
                v = int(f.read().strip())
                vals.append(v / 1000.0)
        except Exception:
            pass
    if vals:
        return float(sum(vals) / len(vals))
    return None


def send(conn, obj):
    conn.sendall(json.dumps(obj, separators=(",", ":")).encode("utf-8") + b"\n")


def main():
    with socket.create_connection((HOST, PORT), timeout=5) as c:
        send(c, {"type": "hello", "proto": "glp/0", "role": "peer", "mode": "ro"})
        send(
            c,
            {
                "type": "legend",
                "signals": [
                    {"id": "cpu_temp_c", "unit": "C", "tags": ["Δ"]},
                    {"id": "fault", "unit": "code", "tags": ["SCAR"]},
                ],
                "roi": [{"id": "rack.core", "expr": "zone=='core'"}],
            },
        )
        while True:
            temp = read_temp_c()
            if temp is None:
                time.sleep(2)
                continue
            sample = {
                "type": "sample",
                "ts": time.time(),
                "data": {"zone": "core", "cpu_temp_c": temp, "fault": None},
            }
            send(c, sample)
            time.sleep(1)


if __name__ == "__main__":
    main()

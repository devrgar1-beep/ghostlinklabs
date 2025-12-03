#!/usr/bin/env python3
"""GhostLink Peer Responder - Responds to mesh discovery and queries.

Lightweight service that can be deployed on neighbor hosts to provide
thermal data to the mesh network.

Optional iDRAC integration: set IDRAC_HOST to query out-of-band thermal sensors.
"""
import glob
import json
import os
import socket
import time

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "7422"))
IDRAC_HOST = os.getenv("IDRAC_HOST", "").strip()
IDRAC_USER = os.getenv("IDRAC_USER", "root")
IDRAC_PASS = os.getenv("IDRAC_PASS", "")


def read_temp_c() -> float | None:
    """Read system temperature from OS sensors."""
    try:
        import psutil
        temps = getattr(psutil, "sensors_temperatures", lambda **k: None)(fahrenheit=False) or {}
        for arr in temps.values():
            vals = [getattr(t, "current", None) for t in arr]
            vals = [v for v in vals if v is not None]
            if vals:
                return float(sum(vals) / len(vals))
    except Exception:
        pass

    # Fallback to sysfs
    vals = []
    for path in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
        try:
            with open(path) as f:
                val = int(f.read().strip())
                vals.append(val / 1000.0)
        except Exception:
            pass
    if vals:
        return float(sum(vals) / len(vals))

    return None


def read_idrac_temp_c() -> float | None:
    """Read temperature from iDRAC via Redfish if IDRAC_HOST is set."""
    if not IDRAC_HOST or not IDRAC_PASS:
        return None
    
    try:
        import importlib.util
        # Import gl_idrac from parent directory
        spec = importlib.util.spec_from_file_location("gl_idrac", os.path.join(os.path.dirname(__file__), "gl_idrac.py"))
        if not spec or not spec.loader:
            return None
        gl_idrac = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gl_idrac)
        
        client = gl_idrac.IDRACClient(IDRAC_HOST, IDRAC_USER, IDRAC_PASS)
        temps = client.get_temperatures()
        if temps:
            readings = [t["reading_c"] for t in temps if t["reading_c"] is not None]
            if readings:
                return float(sum(readings) / len(readings))
    except Exception as e:
        print(f"[responder] iDRAC query failed: {e}")
    
    return None


def handle_client(conn: socket.socket, addr: tuple):
    """Handle a single client connection."""
    try:
        # Read request
        data = conn.recv(1024)
        if not data:
            return

        request = json.loads(data.decode("utf-8").strip())
        msg_type = request.get("type")

        # Handle different message types
        if msg_type == "ping":
            response = {
                "type": "pong",
                "proto": "glp/0",
                "hostname": socket.gethostname(),
                "version": "1.0.0",
            }

        elif msg_type == "query":
            # Try iDRAC first if configured, fallback to OS sensors
            temp = read_idrac_temp_c()
            if temp is None:
                temp = read_temp_c()
            
            response = {
                "type": "data",
                "proto": "glp/0",
                "hostname": socket.gethostname(),
                "temp": temp,
                "timestamp": time.time(),
                "source": "idrac" if IDRAC_HOST and temp else "os",
            }

        else:
            response = {
                "type": "error",
                "error": f"Unknown message type: {msg_type}",
            }

        # Send response
        msg = json.dumps(response, separators=(",", ":")).encode("utf-8") + b"\n"
        conn.sendall(msg)

    except Exception as e:
        print(f"[responder] Error handling client {addr}: {e}")

    finally:
        conn.close()


def main():
    """Main server loop."""
    hostname = socket.gethostname()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        print("[responder] GhostLink Peer Responder")
        print(f"[responder] Hostname: {hostname}")
        print(f"[responder] Listening on {HOST}:{PORT}")
        if IDRAC_HOST:
            print(f"[responder] iDRAC integration: {IDRAC_HOST} (user: {IDRAC_USER})")
        print("[responder] Ready to respond to mesh queries")

        try:
            while True:
                conn, addr = server.accept()
                print(f"[responder] Connection from {addr[0]}:{addr[1]}")
                handle_client(conn, addr)

        except KeyboardInterrupt:
            print("\n[responder] Shutting down...")


if __name__ == "__main__":
    main()

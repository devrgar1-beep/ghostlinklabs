#!/usr/bin/env python3
"""GhostLink Peer Responder - Responds to mesh discovery and queries.

Lightweight service that can be deployed on neighbor hosts to provide
thermal data to the mesh network.
"""
import json
import os
import socket
import time
import glob

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "7422"))


def read_temp_c() -> float | None:
    """Read system temperature."""
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
            with open(path, "r") as f:
                val = int(f.read().strip())
                vals.append(val / 1000.0)
        except Exception:
            pass
    if vals:
        return float(sum(vals) / len(vals))
        
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
            temp = read_temp_c()
            response = {
                "type": "data",
                "proto": "glp/0",
                "hostname": socket.gethostname(),
                "temp": temp,
                "timestamp": time.time(),
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
        
        print(f"[responder] GhostLink Peer Responder")
        print(f"[responder] Hostname: {hostname}")
        print(f"[responder] Listening on {HOST}:{PORT}")
        print(f"[responder] Ready to respond to mesh queries")
        
        try:
            while True:
                conn, addr = server.accept()
                print(f"[responder] Connection from {addr[0]}:{addr[1]}")
                handle_client(conn, addr)
                
        except KeyboardInterrupt:
            print("\n[responder] Shutting down...")


if __name__ == "__main__":
    main()

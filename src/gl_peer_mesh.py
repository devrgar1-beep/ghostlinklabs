#!/usr/bin/env python3
"""GhostLink Peer Mesh - Multi-host thermal monitoring network.

Discovers and connects to GhostLink peers on the local network,
aggregating thermal data from all discovered neighbors.
"""
import json
import os
import socket
import threading
import time
from typing import Any

# Network configuration
CONTROLLER_HOST = os.getenv("CONTROLLER_HOST", "127.0.0.1")
CONTROLLER_PORT = int(os.getenv("CONTROLLER_PORT", "7420"))
DISCOVERY_PORT = int(os.getenv("DISCOVERY_PORT", "7422"))
MESH_DISCOVERY_INTERVAL = int(os.getenv("MESH_DISCOVERY_INTERVAL", "30"))

# Known neighbor IPs from network scan or environment
_ENV_NEIGHBORS = os.getenv("NEIGHBOR_IPS", "").strip()
_NEIGHBORS_FILE = os.getenv("NEIGHBORS_FILE", "").strip()

def _load_neighbors_from_file(path: str) -> list[str]:
    out: list[str] = []
    try:
        with open(path) as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#"):  # comments
                    continue
                out.append(s)
    except Exception:
        pass
    return out

if _ENV_NEIGHBORS:
    NEIGHBOR_IPS = [ip.strip() for ip in _ENV_NEIGHBORS.split(",") if ip.strip()]
elif _NEIGHBORS_FILE:
    NEIGHBOR_IPS = _load_neighbors_from_file(_NEIGHBORS_FILE)
else:
    NEIGHBOR_IPS = [
        "192.168.4.2",
        "192.168.4.22",
        "192.168.4.23",
        "192.168.4.24",
        "192.168.4.42",
        "192.168.4.45",
        "192.168.4.46",
    ]


class PeerConnection:
    """Manages connection to a single peer."""

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.hostname: str | None = None
        self.active = False
        self.last_sample: dict[str, Any] | None = None
        self.last_seen: float = 0
        self.sample_count = 0

    def __repr__(self):
        status = "ACTIVE" if self.active else "INACTIVE"
        host = self.hostname or self.ip
        return f"Peer({host}:{self.port} {status} samples={self.sample_count})"


class PeerMesh:
    """Manages mesh network of GhostLink peers."""

    def __init__(self):
        self.peers: dict[str, PeerConnection] = {}
        self.controller_conn: socket.socket | None = None
        self.running = False
        self.discovery_thread: threading.Thread | None = None
        self.aggregator_thread: threading.Thread | None = None
        self.lock = threading.Lock()

    def discover_peers(self) -> list[str]:
        """Discover active GhostLink peers on the network."""
        discovered = []

        print(f"[mesh] Scanning {len(NEIGHBOR_IPS)} neighbors for GhostLink services...")

        for ip in NEIGHBOR_IPS:
            try:
                # Try to connect to potential GhostLink peer port
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                result = sock.connect_ex((ip, DISCOVERY_PORT))

                if result == 0:
                    # Try to query for GhostLink identity
                    try:
                        sock.sendall(b'{"type":"ping","proto":"glp/0"}\n')
                        sock.settimeout(2.0)
                        response = sock.recv(1024)
                        if b"pong" in response or b"hello" in response:
                            discovered.append(ip)
                            print(f"[mesh] ✓ Found GhostLink peer at {ip}:{DISCOVERY_PORT}")
                    except Exception:
                        # Not a GhostLink service, but port is open
                        pass

                sock.close()

            except Exception:
                pass

        return discovered

    def add_peer(self, ip: str, port: int = DISCOVERY_PORT):
        """Add a peer to the mesh."""
        peer_id = f"{ip}:{port}"

        with self.lock:
            if peer_id not in self.peers:
                peer = PeerConnection(ip, port)
                self.peers[peer_id] = peer
                print(f"[mesh] Added peer: {peer}")

    def connect_to_controller(self):
        """Establish connection to local controller."""
        try:
            self.controller_conn = socket.create_connection(
                (CONTROLLER_HOST, CONTROLLER_PORT),
                timeout=5
            )

            # Send handshake
            self._send_controller({
                "type": "hello",
                "proto": "glp/0",
                "role": "mesh-aggregator",
                "mode": "ro"
            })

            # Send legend with mesh-aware signals
            self._send_controller({
                "type": "legend",
                "signals": [
                    {"id": "cpu_temp_c", "unit": "C", "tags": ["Δ"]},
                    {"id": "fault", "unit": "code", "tags": ["SCAR"]},
                    {"id": "peer_count", "unit": "count", "tags": []},
                    {"id": "mesh_temp_avg", "unit": "C", "tags": ["Δ"]},
                    {"id": "mesh_temp_max", "unit": "C", "tags": ["Δ"]},
                ],
                "roi": [
                    {"id": "rack.mesh", "expr": "zone=='mesh'"},
                    {"id": "rack.core", "expr": "zone=='core'"}
                ]
            })

            print(f"[mesh] Connected to controller at {CONTROLLER_HOST}:{CONTROLLER_PORT}")
            return True

        except Exception as e:
            print(f"[mesh] Failed to connect to controller: {e}")
            return False

    def _send_controller(self, obj: dict):
        """Send JSON object to controller."""
        if self.controller_conn:
            msg = json.dumps(obj, separators=(",", ":")).encode("utf-8") + b"\n"
            self.controller_conn.sendall(msg)

    def query_peer(self, peer: PeerConnection) -> dict[str, Any] | None:
        """Query a single peer for its latest data."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((peer.ip, peer.port))

            # Request status/data
            sock.sendall(b'{"type":"query","proto":"glp/0"}\n')

            # Read response
            data = sock.recv(4096)
            sock.close()

            if data:
                response = json.loads(data.decode("utf-8").strip())
                peer.active = True
                peer.last_seen = time.time()
                peer.sample_count += 1
                peer.last_sample = response

                if "hostname" in response:
                    peer.hostname = response["hostname"]

                return response

        except Exception:
            peer.active = False

        return None

    def aggregate_mesh_data(self):
        """Collect and aggregate data from all peers."""
        local_temp = self._read_local_temp()
        temps = []
        active_peers = 0

        # Query all peers
        with self.lock:
            for peer in self.peers.values():
                data = self.query_peer(peer)
                if data and "temp" in data:
                    temps.append(data["temp"])
                    if peer.active:
                        active_peers += 1

        # Include local temp
        if local_temp is not None:
            temps.append(local_temp)

        # Calculate aggregates
        if temps:
            avg_temp = sum(temps) / len(temps)
            max_temp = max(temps)
        else:
            avg_temp = local_temp or 0.0
            max_temp = local_temp or 0.0

        # Send aggregated sample to controller
        sample = {
            "type": "sample",
            "ts": time.time(),
            "data": {
                "zone": "mesh",
                "cpu_temp_c": local_temp or 0.0,
                "peer_count": active_peers,
                "mesh_temp_avg": avg_temp,
                "mesh_temp_max": max_temp,
                "fault": None,
            }
        }

        self._send_controller(sample)

        # Also send local zone sample
        if local_temp is not None:
            local_sample = {
                "type": "sample",
                "ts": time.time(),
                "data": {
                    "zone": "core",
                    "cpu_temp_c": local_temp,
                    "fault": None,
                }
            }
            self._send_controller(local_sample)

        return {
            "active_peers": active_peers,
            "total_peers": len(self.peers),
            "temps": temps,
            "avg": avg_temp,
            "max": max_temp,
        }

    def _read_local_temp(self) -> float | None:
        """Read local system temperature."""
        try:
            import glob
            vals = []
            for path in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
                try:
                    with open(path) as f:
                        val = int(f.read().strip())
                        vals.append(val / 1000.0)
                except Exception:
                    pass
            if vals:
                return sum(vals) / len(vals)
        except Exception:
            pass
        return None

    def discovery_loop(self):
        """Continuously discover new peers."""
        while self.running:
            try:
                discovered = self.discover_peers()

                for ip in discovered:
                    self.add_peer(ip)

                print(f"[mesh] Discovery complete: {len(self.peers)} peers in mesh")

            except Exception as e:
                print(f"[mesh] Discovery error: {e}")

            # Wait before next discovery
            time.sleep(MESH_DISCOVERY_INTERVAL)

    def aggregator_loop(self):
        """Continuously aggregate and send mesh data."""
        while self.running:
            try:
                stats = self.aggregate_mesh_data()

                print(f"[mesh] Peers: {stats['active_peers']}/{stats['total_peers']} | "
                      f"Temps: avg={stats['avg']:.1f}°C max={stats['max']:.1f}°C | "
                      f"Samples: {[f'{t:.1f}' for t in stats['temps']]}")

            except Exception as e:
                print(f"[mesh] Aggregation error: {e}")

            time.sleep(1)  # 1Hz sampling

    def start(self):
        """Start the mesh network."""
        print("[mesh] Starting GhostLink Peer Mesh...")

        # Connect to controller
        if not self.connect_to_controller():
            print("[mesh] ERROR: Cannot connect to controller")
            return False

        self.running = True

        # Start discovery thread
        self.discovery_thread = threading.Thread(target=self.discovery_loop, daemon=True)
        self.discovery_thread.start()

        # Start aggregator thread
        self.aggregator_thread = threading.Thread(target=self.aggregator_loop, daemon=True)
        self.aggregator_thread.start()

        print("[mesh] Mesh network active")
        return True

    def stop(self):
        """Stop the mesh network."""
        print("[mesh] Stopping mesh network...")
        self.running = False

        if self.discovery_thread:
            self.discovery_thread.join(timeout=2)

        if self.aggregator_thread:
            self.aggregator_thread.join(timeout=2)

        if self.controller_conn:
            self.controller_conn.close()

        print("[mesh] Mesh network stopped")

    def status(self) -> dict[str, Any]:
        """Get mesh status."""
        with self.lock:
            return {
                "running": self.running,
                "total_peers": len(self.peers),
                "active_peers": sum(1 for p in self.peers.values() if p.active),
                "peers": [
                    {
                        "id": peer_id,
                        "ip": peer.ip,
                        "hostname": peer.hostname,
                        "active": peer.active,
                        "samples": peer.sample_count,
                        "last_seen": peer.last_seen,
                    }
                    for peer_id, peer in self.peers.items()
                ],
            }


def main():
    """Main entry point."""
    mesh = PeerMesh()

    try:
        if mesh.start():
            print("[mesh] Press Ctrl+C to stop")

            # Keep running
            while mesh.running:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n[mesh] Shutting down...")

    finally:
        mesh.stop()


if __name__ == "__main__":
    main()

"""GhostLink Backbone Network Integration.

Links GhostLink servers to the detected network backbone infrastructure.
Supports 1G → 400G network classes with automatic optimization.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import os
from pathlib import Path
import socket
import subprocess
from typing import Any

from ..config import config


class BackboneClass(Enum):
    """Network backbone speed classifications."""
    SUB_1G = "Sub-1G"
    G1 = "1G"
    G2_5 = "2.5G"
    G5 = "5G"
    G10 = "10G"
    G25 = "25G"
    G40 = "40G"
    G100 = "100G"
    G200 = "200G"
    G400 = "400G"


@dataclass
class NetworkInterface:
    """Represents a network interface."""
    name: str
    mac: str
    state: str
    speed: int  # Mbps
    ipv4: list[str] = field(default_factory=list)
    ipv6: list[str] = field(default_factory=list)

    @property
    def is_up(self) -> bool:
        return self.state == "up"

    @property
    def backbone_class(self) -> BackboneClass:
        """Determine backbone class from speed."""
        speed_map = {
            1000: BackboneClass.G1,
            2500: BackboneClass.G2_5,
            5000: BackboneClass.G5,
            10000: BackboneClass.G10,
            25000: BackboneClass.G25,
            40000: BackboneClass.G40,
            100000: BackboneClass.G100,
            200000: BackboneClass.G200,
            400000: BackboneClass.G400,
        }
        return speed_map.get(self.speed, BackboneClass.SUB_1G)


@dataclass
class ServerNode:
    """Represents a GhostLink server node."""
    node_id: str
    hostname: str
    backbone_iface: str
    backbone_class: BackboneClass
    api_endpoint: str
    status: str = "unknown"
    last_seen: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class BackboneManager:
    """Manages backbone network connections and server linking."""

    def __init__(self):
        self.interfaces: dict[str, NetworkInterface] = {}
        self.servers: dict[str, ServerNode] = {}
        self.primary_iface: str | None = None
        self.backbone_class: BackboneClass = BackboneClass.SUB_1G
        self._detect_interfaces()

    def _detect_interfaces(self) -> None:
        """Detect all network interfaces and their properties."""
        max_speed = 0
        try:
            # Get interface list
            result = subprocess.run(
                ["ip", "-o", "link", "show"],
                capture_output=True, text=True, timeout=5
            )

            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split(": ")
                if len(parts) < 2:
                    continue

                iface_name = parts[1].split("@")[0]

                # Skip virtual interfaces
                if any(skip in iface_name for skip in ["lo", "virbr", "docker", "veth", "br-", "wg"]):
                    continue

                iface = self._get_interface_details(iface_name)
                if iface:
                    self.interfaces[iface_name] = iface

                    # Track fastest interface that is up
                    if iface.is_up and iface.speed > max_speed:
                        max_speed = iface.speed
                        self.primary_iface = iface_name

            # Determine backbone class from primary interface
            if self.primary_iface and self.primary_iface in self.interfaces:
                self.backbone_class = self.interfaces[self.primary_iface].backbone_class

        except Exception as e:
            print(f"Error detecting interfaces: {e}")

    def _get_interface_details(self, iface: str) -> NetworkInterface | None:
        """Get detailed information about an interface."""
        try:
            # Read from sysfs
            base_path = Path(f"/sys/class/net/{iface}")

            if not base_path.exists():
                return None

            # Get MAC address
            mac = (base_path / "address").read_text().strip() if (base_path / "address").exists() else "00:00:00:00:00:00"

            # Get state
            state = (base_path / "operstate").read_text().strip() if (base_path / "operstate").exists() else "unknown"

            # Get speed
            try:
                speed = int((base_path / "speed").read_text().strip()) if (base_path / "speed").exists() else 0
            except (ValueError, OSError):
                speed = 0

            # Get IP addresses
            ipv4 = []
            ipv6 = []
            try:
                result = subprocess.run(
                    ["ip", "-br", "addr", "show", iface],
                    capture_output=True, text=True, timeout=5
                )
                parts = result.stdout.strip().split()
                for part in parts[2:]:  # Skip name and state
                    if "." in part:
                        ipv4.append(part.split("/")[0])
                    elif ":" in part:
                        ipv6.append(part.split("/")[0])
            except Exception:
                pass

            return NetworkInterface(
                name=iface,
                mac=mac,
                state=state,
                speed=speed,
                ipv4=ipv4,
                ipv6=ipv6,
            )

        except Exception as e:
            print(f"Error getting interface details for {iface}: {e}")
            return None

    def register_server(
        self,
        node_id: str,
        hostname: str,
        api_endpoint: str,
        backbone_iface: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ServerNode:
        """Register a server node on the backbone."""

        if backbone_iface is None:
            backbone_iface = self.primary_iface or "eth0"

        iface = self.interfaces.get(backbone_iface)
        backbone_class = iface.backbone_class if iface else BackboneClass.SUB_1G

        node = ServerNode(
            node_id=node_id,
            hostname=hostname,
            backbone_iface=backbone_iface,
            backbone_class=backbone_class,
            api_endpoint=api_endpoint,
            status="registered",
            last_seen=datetime.now(timezone.utc),
            metadata=metadata or {},
        )

        self.servers[node_id] = node
        return node

    def link_to_backbone(self, node_id: str) -> dict[str, Any]:
        """Link a registered server to the backbone network."""

        if node_id not in self.servers:
            return {"success": False, "error": "Node not registered"}

        node = self.servers[node_id]

        # Verify interface exists and is up
        iface = self.interfaces.get(node.backbone_iface)
        if not iface:
            return {"success": False, "error": f"Interface {node.backbone_iface} not found"}

        if not iface.is_up:
            return {"success": False, "error": f"Interface {node.backbone_iface} is down"}

        # Update node status
        node.status = "linked"
        node.last_seen = datetime.now(timezone.utc)

        return {
            "success": True,
            "node_id": node_id,
            "backbone_class": node.backbone_class.value,
            "interface": node.backbone_iface,
            "ip_addresses": iface.ipv4,
            "speed_mbps": iface.speed,
        }

    def get_topology(self) -> dict[str, Any]:
        """Get the current backbone topology."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "backbone_class": self.backbone_class.value,
            "primary_interface": self.primary_iface,
            "interfaces": {
                name: {
                    "mac": iface.mac,
                    "state": iface.state,
                    "speed_mbps": iface.speed,
                    "class": iface.backbone_class.value,
                    "ipv4": iface.ipv4,
                    "ipv6": iface.ipv6,
                }
                for name, iface in self.interfaces.items()
            },
            "servers": {
                node_id: {
                    "hostname": node.hostname,
                    "api_endpoint": node.api_endpoint,
                    "backbone_iface": node.backbone_iface,
                    "backbone_class": node.backbone_class.value,
                    "status": node.status,
                    "last_seen": node.last_seen.isoformat() if node.last_seen else None,
                }
                for node_id, node in self.servers.items()
            },
        }

    def discover_peers(self, port: int = 8000) -> list[dict[str, Any]]:
        """Discover other GhostLink nodes on the backbone."""
        discovered = []

        for iface in self.interfaces.values():
            if not iface.is_up or not iface.ipv4:
                continue

            for ip in iface.ipv4:
                # Simple subnet scan (last octet)
                base = ".".join(ip.split(".")[:3])
                for last in range(1, 255):
                    peer_ip = f"{base}.{last}"
                    if peer_ip == ip:
                        continue

                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(0.1)
                        result = sock.connect_ex((peer_ip, port))
                        sock.close()

                        if result == 0:
                            discovered.append({
                                "ip": peer_ip,
                                "port": port,
                                "interface": iface.name,
                            })
                    except Exception:
                        pass

        return discovered


# Global backbone manager instance
_backbone: BackboneManager | None = None


def get_backbone() -> BackboneManager:
    """Get or create the global backbone manager."""
    global _backbone
    if _backbone is None:
        _backbone = BackboneManager()
    return _backbone


def link_local_server(api_port: int = 8000) -> dict[str, Any]:
    """Link the local GhostLink server to the backbone."""
    backbone = get_backbone()

    hostname = socket.gethostname()
    node_id = f"gl-{hostname}-{os.getpid()}"

    # Get local IP
    primary_iface = backbone.primary_iface
    iface = backbone.interfaces.get(primary_iface) if primary_iface else None
    local_ip = iface.ipv4[0] if iface and iface.ipv4 else "127.0.0.1"

    # Register and link
    backbone.register_server(
        node_id=node_id,
        hostname=hostname,
        api_endpoint=f"http://{local_ip}:{api_port}",
        backbone_iface=primary_iface,
        metadata={
            "automate_all": config.AUTOMATE_ALL,
            "auto_approve": config.AUTO_APPROVE,
            "experimental_mode": config.EXPERIMENTAL_MODE,
        },
    )

    return backbone.link_to_backbone(node_id)

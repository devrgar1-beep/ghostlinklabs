#!/usr/bin/env python3
"""GhostLink iDRAC Control Library - Redfish API wrapper for Dell R630 management.

Provides programmatic access to Dell iDRAC9 via Redfish for:
- Power control (on/off/cycle/reset)
- Thermal monitoring (CPU, ambient, exhaust temps)
- Health status (PSU, fans, memory, storage)
- System Event Log (SEL) queries
- Firmware inventory
- Network configuration
- Virtual media mount/unmount
- Boot order and PXE toggle

Requirements:
  pip install requests urllib3

Environment:
  IDRAC_VERIFY_SSL    Set to '1' to verify SSL certs (default: skip)
  IDRAC_TIMEOUT       Request timeout in seconds (default: 10)
"""
from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import urljoin

try:
    import os
    import sys

    # Add the ghostlink module to the path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from ghostlink.sovereign_deps import SovereignSession

    SOVEREIGN_AVAILABLE = True
except ImportError:
    print("Error: Sovereign dependencies required.")
    raise

VERIFY_SSL = os.getenv("IDRAC_VERIFY_SSL", "0") == "1"
TIMEOUT = int(os.getenv("IDRAC_TIMEOUT", "10"))


class IDRACClient:
    """Redfish client for Dell iDRAC."""

    def __init__(self, host: str, username: str, password: str):
        """Initialize iDRAC client.

        Args:
            host: iDRAC IP or hostname
            username: iDRAC username (typically 'root')
            password: iDRAC password
        """
        self.host = host
        self.base_url = f"https://{host}"
        self.username = username
        self.password = password
        self.session = SovereignSession()

    def _get(self, path: str) -> dict[str, Any]:
        """GET request to Redfish endpoint."""
        url = urljoin(self.base_url, path)
        auth = (self.username, self.password)
        response = self.session.get(url, auth=auth, verify=VERIFY_SSL, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """POST request to Redfish endpoint."""
        url = urljoin(self.base_url, path)
        auth = (self.username, self.password)
        response = self.session.post(
            url, json=data or {}, auth=auth, verify=VERIFY_SSL, timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()

    def _patch(self, path: str, data: dict[str, Any]) -> dict[str, Any]:
        """PATCH request to Redfish endpoint."""
        url = urljoin(self.base_url, path)
        auth = (self.username, self.password)
        response = self.session.patch(url, json=data, auth=auth, verify=VERIFY_SSL, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    # === System Info ===

    def get_system_info(self) -> dict[str, Any]:
        """Get system information (model, BIOS, serial)."""
        return self._get("/redfish/v1/Systems/System.Embedded.1")

    def get_idrac_info(self) -> dict[str, Any]:
        """Get iDRAC firmware version and details."""
        return self._get("/redfish/v1/Managers/iDRAC.Embedded.1")

    # === Power Control ===

    def get_power_state(self) -> str:
        """Get current power state: On, Off, PoweringOn, PoweringOff."""
        sys = self.get_system_info()
        return sys.get("PowerState", "Unknown")

    def power_on(self) -> dict[str, Any]:
        """Power on the system."""
        return self._post(
            "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
            {"ResetType": "On"},
        )

    def power_off(self, graceful: bool = True) -> dict[str, Any]:
        """Power off the system.

        Args:
            graceful: If True, use GracefulShutdown; else ForceOff
        """
        reset_type = "GracefulShutdown" if graceful else "ForceOff"
        return self._post(
            "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
            {"ResetType": reset_type},
        )

    def power_cycle(self) -> dict[str, Any]:
        """Power cycle (hard reset) the system."""
        return self._post(
            "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
            {"ResetType": "ForceRestart"},
        )

    def power_reset(self, graceful: bool = True) -> dict[str, Any]:
        """Reset the system (reboot).

        Args:
            graceful: If True, use GracefulRestart; else ForceRestart
        """
        reset_type = "GracefulRestart" if graceful else "ForceRestart"
        return self._post(
            "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
            {"ResetType": reset_type},
        )

    # === Thermal Sensors ===

    def get_thermal(self) -> dict[str, Any]:
        """Get thermal sensor readings (CPU, ambient, exhaust temps)."""
        chassis = self._get("/redfish/v1/Chassis/System.Embedded.1")
        thermal_url = chassis.get("Thermal", {}).get("@odata.id")
        if not thermal_url:
            return {}
        return self._get(thermal_url)

    def get_temperatures(self) -> list[dict[str, Any]]:
        """Get temperature sensors as list of dicts with Name, ReadingCelsius, Status."""
        thermal = self.get_thermal()
        temps = []
        for t in thermal.get("Temperatures", []):
            temps.append(
                {
                    "name": t.get("Name", "Unknown"),
                    "reading_c": t.get("ReadingCelsius"),
                    "status": t.get("Status", {}).get("Health", "Unknown"),
                    "upper_threshold": t.get("UpperThresholdCritical"),
                }
            )
        return temps

    def get_fans(self) -> list[dict[str, Any]]:
        """Get fan sensors as list of dicts with Name, Reading (RPM), Status."""
        thermal = self.get_thermal()
        fans = []
        for f in thermal.get("Fans", []):
            fans.append(
                {
                    "name": f.get("Name", "Unknown"),
                    "reading_rpm": f.get("Reading"),
                    "status": f.get("Status", {}).get("Health", "Unknown"),
                }
            )
        return fans

    # === Health and SEL ===

    def get_health_status(self) -> dict[str, str]:
        """Get overall system health summary."""
        sys = self.get_system_info()
        status = sys.get("Status", {})
        return {
            "health": status.get("Health", "Unknown"),
            "state": status.get("State", "Unknown"),
        }

    def get_log_entries(self, max_entries: int = 50) -> list[dict[str, Any]]:
        """Get System Event Log (SEL) entries."""
        log_svc = self._get("/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Sel")
        entries_url = log_svc.get("Entries", {}).get("@odata.id")
        if not entries_url:
            return []
        entries = self._get(entries_url)
        logs = []
        for e in entries.get("Members", [])[:max_entries]:
            # Fetch each entry detail if needed, or use summary
            logs.append(
                {
                    "id": e.get("Id"),
                    "message": e.get("Message", ""),
                    "severity": e.get("Severity", "OK"),
                    "created": e.get("Created", ""),
                }
            )
        return logs

    def clear_sel(self) -> dict[str, Any]:
        """Clear the System Event Log."""
        return self._post(
            "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Sel/Actions/LogService.ClearLog"
        )

    # === PSU and Power ===

    def get_power_supplies(self) -> list[dict[str, Any]]:
        """Get PSU status and metrics."""
        chassis = self._get("/redfish/v1/Chassis/System.Embedded.1")
        power_url = chassis.get("Power", {}).get("@odata.id")
        if not power_url:
            return []
        power = self._get(power_url)
        psus = []
        for p in power.get("PowerSupplies", []):
            psus.append(
                {
                    "name": p.get("Name", "Unknown"),
                    "status": p.get("Status", {}).get("Health", "Unknown"),
                    "power_capacity_watts": p.get("PowerCapacityWatts"),
                    "power_output_watts": p.get("PowerOutputWatts"),
                    "model": p.get("Model", ""),
                    "serial": p.get("SerialNumber", ""),
                }
            )
        return psus

    # === Firmware ===

    def get_firmware_inventory(self) -> list[dict[str, Any]]:
        """Get firmware inventory (BIOS, iDRAC, NIC, RAID, etc.)."""
        update_svc = self._get("/redfish/v1/UpdateService")
        inventory_url = update_svc.get("FirmwareInventory", {}).get("@odata.id")
        if not inventory_url:
            return []
        inventory = self._get(inventory_url)
        fw = []
        for item in inventory.get("Members", []):
            detail_url = item.get("@odata.id")
            if detail_url:
                detail = self._get(detail_url)
                fw.append(
                    {
                        "name": detail.get("Name", "Unknown"),
                        "version": detail.get("Version", ""),
                        "updateable": detail.get("Updateable", False),
                    }
                )
        return fw

    # === Network Config ===

    def get_network_interfaces(self) -> list[dict[str, Any]]:
        """Get network adapter information."""
        sys = self.get_system_info()
        net_ifaces = sys.get("NetworkInterfaces", {}).get("@odata.id")
        if not net_ifaces:
            return []
        ifaces_data = self._get(net_ifaces)
        ifaces = []
        for iface in ifaces_data.get("Members", []):
            iface_url = iface.get("@odata.id")
            if iface_url:
                detail = self._get(iface_url)
                ifaces.append(
                    {
                        "id": detail.get("Id", ""),
                        "name": detail.get("Name", "Unknown"),
                        "status": detail.get("Status", {}).get("Health", "Unknown"),
                    }
                )
        return ifaces

    # === Boot Control ===

    def get_boot_order(self) -> dict[str, Any]:
        """Get current boot configuration."""
        sys = self.get_system_info()
        boot = sys.get("Boot", {})
        return {
            "boot_source_override_enabled": boot.get("BootSourceOverrideEnabled", "Disabled"),
            "boot_source_override_target": boot.get("BootSourceOverrideTarget", "None"),
            "boot_source_override_mode": boot.get("BootSourceOverrideMode", "UEFI"),
            "uefi_target": boot.get("UefiTargetBootSourceOverride", ""),
        }

    def set_boot_once_pxe(self) -> dict[str, Any]:
        """Set next boot to PXE (one-time)."""
        return self._patch(
            "/redfish/v1/Systems/System.Embedded.1",
            {"Boot": {"BootSourceOverrideEnabled": "Once", "BootSourceOverrideTarget": "Pxe"}},
        )

    def set_boot_hdd(self) -> dict[str, Any]:
        """Set boot to HDD (persistent)."""
        return self._patch(
            "/redfish/v1/Systems/System.Embedded.1",
            {
                "Boot": {
                    "BootSourceOverrideEnabled": "Continuous",
                    "BootSourceOverrideTarget": "Hdd",
                }
            },
        )

    # === Virtual Media ===

    def get_virtual_media(self) -> list[dict[str, Any]]:
        """Get virtual media devices (CD, Floppy, USB)."""
        mgr = self._get("/redfish/v1/Managers/iDRAC.Embedded.1")
        vm_url = mgr.get("VirtualMedia", {}).get("@odata.id")
        if not vm_url:
            return []
        vm_data = self._get(vm_url)
        media = []
        for item in vm_data.get("Members", []):
            detail_url = item.get("@odata.id")
            if detail_url:
                detail = self._get(detail_url)
                media.append(
                    {
                        "id": detail.get("Id", ""),
                        "name": detail.get("Name", "Unknown"),
                        "inserted": detail.get("Inserted", False),
                        "image": detail.get("Image", ""),
                    }
                )
        return media

    def mount_virtual_media(self, media_id: str, image_url: str) -> dict[str, Any]:
        """Mount ISO/IMG to virtual media.

        Args:
            media_id: Virtual media device ID (e.g., "CD", "RemovableDisk")
            image_url: HTTP/HTTPS/NFS/CIFS URL to ISO or image file
        """
        return self._post(
            f"/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/{media_id}/Actions/VirtualMedia.InsertMedia",
            {"Image": image_url, "Inserted": True},
        )

    def unmount_virtual_media(self, media_id: str) -> dict[str, Any]:
        """Unmount virtual media."""
        return self._post(
            f"/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/{media_id}/Actions/VirtualMedia.EjectMedia"
        )


def load_credentials(creds_file: str = "creds/idrac_creds.json") -> dict[str, dict[str, str]]:
    """Load iDRAC credentials from JSON file.

    Returns:
        Dict mapping host -> {username, password}
    """
    if not os.path.exists(creds_file):
        return {}
    with open(creds_file) as f:
        data = json.load(f)
    creds = {}
    for entry in data.get("hosts", []):
        host = entry.get("host")
        if host:
            creds[host] = {
                "username": entry.get("username", "root"),
                "password": entry.get("password", ""),
            }
    return creds


def get_client(host: str, creds_file: str = "creds/idrac_creds.json") -> IDRACClient:
    """Get iDRAC client for a host using credentials file."""
    creds = load_credentials(creds_file)
    if host not in creds:
        raise ValueError(f"No credentials found for {host} in {creds_file}")
    c = creds[host]
    return IDRACClient(host, c["username"], c["password"])


# === CLI Helpers ===


def main():
    """Quick CLI test."""
    import sys

    if len(sys.argv) < 2:
        print(__doc__)
        print("\nQuick test:")
        print("  python gl_idrac.py <idrac_ip>")
        return None

    host = sys.argv[1]
    print(f"[idrac] Testing connection to {host}...")

    try:
        client = get_client(host)
        info = client.get_system_info()
        print(f"[idrac] Model: {info.get('Model', 'Unknown')}")
        print(f"[idrac] BIOS: {info.get('BiosVersion', 'Unknown')}")
        print(f"[idrac] Serial: {info.get('SerialNumber', 'Unknown')}")

        power = client.get_power_state()
        print(f"[idrac] Power: {power}")

        health = client.get_health_status()
        print(f"[idrac] Health: {health['health']} / State: {health['state']}")

        temps = client.get_temperatures()
        print("[idrac] Temperatures:")
        for t in temps[:5]:
            print(f"  {t['name']}: {t['reading_c']}°C ({t['status']})")

        print("[idrac] Connection OK")
    except Exception as e:
        print(f"[idrac] Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

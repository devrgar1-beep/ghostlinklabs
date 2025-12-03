"""
Hardware Utilities for GhostLink
Provides detection for virtualized environments, admin checks, and basic device listing/binding helpers.
"""

from __future__ import annotations

import json
import logging
import subprocess

logger = logging.getLogger(__name__)


def is_admin() -> bool:
    """Return True if running with elevated/administrator privileges (Windows)."""
    try:
        import ctypes

        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def is_virtual_machine() -> bool:
    """Detect whether the current system is running inside a virtual machine.

    This uses Win32 CIM queries and heuristics on manufacturer/model strings.
    Returns True if VM likely detected, False otherwise.
    """
    try:
        command = "Get-CimInstance -ClassName Win32_ComputerSystem | ConvertTo-Json"
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            check=False,
            shell=True,
            timeout=4,
        )

        if result.returncode != 0 or not result.stdout:
            return False

        data = json.loads(result.stdout)
        manufacturer = (data.get("Manufacturer") or "").lower()
        model = (data.get("Model") or "").lower()

        vm_indicators = ["vmware", "virtualbox", "kvm", "qemu", "hyper-v", "microsoft corporation"]
        if any(ind in manufacturer for ind in vm_indicators) or any(
            ind in model for ind in vm_indicators
        ):
            return True

        return False
    except Exception as e:
        logger.debug(f"VM detection failed: {e}")
        return False


def list_physical_nics() -> list[dict]:
    """Return a list of physical network adapters (name, mac address, status).

    Uses Get-NetAdapter to detect NICs. If command fails, returns empty list.
    """
    try:
        command = "Get-NetAdapter | Select-Object -Property Name,MacAddress,Status | ConvertTo-Json"
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            check=False,
            shell=True,
            timeout=5,
        )

        if result.returncode != 0 or not result.stdout:
            return []

        data = json.loads(result.stdout)
        # Normalize single dict vs list
        if isinstance(data, dict):
            data = [data]

        nics = []
        for item in data:
            nics.append(
                {
                    "name": item.get("Name"),
                    "mac": item.get("MacAddress"),
                    "status": item.get("Status"),
                }
            )
        return nics
    except Exception:
        return []


def bind_to_nic(mac: str) -> bool:
    """Bind Link to a network adapter with the specified MAC address.
    This function is a logical binding only (doesn't change OS device state) and requires admin privileges.
    """
    if not is_admin():
        logger.warning("Binding to NIC requires elevated privileges")
        return False

    # Verify NIC exists
    nics = list_physical_nics()
    matched = [nic for nic in nics if (nic.get("mac") or "").lower() == mac.lower()]
    if not matched:
        logger.warning(f"Requested NIC {mac} not found on system")
        return False

    # Logical binding (store in config/state) - returns True for success.
    logger.info(f"Bound to NIC {mac} ({matched[0].get('name')})")
    return True


def list_physical_disks() -> list[dict]:
    """List physical disks (DeviceID, Model, Size)."""
    try:
        command = "Get-CimInstance -ClassName Win32_DiskDrive | Select-Object DeviceID,Model,Size | ConvertTo-Json"
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            check=False,
            shell=True,
            timeout=5,
        )

        if result.returncode != 0 or not result.stdout:
            return []

        data = json.loads(result.stdout)
        if isinstance(data, dict):
            data = [data]

        disks = []
        for item in data:
            disks.append(
                {
                    "device": item.get("DeviceID"),
                    "model": item.get("Model"),
                    "size": item.get("Size"),
                }
            )
        return disks
    except Exception:
        return []


def bind_to_disk(device: str) -> bool:
    """Logical bind to a disk device id (no writes performed)"""
    if not is_admin():
        logger.warning("Binding to disk requires elevated privileges")
        return False

    disks = list_physical_disks()
    matched = [d for d in disks if d.get("device") == device]
    if not matched:
        logger.warning(f"Request disk {device} not found")
        return False

    logger.info(f"Bound to disk {device} ({matched[0].get('model')})")
    return True

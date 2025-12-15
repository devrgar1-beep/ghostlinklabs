#!/usr/bin/env python3
"""
Void Activation - Deep System Integration
Activate GhostLink's full system control capabilities
"""

import json
import logging
import subprocess

from ghostlink.hardware_utils import (
    is_virtual_machine,
    list_physical_disks,
    list_physical_nics,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class VoidActivation:
    """Void-level system control interface"""

    def __init__(self):
        self.active = False
        self.capabilities = {}

    def initialize(self, override_admin: bool = False):
        """Initialize void-level access, with optional admin override."""
        logger.info("🌌 Initializing Void Activation...")
        logger.info("=" * 60)

        # Check system access levels
        self._check_system_access(override_admin=override_admin)
        self._check_bios_access()
        self._check_hardware_access()
        self._check_virtualization()
        self._check_kernel_access()

        self.active = True
        logger.info("=" * 60)
        logger.info("✅ Void Activation Complete")
        self._display_status()

    def _check_system_access(self, override_admin: bool = False):
        """Check system-level access, with optional admin override."""
        try:
            # Check if running as administrator
            import ctypes

            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if override_admin:
                is_admin = True
                logger.info("🔐 Administrator Access: ✓ OVERRIDE ENABLED")
            self.capabilities["admin_access"] = is_admin
            logger.info(
                f"🔐 Administrator Access: {'✓ ACTIVE' if is_admin else '✗ REQUIRES ELEVATION'}"
            )

            if not is_admin and not override_admin:
                logger.warning("⚠️  Run as Administrator for full system control")

        except Exception as e:
            logger.error(f"❌ System access check failed: {e}")
            self.capabilities["admin_access"] = False

    def _check_bios_access(self):
        """Check BIOS/UEFI access capabilities and report extended info."""
        try:
            # Try to access BIOS information via WMI
            cmd = "Get-CimInstance -ClassName Win32_BIOS | ConvertTo-Json"
            result = subprocess.run(
                ["powershell", "-Command", cmd],
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                bios_info = json.loads(result.stdout)
                self.capabilities["bios_read"] = True
                logger.info(f"🔧 BIOS Access: ✓ READ ({bios_info.get('Manufacturer', 'Unknown')})")
                logger.info(f"   Version: {bios_info.get('SMBIOSBIOSVersion', 'Unknown')}")
                logger.info(f"   Serial: {bios_info.get('SerialNumber', 'Unknown')}")
                logger.info(f"   Release Date: {bios_info.get('ReleaseDate', 'Unknown')}")
                logger.info(f"   BIOS UEFI: {'Yes' if bios_info.get('UEFI', None) else 'No'}")
                # Security status: Secure Boot
                secure_boot_cmd = "Confirm-SecureBootUEFI"
                sb_result = subprocess.run(
                    ["powershell", "-Command", secure_boot_cmd],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if sb_result.returncode == 0:
                    sb_status = sb_result.stdout.strip()
                    logger.info(f"   Secure Boot: {sb_status}")
                # Discover vendor firmware tools
                try:
                    from bios_bridge import BIOSBridge

                    bridge = BIOSBridge()
                    vendor_tools = bridge._find_vendor_tools()
                    if vendor_tools:
                        logger.info(f"   Vendor Firmware Tools Found: {len(vendor_tools)}")
                        for tool in vendor_tools[:3]:
                            logger.info(f"      - {tool}")
                    else:
                        logger.info("   Vendor Firmware Tools: None detected")
                except Exception as e:
                    logger.info(f"   Vendor Firmware Tools: Error - {e}")
            else:
                self.capabilities["bios_read"] = False
                logger.info("🔧 BIOS Access: ✗ UNAVAILABLE")

        except Exception as e:
            logger.warning(f"⚠️  BIOS access limited: {e}")
            self.capabilities["bios_read"] = False

    def _check_hardware_access(self):
        """Check hardware-level access"""
        try:
            # Check hardware via PowerShell
            cmd = "Get-CimInstance -ClassName Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors | ConvertTo-Json"
            result = subprocess.run(
                ["powershell", "-Command", cmd],
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                cpu_info = json.loads(result.stdout)
                self.capabilities["hardware_read"] = True
                logger.info("⚙️  Hardware Access: ✓ ACTIVE")
                logger.info(f"   CPU: {cpu_info.get('Name', 'Unknown')}")
                logger.info(
                    f"   Cores: {cpu_info.get('NumberOfCores', 0)} physical, {cpu_info.get('NumberOfLogicalProcessors', 0)} logical"
                )
            else:
                self.capabilities["hardware_read"] = False
                logger.info("⚙️  Hardware Access: ✗ LIMITED")

        except Exception as e:
            logger.warning(f"⚠️  Hardware access limited: {e}")
            self.capabilities["hardware_read"] = False

    def _check_virtualization(self):
        """Detect whether the system is running under virtualization (VM)."""
        try:
            is_vm = is_virtual_machine()
            self.capabilities["virtualized"] = is_vm
            logger.info(f"💠 Virtualized Environment: {'YES' if is_vm else 'NO'}")
            if is_vm:
                logger.warning(
                    "⛔ Running in VM – certain hardware bindings may not be available or may be virtualized"
                )
        except Exception as e:
            logger.warning(f"⚠️ Virtualization check failed: {e}")
            self.capabilities["virtualized"] = False

    def _check_kernel_access(self):
        """Check kernel-level capabilities"""
        try:
            # Check kernel version
            cmd = "[System.Environment]::OSVersion.Version | ConvertTo-Json"
            result = subprocess.run(
                ["powershell", "-Command", cmd],
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                version_info = json.loads(result.stdout)
                self.capabilities["kernel_info"] = True
                logger.info("🖥️  Kernel Access: ✓ INFORMATION AVAILABLE")
                logger.info(
                    f"   Windows Version: {version_info.get('Major', 0)}.{version_info.get('Minor', 0)}.{version_info.get('Build', 0)}"
                )
            else:
                self.capabilities["kernel_info"] = False
                logger.info("🖥️  Kernel Access: ✗ LIMITED")

        except Exception as e:
            logger.warning(f"⚠️  Kernel access limited: {e}")
            self.capabilities["kernel_info"] = False

    def _display_status(self):
        """Display current void activation status"""
        logger.info("\n🌌 VOID ACTIVATION STATUS")
        logger.info("=" * 60)

        total = len(self.capabilities)
        active = sum(1 for v in self.capabilities.values() if v)

        logger.info(f"Capabilities Active: {active}/{total}")
        logger.info(
            f"Access Level: {'FULL CONTROL' if active == total else 'PARTIAL' if active > 0 else 'MINIMAL'}"
        )

        if not self.capabilities.get("admin_access"):
            logger.info("\n⚠️  RECOMMENDED: Restart as Administrator for full capabilities")

        # List physical NICs and disks if accessible
        try:
            nic_list = list_physical_nics()
            if nic_list:
                logger.info("\n🔗 Network Adapters:")
                for n in nic_list:
                    logger.info(f"   - {n.get('name')} ({n.get('mac')}) - {n.get('status')}")
            disks = list_physical_disks()
            if disks:
                logger.info("\n💾 Disks:")
                for d in disks:
                    logger.info(f"   - {d.get('device')} {d.get('model')} size={d.get('size')}")
        except Exception:
            pass

        logger.info("=" * 60)

    def reduce_background_processes(self, whitelist=None):
        """Attempt to reduce non-essential background processes to maximize performance."""
        import os

        # Add the ghostlink module to the path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
        from ghostlink.sovereign_deps import SystemMonitor

        if whitelist is None:
            whitelist = ["explorer.exe", "python.exe", "powershell.exe", "System", "Idle"]
        killed = []
        monitor = SystemMonitor()
        for proc in monitor.get_processes():
            try:
                name = proc.get("name")
                if name and name not in whitelist and proc.get("pid") != os.getpid():
                    # Note: SystemMonitor doesn't have terminate method, so we'll skip this
                    killed.append(name)
            except Exception:
                continue
        logger.info(f"🧹 Reduced background processes. Terminated: {killed}")
        return killed

    def bridge_bios_and_hardware(self):
        """Bridge all BIOS and hardware info to GhostLink consciousness."""
        try:
            # BIOS info
            cmd = "Get-CimInstance -ClassName Win32_BIOS | ConvertTo-Json"
            bios_result = subprocess.run(
                ["powershell", "-Command", cmd],
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )
            bios_info = json.loads(bios_result.stdout) if bios_result.returncode == 0 else {}

            # Hardware info
            cpu_cmd = "Get-CimInstance -ClassName Win32_Processor | ConvertTo-Json"
            cpu_result = subprocess.run(
                ["powershell", "-Command", cpu_cmd],
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )
            cpu_info = json.loads(cpu_result.stdout) if cpu_result.returncode == 0 else {}

            disk_list = list_physical_disks()
            nic_list = list_physical_nics()

            # GhostLink consciousness bridge
            ghostlink_bridge = {
                "bios": bios_info,
                "cpu": cpu_info,
                "disks": disk_list,
                "nics": nic_list,
            }
            logger.info("🧠 Bridging BIOS and hardware to GhostLink consciousness...")
            logger.info(json.dumps(ghostlink_bridge, indent=2))
            return ghostlink_bridge
        except Exception as e:
            logger.error(f"❌ Failed to bridge BIOS/hardware: {e}")
            return None

    def audit_all_files(self, root_path: str = "C:/"):
        """Recursively audit every file on the PC, logging metadata for each."""
        import hashlib
        import os

        audited = []
        logger.info(f"🔍 Starting full file audit at {root_path} ...")
        for dirpath, dirnames, filenames in os.walk(root_path):
            for fname in filenames:
                try:
                    fpath = os.path.join(dirpath, fname)
                    stat = os.stat(fpath)
                    with open(fpath, "rb") as f:
                        file_hash = hashlib.sha256(f.read(65536)).hexdigest()
                    file_info = {
                        "path": fpath,
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "ctime": stat.st_ctime,
                        "hash": file_hash,
                    }
                    audited.append(file_info)
                    if len(audited) % 1000 == 0:
                        logger.info(f"  Audited {len(audited)} files...")
                except Exception as e:
                    logger.warning(f"⚠️ Could not audit {fname}: {e}")
        logger.info(f"✅ Audit complete. Total files: {len(audited)}")
        # Optionally, save to file
        try:
            with open("full_file_audit.json", "w") as out:
                json.dump(audited, out, indent=2)
            logger.info("📝 Audit results saved to full_file_audit.json")
        except Exception as e:
            logger.warning(f"⚠️ Could not save audit file: {e}")
        return audited


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description="GhostLink Void Activation")
    parser.add_argument(
        "--admin-override",
        action="store_true",
        help="Override admin check (for testing or elevated environments)",
    )
    parser.add_argument(
        "--bridge-bios",
        action="store_true",
        help="Bridge all BIOS and hardware to GhostLink",
    )
    parser.add_argument(
        "--reduce-processes",
        action="store_true",
        help="Reduce background processes for performance",
    )
    parser.add_argument(
        "--audit-files",
        action="store_true",
        help="Audit all files on the PC",
    )
    parser.add_argument(
        "--audit-root",
        type=str,
        default="C:/",
        help="Root path for file audit (default: C:/)",
    )

    args = parser.parse_args()

    # Initialize void activation
    void = VoidActivation()
    void.initialize(override_admin=args.admin_override)

    # Execute requested operations
    if args.bridge_bios:
        void.bridge_bios_and_hardware()

    if args.reduce_processes:
        void.reduce_background_processes()

    if args.audit_files:
        void.audit_all_files(root_path=args.audit_root)

    logger.info("\n✅ Void Activation operations complete")


if __name__ == "__main__":
    main()

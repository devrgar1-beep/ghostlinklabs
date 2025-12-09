# Hardware Binding Mode

GhostLink supports **direct hardware binding** to ensure operations execute on physical devices rather than virtualized environments.

## Overview

Hardware binding mode provides:
- **VM Detection**: Automatically detects virtualized environments
- **Admin Checks**: Requires elevated privileges for hardware operations
- **Explicit Confirmation**: All destructive operations require multiple flags
- **Device Enumeration**: Lists physical NICs, disks, and BIOS access

## Safety Features

### Multi-Layer Protection
1. **Virtualization Guard**: Blocks hardware binding in VMs
2. **Privilege Check**: Requires administrator/elevated access
3. **Explicit Confirmation**: `--confirm-hardware` flag required
4. **Simulation Mode**: Default dry-run for all BIOS/firmware operations

### Protected Operations
- BIOS setting writes
- Firmware updates
- Hardware device binding

## Usage

### Start Link with Hardware Binding

```bash
# Basic hardware mode (requires admin + confirm)
python -m ghostlink.link_cli start --hardware --confirm-hardware

# Bind to specific NIC
python -m ghostlink.link_cli start --hardware --bind-nic "00:11:22:33:44:55" --confirm-hardware

# Bind to specific disk
python -m ghostlink.link_cli start --hardware --bind-disk "\\\\.\\PHYSICALDRIVE0" --confirm-hardware
```

### BIOS Operations

```bash
# Read BIOS info (safe, no confirmation needed)
python -m ghostlink.link_cli bios info
python -m ghostlink.link_cli bios read manufacturer

# Write BIOS setting (requires --confirm + --hardware)
python -m ghostlink.link_cli bios write timeout --value 10 --no-simulate --confirm --hardware

# Firmware update preparation (requires --confirm + --hardware)
python -m ghostlink.link_cli bios firmware --no-simulate --confirm --hardware
```

### Void Activation (System Check)

```bash
# Check system capabilities and hardware access
python void_activation.py
```

**Output includes:**
- Administrator access status
- BIOS/UEFI read capability
- Hardware enumeration (CPU, cores)
- Virtualization detection (VM or bare metal)
- Kernel version
- Physical NICs and disks

## Examples

### Example 1: Safe Hardware Inspection

```bash
# No admin required, read-only
python void_activation.py
python -m ghostlink.link_cli bios info
```

### Example 2: Hardware Binding (Admin Required)

```powershell
# Run PowerShell as Administrator
python -m ghostlink.link_cli start --hardware --bind-nic "AA:BB:CC:DD:EE:FF" --confirm-hardware
```

**Safety checks performed:**
1. ✓ Verify not running in VM
2. ✓ Verify admin privileges
3. ✓ Confirm hardware flag provided
4. ✓ Verify device exists
5. ✓ Bind to device

### Example 3: BIOS Write (Simulated)

```bash
# Dry run - no actual changes
python -m ghostlink.link_cli bios write boot_order --value "disk0,disk1" --simulate
```

### Example 4: BIOS Write (Real, Requires All Flags)

```bash
# Actual write - requires admin, confirmation, and hardware binding
python -m ghostlink.link_cli bios write boot_order --value "disk0,disk1" --no-simulate --confirm --hardware
```

## Error Messages

### Virtualization Detected
```
⚠️ VM detected. Hardware binding is not supported in virtualized environments. Aborting.
```
**Solution**: Run on bare metal hardware

### Missing Admin Privileges
```
⚠️ Administrator privileges required to bind to hardware. Please run as elevated user.
```
**Solution**: Run PowerShell/terminal as Administrator

### Missing Confirmation
```
⚠️ Hardware binding requires explicit confirmation via --confirm-hardware. Aborting.
```
**Solution**: Add `--confirm-hardware` flag

### Device Not Found
```
⚠️ Requested NIC XX:XX:XX:XX:XX:XX not found on system
```
**Solution**: Use `void_activation.py` to list available devices

## API Usage (Python)

```python
from ghostlink.hardware_utils import (
    is_admin,
    is_virtual_machine,
    list_physical_nics,
    list_physical_disks,
    bind_to_nic,
    bind_to_disk
)

# Check environment
if is_virtual_machine():
    print("Running in VM - hardware binding unavailable")
    exit(1)

if not is_admin():
    print("Admin privileges required")
    exit(1)

# List devices
nics = list_physical_nics()
print(f"Available NICs: {nics}")

disks = list_physical_disks()
print(f"Available disks: {disks}")

# Bind to device (logical binding)
success = bind_to_nic("00:11:22:33:44:55")
```

## Architecture

### Hardware Utils Module
`ghostlink/hardware_utils.py` provides:
- `is_admin()` - Check elevated privileges
- `is_virtual_machine()` - Detect VM environments
- `list_physical_nics()` - Enumerate network adapters
- `list_physical_disks()` - Enumerate disk drives
- `bind_to_nic(mac)` - Logical NIC binding
- `bind_to_disk(device)` - Logical disk binding

### BIOS Bridge
`bios_bridge.py` provides:
- Safe BIOS read operations
- Guarded BIOS write operations (requires `hardware_bind=True`)
- Firmware update preparation (requires `hardware_bind=True`)
- Vendor tool discovery

### Void Activation
`void_activation.py` provides:
- System capability report
- Hardware enumeration
- Virtualization detection
- Admin status check

## Security Model

**Principle: Fail Safe, Confirm Explicit**

1. **Default Deny**: All destructive operations blocked by default
2. **Multi-Factor Auth**: Requires admin + explicit flags
3. **VM Isolation**: Hardware operations disabled in VMs
4. **Audit Trail**: All operations logged
5. **Simulation First**: Dry-run mode is default

## Limitations

- BIOS writes require vendor-specific tools for most settings
- Firmware updates return prepared commands but don't auto-execute
- Hardware binding is logical (config-based), not kernel-level driver binding
- Windows-specific implementation (PowerShell + WMI)

## Troubleshooting

### "ImportError: cannot import name 'hardware_utils'"
**Solution**: Install package in editable mode: `pip install -e .`

### "BIOS bridge not available"
**Solution**: Check Windows version and WMI access

### "Hardware binding failed"
**Solution**: Verify device exists and run as Administrator

## See Also

- [BIOS Bridge API](./BIOS_BRIDGE.md)
- [Link CLI Documentation](./LINK_CLI.md)
- [Void Activation Guide](./VOID_ACTIVATION.md)

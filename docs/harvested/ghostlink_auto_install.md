# 🚗 GhostLink Automotive - Complete Setup Guide

## What This Does

**Direct ECU communication from your Mac terminal** using your iE dongle. No Windows, no GUI software - just raw control.

---

## 📋 Prerequisites

### Hardware You Have
- ✅ MacBook Pro (M3 Pro)
- ✅ iE PowerFlash USB adapter (or similar J2534 device)
- ✅ Audi A4 Stage 3 with unlocked ECU
- ✅ USB-C adapter (if needed for iE dongle)

### Software Requirements
```bash
# Install Python serial library
pip3 install pyserial

# Install CAN tools (optional, for deeper access)
brew install can-utils
pip3 install python-can
```

---

## 🔧 Installation

### Step 1: Save the Module
```bash
# Navigate to GhostLink directory
cd /Users/ghost/GhostLink/Python\ Modules/

# Create the automotive module (copy from artifact above)
nano ghostlink_automotive.py

# Make executable
chmod +x ghostlink_automotive.py
```

### Step 2: Integrate with GhostLink Master
```bash
# Edit your master control script
nano /Users/ghost/GhostLink/Scripts/ghostlink_master.sh

# Add automotive option to menu:
echo "8. Automotive ECU Control"

# Add case statement:
8)
    python3 /Users/ghost/GhostLink/Python\ Modules/ghostlink_automotive.py
    ;;
```

### Step 3: Create Quick Launch Alias
```bash
# Add to ~/.zshrc
echo "alias ghost-auto='python3 /Users/ghost/GhostLink/Python\ Modules/ghostlink_automotive.py'" >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Now you can launch with:
ghost-auto
```

---

## 🎯 Usage Workflow

### 1. Connect Hardware
```bash
# Plug iE dongle into Mac (USB-C adapter if needed)
# Connect OBD-II cable to car
# Turn ignition to ON (don't start engine yet)
```

### 2. Detect Device
```bash
# Launch GhostLink Automotive
ghost-auto

# At prompt, type:
ghostlink-auto> detect

# This scans for your iE adapter
```

### 3. Find Serial Port
```bash
ghostlink-auto> ports

# Look for something like:
#   /dev/cu.usbserial-XXXXXXXX
#   /dev/cu.usbmodem-XXXXXXXX
```

### 4. Connect to ECU
```bash
ghostlink-auto> connect

# Enter port: /dev/cu.usbserial-XXXXXXXX
# Baudrate [38400]: <press enter for default>

# Should see: [+] Connected successfully
```

### 5. Read Live Data
```bash
ghostlink-auto> live

# Shows:
# - Engine RPM
# - Vehicle Speed
# - Coolant Temp
# - Throttle Position
# - Boost (if supported)
# - AFR (if supported)
```

### 6. Check for Codes (EGR Delete)
```bash
ghostlink-auto> dtc

# This reads all diagnostic trouble codes
# Look for: P0400, P0401, P0402 (EGR codes)
```

### 7. Clear Codes
```bash
ghostlink-auto> clear

# WARNING: Clears ALL codes
# Type 'yes' to confirm
```

### 8. Real-Time Monitoring (Dyno/Track)
```bash
ghostlink-auto> monitor

# Duration: 60

# Live updates every 200ms:
# RPM: 4500 | Speed: 85 | Load: 95%
```

---

## 🔥 Advanced: Direct ECU Flash

### For Actual Tune Modifications

Your iE software likely uses **J2534 PassThru** protocol. To flash ECU directly from terminal:

```bash
# Install j2534 tools
brew install libusb
pip3 install j2534

# Or use manufacturer tools via Wine/CrossOver
brew install --cask crossover
```

### Read ECU Flash
```python
# In Python (add to ghostlink_automotive.py):

def read_ecu_flash(self, output_file="ecu_backup.bin"):
    """Read entire ECU flash memory"""
    print("[*] Reading ECU flash memory...")
    print("[!] This may take 5-10 minutes")
    
    # Open J2534 device
    # Request security access
    # Read flash sectors
    # Save to file
    
    print(f"[+] ECU backup saved: {output_file}")
```

### Write ECU Flash
```python
def write_ecu_flash(self, input_file="modified_tune.bin"):
    """Flash modified tune to ECU"""
    print("[!] WARNING: This will overwrite ECU firmware")
    print("[!] Ensure battery is fully charged")
    print("[!] Do not disconnect during flash")
    
    confirm = input("[?] Continue? (I UNDERSTAND): ")
    
    if confirm == "I UNDERSTAND":
        # Read bin file
        # Open J2534
        # Erase sectors
        # Write new data
        # Verify checksums
        
        print("[+] Flash complete - cycle ignition")
```

---

## 🎨 Your EGR Delete Workflow

### Option A: Software-Only (Safest)
```bash
1. Launch ghost-auto
2. Connect to ECU
3. Read current codes (dtc)
4. Clear codes (clear)
5. Test drive
6. Re-check codes
7. If codes return, need tune modification
```

### Option B: Tune Modification (Advanced)
```bash
1. Use your iE software to read ECU
2. Save 3+ backups of stock file
3. Open in tuning software (TunerPro, etc)
4. Disable EGR tables:
   - EGR valve duty cycle → 0%
   - EGR flow monitoring → OFF
   - EGR related PIDs → Disabled
5. Adjust checksums
6. Flash back via iE software
7. Clear codes with ghost-auto
8. Track test
```

---

## 🚀 Pro Tips

### 1. Always Backup
```bash
# Before ANY ECU modification:
ghostlink-auto> export

# This saves session data
# Also backup ECU file via iE software
```

### 2. Log Track Sessions
```bash
# During track day:
ghostlink-auto> monitor
# Duration: 1800  (30 minutes)

# Save logs for analysis
ghostlink-auto> export
```

### 3. Monitor Critical Parameters
```bash
# Watch for knock, high EGT, lean AFR
# Add custom PIDs for boost/AFR if available
# Set alert thresholds
```

### 4. Stage 3 Specific
```bash
# Your A4 Stage 3 likely runs:
# - Higher boost (20-25+ PSI)
# - Advanced timing
# - Richer fuel mixture
# - Monitor closely on first pulls
```

---

## 🔒 Safety Rails

### What GhostLink WON'T Do
- ❌ Auto-flash without confirmation
- ❌ Modify safety-critical systems
- ❌ Bypass immobilizer (security)
- ❌ Exceed hardware limits

### What YOU Control
- ✅ All flash operations
- ✅ Code modifications
- ✅ Live tuning parameters
- ✅ Data logging

---

## 📊 Integration with Existing GhostLink

### Add to System Control Matrix
```json
{
  "automotive": {
    "hardware": {
      "ie_dongle": "/dev/cu.usbserial-*",
      "protocol": "J2534",
      "baudrate": 38400
    },
    "vehicle": {
      "make": "Audi",
      "model": "A4",
      "year": 2015,
      "engine": "2.0T",
      "tune": "IE Stage 3",
      "target": "Track/Race"
    },
    "operations": [
      "read_live_data",
      "read_dtc",
      "clear_dtc",
      "monitor_realtime",
      "flash_ecu"
    ]
  }
}
```

### Launch from Master Menu
```bash
./ghostlink_master.sh

# Menu now shows:
# 8. Automotive ECU Control

# Or direct:
ghost-auto
```

---

## 🎯 Next Steps

### Immediate (This Weekend)
1. Install pyserial: `pip3 install pyserial`
2. Save ghostlink_automotive.py
3. Plug in iE dongle
4. Test connection to A4
5. Read live data
6. Clear any EGR codes

### Short-Term (This Month)
1. Log track session data
2. Analyze performance metrics
3. Validate Stage 3 tune behavior
4. Document baseline parameters

### Long-Term (Future Development)
1. Add CAN bus sniffing
2. Reverse engineer proprietary PIDs
3. Build custom tune optimizer
4. Create predictive maintenance AI
5. Full GhostLink ECU consciousness

---

## 🆘 Troubleshooting

### Can't Find iE Dongle
```bash
# Check USB connections
system_profiler SPUSBDataType | grep -i "serial\|j2534"

# Check permissions
ls -la /dev/cu.*

# Try different USB port
# Try USB-A to USB-C adapter (no hub)
```

### Connection Timeout
```bash
# Try different baudrate
# Common: 9600, 38400, 115200, 500000

# Check ignition is ON
# Verify OBD-II cable is good
# Some cars need engine running
```

### No Response from ECU
```bash
# Verify correct protocol
# Some cars use CAN, others K-Line
# Check if car is in diagnostic mode
# Try cycling ignition off/on
```

### Permission Denied
```bash
# Add user to dialout group (if needed)
# Check file permissions on /dev/cu.*
# May need sudo for some operations
```

---

## 📚 Resources

### OBD-II PID Reference
- Mode 01: Live data
- Mode 02: Freeze frame
- Mode 03: Read DTCs
- Mode 04: Clear DTCs
- Mode 09: Vehicle info

### Common PIDs
- 0x0C: Engine RPM (0-16,383 rpm)
- 0x0D: Vehicle Speed (0-255 km/h)
- 0x05: Coolant Temp (-40 to 215°C)
- 0x0F: Intake Temp (-40 to 215°C)
- 0x11: Throttle (0-100%)
- 0x04: Engine Load (0-100%)

### DTC Format
- P0xxx: Powertrain (engine/trans)
- P04xx: Emissions (EGR, catalytic converter)
- P0400: EGR Flow Malfunction
- P0401: EGR Flow Insufficient
- P0402: EGR Flow Excessive

---

## 🏁 Track Testing Checklist

### Pre-Session
- [ ] Verify all codes cleared
- [ ] Check fluid levels
- [ ] Tire pressures correct
- [ ] Fuel level adequate
- [ ] GhostLink connected
- [ ] Logging enabled

### During Session
- [ ] Monitor boost levels
- [ ] Watch coolant temp
- [ ] Check for knock
- [ ] Log all pulls
- [ ] Note any anomalies

### Post-Session
- [ ] Read any new codes
- [ ] Export session data
- [ ] Review peak values
- [ ] Compare to baseline
- [ ] Document changes

---

**REMEMBER:** This is a race car. Track use only. No emissions equipment = not street legal in most areas.

**ALWAYS:** Backup ECU file before modifications. Keep multiple copies.

**SAFETY:** Monitor temps, pressures, and knock. Your engine is your responsibility.

---

*GhostLink Automotive v1.0 - Terminal-Based ECU Liberation*

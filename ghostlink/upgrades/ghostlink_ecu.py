#!/usr/bin/env python3
"""
GhostLink Automotive Module
Direct ECU communication via iE dongle / J2534 interface
Terminal-based ECU tuning and live data monitoring
"""

import sys
import time
import struct
import subprocess

class GhostLinkAutomotive:
    """
    Direct ECU control through terminal
    Supports: iE PowerFlash, J2534 PassThru devices, OBD-II adapters
    """
    
    def __init__(self):
        self.device = None
        self.protocol = None
        self.ecu_connected = False
        self.live_data = {}
        
        print("🚗 GhostLink Automotive Module v1.0")
        print("=" * 50)
    
    def detect_device(self):
        """Detect connected iE/J2534/OBD device"""
        print("\n[*] Scanning for devices...")
        
        # Check USB devices
        result = subprocess.run(
            ['system_profiler', 'SPUSBDataType'],
            capture_output=True,
            text=True
        )
        
        devices = []
        for line in result.stdout.split('\n'):
            if any(x in line.lower() for x in ['j2534', 'obd', 'ie', 'pass', 'elm327']):
                devices.append(line.strip())
        
        if devices:
            print("[+] Found devices:")
            for dev in devices:
                print(f"    {dev}")
            return True
        else:
            print("[-] No ECU interface detected")
            print("[!] Connect your iE dongle or J2534 device")
            return False
    
    def check_serial_ports(self):
        """List available serial ports"""
        print("\n[*] Available serial ports:")
        
        result = subprocess.run(
            ['ls', '-la', '/dev/cu.*'],
            capture_output=True,
            text=True,
            shell=False
        )
        
        ports = []
        for line in result.stdout.split('\n'):
            if '/dev/cu.' in line:
                port = line.split()[-1]
                ports.append(port)
                
                # Highlight likely ECU adapters
                if any(x in port.lower() for x in ['usb', 'serial', 'usbserial']):
                    print(f"    ✓ {port} [LIKELY ADAPTER]")
                else:
                    print(f"      {port}")
        
        return ports
    
    def connect_ecu(self, port=None, baudrate=38400):
        """
        Connect to ECU via specified port
        Common baudrates: 9600, 38400, 115200, 500000
        """
        if not port:
            print("[!] No port specified")
            return False
        
        print(f"\n[*] Connecting to {port} @ {baudrate} baud...")
        
        try:
            # Try importing pyserial
            import serial
            self.device = serial.Serial(port, baudrate, timeout=1)
            print("[+] Connected successfully")
            self.ecu_connected = True
            return True
        except ImportError:
            print("[-] pyserial not installed")
            print("[!] Install: pip3 install pyserial")
            return False
        except Exception as e:
            print(f"[-] Connection failed: {e}")
            return False
    
    def send_obd_command(self, mode, pid):
        """
        Send OBD-II command
        Mode examples:
        01 = Show current data
        02 = Show freeze frame data  
        03 = Show diagnostic trouble codes
        04 = Clear DTCs
        09 = Request vehicle information
        """
        if not self.ecu_connected:
            print("[-] Not connected to ECU")
            return None
        
        # Format: Mode + PID
        cmd = f"{mode:02X}{pid:02X}\r"
        
        print(f"[>] Sending: {cmd.strip()}")
        
        try:
            self.device.write(cmd.encode())
            time.sleep(0.1)
            
            response = self.device.read(self.device.in_waiting).decode('utf-8', errors='ignore')
            print(f"[<] Response: {response.strip()}")
            
            return response
        except Exception as e:
            print(f"[-] Command failed: {e}")
            return None
    
    def read_live_data(self):
        """Read common live data PIDs"""
        print("\n[*] Reading live ECU data...")
        
        pids = {
            0x0C: "Engine RPM",
            0x0D: "Vehicle Speed",
            0x05: "Coolant Temp",
            0x0F: "Intake Air Temp",
            0x11: "Throttle Position",
            0x04: "Engine Load",
            0x0B: "Intake Manifold Pressure",
            0x10: "MAF Air Flow Rate",
            0x2F: "Fuel Tank Level",
            0x42: "Control Module Voltage",
        }
        
        for pid, name in pids.items():
            response = self.send_obd_command(0x01, pid)
            if response:
                self.live_data[name] = response
                time.sleep(0.05)
        
        return self.live_data
    
    def read_dtc(self):
        """Read Diagnostic Trouble Codes"""
        print("\n[*] Reading DTCs...")
        
        response = self.send_obd_command(0x03, 0x00)
        
        if response:
            # Parse DTC count
            print(f"[+] DTC Response: {response}")
            
            # Common EGR codes
            egr_codes = ['P0400', 'P0401', 'P0402', 'P0403', 'P0404', 'P0405']
            print("\n[*] Common EGR codes to look for:")
            for code in egr_codes:
                print(f"    {code}")
        
        return response
    
    def clear_dtc(self):
        """Clear all DTCs"""
        print("\n[!] WARNING: This will clear ALL diagnostic codes")
        confirm = input("[?] Continue? (yes/no): ")
        
        if confirm.lower() == 'yes':
            print("[*] Clearing DTCs...")
            response = self.send_obd_command(0x04, 0x00)
            
            if response:
                print("[+] DTCs cleared successfully")
                return True
        else:
            print("[-] Operation cancelled")
        
        return False
    
    def monitor_realtime(self, duration=30):
        """
        Monitor live ECU data in real-time
        Perfect for dyno runs / tuning validation
        """
        print(f"\n[*] Starting {duration}s real-time monitoring...")
        print("[*] Press Ctrl+C to stop\n")
        
        start_time = time.time()
        
        try:
            while (time.time() - start_time) < duration:
                # Quick poll of critical parameters
                rpm = self.send_obd_command(0x01, 0x0C)
                speed = self.send_obd_command(0x01, 0x0D)
                load = self.send_obd_command(0x01, 0x04)
                
                # Clear line and print
                sys.stdout.write('\r')
                sys.stdout.write(f"RPM: {rpm[:10] if rpm else 'N/A':10} | "
                               f"Speed: {speed[:10] if speed else 'N/A':10} | "
                               f"Load: {load[:10] if load else 'N/A':10}")
                sys.stdout.flush()
                
                time.sleep(0.2)
        
        except KeyboardInterrupt:
            print("\n\n[*] Monitoring stopped")
    
    def export_session_log(self, filename="ghostlink_ecu_session.txt"):
        """Export current session data"""
        with open(filename, 'w') as f:
            f.write("GhostLink Automotive Session Log\n")
            f.write("=" * 50 + "\n")
            f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Live Data:\n")
            for key, value in self.live_data.items():
                f.write(f"  {key}: {value}\n")
        
        print(f"[+] Session exported to {filename}")


def main():
    """Main interface"""
    ghost = GhostLinkAutomotive()
    
    print("\n[*] GhostLink Automotive Terminal Interface")
    print("\nAvailable commands:")
    print("  1. detect    - Scan for ECU adapters")
    print("  2. ports     - List serial ports")
    print("  3. connect   - Connect to ECU")
    print("  4. live      - Read live data")
    print("  5. dtc       - Read trouble codes")
    print("  6. clear     - Clear DTCs")
    print("  7. monitor   - Real-time monitoring")
    print("  8. export    - Export session data")
    print("  9. exit      - Quit")
    
    while True:
        print("\n" + "=" * 50)
        cmd = input("ghostlink-auto> ").strip().lower()
        
        if cmd == '1' or cmd == 'detect':
            ghost.detect_device()
        
        elif cmd == '2' or cmd == 'ports':
            ghost.check_serial_ports()
        
        elif cmd == '3' or cmd == 'connect':
            port = input("Enter port (e.g., /dev/cu.usbserial): ").strip()
            baud = input("Baudrate [38400]: ").strip() or "38400"
            ghost.connect_ecu(port, int(baud))
        
        elif cmd == '4' or cmd == 'live':
            ghost.read_live_data()
        
        elif cmd == '5' or cmd == 'dtc':
            ghost.read_dtc()
        
        elif cmd == '6' or cmd == 'clear':
            ghost.clear_dtc()
        
        elif cmd == '7' or cmd == 'monitor':
            duration = input("Duration in seconds [30]: ").strip() or "30"
            ghost.monitor_realtime(int(duration))
        
        elif cmd == '8' or cmd == 'export':
            ghost.export_session_log()
        
        elif cmd == '9' or cmd == 'exit':
            print("\n[*] Shutting down GhostLink Automotive")
            break
        
        else:
            print(f"[-] Unknown command: {cmd}")


if __name__ == "__main__":
    main()

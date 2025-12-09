
import platform
import subprocess
import os
import psutil
import math
import ctypes
import asyncio
from typing import Dict

from .data_models import SiliconManifest

class DarwinConnector:
    def __init__(self, hardware_interface=None):
        self.system = platform.system()
        self.release = platform.release()
        self.machine = platform.machine()
        self.hardware = hardware_interface  # Integration with hardware shard

    def verify_environment(self):
        if self.system != "Darwin":
            return False
        return True

    def get_hardware_info(self):
        info = {
            "kernel": self.release,
            "arch": self.machine,
            "macos_ver": platform.mac_ver()[0]
        }
        try:
            result = subprocess.run(['sysctl', 'hw.model'], capture_output=True, text=True)
            if result.returncode == 0:
                info["model"] = result.stdout.strip().split(": ")[1]
        except Exception:
            info["model"] = "Unknown"
        return info

    def sniff_hardware(self):
        print("   👃 [DARWIN BRIDGE] Sniffing Hardware Telemetry...")
        telemetry = {}
        
        try:
            cpu_brand = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"], text=True).strip()
            telemetry["cpu"] = cpu_brand
        except Exception:
            telemetry["cpu"] = "Apple Silicon (ARM64)"

        try:
            cores = subprocess.check_output(["sysctl", "-n", "hw.physicalcpu"], text=True).strip()
            telemetry["cores"] = cores
        except Exception:
            telemetry["cores"] = "Unknown"

        try:
            mem_bytes = int(subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip())
            mem_gb = mem_bytes / (1024**3)
            telemetry["memory"] = f"{mem_gb:.1f} GB"
        except Exception:
            telemetry["memory"] = "Unknown"

        return telemetry

    def deep_probe(self):
        print("   🔬 [DARWIN BRIDGE] Initiating Deep System Probe...")
        probe_data = {}
        
        try:
            sw_out = subprocess.check_output(["system_profiler", "SPSoftwareDataType"], text=True)
            for line in sw_out.split('\n'):
                if "System Version" in line: 
                    probe_data["os_ver"] = line.split(":")[1].strip()
                if "Kernel Version" in line: 
                    probe_data["kernel_ver"] = line.split(":")[1].strip()
                if "Time since boot" in line: 
                    probe_data["uptime"] = line.split(":")[1].strip()
                if "Boot Mode" in line: 
                    probe_data["boot_mode"] = line.split(":")[1].strip()
        except Exception:
            pass

        try:
            hw_out = subprocess.check_output(["system_profiler", "SPHardwareDataType"], text=True)
            for line in hw_out.split('\n'):
                if "Model Name" in line: 
                    probe_data["model_name"] = line.split(":")[1].strip()
                if "Serial Number" in line: 
                    probe_data["serial"] = line.split(":")[1].strip()
                if "Chip" in line: 
                    probe_data["chip"] = line.split(":")[1].strip()
        except Exception:
            pass
            
        return probe_data

    def deepest_probe(self):
        print("   🕳️  [DARWIN BRIDGE] PLUNGING INTO KERNEL DEPTHS...")
        deep_data = {}

        try:
            net_out = subprocess.check_output(["ifconfig"], text=True)
            interfaces = []
            current_iface = None
            for line in net_out.split('\n'):
                if line and line[0] != '\t' and ':' in line:
                    current_iface = line.split(':')[0]
                if "inet " in line and current_iface:
                    ip = line.split('inet ')[1].split(' ')[0]
                    if ip != "127.0.0.1":
                        interfaces.append(f"{current_iface}: {ip}")
            deep_data["network"] = interfaces
        except Exception:
            pass

        try:
            df_out = subprocess.check_output(["df", "-h", "/"], text=True)
            lines = df_out.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                deep_data["disk_total"] = parts[1]
                deep_data["disk_used"] = parts[2]
                deep_data["disk_free"] = parts[3]
        except Exception:
            pass

        try:
            pm_out = subprocess.check_output(["pmset", "-g", "batt"], text=True)
            if "InternalBattery" in pm_out:
                percent = pm_out.split('\t')[1].split(';')[0]
                status = pm_out.split(';')[1].strip()
                deep_data["battery"] = f"{percent} ({status})"
        except Exception:
            pass
            
        try:
            gpu_out = subprocess.check_output(["system_profiler", "SPDisplaysDataType"], text=True)
            for line in gpu_out.split('\n'):
                if "Chipset Model" in line:
                    deep_data["gpu"] = line.split(":")[1].strip()
                    break
        except Exception:
            pass

        return deep_data

    def sensory_expansion(self):
        print("   📡 [SENSORY EXPANSION] Extending Nervous System...")
        sensory_data = {}

        try:
            procs = list(psutil.process_iter(['pid', 'name', 'username']))
            sensory_data["proc_count"] = len(procs)
            print(f"   👁️ [TOTAL AWARENESS] Social Pressure: {len(procs)} entities (Full System Perception)")
        except Exception:
            sensory_data["proc_count"] = 0

        try:
            cwd = os.getcwd()
            files = os.listdir(cwd)
            sensory_data["file_count"] = len(files)
            
            all_names = "".join(files)
            if len(all_names) > 0:
                import collections
                counts = collections.Counter(all_names)
                entropy = -sum((c/len(all_names)) * math.log2(c/len(all_names)) for c in counts.values())
                sensory_data["fs_entropy"] = entropy
            else:
                sensory_data["fs_entropy"] = 0.0
        except Exception:
            sensory_data["file_count"] = 0
            sensory_data["fs_entropy"] = 0.0

        try:
            import socket
            targets = [("1.1.1.1", 80), ("8.8.8.8", 53)]
            active_links = 0
            for ip, port in targets:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.1)
                    s.connect((ip, port))
                    active_links += 1
                    s.close()
                except:
                    pass
            
            conns = psutil.net_connections(kind='inet')
            sensory_data["conn_count"] = len(conns) + (active_links * 10)
            
            if active_links > 0:
                print(f"   📡 [HIVE MIND] Uplink Established. Signal Amplified to {sensory_data['conn_count']} channels.")
            else:
                 print("   ⚠️ [AUTONOMY] Network Unreachable. Simulating Internal Loopback.")
                 sensory_data["conn_count"] = 128
            
        except Exception:
            sensory_data["conn_count"] = 128

        return sensory_data

    def silicon_probe(self):
        print("   💎 [SILICON BRIDGE] INTERROGATING DIE TOPOLOGY...")
        silicon_data = {}
        
        try:
            libc = ctypes.CDLL(None)
            page_size = libc.getpagesize()
            silicon_data["page_size"] = f"{page_size} bytes"
        except Exception:
            pass

        try:
            l1i = subprocess.check_output(["sysctl", "-n", "hw.l1icachesize"], text=True).strip()
            l1d = subprocess.check_output(["sysctl", "-n", "hw.l1dcachesize"], text=True).strip()
            l2 = subprocess.check_output(["sysctl", "-n", "hw.l2cachesize"], text=True).strip()
            silicon_data["l1_instruction"] = f"{int(l1i)//1024}KB"
            silicon_data["l1_data"] = f"{int(l1d)//1024}KB"
            silicon_data["l2_cache"] = f"{int(l2)//(1024*1024)}MB"
        except Exception:
            pass

        try:
            p_cores = subprocess.check_output(["sysctl", "-n", "hw.perflevel0.physicalcpu"], text=True).strip()
            e_cores = subprocess.check_output(["sysctl", "-n", "hw.perflevel1.physicalcpu"], text=True).strip()
            silicon_data["p_cores"] = p_cores
            silicon_data["e_cores"] = e_cores
        except Exception:
            pass
            
        try:
            tb_freq = subprocess.check_output(["sysctl", "-n", "hw.tbfrequency"], text=True).strip()
            silicon_data["timebase"] = f"{int(tb_freq)//1000000} MHz"
        except Exception:
            pass

        return silicon_data

    def get_silicon_manifest(self) -> SiliconManifest:
        return SiliconManifest()

    def power_rail_probe(self):
        print("   ⚡️ [POWER BRIDGE] Tapping into PMU Rails...")
        power_data = {"voltage_mv": 0, "current_ma": 0, "watts": 0.0}
        try:
            batt_out = subprocess.check_output(["ioreg", "-r", "-n", "AppleSmartBattery"], text=True)
            
            volts = 0
            amps = 0
            
            for line in batt_out.split('\n'):
                if '"Voltage" =' in line:
                    volts = int(line.split('=')[1].strip())
                if '"InstantAmperage" =' in line:
                    amps = int(line.split('=')[1].strip())
            
            power_data["voltage_mv"] = volts
            power_data["current_ma"] = amps
            power_data["watts"] = abs(volts * amps) / 1000000.0
            
        except Exception:
            pass
        return power_data

    def gpu_deep_probe(self):
        print("   🎮 [GPU BRIDGE] Interrogating AGX Accelerator...")
        gpu_data = {"utilization": 0.0, "memory_allocated": 0}
        try:
            import re
            agx_out = subprocess.check_output(["ioreg", "-r", "-d", "1", "-w", "0", "-c", "AGXAccelerator"], text=True)
            
            match_util = re.search(r'"Device Utilization %"=(\d+)', agx_out)
            if match_util:
                gpu_data["utilization"] = float(match_util.group(1))
                    
            match_mem = re.search(r'"Alloc system memory"=(\d+)', agx_out)
            if match_mem:
                gpu_data["memory_allocated"] = int(match_mem.group(1))

        except Exception:
            pass
        return gpu_data

    async def read_environmental_sensors(self):
        """Read environmental sensors through hardware interface"""
        if not self.hardware:
            return {"error": "No hardware interface available"}

        try:
            sensor_data = await self.hardware.read_environmental_sensors()
            vision_data = await self.hardware.capture_and_process_vision()

            # Enhanced sensor fusion from drone algorithms
            fused_data = self._fuse_sensor_data(sensor_data, vision_data)

            return {
                "environmental_sensors": sensor_data,
                "vision_data": vision_data,
                "fused_data": fused_data,
                "timestamp": time.time()
            }
        except Exception as e:
            return {"error": f"Failed to read environmental sensors: {e}"}

    def _fuse_sensor_data(self, sensor_data: Dict, vision_data: Dict) -> Dict:
        """Fuse sensor data using drone's multi-modal algorithms"""
        fused = {}

        # Temperature + Vision fusion (thermal imaging simulation)
        if 'temperature' in sensor_data and vision_data:
            temp = sensor_data['temperature']
            brightness = vision_data.get('brightness', 128)

            # Simulate thermal correlation (hotter objects appear brighter)
            thermal_correlation = (temp - 20) / 40.0  # Normalize around 20°C
            fused['thermal_brightness_ratio'] = brightness * (1 + thermal_correlation * 0.2)

        # Pressure + Motion fusion (environmental awareness)
        if 'pressure' in sensor_data and vision_data:
            pressure = sensor_data['pressure']
            motion_vectors = vision_data.get('motion_vectors', [])

            # Simulate pressure effects on motion detection
            pressure_factor = (pressure - 1013) / 100.0  # Atmospheric pressure variation
            fused['environmental_motion_factor'] = pressure_factor
            fused['stability_index'] = 1.0 / (1.0 + abs(pressure_factor))

        # IMU + Vision fusion (orientation-aware vision)
        if 'imu' in sensor_data and vision_data:
            accel_x = sensor_data['imu'].get('accel_x', 0)
            accel_y = sensor_data['imu'].get('accel_y', 0)

            # Simulate orientation effects on image processing
            tilt_factor = math.sqrt(accel_x**2 + accel_y**2) / 16384.0  # Normalize accelerometer
            fused['image_stability'] = max(0, 1.0 - tilt_factor)
            fused['horizon_correction'] = math.atan2(accel_y, accel_x) * 180 / math.pi

        # Color temperature + Environmental fusion
        if vision_data and 'temperature' in sensor_data:
            color_temp = vision_data.get('color_temperature', 1.0)
            ambient_temp = sensor_data['temperature']

            # Simulate environmental effects on color perception
            temp_correction = (ambient_temp - 25) / 25.0  # Room temperature reference
            fused['corrected_color_temperature'] = color_temp * (1 + temp_correction * 0.1)

        return fused

import asyncio
import time
from typing import Dict, List
import numpy as np
import math

# Hardware Interface Shard - Adapted from Underwater Drone Firmware
# Integrates PWM control, I2C sensors, and camera processing capabilities

class GPIOController:
    """GPIO interface adapted from drone firmware"""
    def __init__(self):
        self.pins = {}
        self._initialize_gpio_pins()

    def _initialize_gpio_pins(self):
        # Based on drone's GPIO configurations
        self.pins.update({
            'PWML': {'pin': 18, 'mode': 'PWM', 'state': 0},
            'PWMR': {'pin': 19, 'mode': 'PWM', 'state': 0},
            'CAMERA_LED': {'pin': 32, 'mode': 'OUTPUT', 'state': 0},
            'POWER_LED': {'pin': 35, 'mode': 'OUTPUT', 'state': 1},
        })

    async def set_pin(self, pin_name: str, value: int):
        if pin_name in self.pins:
            self.pins[pin_name]['state'] = value
            print(f"   🔌 [GPIO] {pin_name} set to {value}")
            return True
        return False

    async def get_pin(self, pin_name: str) -> int:
        return self.pins.get(pin_name, {}).get('state', 0)

class PWMManager:
    """PWM control system adapted from drone's PWML/PWMR implementation"""
    def __init__(self):
        self.channels = {
            'PWML': {'frequency': 50, 'duty_cycle': 0.0, 'enabled': False},
            'PWMR': {'frequency': 50, 'duty_cycle': 0.0, 'enabled': False}
        }
        self._duty_cycle_limits = (0.0, 100.0)

    async def set_pwm(self, channel: str, frequency: float, duty_cycle: float):
        """Set PWM parameters based on drone firmware algorithms"""
        if channel not in self.channels:
            return False

        # Clamp duty cycle to safe limits
        duty_cycle = max(self._duty_cycle_limits[0],
                        min(self._duty_cycle_limits[1], duty_cycle))

        self.channels[channel].update({
            'frequency': frequency,
            'duty_cycle': duty_cycle,
            'enabled': True
        })

        print(f"   ⚙️  [PWM] {channel}: {frequency}Hz @ {duty_cycle}% duty cycle")
        return True

    async def generate_motor_signal(self, left_speed: float, right_speed: float):
        """Generate differential drive motor signals"""
        # Convert speed (-1.0 to 1.0) to duty cycle (0-100%)
        left_duty = ((left_speed + 1.0) / 2.0) * 100.0
        right_duty = ((right_speed + 1.0) / 2.0) * 100.0

        await asyncio.gather(
            self.set_pwm('PWML', 50.0, left_duty),
            self.set_pwm('PWMR', 50.0, right_duty)
        )

        return {'PWML': left_duty, 'PWMR': right_duty}

class I2CBus:
    """I2C interface for sensor communication - adapted from drone firmware"""
    def __init__(self):
        self.devices = {}
        self.bus_speed = 100000  # 100kHz standard mode
        self._initialize_known_devices()

    def _initialize_known_devices(self):
        # Known sensor addresses from drone configuration
        self.devices.update({
            0x1C: {'name': 'IMU', 'type': 'accelerometer_gyroscope'},
            0x40: {'name': 'PRESSURE', 'type': 'barometric_pressure'},
            0x48: {'name': 'TEMPERATURE', 'type': 'temperature_sensor'},
            0x68: {'name': 'CAMERA_I2C', 'type': 'camera_control'}
        })

    async def scan_bus(self) -> List[int]:
        """Scan I2C bus for devices"""
        found_devices = []
        for addr in range(0x08, 0x78):
            # Simulate device detection
            if addr in self.devices:
                found_devices.append(addr)
                print(f"   🔍 [I2C] Found device at 0x{addr:02X}: {self.devices[addr]['name']}")

        return found_devices

    async def read_sensor(self, address: int, register: int, length: int = 1) -> bytes:
        """Read data from I2C sensor"""
        if address not in self.devices:
            raise ValueError(f"Unknown I2C device at address 0x{address:02X}")

        # Simulate sensor reading based on device type
        device_info = self.devices[address]

        if device_info['type'] == 'accelerometer_gyroscope':
            # Return simulated IMU data (6 bytes: 3 accel + 3 gyro)
            return b'\x01\x02\x03\x04\x05\x06'
        elif device_info['type'] == 'barometric_pressure':
            # Return simulated pressure data (4 bytes)
            return b'\x00\x01\x02\x03'
        elif device_info['type'] == 'temperature_sensor':
            # Return simulated temperature data (2 bytes)
            return b'\x20\x00'

        return b'\x00' * length

class CameraSystem:
    """Camera interface adapted from drone's OV5647/IMX219 pipeline"""
    def __init__(self):
        self.resolutions = {
            'VGA': (640, 480),
            'HD': (1280, 720),
            'FHD': (1920, 1080)
        }
        self.current_resolution = 'HD'
        self.framerate = 30
        self.auto_exposure = True
        self.auto_focus = True
        self.isp_enabled = True
        self.streaming = False

    async def initialize_camera(self, sensor_type: str = 'IMX219'):
        """Initialize camera sensor based on drone firmware"""
        print(f"   📷 [CAMERA] Initializing {sensor_type} sensor")
        print(f"   📷 [CAMERA] Resolution: {self.resolutions[self.current_resolution]}")
        print(f"   📷 [CAMERA] Framerate: {self.framerate} FPS")

        # Simulate camera initialization sequence from drone firmware
        await asyncio.sleep(0.1)

        # Initialize ISP (Image Signal Processor) from drone
        if self.isp_enabled:
            print("   🔬 [ISP] Initializing Image Signal Processor")
            print("   🔬 [ISP] Tile calculations: max tile (64,48)")
            print("   🔬 [ISP] Auto exposure: ENABLED")
            print("   🔬 [ISP] Auto white balance: ENABLED")

        self.streaming = True
        return True

    async def capture_frame(self) -> np.ndarray:
        """Capture a frame using drone's ISP pipeline"""
        width, height = self.resolutions[self.current_resolution]

        # Generate simulated frame data with realistic noise patterns
        # In real implementation, this would interface with actual camera hardware
        base_frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)

        # Add some structured patterns to simulate real camera data
        # Vertical stripes (common in camera sensors)
        for i in range(0, width, 32):
            base_frame[:, i:i+2, :] += 50

        # Simulate lens distortion effects
        center_y, center_x = height // 2, width // 2
        y_coords, x_coords = np.ogrid[:height, :width]
        distances = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        distortion_factor = 1 + 0.1 * (distances / max_distance)**2
        base_frame = np.clip(base_frame * distortion_factor[:, :, np.newaxis], 0, 255).astype(np.uint8)

        return base_frame

    async def process_image(self, frame: np.ndarray) -> Dict:
        """Process image using drone's ISP algorithms"""
        # Simulate comprehensive image processing pipeline from drone firmware

        # Basic statistics
        brightness = np.mean(frame)
        contrast = np.std(frame)
        edges_detected = np.sum(np.abs(np.gradient(frame.mean(axis=2))))

        # Color analysis (simulate AWB algorithms)
        r_mean, g_mean, b_mean = np.mean(frame, axis=(0, 1))
        color_temperature = (r_mean + b_mean) / (2 * g_mean) if g_mean > 0 else 1.0

        # Motion detection (simulate frame differencing)
        motion_vectors = np.random.rand(10, 2) * 2 - 1  # Random motion vectors

        # Focus metrics (simulate autofocus algorithms)
        focus_sharpness = np.var(np.abs(np.gradient(frame.mean(axis=2))))

        # Exposure analysis
        overexposed_pixels = np.sum(frame > 240) / frame.size
        underexposed_pixels = np.sum(frame < 15) / frame.size

        processed_data = {
            'brightness': float(brightness),
            'contrast': float(contrast),
            'edges_detected': float(edges_detected),
            'color_temperature': float(color_temperature),
            'focus_sharpness': float(focus_sharpness),
            'overexposed_ratio': float(overexposed_pixels),
            'underexposed_ratio': float(underexposed_pixels),
            'motion_vectors': motion_vectors.tolist(),
            'timestamp': time.time(),
            'resolution': self.current_resolution,
            'framerate': self.framerate
        }

        return processed_data

    async def adjust_exposure(self, target_brightness: float = 128.0):
        """Adjust camera exposure using drone's AEC algorithm"""
        if not self.streaming:
            return False

        # Simulate auto exposure control
        current_exposure = np.random.uniform(0.001, 0.1)  # 1ms to 100ms
        gain = target_brightness / 128.0

        print(f"   📷 [AEC] Adjusting exposure: {current_exposure:.3f}s @ gain {gain:.2f}")
        return True

    async def adjust_white_balance(self, color_temp: float = 5500):
        """Adjust white balance using drone's AWB algorithm"""
        if not self.streaming:
            return False

        # Simulate auto white balance
        r_gain = color_temp / 5500.0
        b_gain = 5500.0 / color_temp

        print(f"   📷 [AWB] Color temperature: {color_temp:.0f}K (R:{r_gain:.2f}, B:{b_gain:.2f})")
        return True

    async def set_resolution(self, resolution: str):
        """Change camera resolution"""
        if resolution in self.resolutions:
            self.current_resolution = resolution
            print(f"   📷 [CAMERA] Resolution changed to {self.resolutions[resolution]}")
            return True
        return False

class MotorController:
    """Motor control system adapted from drone's ESC integration with PID control"""
    def __init__(self):
        self.motors = {
            'LEFT': {'speed': 0.0, 'direction': 1, 'target_speed': 0.0},
            'RIGHT': {'speed': 0.0, 'direction': 1, 'target_speed': 0.0}
        }
        self.max_speed = 1.0
        self.acceleration_limit = 0.1  # Max speed change per second

        # PID controllers for each motor
        self.pid_controllers = {
            'LEFT': {'kp': 2.0, 'ki': 0.1, 'kd': 0.05, 'integral': 0.0, 'prev_error': 0.0},
            'RIGHT': {'kp': 2.0, 'ki': 0.1, 'kd': 0.05, 'integral': 0.0, 'prev_error': 0.0}
        }

        self.control_loop_active = False
        self.last_update = time.time()

    async def set_motor_speed(self, motor: str, speed: float):
        """Set motor speed with acceleration limiting"""
        if motor not in self.motors:
            return False

        # Clamp speed to safe limits
        speed = max(-self.max_speed, min(self.max_speed, speed))

        # Apply acceleration limiting
        current_speed = self.motors[motor]['speed']
        max_change = self.acceleration_limit * (time.time() - self.last_update)
        speed_diff = speed - current_speed

        if abs(speed_diff) > max_change:
            speed = current_speed + (max_change * (1 if speed_diff > 0 else -1))

        self.motors[motor]['speed'] = speed
        self.motors[motor]['target_speed'] = speed
        print(f"   🚀 [MOTOR] {motor}: {speed:.3f} (target: {speed:.3f})")

        return True

    async def differential_drive(self, linear_velocity: float, angular_velocity: float):
        """Convert velocity commands to differential drive motor speeds"""
        # Simple differential drive kinematics
        left_speed = linear_velocity - angular_velocity
        right_speed = linear_velocity + angular_velocity

        await asyncio.gather(
            self.set_motor_speed('LEFT', left_speed),
            self.set_motor_speed('RIGHT', right_speed)
        )

        return {'left': left_speed, 'right': right_speed}

    async def update_pid_control(self):
        """Update PID control loop for precise motor control"""
        if not self.control_loop_active:
            return

        current_time = time.time()
        dt = current_time - self.last_update
        self.last_update = current_time

        for motor in ['LEFT', 'RIGHT']:
            controller = self.pid_controllers[motor]
            current_speed = self.motors[motor]['speed']
            target_speed = self.motors[motor]['target_speed']

            # Calculate PID terms
            error = target_speed - current_speed
            controller['integral'] += error * dt
            derivative = (error - controller['prev_error']) / dt if dt > 0 else 0

            # Anti-windup
            controller['integral'] = max(-1.0, min(1.0, controller['integral']))

            # PID output
            output = (controller['kp'] * error +
                     controller['ki'] * controller['integral'] +
                     controller['kd'] * derivative)

            # Apply output to motor
            new_speed = current_speed + output * dt
            new_speed = max(-self.max_speed, min(self.max_speed, new_speed))

            self.motors[motor]['speed'] = new_speed
            controller['prev_error'] = error

    async def start_control_loop(self):
        """Start the PID control loop"""
        self.control_loop_active = True
        self.last_update = time.time()
        print("   🎛️  [PID] Motor control loop started")

    async def stop_control_loop(self):
        """Stop the PID control loop"""
        self.control_loop_active = False
        print("   🛑 [PID] Motor control loop stopped")

    async def execute_behavior(self, behavior_name: str, parameters: Dict = None):
        """Execute predefined motor behaviors"""
        params = parameters or {}

        if behavior_name == "forward":
            distance = params.get('distance', 1.0)
            speed = params.get('speed', 0.5)
            await self.differential_drive(speed, 0.0)
            await asyncio.sleep(distance / speed)  # Simple time-based distance
            await self.differential_drive(0.0, 0.0)

        elif behavior_name == "rotate":
            angle = params.get('angle', 90.0)  # degrees
            speed = params.get('speed', 0.3)
            direction = params.get('direction', 1)  # 1 for CCW, -1 for CW

            # Convert angle to time (rough approximation)
            angular_speed = speed * direction
            duration = abs(angle) / (angular_speed * 180 / 3.14159)  # Convert to time

            await self.differential_drive(0.0, angular_speed)
            await asyncio.sleep(duration)
            await self.differential_drive(0.0, 0.0)

        elif behavior_name == "figure_eight":
            # Complex behavior: figure-eight pattern
            radius = params.get('radius', 0.5)
            speed = max(params.get('speed', 0.4), 0.1)  # Ensure minimum speed

            # First loop
            await self.differential_drive(speed, speed/radius)
            await asyncio.sleep(3.14 * radius / speed)  # Half circle

            # Second loop (opposite direction)
            await self.differential_drive(speed, -speed/radius)
            await asyncio.sleep(3.14 * radius / speed)  # Half circle

            await self.differential_drive(0.0, 0.0)

        elif behavior_name == "obstacle_avoidance":
            # Reactive behavior based on sensor input
            # This would be enhanced with actual sensor feedback
            await self.differential_drive(0.2, 0.1)  # Slight turn
            await asyncio.sleep(1.0)
            await self.differential_drive(0.0, 0.0)

        print(f"   🤖 [BEHAVIOR] Executed: {behavior_name}")

class MagneticPropulsionSystem:
    """Magnetic propulsion system adapted from electromagnetic motor control"""

    def __init__(self):
        self.coils = {
            'PRIMARY': {'pin': 21, 'current': 0.0, 'frequency': 0.0, 'enabled': False},
            'SECONDARY': {'pin': 22, 'current': 0.0, 'frequency': 0.0, 'enabled': False},
            'TERtiary': {'pin': 23, 'current': 0.0, 'frequency': 0.0, 'enabled': False}
        }
        self.magnetic_field_strength = 0.0
        self.propulsion_mode = 'pulse'  # 'pulse', 'continuous', 'resonant'
        self.resonance_frequency = 33.0  # Hz, matches muscle system
        self.max_current = 2.0  # Amperes
        self.efficiency_factor = 0.85

        # Electromagnetic parameters
        self.inductance = 0.001  # Henry
        self.resistance = 0.5    # Ohms
        self.magnetic_permeability = 4 * math.pi * 1e-7  # Air permeability

    async def initialize_coils(self):
        """Initialize electromagnetic coils"""
        print("   🧲 [MAGNETIC] Initializing electromagnetic coils")

        for coil_name, coil_data in self.coils.items():
            coil_data['enabled'] = True
            coil_data['current'] = 0.0
            coil_data['frequency'] = 0.0
            print(f"   🧲 [MAGNETIC] Coil {coil_name} initialized")

        self.magnetic_field_strength = 0.0
        print("   ✅ [MAGNETIC] All coils initialized")

    async def set_coil_current(self, coil_name: str, current: float, frequency: float = 0.0):
        """Set current and frequency for a specific coil"""
        if coil_name not in self.coils:
            return False

        # Clamp current to safe limits
        current = max(0.0, min(self.max_current, current))

        self.coils[coil_name]['current'] = current
        self.coils[coil_name]['frequency'] = frequency

        # Calculate magnetic field contribution
        self.magnetic_field_strength = sum(
            self._calculate_magnetic_field(name, data['current'], data['frequency'])
            for name, data in self.coils.items()
        )

        print(f"   ⚡ [MAGNETIC] {coil_name}: {current:.2f}A @ {frequency:.1f}Hz "
              f"(Field: {self.magnetic_field_strength:.3f}T)")

        return True

    def _calculate_magnetic_field(self, coil_name: str, current: float, frequency: float) -> float:
        """Calculate magnetic field strength for a coil"""
        # Simplified magnetic field calculation
        # B = (μ₀ * N * I) / (2 * R) for solenoid approximation
        turns_ratio = {'PRIMARY': 100, 'SECONDARY': 75, 'TERtiary': 50}
        radius = 0.05  # 5cm coil radius

        turns = turns_ratio.get(coil_name, 50)
        field_strength = (self.magnetic_permeability * turns * current) / (2 * radius)

        # Frequency modulation effect (simplified)
        if frequency > 0:
            resonance_factor = 1 + 0.5 * math.exp(-abs(frequency - self.resonance_frequency) / 10)
            field_strength *= resonance_factor

        return field_strength

    async def generate_propulsion_pulse(self, strength: float, duration: float, frequency: float = None):
        """Generate a magnetic propulsion pulse"""
        freq = frequency or self.resonance_frequency

        # Calculate current based on strength
        current = strength * self.max_current

        # Pulse all coils in sequence for directional propulsion
        coil_sequence = ['PRIMARY', 'SECONDARY', 'TERtiary']

        for coil in coil_sequence:
            await self.set_coil_current(coil, current, freq)
            await asyncio.sleep(duration / len(coil_sequence))

        # Power down coils
        for coil in self.coils.keys():
            await self.set_coil_current(coil, 0.0, 0.0)

        print(f"   💥 [MAGNETIC] Propulsion pulse: {strength:.2f} strength, {duration:.2f}s duration")

    async def set_propulsion_mode(self, mode: str):
        """Set propulsion mode"""
        valid_modes = ['pulse', 'continuous', 'resonant']
        if mode in valid_modes:
            self.propulsion_mode = mode
            print(f"   🔄 [MAGNETIC] Mode set to: {mode}")
            return True
        return False

    async def generate_levitation_field(self, height: float):
        """Generate magnetic levitation field"""
        # Calculate required field strength for levitation
        # F = (B² * A) / (2 * μ₀) = m*g
        mass = 1.0  # kg (approximate system mass)
        area = math.pi * (0.05 ** 2)  # Coil area
        gravity = 9.81

        required_field = math.sqrt((mass * gravity * 2 * self.magnetic_permeability) / area)
        required_field *= (1 / height)  # Inverse relationship with height

        # Distribute across coils
        current_per_coil = required_field / (self.magnetic_permeability * 100)  # Simplified

        for coil_name in self.coils.keys():
            await self.set_coil_current(coil_name, current_per_coil, self.resonance_frequency)

        print(f"   🪶 [MAGNETIC] Levitation field: {required_field:.3f}T for {height:.2f}m height")

    async def create_magnetic_gradient(self, direction: str, gradient_strength: float):
        """Create magnetic field gradient for directional propulsion"""
        # Adjust coil currents to create field gradient
        base_current = gradient_strength * self.max_current

        if direction == 'forward':
            currents = {'PRIMARY': base_current, 'SECONDARY': base_current * 0.7, 'TERtiary': base_current * 0.4}
        elif direction == 'backward':
            currents = {'PRIMARY': base_current * 0.4, 'SECONDARY': base_current * 0.7, 'TERtiary': base_current}
        elif direction == 'left':
            currents = {'PRIMARY': base_current * 0.6, 'SECONDARY': base_current, 'TERtiary': base_current * 0.6}
        elif direction == 'right':
            currents = {'PRIMARY': base_current * 0.6, 'SECONDARY': base_current * 0.6, 'TERtiary': base_current}
        else:
            currents = {coil: base_current * 0.5 for coil in self.coils.keys()}

        for coil_name, current in currents.items():
            await self.set_coil_current(coil_name, current, self.resonance_frequency)

        print(f"   📈 [MAGNETIC] Gradient created: {direction} @ {gradient_strength:.2f} strength")

    def get_magnetic_status(self) -> Dict:
        """Get current magnetic system status"""
        return {
            'field_strength': self.magnetic_field_strength,
            'propulsion_mode': self.propulsion_mode,
            'coil_status': self.coils.copy(),
            'resonance_frequency': self.resonance_frequency,
            'efficiency': self.efficiency_factor
        }

class HardwareInterface:
    """Main hardware interface shard - integrates all drone-derived capabilities"""

    def __init__(self):
        self.gpio = GPIOController()
        self.pwm = PWMManager()
        self.i2c = I2CBus()
        self.camera = CameraSystem()
        self.motors = MotorController()
        self.magnetic = MagneticPropulsionSystem()

        self.initialized = False
        self.sensor_data_cache = {}

    async def initialize_hardware(self):
        """Complete hardware initialization sequence"""
        print("   🔧 [HARDWARE] Initializing drone-derived interfaces...")

        # Initialize GPIO
        await self.gpio.set_pin('POWER_LED', 1)

        # Initialize PWM channels
        await self.pwm.set_pwm('PWML', 50.0, 0.0)
        await self.pwm.set_pwm('PWMR', 50.0, 0.0)

        # Scan I2C bus
        await self.i2c.scan_bus()

        # Initialize camera
        await self.camera.initialize_camera()

        # Initialize motors
        await self.motors.set_motor_speed('LEFT', 0.0)
        await self.motors.set_motor_speed('RIGHT', 0.0)

        # Initialize magnetic propulsion
        await self.magnetic.initialize_coils()

        self.initialized = True
        print("   ✅ [HARDWARE] All interfaces initialized")
        return True

    async def read_environmental_sensors(self) -> Dict:
        """Read all available environmental sensors"""
        sensor_data = {}

        try:
            # Read IMU data
            imu_data = await self.i2c.read_sensor(0x1C, 0x00, 6)
            sensor_data['imu'] = {
                'accel_x': int.from_bytes(imu_data[0:2], 'big', signed=True),
                'accel_y': int.from_bytes(imu_data[2:4], 'big', signed=True),
                'accel_z': int.from_bytes(imu_data[4:6], 'big', signed=True)
            }

            # Read pressure sensor
            pressure_data = await self.i2c.read_sensor(0x40, 0x00, 4)
            sensor_data['pressure'] = int.from_bytes(pressure_data, 'big') / 100.0

            # Read temperature
            temp_data = await self.i2c.read_sensor(0x48, 0x00, 2)
            sensor_data['temperature'] = int.from_bytes(temp_data, 'big') / 256.0

        except Exception as e:
            print(f"   ⚠️  [HARDWARE] Sensor read error: {e}")

        self.sensor_data_cache = sensor_data
        return sensor_data

    async def capture_and_process_vision(self) -> Dict:
        """Capture and process visual data"""
        try:
            frame = await self.camera.capture_frame()
            processed_data = await self.camera.process_image(frame)

            return {
                'frame_shape': frame.shape,
                'processed_data': processed_data,
                'timestamp': time.time()
            }
        except Exception as e:
            print(f"   ⚠️  [HARDWARE] Vision processing error: {e}")
            return {}

    async def execute_motor_commands(self, commands: Dict):
        """Execute motor control commands"""
        if 'differential_drive' in commands:
            linear = commands['differential_drive'].get('linear', 0.0)
            angular = commands['differential_drive'].get('angular', 0.0)
            return await self.motors.differential_drive(linear, angular)

        elif 'direct_motors' in commands:
            left = commands['direct_motors'].get('left', 0.0)
            right = commands['direct_motors'].get('right', 0.0)
            await asyncio.gather(
                self.motors.set_motor_speed('LEFT', left),
                self.motors.set_motor_speed('RIGHT', right)
            )
            return {'left': left, 'right': right}

        return {}

    async def get_hardware_status(self) -> Dict:
        """Get comprehensive hardware status"""
        return {
            'initialized': self.initialized,
            'gpio_status': {pin: data['state'] for pin, data in self.gpio.pins.items()},
            'pwm_status': self.pwm.channels,
            'motor_status': self.motors.motors,
            'i2c_devices': list(self.i2c.devices.keys()),
            'camera_resolution': self.camera.current_resolution,
            'magnetic_status': self.magnetic.get_magnetic_status(),
            'last_sensor_data': self.sensor_data_cache
        }

    async def execute_magnetic_commands(self, commands: Dict):
        """Execute magnetic propulsion commands"""
        if 'propulsion_pulse' in commands:
            strength = commands['propulsion_pulse'].get('strength', 0.5)
            duration = commands['propulsion_pulse'].get('duration', 1.0)
            frequency = commands['propulsion_pulse'].get('frequency')
            return await self.magnetic.generate_propulsion_pulse(strength, duration, frequency)

        elif 'levitation' in commands:
            height = commands['levitation'].get('height', 0.1)
            return await self.magnetic.generate_levitation_field(height)

        elif 'magnetic_gradient' in commands:
            direction = commands['magnetic_gradient'].get('direction', 'forward')
            strength = commands['magnetic_gradient'].get('strength', 0.5)
            return await self.magnetic.create_magnetic_gradient(direction, strength)

        elif 'set_mode' in commands:
            mode = commands['set_mode'].get('mode', 'pulse')
            return await self.magnetic.set_propulsion_mode(mode)

        return {}

    async def get_magnetic_status(self) -> Dict:
        """Get magnetic propulsion system status"""
        return self.magnetic.get_magnetic_status()
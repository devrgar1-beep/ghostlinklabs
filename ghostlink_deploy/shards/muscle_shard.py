
import os
import subprocess
import time
import math
import numpy as np

from .data_models import Flux, MuscleThought, CoherenceMetrics

def parse_muscle_output(stderr_output: str):
    thoughts = []
    metrics = CoherenceMetrics()
    
    for line in stderr_output.splitlines():
        line = line.strip()
        if "[SYMBOLIC]" in line:
            try:
                parts = line.split("::", 1)
                left = parts[0].split("|")
                codon = left[0].split("]")[1].strip()
                symbol = left[1].strip()
                msg = parts[1].strip().strip('"')
                thoughts.append(MuscleThought(time.time(), codon, symbol, msg))
            except Exception: 
                pass
            
        if "λ_max" in line:
            try: 
                metrics.lambda_max = float(line.split("≈")[1].split()[0])
            except Exception: 
                pass
            
        if "H_KS" in line:
            try: 
                metrics.h_ks = float(line.split("≈")[1].split()[0])
            except Exception: 
                pass
            
        if "Regime:" in line:
            try: 
                metrics.regime = line.split(":")[1].strip()
            except Exception: 
                pass
            
    return thoughts, metrics

def run_muscle_native(freq: float,
                      duration: float,
                      rate: int,
                      timebase: int,
                      flux: Flux,
                      lorenz_state: tuple,
                      binary_path: str):
    if not os.path.exists(binary_path):
        raise RuntimeError(f"MUSCLE binary not found at {binary_path}")

    sx, sy, sz = lorenz_state

    args = [
        str(binary_path),
        f"{freq:.6f}",
        f"{duration:.6f}",
        str(rate),
        str(timebase),
        f"{flux.load:.6f}",
        f"{flux.gpu_util:.6f}",
        f"{flux.power_watts:.6f}",
        f"{flux.net_flux:.6f}",
        f"{flux.disk_flux:.6f}",
        f"{sx:.6f}",
        f"{sy:.6f}",
        f"{sz:.6f}",
        str(int(flux.process_count)),
        f"{flux.fs_entropy:.6f}",
        str(int(flux.conn_count)),
    ]

    proc = subprocess.run(
        args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stderr_text = ""
    if proc.stderr:
        stderr_text = proc.stderr.decode("utf-8", errors="replace")
        print(stderr_text, end='')

    num_samples = int(duration * rate)
    total_doubles = num_samples * 4
    data = proc.stdout

    if len(data) != total_doubles * 8:
        raise RuntimeError(
            f"MUSCLE output length mismatch: got {len(data)} bytes, "
            f"expected {total_doubles * 8}"
        )

    arr = np.frombuffer(data, dtype="<f8").reshape(num_samples, 4)

    signal = arr[:, 0]
    dream  = arr[:, 1:4]

    next_state = tuple(dream[-1, :])
    thoughts, metrics = parse_muscle_output(stderr_text)

    return signal, dream, next_state, thoughts, metrics

class SignalMuscle:
    def __init__(self, base_dir, hardware_interface=None):
        self.active = True
        self.binary_path = os.path.join(base_dir, "muscle_bin")
        self.dream_state = (0.1, 0.0, 0.0)
        self.hardware = hardware_interface  # Integration with hardware shard
        self._compile_binary(base_dir)

    def _compile_binary(self, base_dir):
        src_path = os.path.join(base_dir, "muscle.c")
        if not os.path.exists(self.binary_path) and os.path.exists(src_path):
            print("   🔨 [MUSCLE] Compiling Native Binary Core...")
            try:
                subprocess.run(["clang", "-O3", src_path, "-o", self.binary_path], check=True)
                print("   ✅ [MUSCLE] Binary Compilation Complete.")
            except Exception as e:
                print(f"   ❌ [MUSCLE] Compilation Failed: {e}")

    def _perform_spectral_analysis(self, signal, sample_rate):
        N = len(signal)
        scan_limit_hz = 200
        k_limit = int(scan_limit_hz * N / sample_rate)
        
        spectrum = []
        for k in range(k_limit):
            re = 0.0
            im = 0.0
            for n in range(N):
                angle = -2 * math.pi * k * n / N
                re += signal[n] * math.cos(angle)
                im += signal[n] * math.sin(angle)
            magnitude = math.sqrt(re**2 + im**2)
            spectrum.append((k * sample_rate / N, magnitude))
        return spectrum

    def _visualize_waveform(self, signal, width=60, height=10):
        print("\n   📈 [OSCILLOSCOPE] SIGNAL WAVEFORM (Time Domain)")
        print("   " + "-"*width)
        
        step = max(1, len(signal) // width)
        samples = signal[::step][:width]
        
        min_val, max_val = min(samples), max(samples)
        range_val = max_val - min_val if max_val != min_val else 1
        
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        for col, val in enumerate(samples):
            row = int((val - min_val) / range_val * (height - 1))
            row = height - 1 - row
            if 0 <= row < height:
                grid[row][col] = '█'

        for row in grid:
            print("   |" + "".join(row) + "|")
        print("   " + "-"*width)

    def _visualize_dream(self, lx, lz):
        print("\n   🌀 [DREAM VISUALIZER] LORENZ ATTRACTOR PROJECTION (X vs Z)")
        print("   " + "="*60)
        
        width = 60
        height = 20
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        density = [[0 for _ in range(width)] for _ in range(height)]
        
        if not lx or not lz: 
            return

        min_x, max_x = min(lx), max(lx)
        min_z, max_z = min(lz), max(lz)
        
        range_x = max_x - min_x if max_x != min_x else 1
        range_z = max_z - min_z if max_z != min_z else 1
        
        for x, z in zip(lx, lz):
            col = int((x - min_x) / range_x * (width - 1))
            row = int((z - min_z) / range_z * (height - 1))
            row = height - 1 - row
            
            if 0 <= row < height and 0 <= col < width:
                density[row][col] += 1

        chars = " ·:!*#@"
        for r in range(height):
            for c in range(width):
                d = density[r][c]
                if d > 0:
                    char_idx = min(d, len(chars) - 1)
                    grid[r][c] = chars[char_idx]

        for row in grid:
            print("   |" + "".join(row) + "|")
        print("   " + "="*60)
        print(f"   🦋 CHAOS METRICS: X_Range=[{min_x:.2f}, {max_x:.2f}] Z_Range=[{min_z:.2f}, {max_z:.2f}]")

    async def generate_pulse(self, frequency, duration, flux, timebase):
        print(f"   ⚡️ [MUSCLE] Initiating {frequency}Hz Pulse Sequence (Chronos Dilation + FM)")
        
        sample_rate = 1000
        signal = []
        thoughts = []
        metrics = CoherenceMetrics()
        
        if os.path.exists(self.binary_path):
            print(f"   🚀 [MUSCLE] HANDING OFF TO NATIVE BINARY: {self.binary_path}")
            print(f"   🧬 [RECURSION] Feeding previous dream state: [{self.dream_state[0]:.2f}, {self.dream_state[1]:.2f}, {self.dream_state[2]:.2f}]")
            try:
                signal_np, _, next_state, thoughts, metrics = run_muscle_native(
                    freq=frequency,
                    duration=duration,
                    rate=sample_rate,
                    timebase=timebase,
                    flux=flux,
                    lorenz_state=self.dream_state,
                    binary_path=self.binary_path
                )
                
                signal = signal_np.tolist()
                self.dream_state = next_state
                
            except Exception as e:
                print(f"   ❌ [MUSCLE] Binary Execution Failed: {e}. Falling back to Python.")
                thoughts = []
                metrics = CoherenceMetrics()
        
        if not signal:
            # Python fallback
            pass
        
        clean_signal = [x for x in signal if not math.isnan(x) and not math.isinf(x)]
        variance = sum((x - (sum(clean_signal) / len(clean_signal))) ** 2 for x in clean_signal) / len(clean_signal) if clean_signal else 0.0
        
        # ... (visualization and analysis)

        # Hardware actuation integration with advanced behaviors
        if self.hardware and hasattr(self.hardware, 'motors'):
            try:
                # Analyze signal characteristics for behavior selection
                signal_strength = max(min(1.0, variance / 10.0), 0.01)  # Normalize variance to 0-1, minimum 0.01
                dominant_freq = max(frequency, 0.1)  # Prevent division by zero

                # Start PID control loop if not active
                if not self.hardware.motors.control_loop_active:
                    await self.hardware.motors.start_control_loop()

                # Select behavior based on signal analysis
                if dominant_freq < 10:  # Low frequency = stable, exploratory behavior
                    if signal_strength > 0.7:  # High variance = figure-eight exploration
                        await self.hardware.motors.execute_behavior("figure_eight",
                            {"radius": 0.5, "speed": min(0.4, signal_strength)})
                        print("   🌀 [BEHAVIOR] Figure-eight exploration pattern")
                    else:  # Low variance = forward movement
                        await self.hardware.motors.execute_behavior("forward",
                            {"distance": signal_strength * 2.0, "speed": signal_strength * 0.5})
                        print("   ➡️  [BEHAVIOR] Forward movement")

                elif 10 <= dominant_freq < 50:  # Medium frequency = rotational behavior
                    rotation_angle = (dominant_freq - 10) * 3.6  # Scale to 0-144 degrees
                    direction = 1 if signal_strength > 0.5 else -1
                    await self.hardware.motors.execute_behavior("rotate",
                        {"angle": rotation_angle, "speed": signal_strength * 0.3, "direction": direction})
                    print(f"   🔄 [BEHAVIOR] Rotation: {rotation_angle:.1f}° {'CCW' if direction > 0 else 'CW'}")

                else:  # High frequency = reactive behavior
                    if signal_strength > 0.8:  # Very high variance = obstacle avoidance
                        await self.hardware.motors.execute_behavior("obstacle_avoidance")
                        print("   ⚠️  [BEHAVIOR] Obstacle avoidance maneuver")
                    else:  # High frequency, low variance = precise positioning
                        # Use PID control for precise motor positioning
                        left_target = (dominant_freq / 100.0 - 0.5) * signal_strength
                        right_target = -left_target  # Opposite for turning
                        await self.hardware.motors.set_motor_speed('LEFT', left_target)
                        await self.hardware.motors.set_motor_speed('RIGHT', right_target)
                        print(f"   🎯 [BEHAVIOR] Precise positioning: L={left_target:.2f}, R={right_target:.2f}")

                # Update PID control
                await self.hardware.motors.update_pid_control()

            except Exception as e:
                print(f"   ⚠️  [MUSCLE] Advanced hardware actuation failed: {e}")
                # Fallback to basic differential drive
                try:
                    linear_velocity = signal_strength * 0.5
                    angular_velocity = (frequency / 100.0 - 0.5) * 0.3
                    motor_commands = await self.hardware.motors.differential_drive(
                        linear_velocity, angular_velocity
                    )
                    print(f"   🤖 [MUSCLE] Fallback actuation: {motor_commands}")
                except Exception as e2:
                    print(f"   ❌ [MUSCLE] Hardware actuation completely failed: {e2}")

        return {"type": "signal", "freq": frequency, "samples": len(signal), "variance": variance}, thoughts, metrics

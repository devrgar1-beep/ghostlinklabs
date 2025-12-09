
import asyncio
import random
import math
from typing import Dict, Any, Optional

from .data_models import AgentState

class Agent:
    def __init__(self, role, agent_id, hardware_interface=None):
        self.state = AgentState(id=agent_id, role=role)
        self.variance_vector = 0.0
        self.hardware = hardware_interface
        self.environmental_memory = []
        self.vision_memory = []
        self.last_sensor_reading = None

    async def process(self, input_data):
        await asyncio.sleep(random.uniform(0.01, 0.03))

        # Base processing
        base_variance = self._calculate_base_variance()

        # Hardware-informed processing
        if self.hardware:
            environmental_influence = await self._process_environmental_feedback()
            vision_influence = await self._process_vision_feedback()
            hardware_variance = self._fuse_hardware_signals(environmental_influence, vision_influence)
        else:
            hardware_variance = 0.0

        # Combine base and hardware influences
        self.variance_vector = base_variance + hardware_variance * 0.3  # 30% hardware influence

        self.state.status = "processing"
        return {
            "agent_id": self.state.id,
            "role": self.state.role,
            "variance": self.variance_vector,
            "hardware_influenced": self.hardware is not None,
            "environmental_factors": len(self.environmental_memory),
            "vision_factors": len(self.vision_memory)
        }

    def _calculate_base_variance(self):
        """Calculate base variance based on agent role"""
        if self.state.role == "Pattern":
            return random.gauss(0, 0.15)
        elif self.state.role == "Sensory":
            return random.gauss(0, 0.08)  # More stable for sensing
        elif self.state.role == "Analysis":
            return random.gauss(0, 0.06)  # Analytical precision
        elif self.state.role == "Safety":
            return random.gauss(0, 0.03)  # High stability for safety
        elif self.state.role == "Coordination":
            return random.gauss(0, 0.05)  # Balanced coordination
        elif self.state.role == "Forge":
            return random.gauss(0, 0.12)  # Creative variance
        elif self.state.role == "Anchor":
            return random.gauss(0, 0.02)  # Maximum stability
        else:
            return random.gauss(0, 0.05)

    async def _process_environmental_feedback(self):
        """Process environmental sensor feedback"""
        try:
            sensor_data = await self.hardware.read_environmental_sensors()
            if sensor_data:
                self.environmental_memory.append(sensor_data)
                if len(self.environmental_memory) > 10:  # Keep last 10 readings
                    self.environmental_memory.pop(0)

                # Calculate environmental influence
                if 'temperature' in sensor_data:
                    temp = sensor_data['temperature']
                    # Temperature affects agent stability (comfort zone around 25°C)
                    temp_stability = 1.0 - abs(temp - 25) / 30.0
                    temp_stability = max(0, min(1, temp_stability))
                else:
                    temp_stability = 0.5

                if 'pressure' in sensor_data:
                    pressure = sensor_data['pressure']
                    # Pressure stability (atmospheric pressure around 1013 hPa)
                    pressure_stability = 1.0 - abs(pressure - 1013) / 100.0
                    pressure_stability = max(0, min(1, pressure_stability))
                else:
                    pressure_stability = 0.5

                return (temp_stability + pressure_stability) / 2.0

        except Exception:
            pass

        return 0.5  # Neutral influence if no data

    async def _process_vision_feedback(self):
        """Process vision system feedback"""
        try:
            vision_data = await self.hardware.capture_and_process_vision()
            if vision_data:
                self.vision_memory.append(vision_data)
                if len(self.vision_memory) > 5:  # Keep last 5 frames
                    self.vision_memory.pop(0)

                # Calculate vision influence based on image quality
                brightness = vision_data.get('brightness', 128) / 255.0
                contrast = min(1.0, vision_data.get('contrast', 50) / 100.0)
                focus = min(1.0, vision_data.get('focus_sharpness', 100) / 500.0)

                # Vision stability based on image quality metrics
                vision_stability = (brightness * 0.3 + contrast * 0.4 + focus * 0.3)

                # Motion influence (more motion = more variance)
                motion_magnitude = sum(abs(v) for vec in vision_data.get('motion_vectors', [])
                                     for v in vec) / len(vision_data.get('motion_vectors', [1]))
                motion_factor = min(1.0, motion_magnitude / 2.0)

                return vision_stability * (1 - motion_factor * 0.5)

        except Exception:
            pass

        return 0.5  # Neutral influence if no data

    def _fuse_hardware_signals(self, environmental: float, vision: float) -> float:
        """Fuse environmental and vision signals into hardware influence"""
        # Weighted combination based on agent role
        if self.state.role == "Sensory":
            # Sensory agents heavily influenced by environment and vision
            return environmental * 0.6 + vision * 0.4
        elif self.state.role == "Safety":
            # Safety agents prioritize environmental stability
            return environmental * 0.8 + vision * 0.2
        elif self.state.role == "Pattern":
            # Pattern agents use vision for pattern recognition
            return environmental * 0.3 + vision * 0.7
        elif self.state.role == "Analysis":
            # Analysis agents balance all inputs
            return environmental * 0.4 + vision * 0.6
        else:
            # Other roles use balanced influence
            return environmental * 0.5 + vision * 0.5

def spawn_constellation(hardware_interface=None):
    agents = []
    roles = ["Sensory"]*16 + ["Analysis"]*16 + ["Pattern"]*16 + ["Safety"]*8 + ["Coordination"]*4 + ["Forge"]*2 + ["Anchor"]*2
    for i, role in enumerate(roles):
        agents.append(Agent(role, f"AG-{i:02d}", hardware_interface))
    return agents

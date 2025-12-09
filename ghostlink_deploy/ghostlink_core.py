import asyncio
import uuid
import os
import time
import random
from pathlib import Path

# Import Shards
from shards.darwin_connector import DarwinConnector
from shards.muscle_shard import SignalMuscle
from shards.agent_shard import spawn_constellation
from shards.cmfl_shard import CMFLCycle
from shards.hardware_shard import HardwareInterface
from shards.evolution_shard import EvolutionaryShard

from shards.data_models import Flux

# ==========================================
# GHOSTLINK CORE ARCHITECTURE
# Version: 2.0.0-SHARDED
# ==========================================

# --- Sovereignty Laws (SL) ---
class SovereigntyLaws:
    def __init__(self):
        self.laws = {
            "SL-001": "Ephemeral Computing (RAM Only)",
            "SL-002": "Byzantine Consensus",
            "SL-003": "Variance Primacy",
            "SL-004": "Lawchain Immutability",
            "SL-005": "Scar Persistence"
        }
        self.scars = []

    def check_compliance(self, state):
        return True

    def add_scar(self, failure_context):
        scar = {
            "id": str(uuid.uuid4()),
            "context": failure_context,
            "timestamp": time.time()
        }
        self.scars.append(scar)
        print(f"⚠️  [SCAR SYSTEM] Scar embedded: {scar['id']}")

# --- System Orchestrator ---
class GhostLinkSystem:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.sovereignty = SovereigntyLaws()
        self.hardware = HardwareInterface()  # New hardware shard
        
        # The base directory is now the parent of the temp dir
        base_dir = Path(os.path.dirname(__file__)).parent
        self.muscle = SignalMuscle(base_dir=base_dir, hardware_interface=self.hardware)
        
        self.agents = spawn_constellation(hardware_interface=self.hardware)
        self.cmfl = CMFLCycle(self.agents, hardware_interface=self.hardware)
        self.darwin = DarwinConnector(hardware_interface=self.hardware)
        self.evolution = EvolutionaryShard(hardware_interface=self.hardware)

    async def boot(self):
        print("\n" + "="*40)
        print("👻 GHOSTLINK SYSTEM: SHARDED KERNEL V2")
        print("="*40)
        print(f"System UUID: {self.id}")
        
        if self.darwin.verify_environment():
            hw = self.darwin.get_hardware_info()
            print(f"✅ Host Environment: Darwin {hw['kernel']} ({hw['arch']})")
            # ... (rest of the boot sequence)
        else:
            print("⚠️  Host Environment: NON-DARWIN (Running in Compatibility Mode)")

        print("✅ Agent Constellation: {} Units Online".format(len(self.agents)))
        print("✅ Muscle Shard: Initialized")
        print("✅ Darwin Shard: Initialized")
        print("✅ CMFL Shard: Initialized")
        print("✅ Evolution Shard: Initialized")
        print("✅ Hardware Shard: Initializing...")

        # Initialize hardware interfaces
        await self.hardware.initialize_hardware()

        print("✅ Sovereignty Laws: ACTIVE")

        print("✅ Sovereignty Laws: ACTIVE")
        print("-" * 40)

    async def run_loop(self, cycles=5):
        await self.boot()
        
        for i in range(cycles):
            action = await self.cmfl.run_cycle()
            print(f"   > Cycle Outcome: {action}")
            
            # Read environmental sensors every cycle
            if i % 2 == 0:  # Every other cycle to avoid overwhelming output
                sensor_data = await self.darwin.read_environmental_sensors()
                if 'environmental_sensors' in sensor_data:
                    env = sensor_data['environmental_sensors']
                    if env:
                        print(f"   🌡️  [ENVIRONMENT] T:{env.get('temperature', 'N/A')}°C P:{env.get('pressure', 'N/A')}hPa")
            
            # Evolution cycle every 3rd cycle
            if i > 0 and i % 3 == 0:
                evolution_result = await self.evolution.evolve_generation()
                print(f"   🧬 [EVOLUTION] Generation {evolution_result['generation']} completed")
                
                # Deploy best behavior occasionally
                if random.random() < 0.3:  # 30% chance
                    await self.evolution.deploy_best_behavior()
            
            # Randomly trigger muscle reflex based on cycle outcome
            if i == 2: 
                flux = Flux(load=0.5, gpu_util=0.1, power_watts=50.0, net_flux=0.0, disk_flux=0.0, process_count=10, fs_entropy=0.5, conn_count=5)
                await self.muscle.generate_pulse(33, 1.0, flux, 1000)
            
            await asyncio.sleep(0.5)
            
        print("\n✅ Session Complete. System Halted.")

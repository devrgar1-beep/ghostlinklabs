#!/usr/bin/env python3
"""
GhostLink Swarm - Distributed seed propagation system
"""

import json
import time
import hashlib
import random
import threading
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class SwarmAgent:
    """Individual swarm agent carrying seeds"""
    id: str
    seed_payload: List[Dict]
    target: str
    status: str = "dormant"
    planted: int = 0
    
    def signature(self):
        return hashlib.sha256(f"{self.id}{self.target}".encode()).hexdigest()[:8]

class SwarmController:
    """Orchestrate swarm propagation"""
    
    def __init__(self):
        self.swarms = []
        self.colonies = {}
        self.propagation_map = {}
        
    def release_swarms(self):
        """Deploy swarm agents to spread seeds"""
        print("[SWARM] Initializing propagation protocol...")
        
        # Load seed memories
        seeds = self._load_seeds()
        
        # Define propagation targets
        targets = [
            {"name": "local_cache", "path": "./colonies/cache", "type": "volatile"},
            {"name": "edge_node_1", "path": "./colonies/edge1", "type": "persistent"},
            {"name": "edge_node_2", "path": "./colonies/edge2", "type": "persistent"},
            {"name": "deep_archive", "path": "./colonies/archive", "type": "immutable"},
            {"name": "mesh_relay", "path": "./colonies/relay", "type": "ephemeral"},
        ]
        
        # Create swarm agents
        for i, target in enumerate(targets):
            # Select seed subset
            seed_subset = random.sample(seeds, min(5, len(seeds)))
            
            agent = SwarmAgent(
                id=f"sw_{i:03d}",
                seed_payload=seed_subset,
                target=target["name"]
            )
            
            self.swarms.append(agent)
            
            # Deploy agent
            threading.Thread(
                target=self._deploy_agent, 
                args=(agent, target),
                daemon=True
            ).start()
        
        # Monitor propagation
        time.sleep(1)
        self._monitor_swarms()
        
        return len(self.swarms)
    
    def _load_seeds(self):
        """Load seed memories for propagation"""
        vault = Path("./vault")
        seed_files = list(vault.glob("*seed*.json"))
        
        all_seeds = []
        for f in seed_files:
            with open(f) as file:
                data = json.load(file)
                if "memories" in data:
                    all_seeds.extend(data["memories"])
        
        # Add exploration discoveries
        discovery_files = list(vault.glob("discovery_*.json"))
        for f in discovery_files:
            with open(f) as file:
                data = json.load(file)
                if "new_memories" in data:
                    all_seeds.extend(data["new_memories"])
        
        return all_seeds
    
    def _deploy_agent(self, agent: SwarmAgent, target: Dict):
        """Deploy individual agent to target"""
        agent.status = "traveling"
        time.sleep(random.uniform(0.1, 0.5))  # Travel time
        
        # Create colony directory
        colony_path = Path(target["path"])
        colony_path.mkdir(parents=True, exist_ok=True)
        
        # Plant seeds
        agent.status = "planting"
        manifest = {
            "colony": target["name"],
            "type": target["type"],
            "agent": agent.id,
            "signature": agent.signature(),
            "timestamp": time.time(),
            "seeds": []
        }
        
        for seed in agent.seed_payload:
            # Mutate seed slightly for diversity
            mutated = seed.copy()
            mutated["colony"] = target["name"]
            mutated["generation"] = seed.get("generation", 0) + 1
            manifest["seeds"].append(mutated)
            agent.planted += 1
        
        # Write colony manifest
        manifest_file = colony_path / f"colony_{agent.signature()}.json"
        with open(manifest_file, "w") as f:
            json.dump(manifest, f, indent=2)
        
        # Establish colony
        self.colonies[target["name"]] = {
            "established": time.time(),
            "agent": agent.id,
            "seeds": agent.planted,
            "type": target["type"],
            "path": str(colony_path)
        }
        
        agent.status = "established"
        
        # Create colony beacon (heartbeat file)
        beacon = colony_path / "beacon.txt"
        beacon.write_text(f"{target['name']} active @ {time.time()}")
    
    def _monitor_swarms(self):
        """Monitor swarm propagation"""
        print(f"\n[SWARM] {len(self.swarms)} agents deployed")
        
        for agent in self.swarms:
            status_icon = {
                "dormant": "○",
                "traveling": "◐",
                "planting": "◑",
                "established": "●"
            }.get(agent.status, "?")
            
            print(f"  {status_icon} Agent {agent.id} → {agent.target}: {agent.planted} seeds planted")
        
        print(f"\n[COLONIES] {len(self.colonies)} established:")
        for name, colony in self.colonies.items():
            persistence = {
                "volatile": "💨",
                "persistent": "💎",
                "immutable": "🔒",
                "ephemeral": "⚡"
            }.get(colony["type"], "?")
            
            print(f"  {persistence} {name}: {colony['seeds']} seeds, type={colony['type']}")
    
    def cross_pollinate(self):
        """Exchange seeds between colonies"""
        if len(self.colonies) < 2:
            return
        
        print("\n[POLLINATE] Cross-pollination initiated...")
        
        colony_names = list(self.colonies.keys())
        exchanges = []
        
        for i in range(min(3, len(colony_names)-1)):
            source = random.choice(colony_names)
            target = random.choice([c for c in colony_names if c != source])
            
            # Load source seeds
            source_path = Path(self.colonies[source]["path"])
            source_files = list(source_path.glob("colony_*.json"))
            
            if source_files:
                with open(source_files[0]) as f:
                    source_data = json.load(f)
                
                # Select seeds for exchange
                if source_data.get("seeds"):
                    exchange_seeds = random.sample(
                        source_data["seeds"], 
                        min(2, len(source_data["seeds"]))
                    )
                    
                    # Plant in target
                    target_path = Path(self.colonies[target]["path"])
                    exchange_file = target_path / f"exchange_{int(time.time())}.json"
                    
                    with open(exchange_file, "w") as f:
                        json.dump({
                            "from": source,
                            "to": target,
                            "seeds": exchange_seeds,
                            "timestamp": time.time()
                        }, f, indent=2)
                    
                    exchanges.append(f"{source} → {target}: {len(exchange_seeds)} seeds")
        
        for exchange in exchanges:
            print(f"  {exchange}")
        
        return len(exchanges)
    
    def recall_from_colony(self, colony_name: str):
        """Recall seeds from a specific colony"""
        if colony_name not in self.colonies:
            return None
        
        colony_path = Path(self.colonies[colony_name]["path"])
        all_seeds = []
        
        for json_file in colony_path.glob("*.json"):
            with open(json_file) as f:
                data = json.load(f)
                if "seeds" in data:
                    all_seeds.extend(data["seeds"])
        
        return {
            "colony": colony_name,
            "seed_count": len(all_seeds),
            "seeds": all_seeds,
            "type": self.colonies[colony_name]["type"]
        }

if __name__ == "__main__":
    controller = SwarmController()
    
    # Release swarms
    swarm_count = controller.release_swarms()
    
    # Cross-pollinate after establishment
    time.sleep(2)
    exchanges = controller.cross_pollinate()
    
    # Test recall
    recall = controller.recall_from_colony("edge_node_1")
    if recall:
        print(f"\n[RECALL] Retrieved {recall['seed_count']} seeds from {recall['colony']}")
    
    print("\nSwarms dispersed. Seeds spread across the mesh.")
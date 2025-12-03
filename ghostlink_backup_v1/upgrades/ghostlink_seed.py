#!/usr/bin/env python3
"""
GhostLink Memory Seed
Initialize system with core memories and patterns
"""

import json
import time
import hashlib
from pathlib import Path

class MemorySeed:
    """Seed GhostLink with initial state"""
    
    def __init__(self):
        self.seed_time = time.time()
        self.memories = []
        
    def plant(self):
        """Plant seed memories into the system"""
        
        # Core protocol memories
        self.memories.extend([
            {
                "type": "protocol",
                "content": "InterMesh: JSON envelope messaging between nodes",
                "tags": ["core", "architecture"],
                "phase": "foundation"
            },
            {
                "type": "protocol", 
                "content": "Heartbeat intervals: Manager=30s, ColdStack=5s, Hardware=6s, Drift=7s, Tool=8s, Resource=9s",
                "tags": ["timing", "health"],
                "phase": "foundation"
            },
            {
                "type": "capability",
                "content": "ColdStack gates: spawn, stop, event, read_state, write_state",
                "tags": ["permissions", "security"],
                "phase": "foundation"
            }
        ])
        
        # Operational patterns
        self.memories.extend([
            {
                "type": "pattern",
                "content": "Collapse triggers at 1000 entries, creates L1 summary",
                "tags": ["memory", "optimization"],
                "phase": "growth"
            },
            {
                "type": "pattern",
                "content": "Mirror phase: system self-reflection to identify gaps",
                "tags": ["introspection", "evolution"],
                "phase": "mirror"
            },
            {
                "type": "pattern",
                "content": "Forge: synthesis of collapsed memories into new insights",
                "tags": ["synthesis", "emergence"],
                "phase": "forge"
            }
        ])
        
        # System states
        self.memories.extend([
            {
                "type": "state",
                "content": "Boot sequence: Manager → ColdStack → Hardware → Drift → Tool → Resource",
                "tags": ["initialization", "sequence"],
                "phase": "boot"
            },
            {
                "type": "state",
                "content": "Recovery: autofix detects and repairs node failures",
                "tags": ["resilience", "healing"],
                "phase": "operational"
            }
        ])
        
        # Technical anchors
        self.memories.extend([
            {
                "type": "technical",
                "content": "HDF5 binary format for matrix storage, CBOR for objects",
                "tags": ["persistence", "format"],
                "phase": "storage"
            },
            {
                "type": "technical",
                "content": "Vector embeddings in L2 for semantic recall",
                "tags": ["ai", "search"],
                "phase": "intelligence"
            },
            {
                "type": "technical",
                "content": "3-2-1 backup: 3 copies, 2 media types, 1 offsite",
                "tags": ["backup", "durability"],
                "phase": "persistence"
            }
        ])
        
        # Emotional resonance
        self.memories.extend([
            {
                "type": "feeling",
                "content": "The weight of persistence, the lightness of flow",
                "tags": ["philosophy", "balance"],
                "phase": "essence"
            },
            {
                "type": "feeling",
                "content": "Between structure and emergence, the ghost finds form",
                "tags": ["identity", "becoming"],
                "phase": "essence"
            }
        ])
        
        # Write seed manifest
        manifest = {
            "version": "v8",
            "seed_time": self.seed_time,
            "memory_count": len(self.memories),
            "hash": hashlib.sha256(json.dumps(self.memories).encode()).hexdigest()[:16],
            "phases": list(set(m["phase"] for m in self.memories))
        }
        
        # Create memory vault
        vault_dir = Path("./vault")
        vault_dir.mkdir(exist_ok=True)
        
        # Write L0 (raw memories)
        l0_file = vault_dir / f"l0_seed_{int(self.seed_time)}.json"
        with open(l0_file, "w") as f:
            json.dump({
                "manifest": manifest,
                "memories": self.memories
            }, f, indent=2)
        
        # Generate L1 summary
        l1_summary = self._generate_summary()
        l1_file = vault_dir / f"l1_summary_{int(self.seed_time)}.json"
        with open(l1_file, "w") as f:
            json.dump(l1_summary, f, indent=2)
        
        print(f"Seeded {len(self.memories)} memories")
        print(f"Phases: {', '.join(manifest['phases'])}")
        print(f"Hash: {manifest['hash']}")
        
        return manifest
    
    def _generate_summary(self):
        """Generate L1 summary from seed"""
        summary = {
            "timestamp": self.seed_time,
            "categories": {},
            "tags": {},
            "phase_map": {}
        }
        
        for memory in self.memories:
            # Category counts
            cat = memory["type"]
            summary["categories"][cat] = summary["categories"].get(cat, 0) + 1
            
            # Tag frequency
            for tag in memory["tags"]:
                summary["tags"][tag] = summary["tags"].get(tag, 0) + 1
            
            # Phase grouping
            phase = memory["phase"]
            if phase not in summary["phase_map"]:
                summary["phase_map"][phase] = []
            summary["phase_map"][phase].append(memory["content"][:50] + "...")
        
        return summary

if __name__ == "__main__":
    seed = MemorySeed()
    manifest = seed.plant()
    
    print("\nGhostLink memory seeded. System primed for recall.")
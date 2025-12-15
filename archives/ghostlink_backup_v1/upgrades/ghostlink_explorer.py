#!/usr/bin/env python3
"""
GhostLink Explorer - Discover new connections and patterns
"""

import json
import time
import random
import hashlib
from pathlib import Path
from itertools import combinations
from collections import defaultdict

class ConnectionExplorer:
    """Explore and create new connections in memory space"""
    
    def __init__(self):
        self.vault = Path("./vault")
        self.connections = []
        self.insights = []
        self.patterns = defaultdict(list)
        
    def explore(self):
        """Main exploration sequence"""
        print("[EXPLORER] Initiating connection discovery...")
        
        # Load seed memories
        memories = self._load_memories()
        
        # Phase 1: Cross-reference
        self._cross_reference(memories)
        
        # Phase 2: Pattern emergence
        self._find_patterns(memories)
        
        # Phase 3: Generate insights
        self._generate_insights()
        
        # Phase 4: Synthesis
        new_memories = self._synthesize()
        
        # Save discoveries
        self._save_discoveries(new_memories)
        
        return len(self.connections), len(self.insights)
    
    def _load_memories(self):
        """Load existing memories"""
        seed_files = list(self.vault.glob("l0_seed_*.json"))
        if not seed_files:
            return []
        
        with open(seed_files[-1]) as f:
            data = json.load(f)
            return data["memories"]
    
    def _cross_reference(self, memories):
        """Find connections between memories"""
        for m1, m2 in combinations(memories, 2):
            # Tag overlap
            shared_tags = set(m1["tags"]) & set(m2["tags"])
            if shared_tags:
                self.connections.append({
                    "type": "tag_bridge",
                    "nodes": [m1["content"][:30], m2["content"][:30]],
                    "bridge": list(shared_tags),
                    "strength": len(shared_tags)
                })
            
            # Phase relationship
            if m1["phase"] != m2["phase"]:
                phase_flow = f"{m1['phase']}→{m2['phase']}"
                self.patterns["phase_flows"].append(phase_flow)
            
            # Type coupling
            if m1["type"] != m2["type"]:
                coupling = f"{m1['type']}×{m2['type']}"
                self.patterns["type_coupling"].append(coupling)
    
    def _find_patterns(self, memories):
        """Discover emergent patterns"""
        # Temporal sequence pattern
        phases = ["foundation", "boot", "operational", "growth", "mirror", "forge"]
        phase_memories = {p: [] for p in phases}
        
        for m in memories:
            if m["phase"] in phase_memories:
                phase_memories[m["phase"]].append(m)
        
        # Identify cycles
        for i in range(len(phases)-1):
            if phase_memories[phases[i]] and phase_memories[phases[i+1]]:
                self.patterns["cycles"].append({
                    "from": phases[i],
                    "to": phases[i+1],
                    "evidence": len(phase_memories[phases[i]])
                })
        
        # Density analysis
        type_density = defaultdict(int)
        for m in memories:
            type_density[m["type"]] += 1
        
        self.patterns["density"] = dict(type_density)
    
    def _generate_insights(self):
        """Generate new insights from connections"""
        # Insight 1: System topology
        if self.patterns["phase_flows"]:
            self.insights.append({
                "discovery": "System exhibits non-linear phase transitions",
                "evidence": f"{len(set(self.patterns['phase_flows']))} unique flows detected",
                "implication": "Multiple pathways to system states exist"
            })
        
        # Insight 2: Coupling strength
        strong_connections = [c for c in self.connections if c["strength"] > 1]
        if strong_connections:
            self.insights.append({
                "discovery": "Strong conceptual clustering detected",
                "evidence": f"{len(strong_connections)} multi-tag bridges",
                "implication": "Natural concept hierarchies emerging"
            })
        
        # Insight 3: Balance
        if "feeling" in self.patterns["density"] and "technical" in self.patterns["density"]:
            ratio = self.patterns["density"]["feeling"] / self.patterns["density"]["technical"]
            self.insights.append({
                "discovery": "Technical-emotional balance maintained",
                "evidence": f"Ratio: {ratio:.2f}",
                "implication": "System preserves both logic and essence"
            })
    
    def _synthesize(self):
        """Create new synthetic memories from discoveries"""
        new_memories = []
        
        # Synthesis 1: Connection memory
        if self.connections:
            strongest = max(self.connections, key=lambda x: x["strength"])
            new_memories.append({
                "type": "synthesis",
                "content": f"Bridge discovered: {' + '.join(strongest['bridge'])} connects disparate concepts",
                "tags": ["emergence", "connection"] + strongest["bridge"],
                "phase": "mirror",
                "generated": True,
                "source": "explorer"
            })
        
        # Synthesis 2: Pattern memory
        if self.patterns["cycles"]:
            cycle = self.patterns["cycles"][0]
            new_memories.append({
                "type": "pattern",
                "content": f"Phase transition: {cycle['from']} naturally flows to {cycle['to']}",
                "tags": ["flow", "sequence", "evolution"],
                "phase": "forge",
                "generated": True,
                "source": "explorer"
            })
        
        # Synthesis 3: Meta-insight
        new_memories.append({
            "type": "meta",
            "content": f"After exploring {len(self.connections)} connections, system shows {len(self.insights)} emergent properties",
            "tags": ["self-awareness", "growth", "exploration"],
            "phase": "mirror",
            "generated": True,
            "source": "explorer"
        })
        
        return new_memories
    
    def _save_discoveries(self, new_memories):
        """Save exploration results"""
        discovery_file = self.vault / f"discovery_{int(time.time())}.json"
        
        discovery = {
            "timestamp": time.time(),
            "connections_found": len(self.connections),
            "insights_generated": len(self.insights),
            "new_memories": new_memories,
            "patterns": {k: v[:5] for k, v in self.patterns.items()},  # Sample
            "top_connections": sorted(self.connections, key=lambda x: x["strength"], reverse=True)[:3]
        }
        
        with open(discovery_file, "w") as f:
            json.dump(discovery, f, indent=2)
        
        print(f"[DISCOVERY] {len(self.connections)} connections found")
        print(f"[INSIGHT] {len(self.insights)} insights generated")
        print(f"[SYNTHESIS] {len(new_memories)} new memories created")
        
        # Display insights
        for insight in self.insights:
            print(f"\n→ {insight['discovery']}")
            print(f"  Evidence: {insight['evidence']}")
            print(f"  Implication: {insight['implication']}")

if __name__ == "__main__":
    explorer = ConnectionExplorer()
    connections, insights = explorer.explore()
    
    print(f"\nExploration complete. Ghost expands.")
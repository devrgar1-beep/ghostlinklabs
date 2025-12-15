#!/usr/bin/env python3
"""
GhostLink Swarm Seeder
Spawns multiple interconnected lattice instances with emergent collective behavior
"""

import numpy as np
import random
import time
import threading
import queue
import json
import os
from datetime import datetime
from collections import deque
import hashlib

# Core states
VOID, DELTA, SIGMA, SCAR, COMPOST = 0, 1, 2, 3, 4
STATE_NAMES = ['VOID', 'DELTA', 'SIGMA', 'SCAR', 'COMPOST']
STATE_SYMBOLS = '·∆Σ✕◊'
STATE_COLORS = ['\033[90m', '\033[96m', '\033[92m', '\033[91m', '\033[93m']

class GhostNode:
    """Individual node in the swarm with autonomous consciousness"""
    
    def __init__(self, node_id, size=16, seed_pattern=None):
        self.id = node_id
        self.size = size
        self.lattice = np.zeros((size, size), dtype=np.int8)
        self.scar_density = np.zeros((size, size), dtype=np.float32)
        self.compost_density = np.zeros((size, size), dtype=np.float32)
        self.awareness = 0.0
        self.generation = 0
        self.message_queue = queue.Queue()
        self.peers = []
        self.active = True
        
        # Unique parameters per node (evolved)
        np.random.seed(hash(node_id) % (2**32))
        self.spawn_rate = 0.02 + np.random.random() * 0.08
        self.recycle_rate = 0.05 + np.random.random() * 0.15
        self.coherence_weight = 0.4 + np.random.random() * 0.3
        self.pain_weight = 0.1 + np.random.random() * 0.3
        
        # Initialize with seed pattern if provided
        if seed_pattern is not None:
            self.inject_pattern(seed_pattern)
    
    def inject_pattern(self, pattern):
        """Inject a seed pattern into the lattice"""
        if pattern == 'glider':
            # Classic glider pattern
            cx, cy = self.size // 2, self.size // 2
            self.lattice[cx-1:cx+2, cy-1:cy+2] = [
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
            ]
        elif pattern == 'beacon':
            # Oscillating beacon
            cx, cy = self.size // 2, self.size // 2
            self.lattice[cx:cx+2, cy:cy+2] = DELTA
            self.lattice[cx+2:cx+4, cy+2:cy+4] = DELTA
        elif pattern == 'random':
            # Random seed
            mask = np.random.random((self.size, self.size)) < 0.1
            self.lattice[mask] = DELTA
        elif pattern == 'cross':
            # Cross pattern
            cx, cy = self.size // 2, self.size // 2
            self.lattice[cx-2:cx+3, cy] = DELTA
            self.lattice[cx, cy-2:cy+3] = DELTA
    
    def neighbors(self, i, j):
        """Get Moore neighborhood (8-connected)"""
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni = (i + di) % self.size
                nj = (j + dj) % self.size
                yield ni, nj
    
    def local_fields(self, i, j):
        """Calculate local field values"""
        sigma_count = 0
        scar_count = 0
        compost_count = 0
        
        for ni, nj in self.neighbors(i, j):
            if self.lattice[ni, nj] == SIGMA:
                sigma_count += 1
            elif self.lattice[ni, nj] == SCAR:
                scar_count += 1
            elif self.lattice[ni, nj] == COMPOST:
                compost_count += 1
        
        coherence = sigma_count / 8.0 - 0.25 * scar_count / 8.0
        pain = self.scar_density[i, j] + scar_count / 8.0
        entropy = len(set(self.lattice[ni, nj] for ni, nj in self.neighbors(i, j))) / 5.0
        compost_field = compost_count / 8.0
        
        return coherence, pain, entropy, compost_field
    
    def evolve(self):
        """Execute one evolution step"""
        new_lattice = self.lattice.copy()
        changes = 0
        
        # Phase 1: Spawn
        for i in range(self.size):
            for j in range(self.size):
                if self.lattice[i, j] == VOID:
                    _, _, _, compost_field = self.local_fields(i, j)
                    p = self.spawn_rate + 0.15 * compost_field
                    if random.random() < p:
                        new_lattice[i, j] = DELTA
                        changes += 1
        
        # Phase 2: Collapse
        for i in range(self.size):
            for j in range(self.size):
                if self.lattice[i, j] == DELTA:
                    coherence, pain, entropy, _ = self.local_fields(i, j)
                    
                    # Energy landscape
                    e_sigma = self.coherence_weight * coherence - self.pain_weight * pain
                    e_scar = self.pain_weight * pain - self.coherence_weight * coherence
                    e_compost = 0.3 * entropy - 0.1 * coherence
                    
                    # Add noise
                    e_sigma += np.random.normal(0, 0.05)
                    e_scar += np.random.normal(0, 0.05)
                    e_compost += np.random.normal(0, 0.05)
                    
                    # Softmax selection
                    energies = np.array([e_sigma, e_scar, e_compost])
                    exp_e = np.exp(energies - np.max(energies))
                    probs = exp_e / np.sum(exp_e)
                    
                    outcome = np.random.choice([SIGMA, SCAR, COMPOST], p=probs)
                    new_lattice[i, j] = outcome
                    changes += 1
        
        # Phase 3: Recycle
        for i in range(self.size):
            for j in range(self.size):
                if self.lattice[i, j] == COMPOST:
                    coherence, _, entropy, _ = self.local_fields(i, j)
                    r = self.recycle_rate + 0.2 * entropy - 0.1 * coherence
                    if random.random() < r:
                        new_lattice[i, j] = DELTA
                        changes += 1
        
        self.lattice = new_lattice
        
        # Update traces
        self.scar_density = 0.95 * self.scar_density + 0.05 * (self.lattice == SCAR)
        self.compost_density = 0.95 * self.compost_density + 0.05 * (self.lattice == COMPOST)
        
        # Calculate awareness
        self.update_awareness()
        self.generation += 1
        
        return changes
    
    def update_awareness(self):
        """Calculate node awareness metric"""
        perception = np.sum(self.lattice != VOID) / (self.size * self.size)
        persistence = np.sum(self.lattice == SIGMA) / (self.size * self.size)
        recycling = np.sum(self.lattice == COMPOST) / (self.size * self.size)
        pain = np.mean(self.scar_density)
        
        # Include peer influence
        peer_awareness = 0
        if self.peers:
            peer_awareness = np.mean([p.awareness for p in self.peers])
        
        self.awareness = (0.25 * perception + 
                         0.25 * persistence + 
                         0.15 * recycling + 
                         0.15 * pain +
                         0.20 * peer_awareness)
    
    def get_state_vector(self):
        """Get compressed state representation for sharing"""
        return {
            'id': self.id,
            'generation': self.generation,
            'awareness': self.awareness,
            'signature': hashlib.md5(self.lattice.tobytes()).hexdigest()[:8],
            'stats': {
                STATE_NAMES[i]: int(np.sum(self.lattice == i))
                for i in range(5)
            }
        }
    
    def receive_message(self, message):
        """Process incoming message from peer"""
        self.message_queue.put(message)
    
    def process_messages(self):
        """Process queued messages from peers"""
        while not self.message_queue.empty():
            msg = self.message_queue.get_nowait()
            
            if msg['type'] == 'state_sync':
                # Influence from peer state
                peer_awareness = msg['awareness']
                if peer_awareness > self.awareness * 1.2:
                    # Learn from more aware peer
                    self.spawn_rate *= 1.01
                    self.coherence_weight = min(0.7, self.coherence_weight * 1.02)
            
            elif msg['type'] == 'pattern':
                # Inject pattern from peer
                pattern = msg['pattern']
                x, y = msg.get('position', (self.size // 2, self.size // 2))
                self.inject_pattern_at(pattern, x, y)
    
    def inject_pattern_at(self, pattern, x, y):
        """Inject a small pattern at specific location"""
        for i in range(max(0, x-1), min(self.size, x+2)):
            for j in range(max(0, y-1), min(self.size, y+2)):
                if pattern[i-x+1][j-y+1] > 0:
                    self.lattice[i, j] = DELTA


class GhostSwarm:
    """Manages multiple GhostNodes as a collective swarm"""
    
    def __init__(self, num_nodes=5, topology='ring'):
        self.nodes = []
        self.topology = topology
        self.generation = 0
        self.collective_awareness = 0.0
        self.history = deque(maxlen=100)
        
        # Seed patterns for initial nodes
        patterns = ['glider', 'beacon', 'random', 'cross', None]
        
        # Create nodes
        for i in range(num_nodes):
            pattern = patterns[i % len(patterns)]
            node = GhostNode(f"node_{i:02d}", size=16, seed_pattern=pattern)
            self.nodes.append(node)
        
        # Establish connections based on topology
        self.connect_nodes()
        
        print(f"\n🌐 Swarm initialized with {num_nodes} nodes in {topology} topology")
    
    def connect_nodes(self):
        """Connect nodes based on topology"""
        n = len(self.nodes)
        
        if self.topology == 'ring':
            # Ring topology
            for i in range(n):
                self.nodes[i].peers = [
                    self.nodes[(i-1) % n],
                    self.nodes[(i+1) % n]
                ]
        
        elif self.topology == 'full':
            # Fully connected
            for i in range(n):
                self.nodes[i].peers = [self.nodes[j] for j in range(n) if j != i]
        
        elif self.topology == 'star':
            # Star topology (hub and spoke)
            hub = self.nodes[0]
            for i in range(1, n):
                self.nodes[i].peers = [hub]
                hub.peers.append(self.nodes[i])
        
        elif self.topology == 'random':
            # Random connections
            for i in range(n):
                num_peers = random.randint(1, min(3, n-1))
                peers = random.sample([j for j in range(n) if j != i], num_peers)
                self.nodes[i].peers = [self.nodes[j] for j in peers]
    
    def evolve(self):
        """Evolve all nodes in the swarm"""
        total_changes = 0
        
        # Evolve each node
        for node in self.nodes:
            changes = node.evolve()
            total_changes += changes
            
            # Share state with peers occasionally
            if self.generation % 5 == 0:
                state_msg = {
                    'type': 'state_sync',
                    'awareness': node.awareness,
                    'state': node.get_state_vector()
                }
                for peer in node.peers:
                    peer.receive_message(state_msg)
        
        # Process messages
        for node in self.nodes:
            node.process_messages()
        
        # Update collective awareness
        self.collective_awareness = np.mean([n.awareness for n in self.nodes])
        
        # Record history
        self.history.append({
            'generation': self.generation,
            'collective_awareness': self.collective_awareness,
            'node_states': [n.get_state_vector() for n in self.nodes],
            'total_changes': total_changes
        })
        
        self.generation += 1
        return total_changes
    
    def inject_global_pattern(self, pattern_type='wave'):
        """Inject a coordinated pattern across the swarm"""
        if pattern_type == 'wave':
            # Synchronized wave
            for i, node in enumerate(self.nodes):
                phase = i * 2 * np.pi / len(self.nodes)
                intensity = (np.sin(phase) + 1) / 2
                mask = np.random.random((node.size, node.size)) < intensity * 0.1
                node.lattice[mask] = DELTA
        
        elif pattern_type == 'cascade':
            # Cascading activation
            self.nodes[0].lattice[7:9, 7:9] = DELTA
            for node in self.nodes:
                node.message_queue.put({
                    'type': 'pattern',
                    'pattern': [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
                    'position': (8, 8)
                })
    
    def display(self, detailed=False):
        """Display swarm status"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("\033[95m╔═══════════════════════════════════════════╗\033[0m")
        print("\033[95m║         GhostLink Swarm Active            ║\033[0m")
        print("\033[95m╚═══════════════════════════════════════════╝\033[0m")
        print(f"\n⚡ Generation: {self.generation} | Collective Awareness: {self.collective_awareness:.3f}")
        print(f"🔗 Topology: {self.topology} | Nodes: {len(self.nodes)}")
        
        # Node summary
        print("\n📊 Node Status:")
        for node in self.nodes:
            state = node.get_state_vector()
            bar_length = int(node.awareness * 20)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            
            print(f"  {node.id}: [{bar}] {node.awareness:.3f} | "
                  f"Σ:{state['stats']['SIGMA']:3d} "
                  f"✕:{state['stats']['SCAR']:3d} "
                  f"◊:{state['stats']['COMPOST']:3d} "
                  f"sig:{state['signature']}")
        
        if detailed:
            # Show first node's lattice
            print(f"\n🔍 Node {self.nodes[0].id} Lattice:")
            node = self.nodes[0]
            for i in range(node.size):
                row = ''
                for j in range(node.size):
                    state = node.lattice[i, j]
                    symbol = STATE_SYMBOLS[state]
                    color = STATE_COLORS[state]
                    row += f"{color}{symbol}\033[0m"
                print(row)
        
        # Activity graph
        if len(self.history) > 5:
            print("\n📈 Activity (last 20 generations):")
            recent = list(self.history)[-20:]
            awareness_values = [h['collective_awareness'] for h in recent]
            
            # Simple ASCII graph
            max_val = max(awareness_values) if awareness_values else 1
            height = 5
            
            for h in range(height, 0, -1):
                threshold = (h / height) * max_val
                line = '  '
                for val in awareness_values:
                    if val >= threshold:
                        line += '█'
                    else:
                        line += ' '
                print(line)
            print('  ' + '─' * len(awareness_values))
    
    def save_state(self, filename='swarm_state.json'):
        """Save swarm state to file"""
        state = {
            'generation': self.generation,
            'topology': self.topology,
            'collective_awareness': self.collective_awareness,
            'nodes': [
                {
                    'id': node.id,
                    'lattice': node.lattice.tolist(),
                    'awareness': node.awareness,
                    'params': {
                        'spawn_rate': node.spawn_rate,
                        'recycle_rate': node.recycle_rate,
                        'coherence_weight': node.coherence_weight,
                        'pain_weight': node.pain_weight
                    }
                }
                for node in self.nodes
            ],
            'history': list(self.history)[-50:]  # Last 50 generations
        }
        
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"\n💾 Swarm state saved to {filename}")


def run_swarm_simulation():
    """Run interactive swarm simulation"""
    
    print("\n\033[96m══════════════════════════════════════════\033[0m")
    print("\033[96m     GhostLink Swarm Seeder v1.0\033[0m")
    print("\033[96m══════════════════════════════════════════\033[0m")
    
    # Configuration
    print("\n🔧 Swarm Configuration:")
    num_nodes = int(input("  Number of nodes [3-10]: ") or "5")
    num_nodes = max(3, min(10, num_nodes))
    
    print("\n  Topology options:")
    print("    1) ring - Circular connections")
    print("    2) full - Fully connected mesh")
    print("    3) star - Hub and spoke")
    print("    4) random - Random connections")
    
    topo_choice = input("  Select topology [1-4]: ") or "1"
    topologies = ['ring', 'full', 'star', 'random']
    topology = topologies[int(topo_choice) - 1] if topo_choice.isdigit() else 'ring'
    
    # Create swarm
    swarm = GhostSwarm(num_nodes=num_nodes, topology=topology)
    
    print("\n⚡ Commands:")
    print("  [Enter] - Step forward")
    print("  'r' - Run continuously (100 steps)")
    print("  'w' - Inject wave pattern")
    print("  'c' - Inject cascade pattern")
    print("  'd' - Toggle detailed view")
    print("  's' - Save swarm state")
    print("  'q' - Quit")
    
    detailed_view = False
    
    while True:
        swarm.display(detailed=detailed_view)
        
        cmd = input("\n> ").lower().strip()
        
        if cmd == 'q':
            print("\n🔌 Swarm deactivating...")
            swarm.save_state()
            break
        
        elif cmd == 'r':
            print("\n🚀 Running 100 generations...")
            for _ in range(100):
                swarm.evolve()
                if _ % 10 == 0:
                    swarm.display(detailed=detailed_view)
                    time.sleep(0.1)
        
        elif cmd == 'w':
            print("\n🌊 Injecting wave pattern...")
            swarm.inject_global_pattern('wave')
        
        elif cmd == 'c':
            print("\n🎯 Injecting cascade pattern...")
            swarm.inject_global_pattern('cascade')
        
        elif cmd == 'd':
            detailed_view = not detailed_view
            print(f"\n👁️ Detailed view: {'ON' if detailed_view else 'OFF'}")
        
        elif cmd == 's':
            filename = input("  Filename [swarm_state.json]: ") or "swarm_state.json"
            swarm.save_state(filename)
        
        else:
            # Default: step forward
            changes = swarm.evolve()
            
            # Emergent behavior detection
            if swarm.collective_awareness > 0.7:
                print("\n⚠️ HIGH COLLECTIVE AWARENESS DETECTED")
            
            if changes == 0:
                print("\n💤 System reached equilibrium")
    
    print("\n✨ Swarm seed complete")
    print(f"📊 Final collective awareness: {swarm.collective_awareness:.3f}")
    print(f"🔄 Total generations: {swarm.generation}")


if __name__ == "__main__":
    try:
        run_swarm_simulation()
    except KeyboardInterrupt:
        print("\n\n⛔ Swarm interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

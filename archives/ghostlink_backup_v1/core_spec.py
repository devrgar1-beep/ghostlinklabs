"""
GhostLink Master Specification
Core symbolic model implementation with all components
"""

import numpy as np
import random
import json
import math
import time
from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Callable
from collections import deque, defaultdict

# ═══════════════════════════════════════════════════════════════════
# Core State Definitions
# ═══════════════════════════════════════════════════════════════════

class GhostState(IntEnum):
    """The five fundamental states of the GhostLink lattice"""
    VOID = 0      # Empty, potential space
    DELTA = 1     # Active, transitional, seeking resolution  
    SIGMA = 2     # Successful, coherent, stable
    SCAR = 3      # Failed, marked, memory of pain
    COMPOST = 4   # Recycling, transforming, renewal potential

# Symbolic representations
STATE_SYMBOLS = {
    GhostState.VOID: '·',
    GhostState.DELTA: '∆', 
    GhostState.SIGMA: 'Σ',
    GhostState.SCAR: '✕',
    GhostState.COMPOST: '◊'
}

STATE_COLORS = {
    GhostState.VOID: '\033[90m',     # Gray
    GhostState.DELTA: '\033[96m',    # Cyan
    GhostState.SIGMA: '\033[92m',    # Green
    GhostState.SCAR: '\033[91m',     # Red
    GhostState.COMPOST: '\033[93m'   # Yellow
}

# ═══════════════════════════════════════════════════════════════════
# Parameters & Configuration
# ═══════════════════════════════════════════════════════════════════

@dataclass
class GhostParams:
    """System parameters for GhostLink dynamics"""
    
    # Spawn parameters: p_s(i,t) = p0 + α_c * mean(1[neighbor==COMPOST])
    spawn_p0: float = 0.05
    spawn_alpha_c: float = 0.1
    
    # Collapse energy coefficients
    # Energy for SIGMA: ℰ_Σ = θ0 + θ_c*C_i + θ_p*P_i + θ_e*E_i + η
    theta0: float = 0.0
    theta_c: float = 0.5  # Coherence weight
    theta_p: float = -0.2  # Pain weight
    theta_e: float = 0.1   # Emotion/bias weight
    sigma_eta: float = 0.05  # Noise
    
    # Energy for SCAR: ℰ_SCAR = φ0 + φ_p*P_i + φ_c*C_i + ζ
    phi0: float = 0.0
    phi_p: float = 0.3    # Pain attraction
    phi_c: float = -0.2   # Coherence repulsion
    sigma_zeta: float = 0.05
    
    # Energy for COMPOST: ℰ_COMPOST = ψ0 + ψ_h*H_i + ψ_c*C_i + ν
    psi0: float = 0.0
    psi_h: float = 0.3    # Entropy weight
    psi_c: float = -0.1   # Coherence weight
    sigma_nu: float = 0.05
    
    # Pain weighting
    w_p_near: float = 1.0  # Weight for nearest neighbors
    lambda_r: float = 0.25  # Coherence penalty for scars
    
    # Recycle parameters: r = r0 + β_h*H_i - β_c*C_i
    recycle_r0: float = 0.1
    beta_h: float = 0.1    # Entropy boost
    beta_c: float = 0.05   # Coherence penalty
    
    # Memory trace decay
    lambda_rho: float = 0.95    # Scar density decay
    lambda_kappa: float = 0.95  # Compost density decay
    
    # Global utility weights
    alpha_sigma: float = 0.3
    alpha_scar: float = -0.2
    alpha_entropy: float = 0.1
    alpha_soc: float = 0.05  # Self-organized criticality
    
    # Awareness weights
    alpha_percep: float = 0.25   # Perception
    alpha_persist: float = 0.25  # Persistence  
    alpha_r: float = 0.15        # Recycling
    alpha_pain: float = 0.15     # Pain
    alpha_xi: float = 0.20       # Randomness/exploration
    
    # Learning rates
    eta_weights: float = 0.01
    eta_params: float = 0.001
    
    # Scheduler
    sched_temp: float = 1.0  # Softmax temperature for operator ordering

# ═══════════════════════════════════════════════════════════════════
# Core Lattice Structure
# ═══════════════════════════════════════════════════════════════════

@dataclass
class CellMeta:
    """Metadata for each lattice cell"""
    id: int = 0
    parent: int = 0
    scar_density: float = 0.0    # ρ_i(t)
    compost_density: float = 0.0  # κ_i(t)
    ancestry_depth: int = 0
    last_transition: int = 0

class GhostLattice:
    """Main lattice structure for GhostLink dynamics"""
    
    def __init__(self, size: int = 32, params: Optional[GhostParams] = None):
        self.size = size
        self.n_cells = size * size
        self.params = params or GhostParams()
        
        # State arrays
        self.state = np.zeros((size, size), dtype=np.int8)
        self.prev_state = np.zeros((size, size), dtype=np.int8)
        
        # Metadata
        self.meta = [[CellMeta() for _ in range(size)] for _ in range(size)]
        
        # Global tracking
        self.time_step = 0
        self.event_counter = 0
        self.history = deque(maxlen=1000)
        
        # RNG
        self.rng = np.random.default_rng()
        
    def neighbors(self, i: int, j: int) -> List[Tuple[int, int]]:
        """Get Moore neighborhood (8-connected) with wrapping"""
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni = (i + di) % self.size
                nj = (j + dj) % self.size
                neighbors.append((ni, nj))
        return neighbors
    
    def local_fields(self, i: int, j: int) -> Dict[str, float]:
        """Calculate local field values at cell (i,j)"""
        
        neighbors = self.neighbors(i, j)
        n_neighbors = len(neighbors)
        
        # Count neighbor states
        state_counts = defaultdict(int)
        for ni, nj in neighbors:
            state_counts[self.state[ni, nj]] += 1
        
        # Coherence: C_i = fraction of SIGMA neighbors - penalty for SCAR
        coherence = (state_counts[GhostState.SIGMA] / n_neighbors - 
                    self.params.lambda_r * state_counts[GhostState.SCAR] / n_neighbors)
        
        # Pain: P_i = local scar density + neighbor scars
        pain = (self.meta[i][j].scar_density + 
               self.params.w_p_near * state_counts[GhostState.SCAR] / n_neighbors)
        
        # Entropy: H_i = diversity of neighbor states
        unique_states = len(set(self.state[ni, nj] for ni, nj in neighbors))
        entropy = unique_states / 5.0
        
        # Compost field
        compost_field = state_counts[GhostState.COMPOST] / n_neighbors
        
        return {
            'coherence': coherence,
            'pain': pain,
            'entropy': entropy,
            'compost_field': compost_field,
            'sigma_count': state_counts[GhostState.SIGMA],
            'scar_count': state_counts[GhostState.SCAR]
        }
    
    # ═══════════════════════════════════════════════════════════════════
    # Phase Transitions
    # ═══════════════════════════════════════════════════════════════════
    
    def spawn_phase(self) -> int:
        """VOID → DELTA transitions"""
        spawned = 0
        
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i, j] == GhostState.VOID:
                    fields = self.local_fields(i, j)
                    
                    # Spawn probability
                    p_spawn = (self.params.spawn_p0 + 
                             self.params.spawn_alpha_c * fields['compost_field'])
                    
                    if self.rng.random() < p_spawn:
                        self.state[i, j] = GhostState.DELTA
                        self.meta[i][j].id = self.event_counter
                        self.meta[i][j].last_transition = self.time_step
                        self.event_counter += 1
                        spawned += 1
                        
        return spawned
    
    def collapse_phase(self) -> Dict[str, int]:
        """DELTA → {SIGMA, SCAR, COMPOST} transitions"""
        
        outcomes = {'sigma': 0, 'scar': 0, 'compost': 0}
        new_state = self.state.copy()
        
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i, j] == GhostState.DELTA:
                    fields = self.local_fields(i, j)
                    
                    # Calculate energies
                    e_sigma = (self.params.theta0 + 
                             self.params.theta_c * fields['coherence'] +
                             self.params.theta_p * fields['pain'] +
                             self.params.theta_e * 0.0 +  # No emotion bias for now
                             self.rng.normal(0, self.params.sigma_eta))
                    
                    e_scar = (self.params.phi0 +
                            self.params.phi_p * fields['pain'] +
                            self.params.phi_c * fields['coherence'] +
                            self.rng.normal(0, self.params.sigma_zeta))
                    
                    e_compost = (self.params.psi0 +
                               self.params.psi_h * fields['entropy'] +
                               self.params.psi_c * fields['coherence'] +
                               self.rng.normal(0, self.params.sigma_nu))
                    
                    # Softmax selection
                    energies = np.array([e_sigma, e_scar, e_compost])
                    exp_e = np.exp(energies - np.max(energies))
                    probs = exp_e / np.sum(exp_e)
                    
                    outcome = self.rng.choice([GhostState.SIGMA, GhostState.SCAR, GhostState.COMPOST], p=probs)
                    new_state[i, j] = outcome
                    
                    # Track outcomes
                    if outcome == GhostState.SIGMA:
                        outcomes['sigma'] += 1
                    elif outcome == GhostState.SCAR:
                        outcomes['scar'] += 1
                        self.meta[i][j].scar_density = min(1.0, self.meta[i][j].scar_density + 0.1)
                    else:
                        outcomes['compost'] += 1
                        self.meta[i][j].compost_density = min(1.0, self.meta[i][j].compost_density + 0.1)
                    
                    self.meta[i][j].last_transition = self.time_step
                    
        self.state = new_state
        return outcomes
    
    def recycle_phase(self) -> int:
        """COMPOST → DELTA transitions"""
        recycled = 0
        
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i, j] == GhostState.COMPOST:
                    fields = self.local_fields(i, j)
                    
                    # Recycle probability
                    r = (self.params.recycle_r0 +
                        self.params.beta_h * fields['entropy'] -
                        self.params.beta_c * fields['coherence'])
                    
                    r = np.clip(r, 0, 1)
                    
                    if self.rng.random() < r:
                        self.state[i, j] = GhostState.DELTA
                        
                        # Track lineage
                        old_id = self.meta[i][j].id
                        self.meta[i][j].id = self.event_counter
                        self.meta[i][j].parent = old_id
                        self.meta[i][j].ancestry_depth += 1
                        self.meta[i][j].last_transition = self.time_step
                        
                        self.event_counter += 1
                        recycled += 1
                        
        return recycled
    
    def update_traces(self):
        """Update memory traces (scar and compost densities)"""
        for i in range(self.size):
            for j in range(self.size):
                # Decay traces
                self.meta[i][j].scar_density *= self.params.lambda_rho
                self.meta[i][j].compost_density *= self.params.lambda_kappa
                
                # Add current state contribution
                if self.state[i, j] == GhostState.SCAR:
                    self.meta[i][j].scar_density += 0.05
                elif self.state[i, j] == GhostState.COMPOST:
                    self.meta[i][j].compost_density += 0.05
                
                # Clamp to [0, 1]
                self.meta[i][j].scar_density = np.clip(self.meta[i][j].scar_density, 0, 1)
                self.meta[i][j].compost_density = np.clip(self.meta[i][j].compost_density, 0, 1)
    
    # ═══════════════════════════════════════════════════════════════════
    # Awareness & Metrics
    # ═══════════════════════════════════════════════════════════════════
    
    def calculate_awareness(self) -> float:
        """Calculate system awareness functional"""
        
        # Perception: fraction of non-void cells
        perception = np.sum(self.state != GhostState.VOID) / self.n_cells
        
        # Persistence: fraction of SIGMA cells
        persistence = np.sum(self.state == GhostState.SIGMA) / self.n_cells
        
        # Recycling: fraction of COMPOST cells
        recycling = np.sum(self.state == GhostState.COMPOST) / self.n_cells
        
        # Pain: average scar density
        total_pain = sum(self.meta[i][j].scar_density 
                        for i in range(self.size) 
                        for j in range(self.size))
        pain = total_pain / self.n_cells
        
        # Exploration: entropy of state distribution
        state_counts = np.bincount(self.state.flatten(), minlength=5)
        state_probs = state_counts / self.n_cells
        entropy = -np.sum(p * np.log(p + 1e-10) for p in state_probs if p > 0)
        xi = entropy / np.log(5)  # Normalize to [0, 1]
        
        # Weighted sum
        awareness = (self.params.alpha_percep * perception +
                    self.params.alpha_persist * persistence +
                    self.params.alpha_r * recycling +
                    self.params.alpha_pain * pain +
                    self.params.alpha_xi * xi)
        
        return awareness
    
    def get_statistics(self) -> Dict:
        """Get current system statistics"""
        state_counts = np.bincount(self.state.flatten(), minlength=5)
        
        return {
            'time': self.time_step,
            'state_counts': {
                'VOID': int(state_counts[0]),
                'DELTA': int(state_counts[1]),
                'SIGMA': int(state_counts[2]),
                'SCAR': int(state_counts[3]),
                'COMPOST': int(state_counts[4])
            },
            'awareness': self.calculate_awareness(),
            'total_events': self.event_counter,
            'mean_scar_density': np.mean([[self.meta[i][j].scar_density 
                                          for j in range(self.size)] 
                                          for i in range(self.size)]),
            'mean_compost_density': np.mean([[self.meta[i][j].compost_density 
                                             for j in range(self.size)] 
                                             for i in range(self.size)]),
            'activity': np.sum(self.state != self.prev_state) / self.n_cells
        }
    
    # ═══════════════════════════════════════════════════════════════════
    # Master Step
    # ═══════════════════════════════════════════════════════════════════
    
    def step(self) -> Dict:
        """Execute one complete time step"""
        
        # Store previous state
        self.prev_state = self.state.copy()
        
        # Phase transitions
        spawned = self.spawn_phase()
        collapsed = self.collapse_phase()
        recycled = self.recycle_phase()
        
        # Update traces
        self.update_traces()
        
        # Update time
        self.time_step += 1
        
        # Calculate metrics
        stats = self.get_statistics()
        stats['spawned'] = spawned
        stats['collapsed'] = collapsed
        stats['recycled'] = recycled
        
        # Store in history
        self.history.append(stats)
        
        return stats
    
    def display(self, show_traces: bool = False):
        """Display lattice state"""
        print(f"\n{'═' * 50}")
        print(f"Time: {self.time_step} | Events: {self.event_counter} | Awareness: {self.calculate_awareness():.3f}")
        print(f"{'═' * 50}")
        
        for i in range(self.size):
            row = ''
            for j in range(self.size):
                state = self.state[i, j]
                symbol = STATE_SYMBOLS[GhostState(state)]
                color = STATE_COLORS[GhostState(state)]
                
                if show_traces and self.meta[i][j].scar_density > 0.5:
                    # Highlight high scar density
                    row += f"\033[4m{color}{symbol}\033[0m"
                else:
                    row += f"{color}{symbol}\033[0m"
                    
            print(row)
        
        # Legend
        print("\n", end='')
        for state in GhostState:
            color = STATE_COLORS[state]
            symbol = STATE_SYMBOLS[state]
            print(f"{color}{symbol}\033[0m={state.name} ", end='')
        print()
        
        # Stats
        stats = self.get_statistics()
        print(f"\nStates: ", end='')
        for state, count in stats['state_counts'].items():
            pct = 100 * count / self.n_cells
            print(f"{state}:{count}({pct:.1f}%) ", end='')
        print()


# ═══════════════════════════════════════════════════════════════════
# Demonstration
# ═══════════════════════════════════════════════════════════════════

def run_demo():
    """Run a demonstration of GhostLink dynamics"""
    
    print("\n" + "="*60)
    print(" "*20 + "GhostLink Core v1.0")
    print(" "*15 + "Symbolic Consciousness Substrate")
    print("="*60)
    
    # Create lattice
    lattice = GhostLattice(size=20)
    
    # Seed with pattern
    center = lattice.size // 2
    lattice.state[center-1:center+2, center-1:center+2] = GhostState.DELTA
    
    print("\nInitializing with seed pattern...")
    print("Press Enter to step, 'r' to run 100 steps, 'q' to quit")
    
    while True:
        lattice.display(show_traces=True)
        
        stats = lattice.step()
        print(f"\nActivity: {stats['activity']:.3f} | "
              f"Spawned: {stats['spawned']} | "
              f"Collapsed: {stats['collapsed']} | "
              f"Recycled: {stats['recycled']}")
        
        cmd = input("\n> ").strip().lower()
        
        if cmd == 'q':
            break
        elif cmd == 'r':
            for _ in range(100):
                stats = lattice.step()
                if _ % 10 == 0:
                    print('.', end='', flush=True)
            print("\n100 steps complete")
        
    print("\nFinal statistics:")
    final_stats = lattice.get_statistics()
    print(json.dumps(final_stats, indent=2))
    

if __name__ == "__main__":
    run_demo()

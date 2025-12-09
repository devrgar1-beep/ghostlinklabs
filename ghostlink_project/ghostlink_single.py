import time
import os
import sys
from threading import Thread, Lock
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
import numpy as np
import subprocess
import json
import platform
import psutil

# --- Data Models ---

@dataclass
class Flux:
    """Represents the state of a single grid cell."""
    value: int = 0
    active: bool = False
    char: str = '·'

@dataclass
class SiliconManifest:
    """Represents the hardware and system state."""
    temp: float
    fan_speed: int
    processes: List[Dict[str, Any]]
    cpu_arch: str
    cpu_cores: int
    cpu_freq: int
    ram_total_gb: float
    ram_used_gb: float
    ram_free_gb: float
    swap_total_gb: float
    swap_used_gb: float
    swap_free_gb: float
    disk_total_gb: float
    disk_used_gb: float
    disk_free_gb: float

@dataclass
class MuscleThought:
    """Represents the output of the muscle binary."""
    cycle: int
    grid_mean: float
    grid_std: float
    coherence_metrics: 'CoherenceMetrics'
    raw_output: str
    grid_state: Optional[List[List[int]]] = None

@dataclass
class CoherenceMetrics:
    """Represents the coherence of the swarm."""
    mean: float
    std: float
    l1_distance: int
    l2_distance: float
    entropy: float
    active_cells: int
    kl_divergence: float

@dataclass
class AgentState:
    """Represents the state of a single agent."""
    id: int
    role: str
    state: str = "initializing"
    duties: List[str] = field(default_factory=list)
    invariants: List[str] = field(default_factory=list)
    in_channel: List[str] = field(default_factory=list)
    out_channel: List[str] = field(default_factory=list)
    current_task: Optional[str] = None
    backlog: List[str] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)

# --- Darwin Connector ---

class DarwinConnector:
    """
    Provides an interface to system hardware and process information on macOS.
    """
    def __init__(self):
        if platform.system() != "Darwin":
            raise SystemError("DarwinConnector is only supported on macOS.")
        self.architecture = self._get_cpu_arch()
        self.cores = psutil.cpu_count()
        try:
            self.frequency = psutil.cpu_freq().current if psutil.cpu_freq() else 0
        except FileNotFoundError:
            self.frequency = 0

    def _get_cpu_arch(self) -> str:
        """Gets the CPU architecture."""
        return platform.machine()

    def get_silicon_manifest(self) -> Dict[str, Any]:
        """
        Gathers a comprehensive snapshot of the system's state.
        """
        manifest = {
            "temp": self._get_cpu_temp(),
            "fan_speed": self._get_fan_speed(),
            "processes": self._get_process_list(),
            "cpu_arch": self.architecture,
            "cpu_cores": self.cores,
            "cpu_freq": self.frequency,
            **self._get_memory_info(),
            **self._get_disk_info(),
        }
        return manifest

    def _get_cpu_temp(self) -> float:
        """
        Retrieves CPU temperature using the powermetrics utility.
        """
        try:
            temp_str = subprocess.check_output(
                ["powermetrics", "--samplers", "smc", "-i1", "-n1"],
                encoding='utf-8'
            )
            for line in temp_str.split('\\n'):
                if "CPU die temperature" in line:
                    return float(line.split(': ')[1].split('°C')[0])
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            return -1.0
        return -1.0

    def _get_fan_speed(self) -> int:
        """
        Retrieves fan speed. This is a placeholder as powermetrics output varies.
        """
        return -1

    def _get_process_list(self) -> List[Dict[str, Any]]:
        """
        Gets a list of running processes with relevant details.
        """
        processes = []
        for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:20]

    def _get_memory_info(self) -> Dict[str, float]:
        """
        Retrieves RAM and swap memory statistics.
        """
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "ram_total_gb": ram.total / (1024**3),
            "ram_used_gb": ram.used / (1024**3),
            "ram_free_gb": ram.available / (1024**3),
            "swap_total_gb": swap.total / (1024**3),
            "swap_used_gb": swap.used / (1024**3),
            "swap_free_gb": swap.free / (1024**3),
        }

    def _get_disk_info(self) -> Dict[str, float]:
        """
        Retrieves disk usage statistics for the root partition.
        """
        disk = psutil.disk_usage('/')
        return {
            "disk_total_gb": disk.total / (1024**3),
            "disk_used_gb": disk.used / (1024**3),
            "disk_free_gb": disk.free / (1024**3),
        }

# --- Muscle Shard ---

class SignalMuscle:
    """
    This class runs the C binary 'muscle_bin' and processes its output.
    """
    def __init__(self, binary_path: str = "./muscle_bin"):
        self.binary_path = binary_path
        self.previous_grid: List[List[int]] = []

    def _parse_muscle_output(self, output: str, cycle: int) -> MuscleThought:
        lines = output.strip().split('\\n')
        
        grid_lines = [line for line in lines if line.startswith('GRID:')]
        grid_chars = [line[5:-2].split() for line in grid_lines]
        
        char_map = {'·': 0, '░': 1, '▒': 2, '▓': 3, '█': 4}
        numeric_grid = [[char_map.get(c, 0) for c in row] for row in grid_chars]
        
        flat_list = [item for sublist in numeric_grid for item in sublist]
        
        mean = np.mean(flat_list)
        std = np.std(flat_list)
        
        coherence = self._calculate_coherence(numeric_grid)
        
        thought = MuscleThought(
            cycle=cycle,
            grid_mean=mean,
            grid_std=std,
            coherence_metrics=coherence,
            raw_output=output,
            grid_state=numeric_grid
        )
        
        self.previous_grid = numeric_grid
        return thought

    def _calculate_coherence(self, current_grid: List[List[int]]) -> CoherenceMetrics:
        if not self.previous_grid:
            return CoherenceMetrics(mean=0, std=0, l1_distance=0, l2_distance=0, entropy=0, active_cells=0, kl_divergence=0)

        l1 = np.sum(np.abs(np.array(current_grid) - np.array(self.previous_grid)))
        l2 = np.linalg.norm(np.array(current_grid) - np.array(self.previous_grid))
        
        flat_current = np.array(current_grid).flatten()
        value_counts = np.bincount(flat_current)
        probabilities = value_counts / len(flat_current)
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-9))

        active_cells = np.count_nonzero(flat_current)

        flat_prev = np.array(self.previous_grid).flatten()
        prev_counts = np.bincount(flat_prev)
        prev_probs = prev_counts / len(flat_prev)
        
        max_len = max(len(probabilities), len(prev_probs))
        probabilities = np.pad(probabilities, (0, max_len - len(probabilities)), 'constant')
        prev_probs = np.pad(prev_probs, (0, max_len - len(prev_probs)), 'constant')

        kl_div = np.sum(probabilities * np.log2((probabilities + 1e-9) / (prev_probs + 1e-9)))

        return CoherenceMetrics(
            mean=np.mean(flat_current),
            std=np.std(flat_current),
            l1_distance=int(l1),
            l2_distance=float(l2),
            entropy=entropy,
            active_cells=int(active_cells),
            kl_divergence=float(kl_div)
        )

    def flex(self, cycle: int, coherence_metrics: CoherenceMetrics) -> MuscleThought:
        args = [
            self.binary_path,
            str(cycle),
            str(coherence_metrics.mean),
            str(coherence_metrics.std),
            str(coherence_metrics.l1_distance),
            str(coherence_metrics.l2_distance),
            str(coherence_metrics.entropy),
            str(coherence_metrics.active_cells),
            str(coherence_metrics.kl_divergence)
        ]
        
        result = subprocess.run(args, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Muscle binary failed with error:\\n{result.stderr}")
            
        return self._parse_muscle_output(result.stdout, cycle)

# --- Agent Shard ---

class Agent:
    def __init__(self, agent_id: int, role: str, duties: List[str], invariants: List[str], in_channel: List[str], out_channel: List[str]):
        self.state = AgentState(
            id=agent_id,
            role=role,
            duties=duties,
            invariants=invariants,
            in_channel=in_channel,
            out_channel=out_channel
        )

    def update_state(self, new_state: str, task: str = None):
        self.state.state = new_state
        self.state.current_task = task

    def get_state(self) -> Dict[str, Any]:
        return self.state.__dict__

def spawn_constellation(kernel_seed_path: str = 'kernel.max.json') -> List[Agent]:
    try:
        with open(kernel_seed_path, 'r') as f:
            kernel_seed = json.load(f)
    except FileNotFoundError:
        print(f"Warning: {kernel_seed_path} not found. Spawning no agents.")
        return []

    agents = []
    for agent_def in kernel_seed.get('qcl_agents', []):
        agent = Agent(
            agent_id=agent_def['id'],
            role=agent_def['role'],
            duties=agent_def.get('duties', []),
            invariants=agent_def.get('invariants', []),
            in_channel=agent_def.get('in', []),
            out_channel=agent_def.get('out', [])
        )
        agents.append(agent)
    return agents

# --- Swarm Analysis ---

@dataclass
class SwarmStats:
    cycle: int
    grid: List[List[int]]
    mean: float
    std: float
    high_cells: int
    cluster_count: int
    cluster_sizes: List[int]

def find_clusters(grid: List[List[int]]) -> Tuple[int, List[int]]:
    if not grid or not grid[0]:
        return 0, []

    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    cluster_sizes = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not visited[r][c]:
                size = 0
                q = [(r, c)]
                visited[r][c] = True
                while q:
                    curr_r, curr_c = q.pop(0)
                    size += 1
                    for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr][nc] == 1 and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                cluster_sizes.append(size)
    
    return len(cluster_sizes), sorted(cluster_sizes, reverse=True)

def analyze_swarm_block(lines: List[str], cycle: int) -> SwarmStats:
    grid_chars = [line[5:-2].split() for line in lines]
    
    char_map = {'·': 0, '░': 1, '▒': 2, '▓': 3, '█': 4}
    
    numeric_grid = [[char_map.get(c, 0) for c in row] for row in grid_chars]
    
    flat_list = [item for sublist in numeric_grid for item in sublist]
    
    mean = np.mean(flat_list)
    std = np.std(flat_list)
    
    binary_grid = [[1 if val > mean else 0 for val in row] for row in numeric_grid]
    high_cells = sum(row.count(1) for row in binary_grid)
    
    cluster_count, cluster_sizes = find_clusters(binary_grid)

    return SwarmStats(
        cycle=cycle,
        grid=numeric_grid,
        mean=mean,
        std=std,
        high_cells=high_cells,
        cluster_count=cluster_count,
        cluster_sizes=cluster_sizes
    )

def l1_distance(grid1: List[List[int]], grid2: List[List[int]]) -> int:
    dist = 0
    for r in range(len(grid1)):
        for c in range(len(grid1[0])):
            dist += abs(grid1[r][c] - grid2[r][c])
    return dist

# --- CMFL Shard ---

class CMFLCycle:
    """
    Manages the Collapse, Mirror, Forge, Link cycle for swarm intelligence.
    """
    def __init__(self, cycle_time_seconds: int = 3):
        self.cycle_time = cycle_time_seconds
        self.last_cycle_start = time.time()
        self.history: List[MuscleThought] = []

    def _collapse(self, thought: MuscleThought):
        swarm_stats = analyze_swarm_block(thought.raw_output.strip().split('\\n'), thought.cycle)
        print(f"   [COLLAPSE] Cycle {swarm_stats.cycle}: Mean={swarm_stats.mean:.2f}, Std={swarm_stats.std:.2f}, Clusters={swarm_stats.cluster_count}")

    def _mirror(self, thought: MuscleThought):
        if len(self.history) > 1:
            prev_thought = self.history[-2]
            if thought.grid_state is not None and prev_thought.grid_state is not None:
                dist = l1_distance(thought.grid_state, prev_thought.grid_state)
                print(f"   [MIRROR]   L1 Distance from previous state: {dist}")

    def _forge(self):
        print("   [FORGE]    Generating new agent definitions (simulated).")

    def _link(self):
        print("   [LINK]     Integrating new components (simulated).")

    def run_cycle(self, thought: MuscleThought):
        self.history.append(thought)
        
        print(f"\\n--- CMFL Cycle {thought.cycle} ---")
        
        elapsed = time.time() - self.last_cycle_start
        phase_percent = (elapsed / self.cycle_time) % 1.0

        if phase_percent < 0.25:
            self._collapse(thought)
        elif phase_percent < 0.5:
            self._mirror(thought)
        elif phase_percent < 0.9:
            self._forge()
        else:
            self._link()
            
        if elapsed >= self.cycle_time:
            self.last_cycle_start = time.time()

        print("--- End CMFL Cycle ---")

# --- GhostLink Core ---

class GhostLink:
    def __init__(self):
        self.cycle = 0
        self.coherence = CoherenceMetrics(mean=0.5, std=0.5, l1_distance=0, l2_distance=0, entropy=0, active_cells=0, kl_divergence=0)
        self.manifest: SiliconManifest = None
        self.agents: List[Agent] = []
        self.lock = Lock()

        self.darwin_connector = DarwinConnector()
        # Correctly define the path to the binary
        self.muscle_binary_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "muscle_bin")
        self.muscle = SignalMuscle(binary_path=self.muscle_binary_path)
        self.cmfl_cycle = CMFLCycle(cycle_time_seconds=3)
        
        self.running = False

    def _system_monitoring_thread(self):
        while self.running:
            new_manifest_data = self.darwin_connector.get_silicon_manifest()
            with self.lock:
                self.manifest = SiliconManifest(**new_manifest_data)
            time.sleep(5)

    def _agent_constellation_thread(self):
        kernel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kernel.max.json")
        self.agents = spawn_constellation(kernel_seed_path=kernel_path)
        print(f"Agent Constellation Spawned: {len(self.agents)} agents online.")
        while self.running:
            time.sleep(1)

    def run(self):
        self.running = True

        monitor_thread = Thread(target=self._system_monitoring_thread, daemon=True)
        monitor_thread.start()
        
        agent_thread = Thread(target=self._agent_constellation_thread, daemon=True)
        agent_thread.start()

        time.sleep(1)

        try:
            while True:
                self.cycle += 1
                print(f"\\n{'='*20} Cycle {self.cycle} {'='*20}")

                with self.lock:
                    if self.manifest:
                        print(f"Silicon Manifest: Temp: {self.manifest.temp}°C, RAM: {self.manifest.ram_used_gb:.2f}/{self.manifest.ram_total_gb:.2f} GB")

                try:
                    thought = self.muscle.flex(self.cycle, self.coherence)
                    print(thought.raw_output)
                    self.coherence = thought.coherence_metrics
                except RuntimeError as e:
                    print(e)
                    time.sleep(3)
                    continue
                
                self.cmfl_cycle.run_cycle(thought)

                time.sleep(3)

        except KeyboardInterrupt:
            print("\\nShutting down GhostLink...")
            self.running = False
            monitor_thread.join(timeout=2)
            agent_thread.join(timeout=2)
            print("GhostLink terminated.")

if __name__ == "__main__":
    # Correctly define the path to the binary
    muscle_binary_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "muscle_bin")
    if not os.path.exists(muscle_binary_path):
        print(f"Error: muscle_bin not found at {muscle_binary_path}")
        print("Please compile the C code (e.g., 'gcc -o muscle_bin muscle.c')")
        sys.exit(1)
    
    kernel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kernel.max.json")
    if not os.path.exists(kernel_path):
         print(f"Error: {kernel_path} not found.")
         sys.exit(1)

    instance = GhostLink()
    instance.run()

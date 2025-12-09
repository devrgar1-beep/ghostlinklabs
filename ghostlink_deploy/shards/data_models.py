
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple

@dataclass
class Flux:
    load: float
    gpu_util: float
    power_watts: float
    net_flux: float
    disk_flux: float
    process_count: float
    fs_entropy: float
    conn_count: float

@dataclass
class SiliconManifest:
    chip_generation: str = "M3 Series"
    microcode_policy: str = "IMMUTABLE (Hardware Fused)"
    boot_trust: str = "SEP_SIGNED (GID Key)"
    prefetcher_state: str = "DMP_ACTIVE (GoFetch Risk)"
    side_channels: List[str] = field(default_factory=lambda: ["Cache Timing", "Speculative Execution"])

@dataclass
class MuscleThought:
    timestamp: float
    codon: str
    symbol: str
    message: str

@dataclass
class CoherenceMetrics:
    h_ks: float = 0.0
    lambda_max: float = 0.0
    x_range: Tuple[float, float] = (0.0, 0.0)
    z_range: Tuple[float, float] = (0.0, 0.0)
    regime: str = "UNKNOWN"

@dataclass
class AgentState:
    id: str
    role: str
    status: str = "idle"
    memory: Dict[str, Any] = field(default_factory=dict)

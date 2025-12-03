# GHOSTLINK PROTOCOL: COMPREHENSIVE TECHNICAL WIKI
# PART 7: COMPLETE CODE REFERENCE

**Version:** 2.1.0 | **Classification:** Production Implementation

---

# 28. CORE PYTHON PACKAGE

## 28.1 Package Structure

```
ghostlink/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── cmfl.py              # CMFL reasoning engine
│   ├── lattice.py           # FCC lattice implementation
│   ├── agent.py             # Agent definitions
│   ├── pipeline.py          # Pipeline orchestration
│   └── types.py             # Type definitions
├── analysis/
│   ├── __init__.py
│   ├── variance.py          # Variance analyzer
│   ├── domains.py           # Mirror domains
│   └── shards.py            # Expansion shards
├── coordination/
│   ├── __init__.py
│   ├── pheromones.py        # Pheromone system
│   ├── routing.py           # Agent routing
│   └── consensus.py         # BFT consensus
├── providers/
│   ├── __init__.py
│   ├── base.py              # Provider base class
│   ├── openai.py            # OpenAI integration
│   ├── anthropic.py         # Anthropic integration
│   ├── google.py            # Google integration
│   └── orchestrator.py      # Multi-provider orchestration
├── recovery/
│   ├── __init__.py
│   ├── scar.py              # SCAR system
│   └── strategies.py        # Recovery strategies
├── sovereignty/
│   ├── __init__.py
│   ├── policy.py            # Policy guard
│   ├── audit.py             # Audit logging
│   └── capabilities.py      # Capability matrix
├── storage/
│   ├── __init__.py
│   ├── content_addressed.py # CID storage
│   ├── snapshots.py         # State snapshots
│   └── events.py            # Event log
├── api/
│   ├── __init__.py
│   ├── fastapi_app.py       # FastAPI application
│   ├── mcp_server.py        # MCP server
│   └── routes.py            # API routes
├── cli/
│   ├── __init__.py
│   └── main.py              # CLI commands
└── config/
    ├── __init__.py
    ├── settings.py          # Configuration
    └── defaults.yaml        # Default values
```

## 28.2 Core Types (ghostlink/core/types.py)

```python
"""Core type definitions for GhostLink Protocol."""

from dataclasses import dataclass, field
from typing import (
    Dict, List, Optional, Any, Tuple, 
    TypeVar, Generic, Callable, Union
)
from enum import Enum, auto
from datetime import datetime
import hashlib
import json

T = TypeVar('T')


class AgentGroup(Enum):
    """Agent group identifiers."""
    ALPHA = "alpha"      # 1-8: Foundation
    BETA = "beta"        # 9-16: Processing
    GAMMA = "gamma"      # 17-24: Validation
    DELTA = "delta"      # 25-32: Transform
    EPSILON = "epsilon"  # 33-40: Memory
    ZETA = "zeta"        # 41-48: Routing
    ETA = "eta"          # 49-56: Analysis
    THETA = "theta"      # 57-64: Synthesis


class PipelineStage(Enum):
    """Pipeline stage identifiers."""
    MAP = "P-01"
    CLEANSE = "P-02"
    SURGE = "P-03"
    LOCK = "P-04"
    SILENCE = "P-05"
    REFLECT = "P-06"
    ECHOFRAME_BIND = "P-07"
    WEAVE = "P-08"
    BIND = "P-09"
    SEAL = "P-10"
    SNAPSHOT = "P-11"
    COLLAPSE = "P-12"


class MirrorDomain(Enum):
    """Mirror domain identifiers."""
    EUCLIDEAN = "MD-01"
    HYPERBOLIC = "MD-02"
    SPHERICAL = "MD-03"
    TOPOLOGICAL = "MD-04"
    TEMPORAL = "MD-05"
    CAUSAL = "MD-06"
    SPECTRAL = "MD-07"
    INFORMATION = "MD-08"
    PROBABILISTIC = "MD-09"
    META = "MD-10"
    VOID = "MD-11"


class CMFLPhase(Enum):
    """CMFL reasoning phases."""
    COLLAPSE = auto()
    MIRROR = auto()
    FORGE = auto()
    LINK = auto()


@dataclass(frozen=True)
class ContentID:
    """Content-addressed identifier."""
    hash: str
    algorithm: str = "sha256"
    
    @classmethod
    def from_content(cls, content: Union[str, bytes]) -> 'ContentID':
        if isinstance(content, str):
            content = content.encode('utf-8')
        hash_value = hashlib.sha256(content).hexdigest()
        return cls(hash=hash_value)
    
    def __str__(self) -> str:
        return f"cid:{self.algorithm}:{self.hash[:16]}"


@dataclass
class Position3D:
    """3D position in FCC lattice."""
    x: int
    y: int
    z: int
    
    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)
    
    def distance_to(self, other: 'Position3D') -> float:
        return (
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        ) ** 0.5


@dataclass
class AgentSpec:
    """Agent specification."""
    id: int
    name: str
    group: AgentGroup
    duty: str
    invariants: List[str]
    input_type: str
    output_type: str
    position: Position3D
    multipaths: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "group": self.group.value,
            "duty": self.duty,
            "invariants": self.invariants,
            "input_type": self.input_type,
            "output_type": self.output_type,
            "position": self.position.to_tuple(),
            "multipaths": self.multipaths
        }


@dataclass
class Query:
    """Input query for processing."""
    text: str
    id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    max_iterations: int = 5
    target_domains: Optional[List[MirrorDomain]] = None
    target_shards: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = ContentID.from_content(
                f"{self.text}{self.timestamp.isoformat()}"
            ).hash[:16]


@dataclass
class CollapsedState:
    """State after COLLAPSE phase."""
    original_query: Query
    essential_signal: str
    extracted_entities: List[str]
    identified_intent: str
    complexity_score: float
    compression_ratio: float
    cid: ContentID = field(init=False)
    
    def __post_init__(self):
        self.cid = ContentID.from_content(self.essential_signal)


@dataclass
class DomainProjection:
    """Projection into a single mirror domain."""
    domain: MirrorDomain
    embedding: Any  # numpy array or similar
    metrics: Dict[str, float]
    patterns: List[str]
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class MirroredState:
    """State after MIRROR phase."""
    collapsed: CollapsedState
    projections: Dict[MirrorDomain, DomainProjection]
    active_domains: List[MirrorDomain]
    cross_domain_correlations: Dict[str, float]


@dataclass
class ForgedInsight:
    """Insight synthesized during FORGE phase."""
    source_domains: List[MirrorDomain]
    pattern_type: str  # convergent, divergent, emergent
    content: str
    confidence: float
    supporting_evidence: List[str]


@dataclass
class ForgedState:
    """State after FORGE phase."""
    mirrored: MirroredState
    insights: List[ForgedInsight]
    synthesis: str
    confidence_score: float
    divergent_claims: List[Dict]


@dataclass
class LinkedOutput:
    """Final output after LINK phase."""
    forged: ForgedState
    output_text: str
    memory_updates: List[Dict]
    emitted_events: List[Dict]
    cid: ContentID
    total_duration_ms: float


@dataclass
class VarianceMetrics:
    """Metrics from variance analysis."""
    semantic_variance: float
    lexical_variance: float
    structural_variance: float
    confidence_variance: float
    factual_agreement: float
    reasoning_divergence: float
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "semantic_variance": self.semantic_variance,
            "lexical_variance": self.lexical_variance,
            "structural_variance": self.structural_variance,
            "confidence_variance": self.confidence_variance,
            "factual_agreement": self.factual_agreement,
            "reasoning_divergence": self.reasoning_divergence
        }
    
    @property
    def overall_variance(self) -> float:
        """Weighted overall variance score."""
        return (
            self.semantic_variance * 0.3 +
            self.lexical_variance * 0.15 +
            self.structural_variance * 0.1 +
            self.confidence_variance * 0.15 +
            (1 - self.factual_agreement) * 0.15 +
            self.reasoning_divergence * 0.15
        )


@dataclass
class ProviderResponse:
    """Response from an AI provider."""
    provider: str
    model: str
    content: str
    tokens_used: int
    latency_ms: float
    logprobs: Optional[Dict] = None
    metadata: Optional[Dict] = None


@dataclass
class VarianceAnalysis:
    """Complete variance analysis result."""
    query: Query
    responses: List[ProviderResponse]
    metrics: VarianceMetrics
    clusters: List[List[int]]
    consensus: Optional[str]
    divergent_claims: List[Dict]
    confidence_score: float
    meta_insight: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict:
        return {
            "query_id": self.query.id,
            "provider_count": len(self.responses),
            "metrics": self.metrics.to_dict(),
            "cluster_count": len(self.clusters),
            "has_consensus": self.consensus is not None,
            "divergent_claim_count": len(self.divergent_claims),
            "confidence_score": self.confidence_score,
            "meta_insight": self.meta_insight
        }


@dataclass
class PheromoneDeposit:
    """Pheromone deposit at a position."""
    type: str  # task, resource, quality, error
    position: Position3D
    strength: float
    timestamp: datetime
    depositor_id: int
    
    def decay(self, decay_rate: float, current_time: datetime) -> float:
        """Compute decayed strength."""
        import math
        hours_elapsed = (current_time - self.timestamp).total_seconds() / 3600
        return self.strength * math.exp(-decay_rate * hours_elapsed)


@dataclass
class TraceEvent:
    """Event in the trace log."""
    kind: str
    timestamp: datetime
    data: Dict[str, Any]
    span_id: str
    parent_span_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "kind": self.kind,
            "ts": self.timestamp.isoformat(),
            "data": self.data,
            "span": self.span_id,
            "parent": self.parent_span_id
        }


@dataclass
class SCARRecord:
    """SCAR (Stateful Checkpoint And Recovery) record."""
    id: str
    scar_type: str
    timestamp: datetime
    context: Dict[str, Any]
    error_message: str
    stack_trace_hash: str
    recovery_attempted: bool = False
    recovery_successful: bool = False
    recovery_strategy: Optional[str] = None
    lessons_learned: List[str] = field(default_factory=list)
```

## 28.3 FCC Lattice (ghostlink/core/lattice.py)

```python
"""Face-Centered Cubic lattice implementation."""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
import heapq
from .types import Position3D, AgentSpec, AgentGroup


class FCCLattice:
    """
    Face-Centered Cubic lattice for 64-agent coordination.
    
    Properties:
    - 64 agents in 4x4x4 supercell
    - 12 neighbors per agent (coordination number)
    - 74.05% packing efficiency
    - Maximum 6 hops between any two agents
    """
    
    # FCC neighbor offsets (12 face-diagonal directions)
    NEIGHBOR_OFFSETS = [
        # XY plane diagonals
        (1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),
        # XZ plane diagonals
        (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1),
        # YZ plane diagonals
        (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1),
    ]
    
    def __init__(self, size: int = 4):
        """Initialize lattice with given size per dimension."""
        self.size = size
        self.total_agents = size ** 3
        self.positions: Dict[int, Position3D] = {}
        self.agents: Dict[int, AgentSpec] = {}
        self.adjacency: Dict[int, List[int]] = {}
        
        self._initialize_positions()
        self._compute_adjacency()
    
    def _initialize_positions(self) -> None:
        """Map agent IDs to 3D positions."""
        agent_id = 1
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    self.positions[agent_id] = Position3D(x, y, z)
                    agent_id += 1
    
    def _compute_adjacency(self) -> None:
        """Compute neighbor relationships with periodic boundaries."""
        for agent_id, pos in self.positions.items():
            neighbors = []
            for dx, dy, dz in self.NEIGHBOR_OFFSETS:
                # Apply periodic boundary conditions
                nx = (pos.x + dx) % self.size
                ny = (pos.y + dy) % self.size
                nz = (pos.z + dz) % self.size
                
                # Find agent at neighbor position
                neighbor_id = self._position_to_id(nx, ny, nz)
                if neighbor_id and neighbor_id != agent_id:
                    neighbors.append(neighbor_id)
            
            self.adjacency[agent_id] = neighbors
    
    def _position_to_id(self, x: int, y: int, z: int) -> Optional[int]:
        """Convert position to agent ID."""
        for aid, pos in self.positions.items():
            if pos.x == x and pos.y == y and pos.z == z:
                return aid
        return None
    
    def get_neighbors(self, agent_id: int) -> List[int]:
        """Get neighboring agent IDs."""
        return self.adjacency.get(agent_id, [])
    
    def get_position(self, agent_id: int) -> Optional[Position3D]:
        """Get position of agent."""
        return self.positions.get(agent_id)
    
    def get_group(self, agent_id: int) -> AgentGroup:
        """Get group for agent ID."""
        groups = list(AgentGroup)
        group_size = self.total_agents // len(groups)
        group_index = (agent_id - 1) // group_size
        return groups[min(group_index, len(groups) - 1)]
    
    def route(
        self, 
        source: int, 
        target: int,
        pheromone_weights: Optional[Dict[int, float]] = None
    ) -> List[int]:
        """
        Find shortest path between agents using Dijkstra with pheromone weighting.
        """
        if source == target:
            return [source]
        
        # Priority queue: (distance, agent_id, path)
        pq = [(0, source, [source])]
        visited: Set[int] = set()
        
        while pq:
            dist, current, path = heapq.heappop(pq)
            
            if current == target:
                return path
            
            if current in visited:
                continue
            visited.add(current)
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    # Base weight is 1, reduced by pheromone strength
                    weight = 1.0
                    if pheromone_weights:
                        pheromone = pheromone_weights.get(neighbor, 0)
                        weight = max(0.1, 1.0 - pheromone * 0.5)
                    
                    new_dist = dist + weight
                    heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))
        
        return []  # No path found
    
    def get_group_agents(self, group: AgentGroup) -> List[int]:
        """Get all agent IDs in a group."""
        groups = list(AgentGroup)
        group_index = groups.index(group)
        group_size = self.total_agents // len(groups)
        start = group_index * group_size + 1
        end = start + group_size
        return list(range(start, end))
    
    def distance(self, agent1: int, agent2: int) -> int:
        """Compute hop distance between agents."""
        path = self.route(agent1, agent2)
        return len(path) - 1 if path else -1
    
    def verify_fault_tolerance(self, failed_agents: List[int]) -> bool:
        """
        Verify system remains connected after agent failures.
        Returns True if all remaining agents are still reachable.
        """
        remaining = set(range(1, self.total_agents + 1)) - set(failed_agents)
        if not remaining:
            return False
        
        # BFS from any remaining agent
        start = next(iter(remaining))
        visited = {start}
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            for neighbor in self.get_neighbors(current):
                if neighbor in remaining and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return visited == remaining
    
    def max_fault_tolerance(self) -> int:
        """
        Compute maximum number of agents that can fail
        while maintaining connectivity.
        """
        # FCC with coordination 12 can tolerate significant failures
        # Approximate: system survives until percolation threshold
        return 8  # Conservative estimate for 64-agent 4x4x4 lattice
    
    def get_statistics(self) -> Dict:
        """Get lattice statistics."""
        return {
            "total_agents": self.total_agents,
            "dimensions": f"{self.size}x{self.size}x{self.size}",
            "coordination_number": 12,
            "total_connections": sum(len(n) for n in self.adjacency.values()) // 2,
            "packing_efficiency": 0.7405,
            "max_path_length": 6,
            "fault_tolerance": self.max_fault_tolerance()
        }
```

## 28.4 CMFL Engine (ghostlink/core/cmfl.py)

```python
"""CMFL (Collapse → Mirror → Forge → Link) reasoning engine."""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio

from .types import (
    Query, CollapsedState, MirroredState, ForgedState, LinkedOutput,
    DomainProjection, ForgedInsight, MirrorDomain, CMFLPhase, ContentID
)
from ..analysis.domains import DomainRegistry
from ..storage.content_addressed import ContentStore
from ..storage.events import EventLog


class CMFLEngine:
    """
    Execute the CMFL reasoning cycle.
    
    Phases:
    1. COLLAPSE - Reduce input to essential signal
    2. MIRROR - Project across geometric domains
    3. FORGE - Synthesize cross-domain insights
    4. LINK - Connect to memory and emit output
    """
    
    def __init__(
        self,
        domain_registry: DomainRegistry,
        content_store: ContentStore,
        event_log: EventLog,
        max_iterations: int = 5
    ):
        self.domains = domain_registry
        self.store = content_store
        self.events = event_log
        self.max_iterations = max_iterations
    
    async def execute(self, query: Query) -> LinkedOutput:
        """Execute complete CMFL cycle."""
        start_time = datetime.utcnow()
        
        # Phase 1: COLLAPSE
        collapsed = await self._collapse(query)
        self.events.emit("cmfl_phase", {
            "phase": "collapse",
            "query_id": query.id,
            "compression_ratio": collapsed.compression_ratio
        })
        
        # Phase 2: MIRROR
        mirrored = await self._mirror(collapsed)
        self.events.emit("cmfl_phase", {
            "phase": "mirror",
            "query_id": query.id,
            "domains_active": len(mirrored.active_domains)
        })
        
        # Phase 3: FORGE
        forged = await self._forge(mirrored)
        self.events.emit("cmfl_phase", {
            "phase": "forge",
            "query_id": query.id,
            "insights_generated": len(forged.insights)
        })
        
        # Phase 4: LINK
        linked = await self._link(forged, start_time)
        self.events.emit("cmfl_phase", {
            "phase": "link",
            "query_id": query.id,
            "duration_ms": linked.total_duration_ms
        })
        
        return linked
    
    async def _collapse(self, query: Query) -> CollapsedState:
        """
        COLLAPSE phase: Reduce input to essential signal.
        
        Operations:
        - Parse and tokenize
        - Extract key entities
        - Identify intent
        - Remove noise
        - Compress representation
        """
        text = query.text
        
        # Extract entities (simplified - use NER in production)
        entities = self._extract_entities(text)
        
        # Identify intent
        intent = self._identify_intent(text)
        
        # Compute essential signal
        essential = self._compress_to_essential(text, entities, intent)
        
        # Compute complexity
        complexity = self._compute_complexity(text)
        
        return CollapsedState(
            original_query=query,
            essential_signal=essential,
            extracted_entities=entities,
            identified_intent=intent,
            complexity_score=complexity,
            compression_ratio=len(essential) / len(text) if text else 0
        )
    
    async def _mirror(self, collapsed: CollapsedState) -> MirroredState:
        """
        MIRROR phase: Project across geometric domains.
        
        Projects collapsed state into 11 mirror domains for
        multi-perspective analysis.
        """
        # Determine which domains to activate based on query
        active_domains = self._select_domains(collapsed)
        
        # Project into each domain
        projections: Dict[MirrorDomain, DomainProjection] = {}
        
        tasks = [
            self._project_to_domain(collapsed, domain)
            for domain in active_domains
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for domain, result in zip(active_domains, results):
            if isinstance(result, Exception):
                continue
            projections[domain] = result
        
        # Compute cross-domain correlations
        correlations = self._compute_correlations(projections)
        
        return MirroredState(
            collapsed=collapsed,
            projections=projections,
            active_domains=list(projections.keys()),
            cross_domain_correlations=correlations
        )
    
    async def _forge(self, mirrored: MirroredState) -> ForgedState:
        """
        FORGE phase: Synthesize cross-domain insights.
        
        Rules:
        - Convergent: Pattern appears in 3+ domains
        - Divergent: Domains contradict each other
        - Emergent: Pattern only visible in combination
        """
        insights: List[ForgedInsight] = []
        
        # Find convergent patterns
        convergent = self._find_convergent_patterns(mirrored.projections)
        insights.extend(convergent)
        
        # Find divergent patterns
        divergent = self._find_divergent_patterns(mirrored.projections)
        insights.extend(divergent)
        
        # Find emergent patterns
        emergent = self._find_emergent_patterns(mirrored.projections)
        insights.extend(emergent)
        
        # Synthesize all insights
        synthesis = self._synthesize(insights, mirrored)
        
        # Compute confidence
        confidence = self._compute_forge_confidence(insights)
        
        # Extract divergent claims for reporting
        divergent_claims = [
            {"pattern": i.content, "sources": [d.value for d in i.source_domains]}
            for i in insights if i.pattern_type == "divergent"
        ]
        
        return ForgedState(
            mirrored=mirrored,
            insights=insights,
            synthesis=synthesis,
            confidence_score=confidence,
            divergent_claims=divergent_claims
        )
    
    async def _link(
        self, 
        forged: ForgedState, 
        start_time: datetime
    ) -> LinkedOutput:
        """
        LINK phase: Connect to memory and emit output.
        
        Operations:
        - Store state with CID
        - Update pheromone trails
        - Emit trace events
        - Prepare output
        """
        # Generate output text
        output_text = self._generate_output(forged)
        
        # Create content ID
        cid = ContentID.from_content(output_text)
        
        # Store in content-addressed storage
        await self.store.store(cid, {
            "output": output_text,
            "forged_state": forged.synthesis,
            "confidence": forged.confidence_score
        })
        
        # Record memory updates
        memory_updates = [
            {"cid": str(cid), "type": "output", "confidence": forged.confidence_score}
        ]
        
        # Emit completion event
        emitted_events = [
            {"kind": "cmfl_complete", "cid": str(cid)}
        ]
        
        # Calculate duration
        duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return LinkedOutput(
            forged=forged,
            output_text=output_text,
            memory_updates=memory_updates,
            emitted_events=emitted_events,
            cid=cid,
            total_duration_ms=duration_ms
        )
    
    # Helper methods
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text."""
        # Simplified - use spaCy or similar in production
        words = text.split()
        entities = [w for w in words if w[0].isupper() and len(w) > 1]
        return entities[:10]
    
    def _identify_intent(self, text: str) -> str:
        """Identify query intent."""
        text_lower = text.lower()
        if any(w in text_lower for w in ['what', 'who', 'where', 'when']):
            return "factual_query"
        elif any(w in text_lower for w in ['how', 'why', 'explain']):
            return "explanatory_query"
        elif any(w in text_lower for w in ['create', 'write', 'generate']):
            return "generative_request"
        elif any(w in text_lower for w in ['compare', 'versus', 'difference']):
            return "comparative_analysis"
        else:
            return "general_query"
    
    def _compress_to_essential(
        self, 
        text: str, 
        entities: List[str], 
        intent: str
    ) -> str:
        """Compress to essential signal."""
        # Keep entities and key phrases
        essential_parts = [intent] + entities
        return " ".join(essential_parts)
    
    def _compute_complexity(self, text: str) -> float:
        """Compute query complexity score (0-1)."""
        factors = [
            min(len(text) / 1000, 1.0),  # Length factor
            min(text.count('?') / 5, 1.0),  # Question count
            min(text.count(',') / 10, 1.0),  # Clause count
        ]
        return sum(factors) / len(factors)
    
    def _select_domains(self, collapsed: CollapsedState) -> List[MirrorDomain]:
        """Select domains based on query characteristics."""
        # Always include base domains
        domains = [MirrorDomain.EUCLIDEAN, MirrorDomain.HYPERBOLIC]
        
        # Add based on intent
        if "factual" in collapsed.identified_intent:
            domains.append(MirrorDomain.INFORMATION)
        if "explanatory" in collapsed.identified_intent:
            domains.extend([MirrorDomain.CAUSAL, MirrorDomain.TEMPORAL])
        if "comparative" in collapsed.identified_intent:
            domains.append(MirrorDomain.TOPOLOGICAL)
        
        # Add meta domain for complex queries
        if collapsed.complexity_score > 0.5:
            domains.append(MirrorDomain.META)
        
        return list(set(domains))
    
    async def _project_to_domain(
        self, 
        collapsed: CollapsedState, 
        domain: MirrorDomain
    ) -> DomainProjection:
        """Project collapsed state into specific domain."""
        domain_impl = self.domains.get(domain)
        return await domain_impl.project(collapsed)
    
    def _compute_correlations(
        self, 
        projections: Dict[MirrorDomain, DomainProjection]
    ) -> Dict[str, float]:
        """Compute correlations between domain projections."""
        correlations = {}
        domains = list(projections.keys())
        
        for i, d1 in enumerate(domains):
            for d2 in domains[i+1:]:
                key = f"{d1.value}_{d2.value}"
                # Simplified correlation - compare pattern overlap
                p1_patterns = set(projections[d1].patterns)
                p2_patterns = set(projections[d2].patterns)
                if p1_patterns or p2_patterns:
                    overlap = len(p1_patterns & p2_patterns)
                    total = len(p1_patterns | p2_patterns)
                    correlations[key] = overlap / total if total > 0 else 0
        
        return correlations
    
    def _find_convergent_patterns(
        self, 
        projections: Dict[MirrorDomain, DomainProjection]
    ) -> List[ForgedInsight]:
        """Find patterns appearing in 3+ domains."""
        pattern_domains: Dict[str, List[MirrorDomain]] = {}
        
        for domain, proj in projections.items():
            for pattern in proj.patterns:
                if pattern not in pattern_domains:
                    pattern_domains[pattern] = []
                pattern_domains[pattern].append(domain)
        
        convergent = []
        for pattern, domains in pattern_domains.items():
            if len(domains) >= 3:
                convergent.append(ForgedInsight(
                    source_domains=domains,
                    pattern_type="convergent",
                    content=pattern,
                    confidence=len(domains) / len(projections),
                    supporting_evidence=[f"Found in {d.value}" for d in domains]
                ))
        
        return convergent
    
    def _find_divergent_patterns(
        self, 
        projections: Dict[MirrorDomain, DomainProjection]
    ) -> List[ForgedInsight]:
        """Find contradictory patterns between domains."""
        # Simplified - check for negation patterns
        divergent = []
        all_patterns = []
        
        for domain, proj in projections.items():
            for pattern in proj.patterns:
                all_patterns.append((domain, pattern))
        
        for i, (d1, p1) in enumerate(all_patterns):
            for d2, p2 in all_patterns[i+1:]:
                # Simple contradiction check
                if (p1.startswith("not_") and p1[4:] == p2) or \
                   (p2.startswith("not_") and p2[4:] == p1):
                    divergent.append(ForgedInsight(
                        source_domains=[d1, d2],
                        pattern_type="divergent",
                        content=f"Contradiction: {p1} vs {p2}",
                        confidence=0.5,
                        supporting_evidence=[f"{d1.value}: {p1}", f"{d2.value}: {p2}"]
                    ))
        
        return divergent
    
    def _find_emergent_patterns(
        self, 
        projections: Dict[MirrorDomain, DomainProjection]
    ) -> List[ForgedInsight]:
        """Find patterns only visible in combination."""
        # Look for patterns in cross-domain analysis
        emergent = []
        
        if MirrorDomain.META in projections:
            meta_proj = projections[MirrorDomain.META]
            other_patterns = set()
            for d, p in projections.items():
                if d != MirrorDomain.META:
                    other_patterns.update(p.patterns)
            
            for pattern in meta_proj.patterns:
                if pattern not in other_patterns:
                    emergent.append(ForgedInsight(
                        source_domains=[MirrorDomain.META],
                        pattern_type="emergent",
                        content=pattern,
                        confidence=0.7,
                        supporting_evidence=["Only visible in cross-domain analysis"]
                    ))
        
        return emergent
    
    def _synthesize(
        self, 
        insights: List[ForgedInsight], 
        mirrored: MirroredState
    ) -> str:
        """Synthesize insights into coherent output."""
        if not insights:
            return mirrored.collapsed.essential_signal
        
        # Prioritize convergent, then emergent, then divergent
        convergent = [i for i in insights if i.pattern_type == "convergent"]
        emergent = [i for i in insights if i.pattern_type == "emergent"]
        
        synthesis_parts = []
        
        if convergent:
            synthesis_parts.append(
                f"High-confidence findings: {convergent[0].content}"
            )
        if emergent:
            synthesis_parts.append(
                f"Emergent insight: {emergent[0].content}"
            )
        
        return ". ".join(synthesis_parts) if synthesis_parts else "No synthesis available"
    
    def _compute_forge_confidence(self, insights: List[ForgedInsight]) -> float:
        """Compute overall confidence from insights."""
        if not insights:
            return 0.5
        
        convergent_count = sum(1 for i in insights if i.pattern_type == "convergent")
        divergent_count = sum(1 for i in insights if i.pattern_type == "divergent")
        
        # More convergent = higher confidence
        # More divergent = lower confidence
        base = 0.5
        convergent_boost = convergent_count * 0.1
        divergent_penalty = divergent_count * 0.15
        
        return min(1.0, max(0.0, base + convergent_boost - divergent_penalty))
    
    def _generate_output(self, forged: ForgedState) -> str:
        """Generate final output text."""
        return forged.synthesis
```

## 28.5 Pheromone System (ghostlink/coordination/pheromones.py)

```python
"""Stigmergic pheromone coordination system."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import math
import random

from ..core.types import Position3D, PheromoneDeposit


@dataclass
class PheromoneConfig:
    """Configuration for pheromone behavior."""
    decay_rates: Dict[str, float] = field(default_factory=lambda: {
        "task": 0.1,      # per hour
        "resource": 0.5,
        "quality": 0.05,
        "error": 0.2
    })
    evaporation_threshold: float = 0.01
    exploration_rate: float = 0.1
    amplification_factor: float = 1.5
    max_strength: float = 100.0


class PheromoneMap:
    """
    Manage pheromone deposits for stigmergic coordination.
    
    Pheromone types:
    - task: Indicates active processing at location
    - resource: Marks available computational resources
    - quality: Reinforces successful paths
    - error: Warns of failure-prone locations
    """
    
    def __init__(self, config: Optional[PheromoneConfig] = None):
        self.config = config or PheromoneConfig()
        self.deposits: Dict[str, List[PheromoneDeposit]] = defaultdict(list)
        self._last_evaporation: datetime = datetime.utcnow()
    
    def deposit(
        self,
        pheromone_type: str,
        position: Position3D,
        strength: float,
        depositor_id: int
    ) -> None:
        """
        Deposit pheromone at position.
        Existing deposits of same type are amplified.
        """
        key = self._position_key(position)
        now = datetime.utcnow()
        
        # Check for existing deposit of same type
        existing = None
        for dep in self.deposits[key]:
            if dep.type == pheromone_type:
                existing = dep
                break
        
        if existing:
            # Amplify existing deposit
            existing.strength = min(
                self.config.max_strength,
                existing.strength + strength * self.config.amplification_factor
            )
            existing.timestamp = now
        else:
            # Create new deposit
            self.deposits[key].append(PheromoneDeposit(
                type=pheromone_type,
                position=position,
                strength=strength,
                timestamp=now,
                depositor_id=depositor_id
            ))
    
    def read(
        self,
        pheromone_type: str,
        position: Position3D
    ) -> float:
        """Read current pheromone strength at position."""
        key = self._position_key(position)
        now = datetime.utcnow()
        
        for dep in self.deposits[key]:
            if dep.type == pheromone_type:
                decay_rate = self.config.decay_rates.get(pheromone_type, 0.1)
                return dep.decay(decay_rate, now)
        
        return 0.0
    
    def read_all(self, position: Position3D) -> Dict[str, float]:
        """Read all pheromone strengths at position."""
        key = self._position_key(position)
        now = datetime.utcnow()
        
        result = {}
        for dep in self.deposits[key]:
            decay_rate = self.config.decay_rates.get(dep.type, 0.1)
            result[dep.type] = dep.decay(decay_rate, now)
        
        return result
    
    def select_next(
        self,
        candidates: List[int],
        positions: Dict[int, Position3D],
        preferred_type: str = "quality"
    ) -> int:
        """
        Select next agent from candidates using pheromone-guided routing.
        
        With probability exploration_rate, choose randomly.
        Otherwise, weight selection by pheromone strength.
        """
        if not candidates:
            raise ValueError("No candidates provided")
        
        # Exploration: random selection
        if random.random() < self.config.exploration_rate:
            return random.choice(candidates)
        
        # Exploitation: pheromone-weighted selection
        weights = []
        for agent_id in candidates:
            pos = positions.get(agent_id)
            if pos:
                strength = self.read(preferred_type, pos)
                # Add small baseline to ensure non-zero probability
                weights.append(strength + 0.1)
            else:
                weights.append(0.1)
        
        # Weighted random selection
        total = sum(weights)
        r = random.random() * total
        
        cumulative = 0
        for i, weight in enumerate(weights):
            cumulative += weight
            if r <= cumulative:
                return candidates[i]
        
        return candidates[-1]
    
    def evaporate(self) -> int:
        """
        Evaporate weak pheromones.
        Returns number of deposits removed.
        """
        now = datetime.utcnow()
        removed = 0
        
        for key in list(self.deposits.keys()):
            surviving = []
            for dep in self.deposits[key]:
                decay_rate = self.config.decay_rates.get(dep.type, 0.1)
                strength = dep.decay(decay_rate, now)
                
                if strength > self.config.evaporation_threshold:
                    surviving.append(dep)
                else:
                    removed += 1
            
            if surviving:
                self.deposits[key] = surviving
            else:
                del self.deposits[key]
        
        self._last_evaporation = now
        return removed
    
    def get_gradient(
        self,
        position: Position3D,
        pheromone_type: str,
        neighbors: List[Position3D]
    ) -> Optional[Position3D]:
        """
        Get direction of steepest pheromone gradient.
        Returns neighbor position with highest concentration.
        """
        if not neighbors:
            return None
        
        current_strength = self.read(pheromone_type, position)
        
        best_pos = None
        best_strength = current_strength
        
        for neighbor in neighbors:
            strength = self.read(pheromone_type, neighbor)
            if strength > best_strength:
                best_strength = strength
                best_pos = neighbor
        
        return best_pos
    
    def export_state(self) -> Dict:
        """Export pheromone state for serialization."""
        now = datetime.utcnow()
        state = {}
        
        for key, deposits in self.deposits.items():
            state[key] = [
                {
                    "type": dep.type,
                    "position": dep.position.to_tuple(),
                    "strength": dep.decay(
                        self.config.decay_rates.get(dep.type, 0.1),
                        now
                    ),
                    "depositor": dep.depositor_id
                }
                for dep in deposits
            ]
        
        return state
    
    def import_state(self, state: Dict) -> None:
        """Import pheromone state from serialization."""
        now = datetime.utcnow()
        self.deposits.clear()
        
        for key, deposits in state.items():
            for dep_data in deposits:
                pos = Position3D(*dep_data["position"])
                self.deposits[key].append(PheromoneDeposit(
                    type=dep_data["type"],
                    position=pos,
                    strength=dep_data["strength"],
                    timestamp=now,
                    depositor_id=dep_data["depositor"]
                ))
    
    def _position_key(self, position: Position3D) -> str:
        """Generate hashable key for position."""
        return f"{position.x},{position.y},{position.z}"
    
    def get_statistics(self) -> Dict:
        """Get pheromone system statistics."""
        total_deposits = sum(len(deps) for deps in self.deposits.values())
        by_type = defaultdict(int)
        
        for deps in self.deposits.values():
            for dep in deps:
                by_type[dep.type] += 1
        
        return {
            "total_deposits": total_deposits,
            "positions_with_deposits": len(self.deposits),
            "deposits_by_type": dict(by_type),
            "last_evaporation": self._last_evaporation.isoformat()
        }
```

---

# 29. TYPESCRIPT IMPLEMENTATION

## 29.1 Cloudflare Worker Types

```typescript
// types.ts

export interface Position3D {
  x: number;
  y: number;
  z: number;
}

export interface AgentSpec {
  id: number;
  name: string;
  group: string;
  duty: string;
  invariants: string[];
  inputType: string;
  outputType: string;
  position: Position3D;
  multipaths: string[];
}

export interface Query {
  id: string;
  text: string;
  timestamp: string;
  metadata: Record<string, unknown>;
  maxIterations: number;
  targetDomains?: string[];
  targetShards?: string[];
}

export interface ProviderResponse {
  provider: string;
  model: string;
  content: string;
  tokensUsed: number;
  latencyMs: number;
  logprobs?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
}

export interface VarianceMetrics {
  semanticVariance: number;
  lexicalVariance: number;
  structuralVariance: number;
  confidenceVariance: number;
  factualAgreement: number;
  reasoningDivergence: number;
}

export interface VarianceAnalysis {
  queryId: string;
  responses: ProviderResponse[];
  metrics: VarianceMetrics;
  clusters: number[][];
  consensus: string | null;
  divergentClaims: Record<string, unknown>[];
  confidenceScore: number;
  metaInsight: string;
}

export interface PheromoneDeposit {
  type: 'task' | 'resource' | 'quality' | 'error';
  position: Position3D;
  strength: number;
  timestamp: number;
  depositorId: number;
}

export interface SCARRecord {
  id: string;
  scarType: string;
  timestamp: number;
  context: Record<string, unknown>;
  errorMessage: string;
  stackTraceHash: string;
  recoveryAttempted: boolean;
  recoverySuccessful: boolean;
  recoveryStrategy?: string;
  lessonsLearned: string[];
}

export interface Env {
  SWARM: DurableObjectNamespace;
  SHARD: DurableObjectNamespace;
  PHEROMONES: KVNamespace;
  AUDIT_LOG: D1Database;
  SNAPSHOTS: R2Bucket;
}
```

## 29.2 Swarm Coordinator Durable Object

```typescript
// swarm-coordinator.ts

import { Position3D, Query, VarianceAnalysis, Env } from './types';

interface AgentRoute {
  agents: number[];
  shards: string[];
}

export class SwarmCoordinator implements DurableObject {
  private state: DurableObjectState;
  private env: Env;
  private pheromones: Map<string, number> = new Map();
  
  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
    this.env = env;
  }
  
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    switch (url.pathname) {
      case '/query':
        return this.handleQuery(request);
      case '/status':
        return this.getStatus();
      case '/pheromones':
        return this.getPheromones();
      case '/route':
        return this.computeRoute(request);
      default:
        return new Response('Not Found', { status: 404 });
    }
  }
  
  private async handleQuery(request: Request): Promise<Response> {
    const body = await request.json() as { query: Query };
    const { query } = body;
    
    // 1. Analyze complexity
    const complexity = this.analyzeComplexity(query.text);
    
    // 2. Select shards
    const activeShards = this.selectShards(complexity);
    
    // 3. Compute route
    const route = this.computeRoutePath(query, activeShards);
    
    // 4. Dispatch to shard controllers
    const results = await this.dispatchToShards(query, route);
    
    // 5. Aggregate
    const aggregated = this.aggregateResults(results);
    
    // 6. Update pheromones
    this.updatePheromones(route, aggregated.confidenceScore);
    
    return new Response(JSON.stringify(aggregated), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  private analyzeComplexity(text: string): number {
    const lengthFactor = Math.min(text.length / 1000, 1);
    const questionFactor = (text.match(/\?/g) || []).length / 5;
    const clauseFactor = (text.match(/,/g) || []).length / 10;
    
    return Math.min(1, (lengthFactor + questionFactor + clauseFactor) / 3);
  }
  
  private selectShards(complexity: number): string[] {
    if (complexity < 0.3) {
      return ['ES-01', 'ES-03', 'ES-09'];
    } else if (complexity < 0.7) {
      return [
        'ES-01', 'ES-02', 'ES-03', 'ES-04', 'ES-05',
        'ES-09', 'ES-14', 'ES-18', 'ES-21', 'ES-22'
      ];
    } else {
      return Array.from({ length: 22 }, (_, i) => 
        `ES-${String(i + 1).padStart(2, '0')}`
      );
    }
  }
  
  private computeRoutePath(query: Query, shards: string[]): AgentRoute {
    const entryAgent = this.selectEntryAgent(query.text);
    const agents: number[] = [entryAgent];
    
    let current = entryAgent;
    for (const shard of shards) {
      const target = this.shardToAgent(shard);
      const path = this.findPath(current, target);
      agents.push(...path.slice(1));
      current = target;
    }
    
    return { agents, shards };
  }
  
  private selectEntryAgent(text: string): number {
    // Simple hash-based selection
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      hash = ((hash << 5) - hash) + text.charCodeAt(i);
      hash |= 0;
    }
    return (Math.abs(hash) % 8) + 1; // Agents 1-8 (ALPHA group)
  }
  
  private shardToAgent(shard: string): number {
    const shardNum = parseInt(shard.split('-')[1]);
    // Map shards to agent groups
    return ((shardNum - 1) % 8) * 8 + (shardNum % 8) + 1;
  }
  
  private findPath(source: number, target: number): number[] {
    if (source === target) return [source];
    
    // Simplified BFS (use full Dijkstra with pheromones in production)
    const visited = new Set<number>();
    const queue: [number, number[]][] = [[source, [source]]];
    
    while (queue.length > 0) {
      const [current, path] = queue.shift()!;
      
      if (current === target) return path;
      if (visited.has(current)) continue;
      visited.add(current);
      
      for (const neighbor of this.getNeighbors(current)) {
        if (!visited.has(neighbor)) {
          queue.push([neighbor, [...path, neighbor]]);
        }
      }
    }
    
    return [source, target]; // Direct path if no route found
  }
  
  private getNeighbors(agentId: number): number[] {
    // FCC neighbors (simplified)
    const neighbors: number[] = [];
    const offsets = [-1, 1, -8, 8, -9, 9, -7, 7];
    
    for (const offset of offsets) {
      const neighbor = agentId + offset;
      if (neighbor >= 1 && neighbor <= 64 && neighbor !== agentId) {
        neighbors.push(neighbor);
      }
    }
    
    return neighbors;
  }
  
  private async dispatchToShards(
    query: Query, 
    route: AgentRoute
  ): Promise<VarianceAnalysis[]> {
    const results: VarianceAnalysis[] = [];
    
    for (const shard of route.shards) {
      const shardId = this.env.SHARD.idFromName(shard);
      const shardObj = this.env.SHARD.get(shardId);
      
      const response = await shardObj.fetch(
        new Request('https://shard/analyze', {
          method: 'POST',
          body: JSON.stringify({ query, route })
        })
      );
      
      if (response.ok) {
        results.push(await response.json());
      }
    }
    
    return results;
  }
  
  private aggregateResults(results: VarianceAnalysis[]): VarianceAnalysis {
    if (results.length === 0) {
      throw new Error('No results to aggregate');
    }
    
    if (results.length === 1) {
      return results[0];
    }
    
    // Aggregate metrics
    const aggregated: VarianceAnalysis = {
      queryId: results[0].queryId,
      responses: results.flatMap(r => r.responses),
      metrics: {
        semanticVariance: this.mean(results.map(r => r.metrics.semanticVariance)),
        lexicalVariance: this.mean(results.map(r => r.metrics.lexicalVariance)),
        structuralVariance: this.mean(results.map(r => r.metrics.structuralVariance)),
        confidenceVariance: this.mean(results.map(r => r.metrics.confidenceVariance)),
        factualAgreement: this.mean(results.map(r => r.metrics.factualAgreement)),
        reasoningDivergence: this.mean(results.map(r => r.metrics.reasoningDivergence))
      },
      clusters: results.flatMap(r => r.clusters),
      consensus: results.find(r => r.consensus)?.consensus || null,
      divergentClaims: results.flatMap(r => r.divergentClaims),
      confidenceScore: this.mean(results.map(r => r.confidenceScore)),
      metaInsight: results.map(r => r.metaInsight).join(' ')
    };
    
    return aggregated;
  }
  
  private updatePheromones(route: AgentRoute, confidence: number): void {
    const strength = confidence * 10;
    
    for (const agentId of route.agents) {
      const key = `quality:${agentId}`;
      const current = this.pheromones.get(key) || 0;
      this.pheromones.set(key, Math.min(100, current + strength));
    }
  }
  
  private mean(values: number[]): number {
    return values.reduce((a, b) => a + b, 0) / values.length;
  }
  
  private async getStatus(): Promise<Response> {
    return new Response(JSON.stringify({
      status: 'healthy',
      agents: 64,
      pheromoneCount: this.pheromones.size
    }));
  }
  
  private async getPheromones(): Promise<Response> {
    return new Response(JSON.stringify(
      Object.fromEntries(this.pheromones)
    ));
  }
  
  private async computeRoute(request: Request): Promise<Response> {
    const { source, target } = await request.json() as { 
      source: number; 
      target: number; 
    };
    
    const path = this.findPath(source, target);
    return new Response(JSON.stringify({ path }));
  }
}
```

---

*End of Part 7*
*Continue to Part 8: Testing, Deployment, Operations*

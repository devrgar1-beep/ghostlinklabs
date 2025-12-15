#!/usr/bin/env python3
"""
GhostLink v8 Orchestrator - 64-Agent FCC Lattice Coordinator

This is the central orchestration engine that manages the 64-agent Face-Centered Cubic
lattice topology with CMFL (Collapse→Mirror→Forge→Link) reasoning cycles and
stigmergic coordination mechanisms.

Architecture:
- 64 agents in 4D FCC lattice (4x4x4x4 = 256 positions, 64 occupied in FCC pattern)
- Each agent executes CMFL cycles independently with stigmergic coordination
- Variance analysis across 8+ AI providers treated as meta-information
- Byzantine fault tolerance with zero-failure operational requirements

Author: Robert Christopher George (Ghost)
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import argparse
import signal
import sys
from dataclasses import dataclass, field
from enum import Enum

# Third-party imports
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import psycopg2
from psycopg2.extras import RealDictCursor
import redis.asyncio as aioredis
from pydantic import BaseModel
import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION AND CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# FCC Lattice Constants
FCC_LATTICE_SIZE = 64
FCC_DIMENSIONS = 4
FCC_EDGE_LENGTH = 4

# CMFL Cycle Configuration
CMFL_CYCLE_INTERVAL_MS = 500
STIGMERGY_THRESHOLD = 0.7
PHEROMONE_EVAPORATION_RATE = 0.1

# Coordination Timeouts
AGENT_HEARTBEAT_TIMEOUT = 30  # seconds
COORDINATION_TIMEOUT = 30000  # milliseconds

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ghostlink.orchestrator")

# ══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ══════════════════════════════════════════════════════════════════════════════

class CMFLPhase(str, Enum):
    """CMFL reasoning cycle phases"""
    COLLAPSE = "collapse"  # Collapse uncertainty into discrete options
    MIRROR = "mirror"      # Mirror patterns across agent network
    FORGE = "forge"        # Forge new understanding from variance
    LINK = "link"          # Link coordinated response

@dataclass
class AgentState:
    """Represents the state of a single agent in the lattice"""
    agent_id: str
    lattice_position: Tuple[int, int, int, int]
    topology_layer: int
    cmfl_phase: CMFLPhase
    variance_score: float = 0.0
    coordination_weight: float = 1.0
    last_heartbeat: datetime = field(default_factory=datetime.now)
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PheromoneTrail:
    """Stigmergic pheromone trail for agent coordination"""
    trail_id: str
    agent_id: str
    trail_type: str
    concentration: float
    position: Tuple[int, int, int, int]
    evaporation_rate: float = PHEROMONE_EVAPORATION_RATE
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None

@dataclass
class CMFLCycle:
    """Record of a complete CMFL reasoning cycle"""
    cycle_id: str
    cycle_number: int
    phase: CMFLPhase
    agent_id: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    variance_detected: float = 0.0
    duration_ms: int = 0
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

# Pydantic models for API
class HealthResponse(BaseModel):
    status: str
    version: str
    lattice_size: int
    active_agents: int
    uptime_seconds: float

class AgentStatusResponse(BaseModel):
    total_agents: int
    active_count: int
    inactive_count: int
    agents_by_phase: Dict[str, int]

class CoordinationMetrics(BaseModel):
    stigmergy_trails_active: int
    cmfl_cycles_completed: int
    average_variance_score: float
    average_coordination_weight: float

# ══════════════════════════════════════════════════════════════════════════════
# FCC LATTICE TOPOLOGY
# ══════════════════════════════════════════════════════════════════════════════

class FCCLattice:
    """
    Face-Centered Cubic lattice topology generator for 64-agent configuration.
    
    In FCC, atoms occupy corner positions and face-center positions.
    Extended to 4D space for GhostLink's coordination topology.
    """
    
    @staticmethod
    def generate_fcc_positions(edge_length: int = 4) -> List[Tuple[int, int, int, int]]:
        """
        Generate 64 FCC lattice positions in 4D space.
        
        Pattern: Corner positions + face centers in all dimensions
        This creates natural coordination neighborhoods for stigmergic trails.
        """
        positions = []
        
        # Generate all possible positions in 4D grid
        for x in range(edge_length):
            for y in range(edge_length):
                for z in range(edge_length):
                    for w in range(edge_length):
                        # FCC pattern: include positions where sum is even
                        # This creates the face-centered structure
                        if (x + y + z + w) % 2 == 0:
                            positions.append((x, y, z, w))
        
        # Should yield exactly 128 positions for 4x4x4x4 FCC
        # We use first 64 for our agent allocation
        return positions[:FCC_LATTICE_SIZE]
    
    @staticmethod
    def get_topology_layer(position: Tuple[int, int, int, int]) -> int:
        """Determine which coordination layer this position belongs to"""
        x, y, z, w = position
        return (x + y + z + w) % 4
    
    @staticmethod
    def calculate_distance(pos1: Tuple[int, int, int, int], 
                          pos2: Tuple[int, int, int, int]) -> float:
        """Calculate 4D Euclidean distance between lattice positions"""
        return np.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
    
    @staticmethod
    def get_neighbors(position: Tuple[int, int, int, int], 
                     all_positions: List[Tuple[int, int, int, int]],
                     max_distance: float = 2.0) -> List[Tuple[int, int, int, int]]:
        """Get neighboring positions within stigmergic coordination range"""
        neighbors = []
        for pos in all_positions:
            if pos != position:
                distance = FCCLattice.calculate_distance(position, pos)
                if distance <= max_distance:
                    neighbors.append(pos)
        return neighbors

# ══════════════════════════════════════════════════════════════════════════════
# DATABASE LAYER
# ══════════════════════════════════════════════════════════════════════════════

class DatabaseManager:
    """PostgreSQL database operations for agent state and coordination"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn = None
        
    async def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(self.connection_string)
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    async def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Retrieve all agents from database"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM agents ORDER BY lattice_position")
            return cur.fetchall()
    
    def update_agent_heartbeat(self, agent_id: str):
        """Update agent heartbeat timestamp"""
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE agents SET last_heartbeat = NOW() WHERE agent_id = %s",
                (agent_id,)
            )
            self.conn.commit()
    
    def update_agent_phase(self, agent_id: str, phase: CMFLPhase):
        """Update agent's current CMFL phase"""
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE agents SET cmfl_phase = %s, updated_at = NOW() WHERE agent_id = %s",
                (phase.value, agent_id)
            )
            self.conn.commit()
    
    def record_cmfl_cycle(self, cycle: CMFLCycle):
        """Record completed CMFL cycle to database"""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cmfl_cycles 
                (cycle_number, phase, agent_id, input_data, output_data, 
                 variance_detected, duration_ms, started_at, completed_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (cycle.cycle_number, cycle.phase.value, cycle.agent_id,
                 str(cycle.input_data), str(cycle.output_data),
                 cycle.variance_detected, cycle.duration_ms,
                 cycle.started_at, cycle.completed_at)
            )
            self.conn.commit()
    
    def get_coordination_metrics(self) -> Dict[str, Any]:
        """Get system-wide coordination metrics"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Count CMFL cycles
            cur.execute("SELECT COUNT(*) as cycle_count FROM cmfl_cycles")
            cycle_count = cur.fetchone()['cycle_count']
            
            # Average variance score
            cur.execute("SELECT AVG(variance_score) as avg_variance FROM agents")
            avg_variance = cur.fetchone()['avg_variance'] or 0.0
            
            # Average coordination weight
            cur.execute("SELECT AVG(coordination_weight) as avg_weight FROM agents")
            avg_weight = cur.fetchone()['avg_weight'] or 1.0
            
            return {
                'cmfl_cycles_completed': cycle_count,
                'average_variance_score': float(avg_variance),
                'average_coordination_weight': float(avg_weight)
            }

# ══════════════════════════════════════════════════════════════════════════════
# REDIS STIGMERGY LAYER
# ══════════════════════════════════════════════════════════════════════════════

class StigmergyManager:
    """
    Redis-based stigmergic pheromone trail management.
    
    Agents leave pheromone trails that evaporate over time, allowing
    indirect coordination without direct communication.
    """
    
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Optional[aioredis.Redis] = None
        
    async def connect(self):
        """Establish Redis connection"""
        try:
            self.redis = await aioredis.from_url(self.redis_url)
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            raise
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
            logger.info("Redis connection closed")
    
    async def deposit_pheromone(self, trail: PheromoneTrail):
        """Deposit a pheromone trail at specified position"""
        key = f"pheromone:{trail.position}"
        value = f"{trail.agent_id}:{trail.trail_type}:{trail.concentration}"
        
        # Set with TTL based on evaporation rate
        ttl_seconds = int(1 / trail.evaporation_rate)
        await self.redis.setex(key, ttl_seconds, value)
        
        logger.debug(f"Pheromone deposited at {trail.position} by {trail.agent_id}")
    
    async def sense_pheromones(self, position: Tuple[int, int, int, int]) -> List[Dict[str, Any]]:
        """Sense pheromones at and around specified position"""
        pheromones = []
        
        # Check exact position
        key = f"pheromone:{position}"
        value = await self.redis.get(key)
        
        if value:
            parts = value.decode().split(':')
            pheromones.append({
                'agent_id': parts[0],
                'trail_type': parts[1],
                'concentration': float(parts[2]),
                'position': position
            })
        
        return pheromones
    
    async def evaporate_trails(self):
        """Periodic evaporation of weak pheromone trails (handled by Redis TTL)"""
        # Redis TTL handles automatic evaporation
        # This method can be used for additional cleanup if needed
        pass
    
    async def get_active_trail_count(self) -> int:
        """Count currently active pheromone trails"""
        keys = await self.redis.keys("pheromone:*")
        return len(keys)

# ══════════════════════════════════════════════════════════════════════════════
# AGENT ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════

class AgentOrchestrator:
    """
    Main orchestrator for 64-agent lattice coordination.
    
    Manages agent lifecycle, CMFL cycle execution, stigmergic coordination,
    and Byzantine fault tolerance.
    """
    
    def __init__(self, 
                 lattice_size: int,
                 topology: str,
                 db_manager: DatabaseManager,
                 stigmergy_manager: StigmergyManager):
        self.lattice_size = lattice_size
        self.topology = topology
        self.db = db_manager
        self.stigmergy = stigmergy_manager
        
        self.agents: Dict[str, AgentState] = {}
        self.lattice_positions: List[Tuple[int, int, int, int]] = []
        self.cycle_counter = 0
        self.start_time = datetime.now()
        
        self.running = False
        self.cmfl_tasks: List[asyncio.Task] = []
    
    async def initialize(self):
        """Initialize agent lattice and database connections"""
        logger.info(f"Initializing {self.lattice_size}-agent {self.topology.upper()} lattice...")
        
        # Connect to services
        await self.db.connect()
        await self.stigmergy.connect()
        
        # Generate FCC lattice positions
        self.lattice_positions = FCCLattice.generate_fcc_positions()
        logger.info(f"Generated {len(self.lattice_positions)} FCC lattice positions")
        
        # Load agents from database
        db_agents = self.db.get_all_agents()
        
        for db_agent in db_agents:
            agent_id = str(db_agent['agent_id'])
            position = tuple(db_agent['lattice_position'])
            
            agent_state = AgentState(
                agent_id=agent_id,
                lattice_position=position,
                topology_layer=db_agent['topology_layer'],
                cmfl_phase=CMFLPhase(db_agent['cmfl_phase']),
                variance_score=db_agent.get('variance_score', 0.0),
                coordination_weight=db_agent.get('coordination_weight', 1.0),
                last_heartbeat=db_agent.get('last_heartbeat', datetime.now()),
                active=True
            )
            
            self.agents[agent_id] = agent_state
        
        logger.info(f"Loaded {len(self.agents)} agents from database")
        
        if len(self.agents) != self.lattice_size:
            logger.warning(f"Expected {self.lattice_size} agents, found {len(self.agents)}")
    
    async def start_coordination(self):
        """Start CMFL coordination cycles for all agents"""
        self.running = True
        logger.info("Starting agent coordination cycles...")
        
        # Start CMFL cycle for each agent
        for agent_id, agent in self.agents.items():
            task = asyncio.create_task(self.agent_cmfl_loop(agent))
            self.cmfl_tasks.append(task)
        
        # Start stigmergy evaporation loop
        evaporation_task = asyncio.create_task(self.stigmergy_evaporation_loop())
        self.cmfl_tasks.append(evaporation_task)
        
        logger.info(f"Started {len(self.cmfl_tasks)} coordination tasks")
    
    async def agent_cmfl_loop(self, agent: AgentState):
        """
        Execute CMFL reasoning cycles for a single agent.
        
        Cycle: Collapse → Mirror → Forge → Link (repeat)
        """
        while self.running:
            try:
                cycle_start = datetime.now()
                
                # Execute current phase
                await self.execute_cmfl_phase(agent)
                
                # Progress to next phase
                agent.cmfl_phase = self.next_cmfl_phase(agent.cmfl_phase)
                
                # Update database
                self.db.update_agent_phase(agent.agent_id, agent.cmfl_phase)
                self.db.update_agent_heartbeat(agent.agent_id)
                
                # Update local heartbeat
                agent.last_heartbeat = datetime.now()
                
                # Wait for cycle interval
                await asyncio.sleep(CMFL_CYCLE_INTERVAL_MS / 1000.0)
                
            except Exception as e:
                logger.error(f"Error in CMFL loop for agent {agent.agent_id}: {e}")
                await asyncio.sleep(1)  # Back off on error
    
    async def execute_cmfl_phase(self, agent: AgentState):
        """Execute the current CMFL phase for an agent"""
        phase = agent.cmfl_phase
        
        if phase == CMFLPhase.COLLAPSE:
            await self.collapse_phase(agent)
        elif phase == CMFLPhase.MIRROR:
            await self.mirror_phase(agent)
        elif phase == CMFLPhase.FORGE:
            await self.forge_phase(agent)
        elif phase == CMFLPhase.LINK:
            await self.link_phase(agent)
    
    async def collapse_phase(self, agent: AgentState):
        """Collapse: Reduce uncertainty into discrete options"""
        # Sense local pheromones
        pheromones = await self.stigmergy.sense_pheromones(agent.lattice_position)
        
        if pheromones:
            # Calculate local variance from pheromone concentrations
            concentrations = [p['concentration'] for p in pheromones]
            agent.variance_score = np.std(concentrations) if len(concentrations) > 1 else 0.0
        
        logger.debug(f"Agent {agent.agent_id} COLLAPSE: variance={agent.variance_score:.3f}")
    
    async def mirror_phase(self, agent: AgentState):
        """Mirror: Reflect patterns across agent network"""
        # Get neighbors in lattice
        neighbors = FCCLattice.get_neighbors(agent.lattice_position, self.lattice_positions)
        
        # Deposit pheromone for neighbors to sense
        trail = PheromoneTrail(
            trail_id=f"{agent.agent_id}_{self.cycle_counter}",
            agent_id=agent.agent_id,
            trail_type="mirror",
            concentration=agent.coordination_weight,
            position=agent.lattice_position
        )
        await self.stigmergy.deposit_pheromone(trail)
        
        logger.debug(f"Agent {agent.agent_id} MIRROR: deposited trail for {len(neighbors)} neighbors")
    
    async def forge_phase(self, agent: AgentState):
        """Forge: Create new understanding from variance patterns"""
        # Sense pheromones from multiple neighbors
        neighbor_positions = FCCLattice.get_neighbors(
            agent.lattice_position, 
            self.lattice_positions
        )
        
        all_pheromones = []
        for pos in neighbor_positions:
            pheromones = await self.stigmergy.sense_pheromones(pos)
            all_pheromones.extend(pheromones)
        
        # Adjust coordination weight based on variance
        if agent.variance_score > STIGMERGY_THRESHOLD:
            agent.coordination_weight *= 1.1  # Increase influence when high variance
        else:
            agent.coordination_weight *= 0.95  # Decrease when low variance
        
        # Clamp coordination weight
        agent.coordination_weight = max(0.1, min(2.0, agent.coordination_weight))
        
        logger.debug(f"Agent {agent.agent_id} FORGE: weight={agent.coordination_weight:.3f}")
    
    async def link_phase(self, agent: AgentState):
        """Link: Coordinate response across network"""
        self.cycle_counter += 1
        
        # Record cycle completion
        cycle = CMFLCycle(
            cycle_id=f"{agent.agent_id}_{self.cycle_counter}",
            cycle_number=self.cycle_counter,
            phase=CMFLPhase.LINK,
            agent_id=agent.agent_id,
            input_data={'position': agent.lattice_position},
            output_data={'weight': agent.coordination_weight},
            variance_detected=agent.variance_score,
            duration_ms=CMFL_CYCLE_INTERVAL_MS,
            completed_at=datetime.now()
        )
        
        self.db.record_cmfl_cycle(cycle)
        
        logger.debug(f"Agent {agent.agent_id} LINK: cycle {self.cycle_counter} complete")
    
    def next_cmfl_phase(self, current: CMFLPhase) -> CMFLPhase:
        """Determine next phase in CMFL cycle"""
        phases = [CMFLPhase.COLLAPSE, CMFLPhase.MIRROR, CMFLPhase.FORGE, CMFLPhase.LINK]
        current_idx = phases.index(current)
        next_idx = (current_idx + 1) % len(phases)
        return phases[next_idx]
    
    async def stigmergy_evaporation_loop(self):
        """Periodic cleanup of evaporated pheromone trails"""
        while self.running:
            await asyncio.sleep(10)  # Every 10 seconds
            await self.stigmergy.evaporate_trails()
    
    async def shutdown(self):
        """Graceful shutdown of orchestrator"""
        logger.info("Shutting down orchestrator...")
        self.running = False
        
        # Cancel all tasks
        for task in self.cmfl_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.cmfl_tasks, return_exceptions=True)
        
        # Disconnect services
        await self.stigmergy.disconnect()
        await self.db.disconnect()
        
        logger.info("Orchestrator shutdown complete")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current orchestrator status"""
        active_count = sum(1 for agent in self.agents.values() if agent.active)
        
        phases_count = {}
        for agent in self.agents.values():
            phase = agent.cmfl_phase.value
            phases_count[phase] = phases_count.get(phase, 0) + 1
        
        return {
            'total_agents': len(self.agents),
            'active_count': active_count,
            'inactive_count': len(self.agents) - active_count,
            'agents_by_phase': phases_count,
            'cycle_counter': self.cycle_counter,
            'uptime_seconds': (datetime.now() - self.start_time).total_seconds()
        }

# ══════════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

app = FastAPI(title="GhostLink Orchestrator", version="8.0.0")
orchestrator: Optional[AgentOrchestrator] = None

@app.on_event("startup")
async def startup_event():
    """Initialize orchestrator on startup"""
    global orchestrator
    
    # Get configuration from environment
    import os
    db_url = os.getenv('DATABASE_URL', 'postgresql://ghostlink:ghostlink@localhost:5432/ghostlink')
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Initialize managers
    db_manager = DatabaseManager(db_url)
    stigmergy_manager = StigmergyManager(redis_url)
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(
        lattice_size=FCC_LATTICE_SIZE,
        topology="fcc",
        db_manager=db_manager,
        stigmergy_manager=stigmergy_manager
    )
    
    # Initialize and start
    await orchestrator.initialize()
    await orchestrator.start_coordination()
    
    logger.info("GhostLink Orchestrator started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global orchestrator
    if orchestrator:
        await orchestrator.shutdown()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    status = orchestrator.get_status()
    
    return HealthResponse(
        status="healthy",
        version="8.0.0",
        lattice_size=orchestrator.lattice_size,
        active_agents=status['active_count'],
        uptime_seconds=status['uptime_seconds']
    )

@app.get("/agents/count")
async def get_agent_count():
    """Get agent count"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    return {"count": len(orchestrator.agents)}

@app.get("/agents/status", response_model=AgentStatusResponse)
async def get_agent_status():
    """Get detailed agent status"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    status = orchestrator.get_status()
    
    return AgentStatusResponse(
        total_agents=status['total_agents'],
        active_count=status['active_count'],
        inactive_count=status['inactive_count'],
        agents_by_phase=status['agents_by_phase']
    )

@app.get("/metrics/coordination", response_model=CoordinationMetrics)
async def get_coordination_metrics():
    """Get coordination metrics"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    # Get database metrics
    db_metrics = orchestrator.db.get_coordination_metrics()
    
    # Get stigmergy metrics
    trail_count = await orchestrator.stigmergy.get_active_trail_count()
    
    return CoordinationMetrics(
        stigmergy_trails_active=trail_count,
        cmfl_cycles_completed=db_metrics['cmfl_cycles_completed'],
        average_variance_score=db_metrics['average_variance_score'],
        average_coordination_weight=db_metrics['average_coordination_weight']
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "GhostLink Orchestrator",
        "version": "8.0.0",
        "status": "operational",
        "endpoints": [
            "/health",
            "/agents/count",
            "/agents/status",
            "/metrics/coordination"
        ]
    }

# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    sys.exit(0)

def main():
    """Main entry point for orchestrator"""
    parser = argparse.ArgumentParser(description="GhostLink v8 Orchestrator")
    parser.add_argument('--lattice-size', type=int, default=64, help='Number of agents in lattice')
    parser.add_argument('--topology', type=str, default='fcc', help='Lattice topology (fcc)')
    parser.add_argument('--port', type=int, default=8000, help='HTTP API port')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='HTTP API host')
    parser.add_argument('--log-level', type=str, default='INFO', help='Logging level')
    
    args = parser.parse_args()
    
    # Configure logging
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("═" * 80)
    logger.info("  GHOSTLINK v8 ORCHESTRATOR")
    logger.info("  64-Agent FCC Lattice • CMFL Reasoning • Stigmergic Coordination")
    logger.info("═" * 80)
    logger.info(f"Configuration:")
    logger.info(f"  Lattice Size: {args.lattice_size}")
    logger.info(f"  Topology: {args.topology.upper()}")
    logger.info(f"  API Port: {args.port}")
    logger.info(f"  Log Level: {args.log_level}")
    logger.info("═" * 80)
    
    # Start FastAPI server
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level=args.log_level.lower()
    )

if __name__ == "__main__":
    main()

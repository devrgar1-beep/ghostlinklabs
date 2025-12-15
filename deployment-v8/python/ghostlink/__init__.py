"""
GhostLink v8 - Distributed AI Coordination Protocol

A production-grade distributed AI coordination system implementing 64-agent 
Face-Centered Cubic lattice topology with CMFL reasoning cycles and stigmergic 
coordination mechanisms.

Author: Robert Christopher George (Ghost)
Version: 8.0.0
"""

__version__ = "8.0.0"
__author__ = "Robert Christopher George"
__email__ = "ghost@ghostlinklabs.com"

from .orchestrator import (
    AgentOrchestrator,
    CMFLPhase,
    AgentState,
    PheromoneTrail,
    FCCLattice,
    DatabaseManager,
    StigmergyManager
)

__all__ = [
    'AgentOrchestrator',
    'CMFLPhase',
    'AgentState',
    'PheromoneTrail',
    'FCCLattice',
    'DatabaseManager',
    'StigmergyManager',
]

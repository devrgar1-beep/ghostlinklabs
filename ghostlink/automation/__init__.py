"""Automation layer for GhostLink.

This module provides automation policy helpers and autonomous operation components.
"""
from . import policy
from .auto_trigger_engine import AUTO_TRIGGER_ENGINE
from .autonomous_repair_loop import AUTONOMOUS_REPAIR_LOOP
from .lattice_watchdog import LATTICE_WATCHDOG
from .symbolic_task_scheduler import SYMBOLIC_TASK_SCHEDULER
from .tool_chain_orchestrator import TOOL_CHAIN_ORCHESTRATOR

__all__ = [
    "policy",
    "AUTO_TRIGGER_ENGINE",
    "LATTICE_WATCHDOG", 
    "TOOL_CHAIN_ORCHESTRATOR",
    "AUTONOMOUS_REPAIR_LOOP",
    "SYMBOLIC_TASK_SCHEDULER",
]

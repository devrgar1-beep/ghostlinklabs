"""GhostLink AI Ecosystem"""

__version__ = "0.1.0"

import asyncio

# Import main modules
from . import config, core, diagnostic, gui, main, network, obd, orchestration, tools, translator
from .orchestration import main as orchestration_main

__all__ = [
    "__version__",
    "config",
    "core",
    "diagnostic",
    "gui",
    "main",
    "network",
    "obd",
    "orchestration",
    "tools",
    "translator",
]


def run_orchestration_matrix():
    """Run the pure pipeline orchestration matrix."""
    asyncio.run(orchestration_main())

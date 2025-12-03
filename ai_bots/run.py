#!/usr/bin/env python3
"""
Convenience runner for GhostLink AI Bots CLI.
Allows running without tweaking PYTHONPATH.
"""
import asyncio
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_bots.cli import main as cli_main  # noqa: E402

if __name__ == "__main__":
    asyncio.run(cli_main())

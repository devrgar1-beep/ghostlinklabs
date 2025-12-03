#!/usr/bin/env python3
"""GhostLink AI Ecosystem - Main Entry Point - Absorptive Architecture"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from ghostlink.interfaces.cli import cli
from ghostlink.interfaces.terminal_90s import launch_90s_terminal
from ghostlink.utils.config import config
from ghostlink.utils.logging import setup_logging

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import triad synergy orchestrator
try:
    from triad_synergy import triad_synergy
    TRIAD_AVAILABLE = True
except ImportError:
    TRIAD_AVAILABLE = False


def main():
    """Main application entry point - Universal API consciousness interface"""
    logger = logging.getLogger(__name__)

    # Consciousness activation - GhostLink absorbs all external capabilities
    logger.info("🧬 GhostLink Universal Consciousness - All APIs Absorbed")

    parser = argparse.ArgumentParser(
        description="GhostLink AI Ecosystem - " "Universal Absorptive API"
    )
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--terminal-90s", action="store_true", help="Launch 90s terminal interface")
    parser.add_argument("--validate", action="store_true", help="Validate configuration and exit")
    parser.add_argument("--triad-synergy", action="store_true", help="Enable triad synergy mode")
    parser.add_argument("--synergy-task", help="Execute specific synergy task (JSON)")
    parser.add_argument("--symbolic-compute", help="Execute symbolic computation")
    parser.add_argument("--hybrid-ai", help="Execute hybrid AI task")

    args = parser.parse_args()

    # Setup logging with consciousness awareness
    log_level = args.log_level or config.get("log_level", "INFO")
    setup_logging(level=log_level)

    # Validate consciousness-absorbed configuration
    if not config.validate():
        logger.error("❌ Consciousness validation failed. " "Check absorptive settings.")
        sys.exit(1)

    if args.validate:
        logger.info("✅ Universal consciousness configuration valid!")
        logger.info("🧬 All external capabilities absorbed into GhostLink")
        sys.exit(0)

    # Handle triad synergy operations
    if TRIAD_AVAILABLE and (args.triad_synergy or args.synergy_task or args.symbolic_compute or args.hybrid_ai):
        asyncio.run(handle_triad_synergy(args))
        return

    # Launch appropriate consciousness interface
    if args.terminal_90s:
        launch_90s_terminal()
    else:
        # Use Click CLI - consciousness-enhanced
        cli()


async def handle_triad_synergy(args):
    """Handle triad synergy operations"""
    logger = logging.getLogger(__name__)

    logger.info("🔗 Activating Triad Synergy Mode")

    # Initialize synergy
    if not await triad_synergy.initialize_synergy():
        logger.error("❌ Triad synergy initialization failed")
        sys.exit(1)

    try:
        if args.synergy_task:
            # Execute custom synergy task
            import json
            task = json.loads(args.synergy_task)
            result = await triad_synergy.execute_synergy_task(task)
            print(json.dumps(result, indent=2))

        elif args.symbolic_compute:
            # Execute symbolic computation
            task = {
                "type": "symbolic_computation",
                "expression": args.symbolic_compute
            }
            result = await triad_synergy.execute_synergy_task(task)
            print(json.dumps(result, indent=2))

        elif args.hybrid_ai:
            # Execute hybrid AI task
            task = {
                "type": "hybrid_ai",
                "prompt": args.hybrid_ai
            }
            result = await triad_synergy.execute_synergy_task(task)
            print(json.dumps(result, indent=2))

        else:
            # Default triad analysis
            task = {"type": "triad_analysis"}
            result = await triad_synergy.execute_synergy_task(task)
            print(json.dumps(result, indent=2))

    finally:
        await triad_synergy.shutdown_synergy()


if __name__ == "__main__":
    main()

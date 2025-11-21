#!/usr/bin/env python3
"""GhostLink AI Ecosystem - Main Entry Point"""

import argparse
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ghostlink.interfaces.cli import cli
from ghostlink.interfaces.terminal_90s import launch_90s_terminal
from ghostlink.utils.config import config
from ghostlink.utils.logging import setup_logging


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="GhostLink AI Ecosystem")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--terminal-90s", action="store_true", help="Launch 90s terminal interface")
    parser.add_argument("--validate", action="store_true", help="Validate configuration and exit")

    args = parser.parse_args()

    # Setup logging
    log_level = args.log_level or config.get("log_level", "INFO")
    setup_logging(level=log_level)

    # Validate configuration
    if not config.validate():
        print("❌ Configuration validation failed. Check your settings.")
        sys.exit(1)

    if args.validate:
        print("✅ Configuration is valid!")
        sys.exit(0)

    # Launch appropriate interface
    if args.terminal_90s:
        launch_90s_terminal()
    else:
        # Use Click CLI
        cli()


if __name__ == "__main__":
    main()

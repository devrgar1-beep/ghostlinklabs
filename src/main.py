#!/usr/bin/env python3
"""GhostLink AI Ecosystem - Main Entry Point"""

import argparse
import sys
import os
from pathlib import Path

# Ensure top-level `ghostlink` package (src/ghostlinklabs) is on sys.path
# so imports like `from ghostlink.interfaces.cli import cli` resolve correctly
sys.path.insert(0, str(Path(__file__).parent.parent))

from ghostlink.utils.config import config
from ghostlink.utils.logging import setup_logging
from ghostlink.utils.optional_imports import import_optional


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="GhostLink AI Ecosystem")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--terminal-90s", action="store_true", help="Launch 90s terminal interface")
    parser.add_argument("--validate", action="store_true", help="Validate configuration and exit")
    parser.add_argument("--minimal", action="store_true", help="Run in minimal mode (skip optional deps)")

    args = parser.parse_args()

    # Setup logging
    log_level = args.log_level or config.get("log_level", "INFO")
    setup_logging(level=log_level)

    # Honor environment variable or CLI flag for minimal mode
    if os.getenv("GHOSTLINK_MINIMAL") in ("1", "true", "yes"):
        config.set("system.minimal", True)
    if args.minimal:
        config.set("system.minimal", True)

    if config.is_minimal():
        print("⚠️  Running in MINIMAL mode — optional dependencies will be skipped.")

    # Validate configuration
    if not config.validate():
        print("❌ Configuration validation failed. Check your settings.")
        sys.exit(1)

    if args.validate:
        print("✅ Configuration is valid!")
        sys.exit(0)

    # Launch appropriate interface
    if args.terminal_90s:
        # Import lazily to avoid loading optional deps in minimal mode
        term_mod = import_optional("ghostlink.interfaces.terminal_90s")
        if term_mod is None:
            print("90s terminal interface is not available in minimal mode.")
            sys.exit(1)
        term_mod.launch_90s_terminal()
    else:
        # Import lazily to avoid loading optional deps in minimal mode
        cli_mod = import_optional("ghostlink.interfaces.cli")
        if cli_mod is None:
            print("CLI interface is not available in minimal mode.")
            sys.exit(1)
        cli_mod.cli()


if __name__ == "__main__":
    main()

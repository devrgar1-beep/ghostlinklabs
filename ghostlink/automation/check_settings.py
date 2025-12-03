#!/usr/bin/env python3
"""CLI tool to check and display GhostLink automation settings.

Usage:
    python -m ghostlink.automation.check_settings
"""
from __future__ import annotations

from ..config import config
from . import policy


def print_setting(name: str, value: bool | str, description: str) -> None:
    """Print a formatted setting line."""
    value_str = str(value)
    if isinstance(value, bool):
        value_str = "✓ ENABLED" if value else "✗ DISABLED"
        color = "\033[92m" if value else "\033[91m"
        reset = "\033[0m"
    else:
        color = "\033[94m"
        reset = "\033[0m"
    
    print(f"  {name:20} {color}{value_str:15}{reset} {description}")


def main() -> None:
    """Display current automation settings."""
    print()
    print("=" * 80)
    print("GhostLink Automation Settings")
    print("=" * 80)
    print()
    
    print("Core Settings:")
    print("-" * 80)
    print_setting(
        "AUTOMATE_ALL",
        policy.automate_all(),
        "Components run autonomously without manual confirmation"
    )
    print_setting(
        "AUTO_APPROVE",
        policy.auto_approve(),
        "Actions are automatically approved"
    )
    print_setting(
        "EXPERIMENTAL_MODE",
        policy.experimental_level(),
        f"Experimental features ({policy.experimental_level()})"
    )
    print()
    
    print("Additional Config:")
    print("-" * 80)
    print_setting(
        "DEBUG",
        config.DEBUG,
        "Debug mode enabled"
    )
    db_url = config.DATABASE_URL.split("///")[-1] if "///" in config.DATABASE_URL else "configured"
    print(f"  {'DATABASE_URL':20} {db_url:15} Database location")
    print()
    
    print("Environment Variables:")
    print("-" * 80)
    print("  Set these in your .env file or environment to change settings:")
    print()
    print("    export AUTOMATE_ALL=false          # Disable automation")
    print("    export AUTO_APPROVE=false          # Require manual approval")
    print("    export EXPERIMENTAL_MODE=off       # Disable experimental features")
    print("    export DEBUG=true                  # Enable debug mode")
    print()
    
    # Determine environment profile
    if policy.automate_all() and policy.auto_approve() and policy.experimental_level() == "full":
        profile = "DEVELOPMENT (fully automated)"
        color = "\033[93m"
    elif not policy.automate_all() and not policy.auto_approve() and policy.experimental_level() == "off":
        profile = "PRODUCTION (conservative)"
        color = "\033[92m"
    else:
        profile = "CUSTOM (mixed settings)"
        color = "\033[94m"
    
    reset = "\033[0m"
    print(f"Current Profile: {color}{profile}{reset}")
    print()
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()

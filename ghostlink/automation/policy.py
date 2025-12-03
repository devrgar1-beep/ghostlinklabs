"""Policy helpers for automation and experimental features.

Components should import these helpers to decide whether to run autonomously
or require manual confirmation.
"""
from __future__ import annotations

from ..config import config


def automate_all() -> bool:
    """Return True when the application is allowed to automate operations."""
    return bool(getattr(config, "AUTOMATE_ALL", False))


def auto_approve() -> bool:
    """Return True when actions should be auto-approved by default."""
    return bool(getattr(config, "AUTO_APPROVE", False))


def experimental_level() -> str:
    """Return the experimental level string: 'off', 'partial', or 'full'."""
    return getattr(config, "EXPERIMENTAL_MODE", "off")


def experimental_enabled() -> bool:
    """True when experimental features are enabled (any level except 'off')."""
    return experimental_level() != "off"

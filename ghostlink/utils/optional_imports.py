"""Helpers for optional (non-critical) imports.

Call import_optional("rich") to attempt to import and get None if missing.
This centralizes warnings and keeps runtime safe when optional deps are absent.
"""
from importlib import import_module
from typing import Any, Optional
from loguru import logger


def import_optional(module_name: str) -> Optional[Any]:
    """Try to import a module and return it or None without raising.

    Logs a single warning the first time an optional module is missing.
    """
    try:
        return import_module(module_name)
    except Exception as exc:  # pragma: no cover - import failure handling
        logger.debug(f"Optional module '{module_name}' not available: {exc}")
        return None

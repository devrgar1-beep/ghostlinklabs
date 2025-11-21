from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

KERNEL_PATH = Path(__file__).resolve().parents[2] / "kernel" / "gl-kernel.max.json"


NEWLINE = chr(10)


@lru_cache(maxsize=1)
def _kernel_payload() -> Dict[str, Any]:
    with KERNEL_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_tools() -> List[str]:
    """Return the ordered list of tool primitives registered by the kernel."""
    return list(_kernel_payload()["tools"])


def describe_tool(name: str) -> Dict[str, Any]:
    """Return metadata for the requested tool."""
    kernel = _kernel_payload()
    pipelines = {pipe["name"]: pipe for pipe in kernel["pipelines"]}
    info = pipelines.get(name)
    if info is None:
        return {
            "name": name,
            "action": None,
            "multipaths": [],
        }
    return {
        "name": name,
        "action": info["action"],
        "multipaths": list(info["multipaths"]),
    }


def tool_manifest() -> Dict[str, Dict[str, Any]]:
    """Return the tool manifest keyed by tool name."""
    return {tool: describe_tool(tool) for tool in list_tools()}


# Import translator functionality
_TRANSLATOR_AVAILABLE = False
try:
    from ghostlink.translator import (
        ComputationLanguageTranslator,
        detect_language,
        get_supported_languages,
        register_translator_opcodes,
        translate_code,
    )

    _TRANSLATOR_AVAILABLE = True
except ImportError:
    # Define no-op versions if translator is not available
    def detect_language(*args, **kwargs):
        raise ImportError("Translator module is not available")

    def translate_code(*args, **kwargs):
        raise ImportError("Translator module is not available")

    def get_supported_languages(*args, **kwargs):
        raise ImportError("Translator module is not available")

    def register_translator_opcodes(*args, **kwargs):
        raise ImportError("Translator module is not available")


def get_translator():
    """Get instance of ComputationLanguageTranslator if available."""
    if _TRANSLATOR_AVAILABLE:
        return ComputationLanguageTranslator()
    return None


# Build __all__ list conditionally
__all__ = [
    "list_tools",
    "describe_tool",
    "tool_manifest",
    "get_translator",
]

if _TRANSLATOR_AVAILABLE:
    __all__.extend(
        [
            "detect_language",
            "translate_code",
            "get_supported_languages",
            "register_translator_opcodes",
        ]
    )

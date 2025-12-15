"""Performance and openness configuration utilities.

This module centralizes environment-driven runtime tuning profiles so the
system can switch between conservative, low-latency and open/integration
profiles without scattering literals throughout code.
"""
from __future__ import annotations

import os
import multiprocessing
from typing import Dict, Any


def _env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.lower() in ("1", "true", "yes", "on")


PROFILE = os.getenv("GHOSTLINK_PERF_PROFILE", "conservative").lower()
OPEN_NETWORK = _env_bool("GHOSTLINK_OPEN_NETWORK", False)


def is_low_latency() -> bool:
    return PROFILE in ("low-latency", "low_latency", "fast")


def is_maximized() -> bool:
    """Return True when profile selects an aggressive / turbo / maximized mode."""
    return PROFILE in ("maximized", "turbo", "turbo-mode")


def is_open() -> bool:
    return PROFILE in ("open", "integration") or OPEN_NETWORK


def cpu_count() -> int:
    try:
        return multiprocessing.cpu_count()
    except Exception:
        return 4


def request_timeout_seconds() -> int:
    """Return an aggressive (lower) request timeout when in low-latency mode."""
    if is_maximized():
        # extremely short timeouts for maximized mode (edge: 0.5s)
        return int(float(os.getenv("GHOSTLINK_REQUEST_TIMEOUT", "0.5")))
    if is_low_latency():
        return int(os.getenv("GHOSTLINK_REQUEST_TIMEOUT", "2"))
    return int(os.getenv("GHOSTLINK_REQUEST_TIMEOUT", "10"))


def max_workers() -> int:
    """Return a higher worker target for low-latency / open profiles."""
    base = cpu_count()
    if is_maximized():
        # cap aggressively high but sane for most systems
        return int(os.getenv("GHOSTLINK_MAX_WORKERS", str(min(1024, base * 8))))
    if is_low_latency() or is_open():
        return int(os.getenv("GHOSTLINK_MAX_WORKERS", str(min(128, base * 4))))
    return int(os.getenv("GHOSTLINK_MAX_WORKERS", str(min(32, base + 4))))


def sandbox_overrides() -> Dict[str, Any]:
    """Return sandbox policy overrides based on profile.

    Keys mirror SandboxPolicy attributes such as max_memory_mb, max_cpu_percent,
    max_network_connections, blocked_paths, time_limit_seconds, and max_processes.
    """
    if is_open():
        return {
            "max_memory_mb": int(os.getenv("GHOSTLINK_SANDBOX_MAX_MEMORY_MB", "1024")),
            "max_cpu_percent": int(os.getenv("GHOSTLINK_SANDBOX_MAX_CPU_PCT", "90")),
            "max_disk_mb": int(os.getenv("GHOSTLINK_SANDBOX_MAX_DISK_MB", "1024")),
            "max_processes": int(os.getenv("GHOSTLINK_SANDBOX_MAX_PROCS", "256")),
            "max_network_connections": int(os.getenv("GHOSTLINK_SANDBOX_MAX_NET", "100")),
            "blocked_paths": [] if _env_bool("GHOSTLINK_SANDBOX_ALLOW_ALL_PATHS", False) else [],
            "time_limit_seconds": int(os.getenv("GHOSTLINK_SANDBOX_TIME_LIMIT", "3600")),
        }

    if is_low_latency():
        return {
            "max_memory_mb": int(os.getenv("GHOSTLINK_SANDBOX_MAX_MEMORY_MB", "512")),
            "max_cpu_percent": int(os.getenv("GHOSTLINK_SANDBOX_MAX_CPU_PCT", "80")),
            "max_disk_mb": int(os.getenv("GHOSTLINK_SANDBOX_MAX_DISK_MB", "200")),
            "max_processes": int(os.getenv("GHOSTLINK_SANDBOX_MAX_PROCS", "64")),
            "max_network_connections": int(os.getenv("GHOSTLINK_SANDBOX_MAX_NET", "10")),
            "blocked_paths": ["/etc/shadow"] if not OPEN_NETWORK else [],
            "time_limit_seconds": int(os.getenv("GHOSTLINK_SANDBOX_TIME_LIMIT", "1800")),
        }

    # conservative defaults (existing behavior)
    return {}

"""GhostLink Network Layer.

Provides backbone networking, server linking, and mesh connectivity.
"""
from .backbone import (
    BackboneClass,
    BackboneManager,
    NetworkInterface,
    ServerNode,
    get_backbone,
    link_local_server,
)

__all__ = [
    "BackboneClass",
    "BackboneManager",
    "NetworkInterface",
    "ServerNode",
    "get_backbone",
    "link_local_server",
]

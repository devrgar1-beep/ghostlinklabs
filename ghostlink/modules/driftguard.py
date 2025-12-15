"""DriftGuard

Minimal implementation to satisfy references across upgrades and provide
heartbeat and simple drift-detection hooks.
"""

import time
import logging
from typing import Dict, Any

logger = logging.getLogger("ghostlink.driftguard")


class DriftGuard:
    def __init__(self, interval: int = 7):
        self.interval = interval
        self.last_heartbeat = time.time()
        self.state = "initialized"

    def heartbeat(self):
        self.last_heartbeat = time.time()
        logger.debug("DriftGuard heartbeat at %s", self.last_heartbeat)

    def analyze(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Basic analysis stub - check for obvious drift signs
        findings = []
        # Example: if payload has conflicting timestamps
        if payload.get("meta"):
            created = payload.get("created_at")
            updated = payload.get("meta", {}).get("updated_at")
            if created and updated and updated < created:
                findings.append({"type": "temporal_anomaly"})
        return {"findings": findings}

    def status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "last_heartbeat": self.last_heartbeat,
            "interval": self.interval,
        }


# module-level convenience
default = DriftGuard()

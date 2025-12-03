#!/usr/bin/env python3
"""Lightweight test harness for DesignClarityOS.

This harness imports DesignClarityOS, instantiates it with the workspace path,
replaces heavy subsystems with safe stubs, and prints a protocol status snapshot.
"""
import sys
from pathlib import Path

# Ensure local module path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / '..'))

try:
    from design_clarity_os import DesignClarityOS
except Exception as e:
    print(f"Import failed: {e}")
    raise

# Instantiate
protocol = DesignClarityOS(workspace_path=str(Path(__file__).resolve().parent))

# Replace heavy subsystems if present
class Stub:
    def __init__(self):
        pass
    def get_engine_status(self):
        return {'agent_types': {'compression': 2, 'expansion': 1, 'refinement': 3}, 'active_tasks': 0, 'queued_tasks': 0}
    async def optimize_model(self, name, size):
        return {'success': True, 'name': name, 'size': str(size)}

# Monkeypatch
try:
    protocol.multi_agent_engine = Stub()
    protocol.evolutionary_intelligence = Stub()
    # scheduled_evolution_manager may be present; if so, disable scheduling
    if hasattr(protocol, 'scheduled_evolution_manager'):
        protocol.scheduled_evolution_manager.monitoring_active = False
except Exception:
    pass

# Print lightweight status
status = protocol.get_protocol_status()
print('Protocol status snapshot:')
print(f"  protocol_active: {status.get('protocol_active')}")
print(f"  system_id: {status.get('system_id')}")
print(f"  protocol_version: {status.get('protocol_version')}")
print(f"  hardware_profiles: {status.get('hardware_profiles')}")
print(f"  application_profiles: {status.get('application_profiles')}")
print(f"  agent_assignments: {status.get('agent_assignments')}")
print(f"  consciousness_level: {status.get('consciousness_level')}")

print('\nTest harness completed successfully')

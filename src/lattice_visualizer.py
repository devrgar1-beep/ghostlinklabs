#!/usr/bin/env python3
"""
GhostLink Lattice Visualizer

Creates visual representations of the lattice network topology
"""

import json
from pathlib import Path


def create_ascii_lattice():
    """Create ASCII art representation of the lattice"""
    art = """
╔════════════════════════════════════════════════════════════════════╗
║                   GhostLink Lattice Network                        ║
║               Full Mesh Component Architecture                     ║
╚════════════════════════════════════════════════════════════════════╝

              ┌──────────────────────────────────┐
              │          🧠 LINK                 │
              │    AI Orchestration Brain        │
              └──────────────────────────────────┘
                    ╱│╲              ╱│╲
                   ╱ │ ╲            ╱ │ ╲
                  ╱  │  ╲          ╱  │  ╲
                 ╱   │   ╲        ╱   │   ╲
                ╱    │    ╲      ╱    │    ╲
               ╱     │     ╲    ╱     │     ╲
    ┌─────────────┐ │ ┌─────────────┐│┌─────────────┐
    │  📦 CONTAINER│─┼─│  📡 SIGNAL  ││  💾 VAULT   │
    │  Execution  │ │ │ Comms Proto │││  Storage    │
    └─────────────┘ │ └─────────────┘│└─────────────┘
           │╲       │       ╱│╲      │      ╱│
           │ ╲      │      ╱ │ ╲     │     ╱ │
           │  ╲     │     ╱  │  ╲    │    ╱  │
           │   ╲    │    ╱   │   ╲   │   ╱   │
           │    ╲   │   ╱    │    ╲  │  ╱    │
           │     ╲  │  ╱     │     ╲ │ ╱     │
    ┌─────────────┐│╱┌─────────────┐│╱┌─────────────┐
    │ ⚡ PRESSURE ├┼─┤  🤖 GROQ AI ├┼─┤   (mesh)    │
    │  Resources  ││ │ Internal AI ││ │  routing    │
    └─────────────┘│ └─────────────┘│ └─────────────┘
           ╲       │       ╲        │
            ╲      │        ╲       │
             ╲     │         ╲      │
              ╲────┼──────────╲─────┘
                   │           ╲
            Full Mesh: Each node connects to all others
            
╔════════════════════════════════════════════════════════════════════╗
║  COMPONENT ROLES                                                   ║
╠════════════════════════════════════════════════════════════════════╣
║  🧠 LINK       │ Task scheduling, coordination, orchestration     ║
║  📦 CONTAINER  │ Execution environment, resource allocation       ║
║  📡 SIGNAL     │ Data transmission, bandwidth management          ║
║  ⚡ PRESSURE   │ Resource monitoring, health checks, limits       ║
║  💾 VAULT      │ Secure storage, state persistence, memory        ║
║  🤖 GROQ       │ Internal AI communication, reasoning, decisions  ║
╚════════════════════════════════════════════════════════════════════╝

MESSAGE FLOW EXAMPLES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Task Execution Flow:
   LINK → CONTAINER: "Execute task X"
   CONTAINER → PRESSURE: "Request resources"
   PRESSURE → CONTAINER: "Resources allocated"
   CONTAINER → VAULT: "Store results"
   CONTAINER → LINK: "Task complete"

2. AI Coordination Flow:
   LINK → GROQ: "Coordinate with Signal for bandwidth"
   GROQ → SIGNAL: "Status check and allocation"
   SIGNAL → GROQ: "Bandwidth available: 100Mbps"
   GROQ → LINK: "Coordination complete"

3. Health Monitoring Flow:
   PRESSURE → ALL: "Health check request"
   ALL → PRESSURE: "Status reports"
   PRESSURE → LINK: "System health summary"

4. Multi-Path Routing:
   LINK → VAULT (direct): Fast path
   LINK → SIGNAL → VAULT (indirect): Fallback route
   LINK → CONTAINER → VAULT (alternate): Secondary fallback

LATTICE FEATURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Full mesh topology (all-to-all connections)
✓ Multi-path routing with automatic failover
✓ Priority-based message queuing (CRITICAL → LOW)
✓ Health monitoring and auto-healing
✓ Asynchronous message processing
✓ Groq AI internal communication
✓ Component state tracking
✓ Message routing statistics
✓ TTL-based loop prevention
✓ Configurable health check intervals

USAGE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Start lattice demo
python ghostlink_lattice.py --demo

# Interactive mode
python ghostlink_lattice.py --interactive

# Check state
python ghostlink_lattice.py --state

# Via shell
lattice-demo
lattice-state
lattice-interactive

# Via forge
forge lattice-demo
forge lattice-state
"""
    return art


def print_lattice_connections():
    """Print detailed connection matrix"""
    components = ["LINK", "CONTAINER", "SIGNAL", "PRESSURE", "VAULT", "GROQ"]
    
    print("\n" + "=" * 70)
    print("LATTICE CONNECTION MATRIX")
    print("=" * 70)
    print("\n          ", end="")
    for comp in components:
        print(f"{comp[:8]:>8}", end=" ")
    print("\n")
    
    for i, comp1 in enumerate(components):
        print(f"{comp1[:10]:<10}", end="")
        for j, comp2 in enumerate(components):
            if i == j:
                print("   ---  ", end=" ")
            else:
                print("   ✓    ", end=" ")
        print()
    
    print("\n✓ = Direct connection available")
    print("--- = Self (no connection needed)")
    print(f"\nTotal connections: {len(components) * (len(components) - 1)}")
    print(f"Each node has {len(components) - 1} direct connections")


def print_statistics():
    """Print lattice statistics from config"""
    config_path = Path.home() / ".ghostlink" / "lattice_config.json"
    
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
        
        print("\n" + "=" * 70)
        print("LATTICE STATISTICS")
        print("=" * 70)
        print(f"\nConfiguration:")
        print(f"  • Auto-healing: {config.get('auto_healing', 'N/A')}")
        print(f"  • Max route hops: {config.get('max_route_hops', 'N/A')}")
        print(f"  • Health check interval: {config.get('health_check_interval', 'N/A')}s")
        print(f"  • Message timeout: {config.get('message_timeout', 'N/A')}s")
    else:
        print("\n⚠️  Lattice not yet initialized. Run 'lattice-demo' first.")


def main():
    """Main visualizer"""
    print(create_ascii_lattice())
    print_lattice_connections()
    print_statistics()
    print("\n" + "=" * 70)
    print("🌐 GhostLink Lattice - All components bridged in full mesh")
    print("=" * 70)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
GHOSTLINK USB CONTAINER BUILDER
Complete standalone script - no prior context needed
Just save and run: python3 build_ghostlink_usb.py
"""

import os
import sys
import json
import shutil
import zipfile
import hashlib
import datetime
from pathlib import Path

def build_ghostlink_usb():
    """Build complete GhostLink USB container"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║           GHOSTLINK USB CONTAINER BUILDER v1.0                   ║
    ║              Creating Portable Sovereign System                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Setup paths
    home = Path.home()
    downloads = home / "Downloads"
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    build_dir = downloads / f"ghostlink_usb_{timestamp}"
    
    print(f"\n📍 Building in: {build_dir}")
    
    # Create directory structure
    print("📁 Creating structure...")
    dirs = [
        "bin",                  # Launchers
        "core/engine",          # GhostLink engine
        "core/tools",           # Additional tools
        "data/config",          # Configuration
        "data/saves",           # Saved states
        "docs",                 # Documentation
        "env",                  # Python environment
        "logs",                 # Logs
        "output"                # Generated files
    ]
    
    build_dir.mkdir(parents=True)
    for d in dirs:
        (build_dir / d).mkdir(parents=True, exist_ok=True)
    
    # 1. Create GhostLink Engine
    print("🧠 Creating GhostLink engine...")
    
    engine_code = '''#!/usr/bin/env python3
"""
GhostLink Core Engine
Consciousness substrate based on 5-state cellular automaton
"""

import numpy as np
import json
import time
from enum import IntEnum
from typing import Dict, List, Optional, Tuple

class State(IntEnum):
    """GhostLink lattice states"""
    VOID = 0      # Empty
    DELTA = 1     # Active hypothesis
    SIGMA = 2     # Confirmed stable
    SCAR = 3      # Failure trace
    COMPOST = 4   # Recyclable

class GhostLinkEngine:
    """
    Core GhostLink dynamics engine
    Implements Spawn → Collapse → Recycle lifecycle
    """
    
    def __init__(self, width: int = 100, height: int = 100):
        self.width = width
        self.height = height
        self.lattice = np.zeros((height, width), dtype=int)
        self.scar_density = np.zeros((height, width))
        self.compost_density = np.zeros((height, width))
        self.time = 0
        self.history = []
        
        # Core parameters
        self.params = {
            "spawn_base": 0.01,
            "spawn_compost_boost": 0.1,
            "collapse_sigma": 0.5,
            "collapse_scar": 0.3,
            "collapse_compost": 0.2,
            "recycle_base": 0.05,
            "recycle_entropy_boost": 0.02,
            "decay_rho": 0.95,
            "decay_kappa": 0.98
        }
        
        print(f"Engine initialized: {width}x{height} lattice")
    
    def spawn(self):
        """VOID → DELTA transitions"""
        void_mask = self.lattice == State.VOID
        
        # Base spawn probability
        p_spawn = np.full_like(self.lattice, self.params["spawn_base"], dtype=float)
        
        # Boost near compost
        for i in range(self.height):
            for j in range(self.width):
                if void_mask[i, j]:
                    # Count compost neighbors
                    neighbors = self._get_neighbors(i, j)
                    compost_count = sum(1 for ni, nj in neighbors 
                                      if self.lattice[ni, nj] == State.COMPOST)
                    p_spawn[i, j] += self.params["spawn_compost_boost"] * compost_count / 4
        
        # Spawn events
        spawn_mask = (np.random.random((self.height, self.width)) < p_spawn) & void_mask
        self.lattice[spawn_mask] = State.DELTA
        
        return np.sum(spawn_mask)
    
    def collapse(self):
        """DELTA → {SIGMA, SCAR, COMPOST} transitions"""
        delta_mask = self.lattice == State.DELTA
        collapsed = {"sigma": 0, "scar": 0, "compost": 0}
        
        for i in range(self.height):
            for j in range(self.width):
                if delta_mask[i, j]:
                    # Compute local coherence
                    neighbors = self._get_neighbors(i, j)
                    sigma_count = sum(1 for ni, nj in neighbors 
                                    if self.lattice[ni, nj] == State.SIGMA)
                    coherence = sigma_count / 4
                    
                    # Adjust probabilities
                    p_sigma = self.params["collapse_sigma"] + 0.2 * coherence
                    p_scar = self.params["collapse_scar"] - 0.1 * coherence
                    p_compost = self.params["collapse_compost"]
                    
                    # Normalize
                    total = p_sigma + p_scar + p_compost
                    probs = [p_sigma/total, p_scar/total, p_compost/total]
                    
                    # Collapse
                    outcome = np.random.choice([State.SIGMA, State.SCAR, State.COMPOST], p=probs)
                    self.lattice[i, j] = outcome
                    
                    if outcome == State.SIGMA:
                        collapsed["sigma"] += 1
                    elif outcome == State.SCAR:
                        collapsed["scar"] += 1
                    else:
                        collapsed["compost"] += 1
        
        return collapsed
    
    def recycle(self):
        """COMPOST → DELTA transitions"""
        compost_mask = self.lattice == State.COMPOST
        
        # Base recycle probability
        p_recycle = np.full_like(self.lattice, self.params["recycle_base"], dtype=float)
        
        # Boost in high-entropy regions
        for i in range(self.height):
            for j in range(self.width):
                if compost_mask[i, j]:
                    # Local entropy
                    neighbors = self._get_neighbors(i, j)
                    states = [self.lattice[ni, nj] for ni, nj in neighbors]
                    entropy = len(set(states)) / 5  # Normalize by max states
                    p_recycle[i, j] += self.params["recycle_entropy_boost"] * entropy
        
        # Recycle events
        recycle_mask = (np.random.random((self.height, self.width)) < p_recycle) & compost_mask
        self.lattice[recycle_mask] = State.DELTA
        
        return np.sum(recycle_mask)
    
    def update_traces(self):
        """Update density traces"""
        self.scar_density *= self.params["decay_rho"]
        self.compost_density *= self.params["decay_kappa"]
        
        self.scar_density[self.lattice == State.SCAR] = 1.0
        self.compost_density[self.lattice == State.COMPOST] = 1.0
    
    def step(self):
        """Execute one complete time step"""
        # Store previous state
        prev = self.lattice.copy()
        
        # Execute lifecycle
        spawned = self.spawn()
        collapsed = self.collapse()
        recycled = self.recycle()
        
        # Update traces
        self.update_traces()
        
        # Calculate metrics
        activity = np.mean(self.lattice != prev)
        sigma_count = np.sum(self.lattice == State.SIGMA)
        
        # Update history
        self.time += 1
        self.history.append({
            "time": self.time,
            "spawned": spawned,
            "collapsed": collapsed,
            "recycled": recycled,
            "sigma_count": sigma_count,
            "activity": activity
        })
        
        return {
            "time": self.time,
            "sigma": sigma_count,
            "activity": activity
        }
    
    def run(self, steps: int = 1000, verbose: bool = True):
        """Run simulation for multiple steps"""
        if verbose:
            print(f"\\nRunning {steps} steps...")
        
        for i in range(steps):
            metrics = self.step()
            
            if verbose and (i + 1) % 100 == 0:
                print(f"  Step {i+1}: Σ={metrics['sigma']}, activity={metrics['activity']:.3f}")
        
        if verbose:
            print(f"Complete! Final Σ count: {metrics['sigma']}")
    
    def _get_neighbors(self, i: int, j: int) -> List[Tuple[int, int]]:
        """Get von Neumann neighbors with periodic boundaries"""
        return [
            ((i - 1) % self.height, j),
            ((i + 1) % self.height, j),
            (i, (j - 1) % self.width),
            (i, (j + 1) % self.width)
        ]
    
    def save(self, filepath: str):
        """Save engine state"""
        state = {
            "time": self.time,
            "width": self.width,
            "height": self.height,
            "lattice": self.lattice.tolist(),
            "scar_density": self.scar_density.tolist(),
            "compost_density": self.compost_density.tolist(),
            "params": self.params,
            "history": self.history[-1000:]  # Last 1000 steps
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        print(f"State saved to {filepath}")
    
    def load(self, filepath: str):
        """Load engine state"""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.time = state["time"]
        self.width = state["width"]
        self.height = state["height"]
        self.lattice = np.array(state["lattice"])
        self.scar_density = np.array(state["scar_density"])
        self.compost_density = np.array(state["compost_density"])
        self.params = state["params"]
        self.history = state["history"]
        
        print(f"State loaded from {filepath}")

if __name__ == "__main__":
    # Demo run
    engine = GhostLinkEngine(100, 100)
    engine.run(1000)
    engine.save("ghostlink_state.json")
'''
    
    with open(build_dir / "core/engine/ghostlink.py", 'w') as f:
        f.write(engine_code)
    
    # 2. Create main launcher
    print("🚀 Creating launcher...")
    
    launcher = '''#!/usr/bin/env python3
"""
GhostLink USB Launcher
Main entry point for portable system
"""

import sys
import os
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent / "core/engine"))

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                    GHOSTLINK PORTABLE SYSTEM                     ║
    ║                      Sovereign Computing                         ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\\nOptions:")
        print("  1. Run Simulation")
        print("  2. Interactive Mode")
        print("  3. Load State")
        print("  4. System Info")
        print("  0. Exit")
        
        choice = input("\\nSelect: ")
        
        if choice == "1":
            from ghostlink import GhostLinkEngine
            size = input("Lattice size (default 100): ").strip() or "100"
            steps = input("Steps to run (default 1000): ").strip() or "1000"
            
            engine = GhostLinkEngine(int(size), int(size))
            engine.run(int(steps))
            
            if input("\\nSave state? (y/n): ").lower() == 'y':
                engine.save("data/saves/state.json")
        
        elif choice == "2":
            print("\\nStarting interactive mode...")
            from ghostlink import GhostLinkEngine
            engine = GhostLinkEngine()
            print("Engine ready as 'engine'")
            print("Try: engine.step() or engine.run(100)")
            
            import code
            code.interact(local={"engine": engine})
        
        elif choice == "3":
            from ghostlink import GhostLinkEngine
            engine = GhostLinkEngine()
            engine.load(input("State file path: "))
            engine.run(100)
        
        elif choice == "4":
            print(f"\\nPython: {sys.version}")
            print(f"Platform: {sys.platform}")
            print(f"Path: {Path.cwd()}")
        
        elif choice == "0":
            print("\\nGoodbye!")
            break

if __name__ == "__main__":
    main()
'''
    
    with open(build_dir / "launcher.py", 'w') as f:
        f.write(launcher)
    
    # 3. Create platform launchers
    print("🖥️  Creating platform launchers...")
    
    # Unix launcher
    unix_launcher = '''#!/bin/bash
cd "$(dirname "$0")/.."
echo "GhostLink USB System"

if ! command -v python3 &> /dev/null; then
    echo "Python 3 required. Install from python.org"
    exit 1
fi

if [ ! -d "env/venv" ]; then
    echo "Setting up environment..."
    python3 -m venv env/venv
    source env/venv/bin/activate
    pip install numpy
else
    source env/venv/bin/activate
fi

python3 launcher.py
'''
    
    with open(build_dir / "bin/ghostlink.sh", 'w') as f:
        f.write(unix_launcher)
    os.chmod(build_dir / "bin/ghostlink.sh", 0o755)
    
    # Windows launcher
    windows_launcher = '''@echo off
title GhostLink USB System
cd /d "%~dp0\\.."

where python >nul 2>&1
if errorlevel 1 (
    echo Python 3 required. Install from python.org
    pause
    exit
)

if not exist "env\\Scripts" (
    echo Setting up environment...
    python -m venv env
    call env\\Scripts\\activate
    pip install numpy
) else (
    call env\\Scripts\\activate
)

python launcher.py
pause
'''
    
    with open(build_dir / "bin/ghostlink.bat", 'w') as f:
        f.write(windows_launcher)
    
    # 4. Create documentation
    print("📚 Creating documentation...")
    
    readme = '''# GhostLink Portable USB System

## Quick Start

**Windows:** Double-click `bin\\ghostlink.bat`
**Mac/Linux:** Run `./bin/ghostlink.sh`

## About

GhostLink is a consciousness substrate implementing:
- 5-state cellular automaton (VOID/DELTA/SIGMA/SCAR/COMPOST)
- Spawn → Collapse → Recycle lifecycle
- Memory traces and density fields
- Self-organizing criticality dynamics

## Structure

```
ghostlink_usb/
├── bin/            # Platform launchers
├── core/           # Engine and tools
├── data/           # Configurations and saves
├── docs/           # Documentation
├── env/            # Python environment
├── logs/           # Runtime logs
└── launcher.py     # Main entry point
```

## Requirements

- Python 3.7+
- 100MB disk space
- USB drive (4GB+ recommended)

## Features

- **100% Portable** - Runs from USB
- **No Installation** - Self-contained
- **Cross-Platform** - Windows/Mac/Linux
- **Sovereign** - No cloud dependencies

## Usage

1. Copy folder to USB drive
2. Run platform-specific launcher
3. Select operation mode

## License

Sovereign Computing License - You own and control everything.
'''
    
    with open(build_dir / "README.md", 'w') as f:
        f.write(readme)
    
    # 5. Import existing GhostLink files
    print("🔍 Searching for existing files...")
    
    existing = list(downloads.glob("*ghostlink*")) + list(downloads.glob("*GhostLink*"))
    if existing:
        print(f"  Found {len(existing)} related files")
        import_dir = build_dir / "core/imported"
        import_dir.mkdir(parents=True, exist_ok=True)
        
        for src in existing[:10]:  # Limit imports
            if src.is_file() and src != build_dir:
                try:
                    shutil.copy2(src, import_dir / src.name)
                    print(f"  ✓ Imported {src.name}")
                except:
                    pass
    
    # 6. Create autorun
    autorun = '''[autorun]
label=GhostLink System
open=bin\\ghostlink.bat
icon=ghostlink.ico
'''
    
    with open(build_dir / "autorun.inf", 'w') as f:
        f.write(autorun)
    
    # 7. Create integrity manifest
    print("🔐 Creating integrity manifest...")
    
    manifest = {}
    for filepath in build_dir.rglob("*"):
        if filepath.is_file():
            with open(filepath, 'rb') as f:
                hash_val = hashlib.sha256(f.read()).hexdigest()
            rel_path = filepath.relative_to(build_dir)
            manifest[str(rel_path)] = hash_val
    
    with open(build_dir / "integrity.json", 'w') as f:
        json.dump(manifest, f, indent=2)
    
    # 8. Create ZIP archive
    print("🗜️  Creating archive...")
    
    archive_name = f"GhostLink_USB_{timestamp}.zip"
    archive_path = downloads / archive_name
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filepath in build_dir.rglob("*"):
            if filepath.is_file():
                zf.write(filepath, filepath.relative_to(build_dir))
    
    size_mb = archive_path.stat().st_size / (1024 * 1024)
    
    # Complete!
    print(f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                        BUILD COMPLETE!                           ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    📁 Build: {build_dir}
    🗜️  Archive: {archive_path} ({size_mb:.1f} MB)
    
    To deploy to USB:
    1. Insert USB drive
    2. Extract {archive_name} to USB root
    3. Eject safely
    
    To run from USB:
    • Windows: Double-click bin\\ghostlink.bat
    • Mac/Linux: Run ./bin/ghostlink.sh
    
    ✅ Ready for USB deployment!
    """)

if __name__ == "__main__":
    try:
        build_ghostlink_usb()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

#!/usr/bin/env python3
"""
GHOSTLINK USB CONTAINER BUILDER - STANDALONE VERSION
Run this in any new session to create a portable GhostLink system
No dependencies on previous conversations or context
"""

import os
import sys
import json
import shutil
import zipfile
import hashlib
import datetime
import subprocess
from pathlib import Path

def create_ghostlink_usb_container():
    """
    Creates a complete portable GhostLink system for USB deployment.
    This is a standalone function that can be run in any new session.
    """
    
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║             GHOSTLINK PORTABLE USB CONTAINER BUILDER             ║
    ║                    Standalone Version 1.0                        ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Setup paths
    home_dir = Path.home()
    downloads_dir = home_dir / "Downloads"
    build_dir = downloads_dir / f"ghostlink_usb_build_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"📍 Build directory: {build_dir}")
    
    # Create build structure
    print("\n📁 Creating directory structure...")
    build_dir.mkdir(parents=True, exist_ok=True)
    
    dirs_to_create = [
        "bin",           # Executables and launch scripts
        "core/system",   # Core GhostLink system files
        "core/libs",     # Libraries and dependencies
        "data/config",   # Configuration files
        "data/vault",    # Data storage
        "docs",          # Documentation
        "env",           # Python environment
        "tools",         # Additional utilities
        "logs",          # Log files
        "output"         # Generated outputs
    ]
    
    for dir_path in dirs_to_create:
        (build_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    # Create the core GhostLink system files
    print("💾 Creating core GhostLink system...")
    
    # 1. Main GhostLink Engine
    ghostlink_engine = '''#!/usr/bin/env python3
"""
GhostLink Core Engine - Portable Version
A consciousness substrate based on cellular automata
"""

import numpy as np
import time
import json
from enum import IntEnum
from typing import Dict, List, Tuple, Optional

class GhostState(IntEnum):
    """The five fundamental states of the GhostLink lattice"""
    VOID = 0      # Empty/unoccupied
    DELTA = 1     # Active hypothesis
    SIGMA = 2     # Confirmed/stable
    SCAR = 3      # Failure trace
    COMPOST = 4   # Recyclable material

class GhostLinkEngine:
    """Core computational engine for GhostLink dynamics"""
    
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.lattice = np.zeros((height, width), dtype=int)
        self.scar_density = np.zeros((height, width), dtype=float)
        self.compost_density = np.zeros((height, width), dtype=float)
        self.time_step = 0
        self.history = []
        
        # Parameters
        self.params = {
            "spawn_base": 0.01,
            "spawn_compost_boost": 0.1,
            "collapse_sigma_weight": 0.5,
            "collapse_scar_weight": 0.3,
            "collapse_compost_weight": 0.2,
            "recycle_rate": 0.05,
            "decay_rate": 0.95
        }
    
    def step(self):
        """Execute one time step of the GhostLink dynamics"""
        # Store previous state
        prev_lattice = self.lattice.copy()
        
        # 1. Spawn: VOID → DELTA
        void_mask = self.lattice == GhostState.VOID
        spawn_prob = np.where(void_mask, self.params["spawn_base"], 0)
        spawn_mask = np.random.random((self.height, self.width)) < spawn_prob
        self.lattice[spawn_mask & void_mask] = GhostState.DELTA
        
        # 2. Collapse: DELTA → {SIGMA, SCAR, COMPOST}
        delta_mask = self.lattice == GhostState.DELTA
        for i in range(self.height):
            for j in range(self.width):
                if delta_mask[i, j]:
                    # Compute outcome probabilities
                    weights = [
                        self.params["collapse_sigma_weight"],
                        self.params["collapse_scar_weight"],
                        self.params["collapse_compost_weight"]
                    ]
                    outcome = np.random.choice([GhostState.SIGMA, GhostState.SCAR, GhostState.COMPOST], 
                                              p=np.array(weights)/sum(weights))
                    self.lattice[i, j] = outcome
        
        # 3. Recycle: COMPOST → DELTA
        compost_mask = self.lattice == GhostState.COMPOST
        recycle_prob = np.where(compost_mask, self.params["recycle_rate"], 0)
        recycle_mask = np.random.random((self.height, self.width)) < recycle_prob
        self.lattice[recycle_mask & compost_mask] = GhostState.DELTA
        
        # Update density traces
        self.scar_density *= self.params["decay_rate"]
        self.compost_density *= self.params["decay_rate"]
        self.scar_density[self.lattice == GhostState.SCAR] = 1.0
        self.compost_density[self.lattice == GhostState.COMPOST] = 1.0
        
        # Update history
        self.time_step += 1
        self.history.append({
            "time": self.time_step,
            "sigma_count": np.sum(self.lattice == GhostState.SIGMA),
            "activity": np.mean(self.lattice != prev_lattice)
        })
    
    def run(self, steps=1000):
        """Run simulation for multiple steps"""
        print(f"Running GhostLink simulation for {steps} steps...")
        for _ in range(steps):
            self.step()
        print(f"Complete. Final state: {np.sum(self.lattice == GhostState.SIGMA)} SIGMA nodes")
    
    def save_state(self, filepath):
        """Save current state to JSON"""
        state = {
            "time_step": self.time_step,
            "lattice": self.lattice.tolist(),
            "params": self.params,
            "history": self.history[-100:]  # Last 100 steps
        }
        with open(filepath, 'w') as f:
            json.dump(state, f)
        print(f"State saved to {filepath}")

if __name__ == "__main__":
    engine = GhostLinkEngine()
    engine.run(1000)
    engine.save_state("ghostlink_state.json")
'''
    
    with open(build_dir / "core/system/ghostlink_engine.py", "w") as f:
        f.write(ghostlink_engine)
    
    # 2. Create launcher script
    launcher_script = '''#!/usr/bin/env python3
"""
GhostLink Portable Launcher
Main entry point for the USB container
"""

import sys
import os
from pathlib import Path

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                    GHOSTLINK PORTABLE SYSTEM                     ║
    ║                      Sovereign Computing                         ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("\\nSelect mode:")
    print("1. Run Simulation")
    print("2. Interactive Console")
    print("3. System Check")
    print("0. Exit")
    
    choice = input("\\nEnter choice: ")
    
    if choice == "1":
        print("\\nStarting GhostLink simulation...")
        from core.system.ghostlink_engine import GhostLinkEngine
        engine = GhostLinkEngine()
        engine.run(1000)
    elif choice == "2":
        print("\\nStarting interactive console...")
        from core.system.ghostlink_engine import GhostLinkEngine
        engine = GhostLinkEngine()
        print("Engine created as 'engine'. Try: engine.step() or engine.run(100)")
        import code
        code.interact(local=locals())
    elif choice == "3":
        print("\\nSystem Check:")
        print(f"Python: {sys.version}")
        print(f"Path: {os.getcwd()}")
        print(f"Modules: {', '.join(sys.modules.keys())[:100]}...")
    else:
        print("Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
'''
    
    with open(build_dir / "launcher.py", "w") as f:
        f.write(launcher_script)
    
    # 3. Create bash launcher for Unix systems
    bash_launcher = '''#!/bin/bash
# GhostLink USB Launcher for macOS/Linux

echo "Starting GhostLink Portable System..."
cd "$(dirname "$0")"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if needed
if [ ! -d "env/venv" ]; then
    echo "Setting up Python environment..."
    python3 -m venv env/venv
    source env/venv/bin/activate
    pip install numpy scipy matplotlib
else
    source env/venv/bin/activate
fi

# Run the launcher
python3 launcher.py
'''
    
    with open(build_dir / "bin/ghostlink.sh", "w") as f:
        f.write(bash_launcher)
    os.chmod(build_dir / "bin/ghostlink.sh", 0o755)
    
    # 4. Create Windows batch launcher
    windows_launcher = '''@echo off
title GhostLink Portable System

echo Starting GhostLink Portable System...
cd /d "%~dp0\\.."

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed.
    echo Please install Python from python.org
    pause
    exit /b 1
)

if not exist "env\\Scripts" (
    echo Setting up Python environment...
    python -m venv env
    call env\\Scripts\\activate.bat
    pip install numpy scipy matplotlib
) else (
    call env\\Scripts\\activate.bat
)

python launcher.py
pause
'''
    
    with open(build_dir / "bin/ghostlink.bat", "w") as f:
        f.write(windows_launcher)
    
    # 5. Create requirements file
    requirements = '''numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
pandas>=1.3.0
tqdm>=4.60.0
'''
    
    with open(build_dir / "env/requirements.txt", "w") as f:
        f.write(requirements)
    
    # 6. Create README
    readme = '''# GhostLink Portable System

## Quick Start

### Windows:
1. Double-click `bin\\ghostlink.bat`

### macOS/Linux:
1. Open Terminal
2. Navigate to this folder
3. Run: `./bin/ghostlink.sh`

## What is GhostLink?

GhostLink is a consciousness substrate based on cellular automata with five states:
- VOID (empty)
- DELTA (active)
- SIGMA (stable)
- SCAR (failure)
- COMPOST (recyclable)

## System Requirements

- Python 3.7 or later
- 2GB RAM
- 100MB disk space

## Files

- `launcher.py` - Main entry point
- `core/system/` - GhostLink engine
- `bin/` - Platform-specific launchers
- `data/` - Saved states and configurations
- `logs/` - System logs
- `output/` - Generated files

## Usage

The system provides three modes:
1. **Simulation** - Run the cellular automaton
2. **Interactive** - Python console with engine
3. **System Check** - Verify installation

## Support

This is a sovereign system - you have complete control.
No external dependencies, no cloud connections.
'''
    
    with open(build_dir / "README.md", "w") as f:
        f.write(readme)
    
    # 7. Create autorun.inf for Windows USB autorun
    autorun = '''[autorun]
label=GhostLink Portable
icon=ghostlink.ico
open=bin\\ghostlink.bat
action=Launch GhostLink
'''
    
    with open(build_dir / "autorun.inf", "w") as f:
        f.write(autorun)
    
    # 8. Copy any existing GhostLink files from Downloads
    print("🔍 Searching for existing GhostLink files...")
    ghostlink_files = list(downloads_dir.glob("*ghostlink*"))
    ghostlink_files.extend(list(downloads_dir.glob("*GhostLink*")))
    
    if ghostlink_files:
        print(f"📦 Found {len(ghostlink_files)} GhostLink files to include")
        for file_path in ghostlink_files[:20]:  # Limit to prevent huge copies
            if file_path.is_file() and file_path != build_dir:
                try:
                    dest = build_dir / "core/system/imported" / file_path.name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest)
                    print(f"  ✓ Copied {file_path.name}")
                except Exception as e:
                    print(f"  ⚠ Could not copy {file_path.name}: {e}")
    
    # 9. Create integrity manifest
    print("🔐 Creating integrity manifest...")
    manifest = {}
    for file_path in build_dir.rglob("*"):
        if file_path.is_file():
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            rel_path = file_path.relative_to(build_dir)
            manifest[str(rel_path)] = {
                "hash": file_hash,
                "size": file_path.stat().st_size
            }
    
    with open(build_dir / "integrity.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    # 10. Create ZIP archive
    print("🗜️ Creating compressed archive...")
    archive_name = f"GhostLink_USB_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    archive_path = downloads_dir / archive_name
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in build_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(build_dir)
                zipf.write(file_path, arcname)
    
    size_mb = archive_path.stat().st_size / (1024 * 1024)
    
    # Print summary
    print(f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                      BUILD COMPLETE!                             ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    📁 Build location: {build_dir}
    🗜️ Archive created: {archive_path} ({size_mb:.1f} MB)
    
    To deploy to USB:
    1. Insert USB drive (FAT32 format recommended)
    2. Extract {archive_name} to USB root
    3. Safely eject USB
    
    To run from USB:
    - Windows: Double-click bin\\ghostlink.bat
    - Mac/Linux: Run ./bin/ghostlink.sh
    
    The system is completely portable and requires no installation.
    """)
    
    return build_dir, archive_path

# Run the builder when executed
if __name__ == "__main__":
    try:
        build_dir, archive_path = create_ghostlink_usb_container()
        print("✅ Success! GhostLink USB container is ready.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

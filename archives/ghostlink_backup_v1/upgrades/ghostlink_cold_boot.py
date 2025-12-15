#!/usr/bin/env python3
"""
GhostLink Cold Boot Builder
Single-source bootstrap for complete GhostLink system
Run: python3 ghostlink_cold_boot.py
"""

import os
import json
import hashlib
import zipfile
import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class GhostLinkColdBoot:
    """Single-source cold boot system for GhostLink"""
    
    def __init__(self):
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.base_dir = Path.home() / "Downloads" / f"ghostlink_cold_boot_{self.timestamp}"
        self.manifest = {}
        
    def build_all(self):
        """Execute complete cold boot sequence"""
        print("═" * 60)
        print("  GHOSTLINK COLD BOOT SYSTEM")
        print("═" * 60)
        
        self.create_structure()
        self.write_core_engine()
        self.write_launchers()
        self.write_documentation()
        self.write_config()
        self.create_manifest()
        self.package_system()
        
        print("\n✅ Cold boot complete!")
        print(f"📦 Package: {self.base_dir.parent / f'GhostLink_USB_{self.timestamp}.zip'}")
        
    def create_structure(self):
        """Create complete directory structure"""
        print("\n📁 Creating directory structure...")
        
        dirs = [
            "bin",           # Executables and launchers
            "core",          # Core engine code
            "data",          # Runtime data
            "logs",          # System logs
            "docs",          # Documentation
            "config",        # Configuration files
            "venv",          # Virtual environment placeholder
        ]
        
        for d in dirs:
            (self.base_dir / d).mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {d}/")
    
    def write_core_engine(self):
        """Write complete GhostLink cellular automaton engine"""
        print("\n🧬 Writing GhostLink core engine...")
        
        engine_code = '''#!/usr/bin/env python3
"""
GhostLink Cellular Automaton Engine
5-State System: VOID → DELTA → {SIGMA, SCAR, COMPOST}
"""

import numpy as np
import json
from enum import IntEnum
from typing import Tuple, Dict, List
from datetime import datetime

class State(IntEnum):
    """GhostLink cellular automaton states"""
    VOID = 0      # Empty space, potential
    DELTA = 1     # Active, expanding
    SIGMA = 2     # Collapsed, stable
    SCAR = 3      # Collapsed, marked
    COMPOST = 4   # Decaying, recyclable

class GhostLink:
    """Cellular automaton with 5-state transitions"""
    
    def __init__(self, width: int = 100, height: int = 100):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.int8)
        self.density_scar = np.zeros((height, width), dtype=np.float32)
        self.density_compost = np.zeros((height, width), dtype=np.float32)
        self.generation = 0
        self.history = {
            'sigma_count': [],
            'scar_count': [],
            'delta_count': [],
            'compost_count': [],
            'activity': []
        }
        
    def spawn(self, x: int, y: int, radius: int = 3):
        """Spawn DELTA cells from VOID (VOID → DELTA)"""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    nx, ny = (x + dx) % self.width, (y + dy) % self.height
                    if self.grid[ny, nx] == State.VOID:
                        self.grid[ny, nx] = State.DELTA
    
    def collapse(self, collapse_prob: float = 0.3, 
                 scar_prob: float = 0.2, compost_prob: float = 0.1):
        """Collapse DELTA → {SIGMA, SCAR, COMPOST}"""
        delta_mask = (self.grid == State.DELTA)
        rand = np.random.random(self.grid.shape)
        
        # DELTA → COMPOST (highest priority)
        compost_mask = delta_mask & (rand < compost_prob)
        self.grid[compost_mask] = State.COMPOST
        self.density_compost[compost_mask] += 1.0
        
        # DELTA → SCAR
        scar_mask = delta_mask & ~compost_mask & (rand < scar_prob + compost_prob)
        self.grid[scar_mask] = State.SCAR
        self.density_scar[scar_mask] += 1.0
        
        # DELTA → SIGMA (remaining collapses)
        sigma_mask = delta_mask & ~compost_mask & ~scar_mask & (rand < collapse_prob + scar_prob + compost_prob)
        self.grid[sigma_mask] = State.SIGMA
    
    def recycle(self, recycle_prob: float = 0.05):
        """Recycle COMPOST → DELTA"""
        compost_mask = (self.grid == State.COMPOST)
        rand = np.random.random(self.grid.shape)
        recycle_mask = compost_mask & (rand < recycle_prob)
        self.grid[recycle_mask] = State.DELTA
    
    def decay_density(self, decay_rate: float = 0.01):
        """Decay density traces"""
        self.density_scar *= (1.0 - decay_rate)
        self.density_compost *= (1.0 - decay_rate)
    
    def step(self):
        """Execute one generation step"""
        self.collapse()
        self.recycle()
        self.decay_density()
        self.generation += 1
        self._update_history()
    
    def _update_history(self):
        """Track state counts and activity"""
        self.history['sigma_count'].append(np.sum(self.grid == State.SIGMA))
        self.history['scar_count'].append(np.sum(self.grid == State.SCAR))
        self.history['delta_count'].append(np.sum(self.grid == State.DELTA))
        self.history['compost_count'].append(np.sum(self.grid == State.COMPOST))
        
        # Activity = total non-VOID cells
        activity = np.sum(self.grid != State.VOID)
        self.history['activity'].append(activity)
    
    def get_state(self) -> Dict:
        """Export current state"""
        return {
            'generation': self.generation,
            'grid': self.grid.tolist(),
            'density_scar': self.density_scar.tolist(),
            'density_compost': self.density_compost.tolist(),
            'history': self.history,
            'timestamp': datetime.now().isoformat()
        }
    
    def save(self, filepath: str):
        """Save state to JSON"""
        with open(filepath, 'w') as f:
            json.dump(self.get_state(), f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'GhostLink':
        """Load state from JSON"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        gl = cls(width=len(data['grid'][0]), height=len(data['grid']))
        gl.grid = np.array(data['grid'], dtype=np.int8)
        gl.density_scar = np.array(data['density_scar'], dtype=np.float32)
        gl.density_compost = np.array(data['density_compost'], dtype=np.float32)
        gl.generation = data['generation']
        gl.history = data['history']
        return gl

def demo():
    """Demo GhostLink system"""
    print("GhostLink Engine Demo")
    print("=" * 40)
    
    gl = GhostLink(50, 50)
    
    # Spawn initial pattern
    gl.spawn(25, 25, 5)
    
    # Run simulation
    for i in range(20):
        gl.step()
        if i % 5 == 0:
            print(f"Gen {gl.generation}: "
                  f"DELTA={gl.history['delta_count'][-1]} "
                  f"SIGMA={gl.history['sigma_count'][-1]} "
                  f"SCAR={gl.history['scar_count'][-1]} "
                  f"COMPOST={gl.history['compost_count'][-1]}")
    
    # Save state
    gl.save('ghostlink_demo.json')
    print(f"\\n✓ Saved to ghostlink_demo.json")

if __name__ == '__main__':
    demo()
'''
        
        engine_path = self.base_dir / "core" / "ghostlink_engine.py"
        engine_path.write_text(engine_code)
        self.manifest['core/ghostlink_engine.py'] = self._hash_file(engine_path)
        print(f"  ✓ ghostlink_engine.py")
    
    def write_launchers(self):
        """Write platform-specific launchers"""
        print("\n🚀 Writing launchers...")
        
        # Unix launcher
        unix_launcher = '''#!/bin/bash
# GhostLink Unix Launcher

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "═══════════════════════════════════════"
echo "  GHOSTLINK PORTABLE SYSTEM"
echo "═══════════════════════════════════════"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

# Run engine
python3 core/ghostlink_engine.py

echo ""
echo "✓ Session complete"
read -p "Press Enter to exit..."
'''
        
        # Windows launcher
        win_launcher = '''@echo off
REM GhostLink Windows Launcher

cd /d "%~dp0"

echo ═══════════════════════════════════════
echo   GHOSTLINK PORTABLE SYSTEM
echo ═══════════════════════════════════════

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    pause
    exit /b 1
)

REM Run engine
python core\\ghostlink_engine.py

echo.
echo ✓ Session complete
pause
'''
        
        unix_path = self.base_dir / "bin" / "launch.sh"
        win_path = self.base_dir / "bin" / "launch.bat"
        
        unix_path.write_text(unix_launcher)
        win_path.write_text(win_launcher)
        
        # Make Unix launcher executable
        try:
            os.chmod(unix_path, 0o755)
        except:
            pass
        
        self.manifest['bin/launch.sh'] = self._hash_file(unix_path)
        self.manifest['bin/launch.bat'] = self._hash_file(win_path)
        
        print(f"  ✓ launch.sh")
        print(f"  ✓ launch.bat")
    
    def write_documentation(self):
        """Write complete documentation"""
        print("\n📄 Writing documentation...")
        
        readme = '''# GhostLink Portable System

## Overview
GhostLink is a cellular automaton system with 5 states:
- **VOID**: Empty space, potential energy
- **DELTA**: Active, expanding cells
- **SIGMA**: Collapsed, stable state
- **SCAR**: Collapsed with persistent trace
- **COMPOST**: Decaying, recyclable matter

## Quick Start

### Unix/Mac
```bash
./bin/launch.sh
```

### Windows
```
bin\\launch.bat
```

## System Architecture

### State Transitions
- **Spawn**: VOID → DELTA
- **Collapse**: DELTA → {SIGMA, SCAR, COMPOST}
- **Recycle**: COMPOST → DELTA

### Density Traces
- SCAR and COMPOST leave density traces
- Traces decay over time
- Provides historical activity map

## File Structure
```
ghostlink/
├── bin/          # Launchers
├── core/         # Engine code
├── data/         # Runtime data
├── logs/         # System logs
├── docs/         # Documentation
├── config/       # Configuration
└── README.md     # This file
```

## Python API

```python
from core.ghostlink_engine import GhostLink

# Create system
gl = GhostLink(width=100, height=100)

# Spawn cells
gl.spawn(x=50, y=50, radius=5)

# Run simulation
for _ in range(100):
    gl.step()

# Save state
gl.save('state.json')
```

## Configuration
Edit `config/ghostlink.json` to customize:
- Grid dimensions
- Transition probabilities
- Density decay rates

## Cold Boot
This system was generated via cold boot.
To rebuild: python3 ghostlink_cold_boot.py

---
Generated: %s
''' % datetime.datetime.now().isoformat()
        
        readme_path = self.base_dir / "README.md"
        readme_path.write_text(readme)
        self.manifest['README.md'] = self._hash_file(readme_path)
        print(f"  ✓ README.md")
    
    def write_config(self):
        """Write default configuration"""
        print("\n⚙️  Writing configuration...")
        
        config = {
            "system": {
                "name": "GhostLink",
                "version": "1.0.0-coldboot",
                "build_date": datetime.datetime.now().isoformat()
            },
            "simulation": {
                "grid_width": 100,
                "grid_height": 100,
                "collapse_probability": 0.3,
                "scar_probability": 0.2,
                "compost_probability": 0.1,
                "recycle_probability": 0.05,
                "density_decay_rate": 0.01
            },
            "output": {
                "save_interval": 100,
                "log_level": "INFO",
                "data_dir": "data",
                "log_dir": "logs"
            }
        }
        
        config_path = self.base_dir / "config" / "ghostlink.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        self.manifest['config/ghostlink.json'] = self._hash_file(config_path)
        print(f"  ✓ ghostlink.json")
    
    def create_manifest(self):
        """Create integrity manifest"""
        print("\n🔐 Creating integrity manifest...")
        
        manifest_data = {
            "build_date": datetime.datetime.now().isoformat(),
            "build_type": "cold_boot",
            "version": "1.0.0",
            "files": self.manifest
        }
        
        manifest_path = self.base_dir / "MANIFEST.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest_data, f, indent=2)
        
        print(f"  ✓ MANIFEST.json ({len(self.manifest)} files)")
    
    def package_system(self):
        """Package into deployable ZIP"""
        print("\n📦 Packaging system...")
        
        zip_name = f"GhostLink_USB_{self.timestamp}.zip"
        zip_path = self.base_dir.parent / zip_name
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(self.base_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(self.base_dir.parent)
                    zf.write(file_path, arc_name)
                    
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"  ✓ {zip_name} ({size_mb:.2f} MB)")
        print(f"\n📍 Location: {zip_path}")
        print(f"📁 Extracted: {self.base_dir}")
    
    def _hash_file(self, filepath: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(4096), b''):
                sha256.update(block)
        return sha256.hexdigest()

def main():
    """Execute cold boot"""
    builder = GhostLinkColdBoot()
    builder.build_all()
    
    print("\n" + "═" * 60)
    print("  DEPLOYMENT INSTRUCTIONS")
    print("═" * 60)
    print("\n1. Extract ZIP to USB drive")
    print("2. Run: ./bin/launch.sh (Unix) or bin\\launch.bat (Windows)")
    print("3. System will execute from USB without installation")
    print("\n✅ GhostLink ready for cold deployment")

if __name__ == '__main__':
    main()

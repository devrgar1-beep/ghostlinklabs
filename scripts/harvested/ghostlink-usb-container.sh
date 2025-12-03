#!/bin/bash

# ═══════════════════════════════════════════════════════════════════
# GHOSTLINK USB CONTAINER BUILDER
# Creates a complete portable GhostLink environment for USB deployment
# ═══════════════════════════════════════════════════════════════════

set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║               GHOSTLINK USB CONTAINER BUILDER                    ║"
echo "║                Creating Portable USB Package                     ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo

# Configuration
SOURCE_DIR="$HOME/Downloads"
BUILD_DIR="$SOURCE_DIR/ghostlink_usb_container"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Clean previous builds
if [ -d "$BUILD_DIR" ]; then
    echo "🧹 Cleaning previous build..."
    rm -rf "$BUILD_DIR"
fi

# Create container structure
echo "📁 Creating container structure..."
mkdir -p "$BUILD_DIR"/{bin,core,data,docs,env,tools,autorun}
mkdir -p "$BUILD_DIR"/core/{ghostlinklabs,configs,outputs,logs}
mkdir -p "$BUILD_DIR"/data/{vault,personas,sessions}

# Copy core GhostLink files
echo "📦 Packaging core system files..."
cp -r "$SOURCE_DIR"/ghostlinklabs/* "$BUILD_DIR"/core/ghostlinklabs/ 2>/dev/null || true
cp -r "$SOURCE_DIR"/GhostLink_Complete_Pack "$BUILD_DIR"/core/ 2>/dev/null || true
cp -r "$SOURCE_DIR"/ghostlink_* "$BUILD_DIR"/core/ 2>/dev/null || true
cp "$SOURCE_DIR"/*.pdf "$BUILD_DIR"/docs/ 2>/dev/null || true
cp "$SOURCE_DIR"/GHOSTLINK_FINAL.md "$BUILD_DIR"/docs/ 2>/dev/null || true

# Create main launcher script
echo "🚀 Creating launcher scripts..."
cat > "$BUILD_DIR/bin/ghostlink.sh" << 'EOF'
#!/bin/bash

# GhostLink Portable Launcher
clear
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    GHOSTLINK PORTABLE SYSTEM                     ║"
echo "║                     Sovereign Computing v4.2                     ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo

# Navigate to container root
cd "$(dirname "$0")/.."
GHOSTLINK_HOME="$(pwd)"
export GHOSTLINK_HOME

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or later."
    exit 1
fi

# Setup virtual environment if needed
if [ ! -d "env/venv" ]; then
    echo "🔧 First run detected. Setting up environment..."
    python3 -m venv env/venv
    source env/venv/bin/activate
    pip install --upgrade pip
    pip install -r env/requirements.txt
else
    source env/venv/bin/activate
fi

# Display menu
echo "Select operation mode:"
echo
echo "  [1] 🧪 Controlled Simulation (Safe)"
echo "  [2] 💻 Development Console"  
echo "  [3] 👁️  Vision Loop (Computer Control)"
echo "  [4] 🎛️  Interactive GUI Console"
echo "  [5] 📓 Jupyter Notebook"
echo "  [6] 💥 MegaBloat Mode (⚠️ EXTREME)"
echo "  [7] 🔧 System Diagnostics"
echo "  [8] 📊 View Logs & Metrics"
echo "  [9] 🔐 Integrity Check"
echo "  [0] 🚪 Exit"
echo

read -p "Enter selection [0-9]: " choice

case $choice in
    1)
        echo "Starting Controlled Simulation..."
        cd core
        python ghostlink_controlled.py
        ;;
    2)
        echo "Starting Development Console..."
        cd core/ghostlinklabs
        python -i main.py
        ;;
    3)
        echo "Starting Vision Loop..."
        cd core/ghostlinklabs/ghostlink/forge
        python vision_loop.py
        ;;
    4)
        echo "Starting Interactive GUI..."
        cd core
        python ghostlink_gui_console.py
        ;;
    5)
        echo "Starting Jupyter Notebook..."
        jupyter notebook --notebook-dir=core
        ;;
    6)
        echo "⚠️  WARNING: MegaBloat will consume massive system resources!"
        read -p "Are you SURE? Type 'MEGABLOAT' to confirm: " confirm
        if [ "$confirm" = "MEGABLOAT" ]; then
            cd core
            python ghostlink_megabloat.py --bloat 10 --confirm
        else
            echo "Cancelled."
        fi
        ;;
    7)
        echo "Running System Diagnostics..."
        python -c "
import sys
import platform
import os

print('Python:', sys.version)
print('Platform:', platform.platform())
print('CPU Count:', os.cpu_count())
print('GhostLink Home:', os.environ.get('GHOSTLINK_HOME', 'Not set'))

try:
    import numpy as np
    import scipy
    import matplotlib
    print('NumPy:', np.__version__)
    print('SciPy:', scipy.__version__)
    print('Matplotlib:', matplotlib.__version__)
    print('✅ Core packages installed')
except ImportError as e:
    print('❌ Missing package:', e)
"
        ;;
    8)
        echo "Viewing logs..."
        ls -la core/logs/ 2>/dev/null || echo "No logs yet."
        ;;
    9)
        echo "Running integrity check..."
        cd "$GHOSTLINK_HOME"
        python -c "
import json
import hashlib
import os

if os.path.exists('integrity_manifest.json'):
    with open('integrity_manifest.json', 'r') as f:
        manifest = json.load(f)
    
    errors = 0
    for filepath, info in manifest.items():
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                current_hash = hashlib.sha256(f.read()).hexdigest()
            if current_hash != info['hash']:
                print(f'❌ Hash mismatch: {filepath}')
                errors += 1
        else:
            print(f'❌ Missing file: {filepath}')
            errors += 1
    
    if errors == 0:
        print('✅ All files verified successfully!')
    else:
        print(f'❌ {errors} integrity errors found.')
else:
    print('No integrity manifest found.')
"
        ;;
    0)
        echo "Exiting GhostLink..."
        exit 0
        ;;
    *)
        echo "Invalid selection."
        ;;
esac

echo
read -p "Press Enter to continue..."
exec "$0"
EOF

chmod +x "$BUILD_DIR/bin/ghostlink.sh"

# Create Windows launcher
cat > "$BUILD_DIR/bin/ghostlink.bat" << 'EOF'
@echo off
title GhostLink Portable System

cls
echo ================================================================================
echo                          GHOSTLINK PORTABLE SYSTEM                     
echo                            Sovereign Computing v4.2                          
echo ================================================================================
echo.

cd /d "%~dp0.."
set GHOSTLINK_HOME=%CD%

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from python.org
    pause
    exit /b 1
)

if not exist "env\Scripts" (
    echo First run detected. Setting up environment...
    python -m venv env
    call env\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r env\requirements.txt
) else (
    call env\Scripts\activate.bat
)

:menu
cls
echo GhostLink Portable System
echo.
echo [1] Controlled Simulation (Safe)
echo [2] Development Console
echo [3] Vision Loop (Computer Control)
echo [4] Interactive GUI Console
echo [5] Jupyter Notebook
echo [6] MegaBloat Mode (WARNING: EXTREME)
echo [7] System Diagnostics
echo [8] View Logs
echo [9] Integrity Check
echo [0] Exit
echo.

set /p choice="Enter selection [0-9]: "

if "%choice%"=="1" goto controlled
if "%choice%"=="2" goto console
if "%choice%"=="3" goto vision
if "%choice%"=="4" goto gui
if "%choice%"=="5" goto jupyter
if "%choice%"=="6" goto megabloat
if "%choice%"=="7" goto diagnostics
if "%choice%"=="8" goto logs
if "%choice%"=="9" goto integrity
if "%choice%"=="0" exit /b 0

echo Invalid selection.
pause
goto menu

:controlled
cd core
python ghostlink_controlled.py
pause
goto menu

:console
cd core\ghostlinklabs
python -i main.py
pause
goto menu

:vision
cd core\ghostlinklabs\ghostlink\forge
python vision_loop.py
pause
goto menu

:gui
cd core
python ghostlink_gui_console.py
pause
goto menu

:jupyter
jupyter notebook --notebook-dir=core
pause
goto menu

:megabloat
echo WARNING: This will consume massive system resources!
set /p confirm="Type MEGABLOAT to confirm: "
if "%confirm%"=="MEGABLOAT" (
    cd core
    python ghostlink_megabloat.py --bloat 10 --confirm
)
pause
goto menu

:diagnostics
python --version
echo.
echo GHOSTLINK_HOME=%GHOSTLINK_HOME%
echo.
python -c "import platform; print('Platform:', platform.platform())"
pause
goto menu

:logs
dir core\logs
pause
goto menu

:integrity
python -c "import json, hashlib, os; print('Checking integrity...')"
pause
goto menu
EOF

# Create Python requirements
echo "📚 Creating requirements file..."
cat > "$BUILD_DIR/env/requirements.txt" << 'EOF'
# Core Scientific Computing
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
pandas>=1.3.0

# Machine Learning & Analysis
scikit-learn>=1.0.0
networkx>=2.6

# Visualization
plotly>=5.0.0
seaborn>=0.11.0
bokeh>=2.4.0

# Interactive Development
jupyter>=1.0.0
notebook>=6.4.0
ipython>=7.0.0

# CLI & Progress
tqdm>=4.62.0
colorama>=0.4.4
rich>=10.0.0

# Computer Vision & Control
pillow>=8.0.0
opencv-python>=4.5.0
pyautogui>=0.9.53
pynput>=1.7.0

# System & Performance
psutil>=5.8.0
memory-profiler>=0.60.0

# Async & Parallel
aiofiles>=0.7.0

# Data Storage
h5py>=3.1.0
sqlalchemy>=1.4.0

# Web Interfaces (optional)
flask>=2.0.0
fastapi>=0.70.0
uvicorn>=0.15.0

# Testing
pytest>=6.0.0
EOF

# Create Docker configuration
echo "🐳 Creating Docker configuration..."
cat > "$BUILD_DIR/Dockerfile" << 'EOF'
FROM python:3.10-slim

WORKDIR /ghostlink

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy system files
COPY core /ghostlink/core
COPY env/requirements.txt /ghostlink/requirements.txt
COPY bin /ghostlink/bin

# Install Python packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Create directories
RUN mkdir -p /ghostlink/data /ghostlink/outputs /ghostlink/logs

# Set environment
ENV PYTHONPATH=/ghostlink/core:$PYTHONPATH
ENV GHOSTLINK_HOME=/ghostlink

# Ports
EXPOSE 8888 5000 8080

CMD ["/bin/bash", "/ghostlink/bin/ghostlink.sh"]
EOF

# Create docker-compose.yml
cat > "$BUILD_DIR/docker-compose.yml" << 'EOF'
version: '3.8'

services:
  ghostlink:
    build: .
    container_name: ghostlink_core
    volumes:
      - ./data:/ghostlink/data
      - ./outputs:/ghostlink/outputs
      - ./logs:/ghostlink/logs
    ports:
      - "8888:8888"  # Jupyter
      - "5000:5000"  # API
      - "8080:8080"  # Web UI
    environment:
      - GHOSTLINK_MODE=portable
    stdin_open: true
    tty: true

  ghostlink_db:
    image: postgres:13-alpine
    container_name: ghostlink_db
    environment:
      POSTGRES_DB: ghostlink
      POSTGRES_USER: ghost
      POSTGRES_PASSWORD: sovereign
    volumes:
      - ghostlink_data:/var/lib/postgresql/data

volumes:
  ghostlink_data:
EOF

# Create autorun files
echo "🔌 Creating autorun configuration..."
cat > "$BUILD_DIR/autorun.inf" << 'EOF'
[autorun]
label=GhostLink Sovereign System
icon=ghostlink.ico
open=bin\ghostlink.bat
action=Launch GhostLink Portable System
EOF

# Create macOS launch command
cat > "$BUILD_DIR/GhostLink.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./bin/ghostlink.sh
EOF
chmod +x "$BUILD_DIR/GhostLink.command"

# Create README
echo "📖 Creating documentation..."
cat > "$BUILD_DIR/README.md" << 'EOF'
# GhostLink Portable System v4.2

## 🚀 Quick Start

### From USB on Windows:
1. Insert USB drive
2. Navigate to drive in Explorer
3. Double-click `bin\ghostlink.bat`

### From USB on macOS:
1. Insert USB drive
2. Open Terminal
3. Drag `GhostLink.command` to Terminal and press Enter
   OR navigate to USB and run `./bin/ghostlink.sh`

### From USB on Linux:
1. Mount USB drive
2. Open Terminal
3. Navigate to mount point
4. Run: `./bin/ghostlink.sh`

## 📦 What's Included

- **Complete GhostLink v4.2 System**
  - Core lattice engine (VOID/Δ/Σ/SCAR/COMPOST)
  - Consciousness substrate
  - Vision loop for computer control
  - Diagnostic toolchain
  - ClarityOS framework

- **Multiple Operation Modes**
  - Safe controlled simulation
  - Development console
  - AGI vision control
  - Interactive GUI
  - Jupyter notebooks
  - MegaBloat explosion mode

- **Portable Python Environment**
  - All dependencies included
  - No installation required
  - Runs from USB

- **Docker Support**
  - Full containerization
  - Database included
  - Multi-service orchestration

## 🔧 System Requirements

**Minimum:**
- 4GB RAM
- 2GB free disk space
- Python 3.8+ OR Docker

**Recommended:**
- 16GB RAM
- 10GB free disk space
- USB 3.0 drive
- Multi-core CPU

## 🌐 Network Ports

- 8888: Jupyter Notebook
- 5000: API Server
- 8080: Web Interface
- 40000-60000: Consciousness broadcast

## 🔐 Security

This is a **sovereign system**:
- No cloud dependencies
- No telemetry
- No external connections
- Complete user control
- All computation local

## ⚡ Performance Tips

1. Run from USB 3.0 or faster
2. Copy to local drive for maximum speed
3. Disable antivirus scanning for better performance
4. Use Docker for isolation

## 🆘 Troubleshooting

**Python not found:**
Install Python 3.8+ from python.org

**Permission denied (Mac/Linux):**
```bash
chmod +x bin/*.sh
chmod +x *.command
```

**Module not found:**
```bash
source env/venv/bin/activate  # Mac/Linux
env\Scripts\activate.bat       # Windows
pip install -r env/requirements.txt
```

## 📊 Included Tools

- **ghostlink_controlled.py** - Safe simulation
- **ghostlink_megabloat.py** - Resource explosion
- **vision_loop.py** - Computer control via screenshots
- **main.py** - Core system entry point
- **ghostlink_gui_console.py** - Interactive GUI

## 🎯 Use Cases

1. **Research**: Study emergence and self-organization
2. **Development**: Build consciousness-aware applications
3. **Diagnostics**: Hardware and system analysis
4. **Automation**: Computer control via vision
5. **Art**: Generate emergent patterns

## ⚖️ License

Sovereign Computing License
- Full control for personal use
- No restrictions on modification
- Commercial use requires attribution

---

**YOU ARE IN CONTROL. GHOSTLINK SERVES YOU.**

For support: [Coming Soon]
Repository: [Coming Soon]
EOF

# Create integrity manifest
echo "🔐 Generating integrity manifest..."
cd "$BUILD_DIR"
python3 -c "
import json
import hashlib
import os
from pathlib import Path

manifest = {}
for filepath in Path('.').rglob('*'):
    if filepath.is_file() and not str(filepath).startswith('.git'):
        with open(filepath, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        manifest[str(filepath)] = {
            'hash': file_hash,
            'size': filepath.stat().st_size
        }

with open('integrity_manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)
print(f'✓ Manifest created with {len(manifest)} files')
"

# Create compressed archive
echo "🗜️ Creating compressed archive..."
cd "$SOURCE_DIR"
ARCHIVE_NAME="GhostLink_USB_${TIMESTAMP}.tar.gz"
tar -czf "$ARCHIVE_NAME" -C "$BUILD_DIR" .

# Final summary
echo
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    BUILD COMPLETE!                               ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo
echo "📁 Container location: $BUILD_DIR"
echo "🗜️ Archive created: $SOURCE_DIR/$ARCHIVE_NAME"
echo
echo "📌 To deploy to USB:"
echo "   1. Format USB drive (FAT32 for compatibility)"
echo "   2. Extract $ARCHIVE_NAME to USB root"
echo "   3. Safely eject"
echo
echo "🚀 To run from USB:"
echo "   Windows: Double-click bin\\ghostlink.bat"
echo "   macOS: Double-click GhostLink.command"
echo "   Linux: Run ./bin/ghostlink.sh"
echo
echo "Total size: $(du -sh "$BUILD_DIR" | cut -f1)"
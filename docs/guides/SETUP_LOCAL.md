# 🛠️ GhostLink Local Setup Guide

## Prerequisites Installation

### 1. Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Node.js and npm
```bash
brew install node
```

### 3. Install Ollama (Local AI)
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 4. Verify Installations
```bash
node --version  # Should show v20.x or higher
npm --version   # Should show v10.x or higher
ollama --version  # Should show ollama version
python3 --version  # Should show Python 3.10+
```

---

## Quick Start (After Prerequisites)

### 1. Download Local AI Models
```bash
ollama pull mistral:7b-instruct
ollama pull codellama:7b
ollama pull phi3:mini
```

### 2. Initialize Electron App
```bash
cd projects/ghostlinklabs
npm init -y
npm install electron electron-builder --save-dev
```

### 3. Install Python Dependencies
```bash
pip3 install fastapi uvicorn ollama-python
```

### 4. Run Local System
```bash
# Terminal 1: Start Python backend
python3 local_server.py

# Terminal 2: Start Electron app
npm start
```

---

## Next Steps
See IMPLEMENTATION_PLAN.md for detailed roadmap.

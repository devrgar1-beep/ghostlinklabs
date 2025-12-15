#!/bin/bash

# GhostLink Local - Quick Start Script
# 100% Local System - No Docker, No APIs, No Cloud

echo "🚀 GhostLink Local - Starting..."
echo "📍 100% Local System"
echo "🔒 No Docker - No APIs - No Cloud"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi
echo "✅ Python 3: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js not found. Installing..."
    if command -v brew &> /dev/null; then
        brew install node
    else
        echo "❌ Please install Node.js from https://nodejs.org/"
        exit 1
    fi
fi
echo "✅ Node.js: $(node --version)"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found. Installing..."
    curl -fsSL https://ollama.com/install.sh | sh
fi
echo "✅ Ollama: Installed"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -q fastapi uvicorn 2>&1 | grep -v "already satisfied" || true
echo "✅ Python dependencies installed"

# Install Node.js dependencies
echo ""
echo "Installing Node.js dependencies..."
if [ ! -d "node_modules" ]; then
    npm install --silent
    echo "✅ Node.js dependencies installed"
else
    echo "✅ Node.js dependencies already installed"
fi

# Check if models are downloaded
echo ""
echo "Checking AI models..."
if ! ollama list | grep -q "mistral"; then
    echo "⚠️  Downloading AI models (this may take a few minutes)..."
    ollama pull mistral:7b-instruct
    echo "✅ Models downloaded"
else
    echo "✅ Models ready"
fi

# Start the application
echo ""
echo "✨ Starting GhostLink Local..."
echo ""
echo "🌐 Access at: Electron App will open automatically"
echo "🔧 Python Server: http://127.0.0.1:8765"
echo ""
echo "Press Ctrl+C to stop"
echo ""

npm start

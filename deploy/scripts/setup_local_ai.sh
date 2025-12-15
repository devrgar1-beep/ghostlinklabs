#!/bin/bash
# GhostLink Local AI Setup Script
# This script helps you install and run Ollama for local AI models

echo "🤖 GhostLink Local AI Setup"
echo "=========================="
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "📦 Installing Ollama..."

    # Install Ollama (works on macOS, Linux, and WSL)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install ollama
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "❌ Unsupported OS. Please install Ollama manually from: https://ollama.ai"
        exit 1
    fi
else
    echo "✅ Ollama is already installed"
fi

echo ""
echo "🚀 Starting Ollama service..."

# Start Ollama service
if [[ "$OSTYPE" == "darwin"* ]]; then
    # On macOS, Ollama runs as a service
    echo "On macOS, Ollama should start automatically."
    echo "If not running, start it manually with: ollama serve"
else
    # On Linux/Windows, start the service
    nohup ollama serve > ollama.log 2>&1 &
    sleep 2
fi

# Check if Ollama is running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running!"
else
    echo "❌ Ollama failed to start. Check ollama.log for details."
    exit 1
fi

echo ""
echo "📥 Pulling default model (llama2)..."
ollama pull llama2

echo ""
echo "🎉 Setup complete! You can now use GhostLink with local AI models."
echo ""
echo "Try it out:"
echo "  python main.py ask 'Hello local AI!'"
echo ""
echo "Other available commands:"
echo "  python main.py --terminal-90s    # Launch cyberpunk interface"
echo "  python main.py status           # Check system status"
echo "  python main.py providers        # List AI providers"
echo ""
echo "To install more models:"
echo "  ollama pull mistral             # Fast and capable"
echo "  ollama pull codellama          # Code-focused model"
echo "  ollama pull llama2:13b         # Larger, more capable model"
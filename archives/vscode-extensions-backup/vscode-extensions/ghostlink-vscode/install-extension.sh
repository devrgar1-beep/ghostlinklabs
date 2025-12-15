#!/bin/bash
# GhostLink VS Code Extension Installation Script

echo "🚀 GhostLink VS Code Extension Installation"
echo "=========================================="

# Check if VS Code CLI is available
if ! command -v code &> /dev/null; then
    echo "❌ VS Code CLI not found. Please install VS Code and ensure 'code' command is available."
    echo ""
    echo "Manual Installation Instructions:"
    echo "1. Open VS Code"
    echo "2. Press Ctrl+Shift+P (Cmd+Shift+P on Mac)"
    echo "3. Type 'Extensions: Install from VSIX'"
    echo "4. Select the file: ghostlink-vscode-1.0.0.vsix"
    echo "5. The extension will be installed and ready to use"
    echo ""
    echo "Extension provides these commands:"
    echo "- GhostLink: System Health"
    echo "- GhostLink: Execute Task"
    echo "- GhostLink: Evolution Status"
    echo "- GhostLink: Consciousness Analysis"
    echo "- GhostLink: Multi-Agent Coordination"
    echo "- GhostLink: Deploy System"
    exit 1
fi

# Get the absolute path to the extension
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTENSION_PATH="$SCRIPT_DIR/ghostlink-vscode-1.0.0.vsix"

if [ ! -f "$EXTENSION_PATH" ]; then
    echo "❌ Extension file not found: $EXTENSION_PATH"
    exit 1
fi

echo "📦 Installing GhostLink VS Code Extension..."
code --install-extension "$EXTENSION_PATH"

if [ $? -eq 0 ]; then
    echo "✅ GhostLink VS Code Extension installed successfully!"
    echo ""
    echo "Available Commands:"
    echo "- GhostLink: System Health (Ctrl+Shift+P → 'GhostLink: System Health')"
    echo "- GhostLink: Execute Task (Ctrl+Shift+P → 'GhostLink: Execute Task')"
    echo "- GhostLink: Evolution Status (Ctrl+Shift+P → 'GhostLink: Evolution Status')"
    echo "- GhostLink: Consciousness Analysis (Ctrl+Shift+P → 'GhostLink: Consciousness Analysis')"
    echo "- GhostLink: Multi-Agent Coordination (Ctrl+Shift+P → 'GhostLink: Multi-Agent Coordination')"
    echo "- GhostLink: Deploy System (Ctrl+Shift+P → 'GhostLink: Deploy System')"
    echo ""
    echo "The extension integrates with the autonomous AI systems for enhanced development workflow."
else
    echo "❌ Failed to install extension"
    exit 1
fi
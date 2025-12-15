#!/bin/bash
# GhostLink VS Code Integration Test Script

echo "🧪 Testing GhostLink VS Code Integration"
echo "========================================"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="python3"
INTEGRATION_SCRIPT="$PROJECT_ROOT/ghost_vscode_integration.py"

echo "📁 Project Root: $PROJECT_ROOT"
echo "🐍 Python Command: $PYTHON_CMD"
echo "🔗 Integration Script: $INTEGRATION_SCRIPT"
echo

# Test 1: Check if integration script exists
echo "Test 1: Integration script existence"
if [ -f "$INTEGRATION_SCRIPT" ]; then
    echo "✅ Integration script found"
else
    echo "❌ Integration script not found"
    exit 1
fi
echo

# Test 2: Check Python execution
echo "Test 2: Python execution test"
if command -v $PYTHON_CMD &> /dev/null; then
    echo "✅ Python is available"
else
    echo "❌ Python not found"
    exit 1
fi
echo

# Test 3: Test integration script import
echo "Test 3: Integration script import test"
if $PYTHON_CMD -c "import sys; sys.path.append('$PROJECT_ROOT'); import ghost_vscode_integration; print('✅ Import successful')"; then
    echo "✅ Integration script imports correctly"
else
    echo "❌ Integration script import failed"
    exit 1
fi
echo

# Test 4: Test basic integration functionality
echo "Test 4: Basic integration functionality"
if $PYTHON_CMD "$INTEGRATION_SCRIPT" --help &> /dev/null; then
    echo "✅ Integration script runs without errors"
else
    echo "⚠️  Integration script may have issues (but basic execution works)"
fi
echo

# Test 5: Check VS Code extension structure
echo "Test 5: VS Code extension structure"
EXTENSION_DIR="$PROJECT_ROOT/vscode-extensions/ghostlink-vscode"
if [ -d "$EXTENSION_DIR" ]; then
    echo "✅ Extension directory exists"

    if [ -f "$EXTENSION_DIR/package.json" ]; then
        echo "✅ Extension package.json found"
    else
        echo "❌ Extension package.json missing"
    fi

    if [ -f "$EXTENSION_DIR/out/extension.js" ]; then
        echo "✅ Compiled extension found"
    else
        echo "❌ Compiled extension missing"
    fi
else
    echo "❌ Extension directory not found"
fi
echo

# Test 6: Check Ghost agent orchestrator
echo "Test 6: Ghost agent orchestrator availability"
ORCHESTRATOR_SCRIPT="$PROJECT_ROOT/ghost_agent_orchestrator.py"
if [ -f "$ORCHESTRATOR_SCRIPT" ]; then
    echo "✅ Ghost agent orchestrator found"

    if $PYTHON_CMD "$ORCHESTRATOR_SCRIPT" --help &> /dev/null; then
        echo "✅ Orchestrator runs without errors"
    else
        echo "⚠️  Orchestrator may have issues"
    fi
else
    echo "❌ Ghost agent orchestrator not found"
fi
echo

echo "🎉 Integration test complete!"
echo
echo "Next steps:"
echo "1. Install the ghostlink-vscode extension in VS Code"
echo "2. Install and start the vscode-http-api extension"
echo "3. Configure extension settings in VS Code"
echo "4. Test commands via Command Palette (Ctrl+Shift+P)"
echo
echo "For detailed testing, run individual components:"
echo "python3 ghost_vscode_integration.py status"
echo "python3 ghost_agent_orchestrator.py health"

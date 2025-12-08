#!/bin/bash

# GhostLink VS Code Integration Setup Script
# Automates the installation and configuration of VS Code extensions for GhostLink AI

set -e

echo "🚀 GhostLink VS Code Integration Setup"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "vscode-extensions" ]; then
    print_error "vscode-extensions directory not found. Please run this script from the ghostlinklabs root directory."
    exit 1
fi

print_status "Starting VS Code integration setup..."

# Step 1: Check VS Code installation
print_step "1. Checking VS Code installation..."
if ! command -v code &> /dev/null; then
    print_error "VS Code CLI (code) not found. Please install VS Code and add it to your PATH."
    echo "Visit: https://code.visualstudio.com/download"
    exit 1
fi
print_status "VS Code CLI found: $(code --version | head -n 1)"

# Step 2: Install GhostLink VS Code Extension
print_step "2. Installing GhostLink VS Code Extension..."
GHOSTLINK_VSIX="vscode-extensions/ghostlink-vscode/ghostlink-vscode-1.0.0.vsix"

if [ ! -f "$GHOSTLINK_VSIX" ]; then
    print_error "GhostLink extension package not found: $GHOSTLINK_VSIX"
    exit 1
fi

print_status "Installing GhostLink extension from: $GHOSTLINK_VSIX"
if code --install-extension "$GHOSTLINK_VSIX"; then
    print_status "✅ GhostLink extension installed successfully"
else
    print_error "Failed to install GhostLink extension"
    exit 1
fi

# Step 3: Check for VS Code HTTP API extension
print_step "3. Checking for VS Code HTTP API extension..."

# First try to install from marketplace
if code --install-extension "ms-vscode.vscode-http-api" 2>/dev/null; then
    print_status "✅ VS Code HTTP API extension installed from marketplace"
    HTTP_API_INSTALLED=true
else
    print_warning "Marketplace installation failed, attempting local build..."

    # Try to build and install locally
    HTTP_API_DIR="vscode-extensions/vscode-http-api"

    if [ ! -d "$HTTP_API_DIR" ]; then
        print_error "VS Code HTTP API source directory not found: $HTTP_API_DIR"
        exit 1
    fi

    cd "$HTTP_API_DIR"

    # Check if node and npm are available
    if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
        print_error "Node.js and npm are required to build the HTTP API extension"
        echo "Visit: https://nodejs.org/"
        exit 1
    fi

    print_status "Building VS Code HTTP API extension..."
    npm install
    npm run compile

    # Create .vsix package
    if command -v vsce &> /dev/null; then
        vsce package
        VSIX_FILE=$(ls *.vsix | head -n 1)
        if [ -n "$VSIX_FILE" ]; then
            code --install-extension "$VSIX_FILE"
            print_status "✅ VS Code HTTP API extension built and installed locally"
            HTTP_API_INSTALLED=true
        else
            print_error "Failed to create .vsix package"
            HTTP_API_INSTALLED=false
        fi
    else
        print_warning "vsce (VS Code Extension Manager) not found. Installing globally..."
        npm install -g @vscode/vsce
        vsce package
        VSIX_FILE=$(ls *.vsix | head -n 1)
        if [ -n "$VSIX_FILE" ]; then
            code --install-extension "$VSIX_FILE"
            print_status "✅ VS Code HTTP API extension built and installed locally"
            HTTP_API_INSTALLED=true
        else
            print_error "Failed to create .vsix package"
            HTTP_API_INSTALLED=false
        fi
    fi

    cd - > /dev/null
fi

# Step 4: Configure extensions
print_step "4. Configuring extensions..."

# Create VS Code settings if they don't exist
VSCODE_SETTINGS_DIR="$HOME/Library/Application Support/Code/User"
if [ ! -d "$VSCODE_SETTINGS_DIR" ]; then
    # Try alternative locations
    VSCODE_SETTINGS_DIR="$HOME/.vscode"
    if [ ! -d "$VSCODE_SETTINGS_DIR" ]; then
        mkdir -p "$VSCODE_SETTINGS_DIR"
    fi
fi

SETTINGS_FILE="$VSCODE_SETTINGS_DIR/settings.json"

# Backup existing settings
if [ -f "$SETTINGS_FILE" ]; then
    cp "$SETTINGS_FILE" "${SETTINGS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    print_status "Backed up existing VS Code settings"
fi

# Read existing settings or create new ones
if [ -f "$SETTINGS_FILE" ]; then
    # Use python to safely update JSON settings
    python3 -c "
import json
import os

settings_file = '$SETTINGS_FILE'
project_root = os.path.abspath('.')

# Read existing settings
with open(settings_file, 'r') as f:
    try:
        settings = json.load(f)
    except json.JSONDecodeError:
        settings = {}

# Update GhostLink settings
settings.update({
    'ghostlink.pythonPath': 'python3',
    'ghostlink.projectRoot': project_root,
    'ghostlink.vscodeApiUrl': 'http://localhost:3000',
    'vscodeHttpApi.port': 8765,
    'vscodeHttpApi.apiKey': 'ghostlink_secure_key_2025',
    'vscodeHttpApi.allowRemote': False,
    'vscodeHttpApi.autoCommit': True,
    'vscodeHttpApi.enforceWorkspaceScope': True
})

# Write back settings
with open(settings_file, 'w') as f:
    json.dump(settings, f, indent=2)

print('✅ VS Code settings updated for GhostLink integration')
"
else
    # Create new settings file
    cat > "$SETTINGS_FILE" << EOF
{
    "ghostlink.pythonPath": "python3",
    "ghostlink.projectRoot": "$(pwd)",
    "ghostlink.vscodeApiUrl": "http://localhost:3000",
    "vscodeHttpApi.port": 8765,
    "vscodeHttpApi.apiKey": "ghostlink_secure_key_2025",
    "vscodeHttpApi.allowRemote": false,
    "vscodeHttpApi.autoCommit": true,
    "vscodeHttpApi.enforceWorkspaceScope": true
}
EOF
    print_status "✅ Created new VS Code settings file"
fi

# Step 5: Start VS Code HTTP API service
print_step "5. Starting VS Code HTTP API service..."

# Check if VS Code is running
if pgrep -f "Code" > /dev/null || pgrep -f "Visual Studio Code" > /dev/null; then
    print_status "VS Code is running"
else
    print_warning "VS Code is not running. Please start VS Code manually."
    print_warning "The HTTP API service will start automatically when VS Code loads."
fi

# Step 6: Verification
print_step "6. Verifying installation..."

echo ""
print_status "Installation Summary:"
echo "✅ GhostLink VS Code Extension: Installed"
if [ "$HTTP_API_INSTALLED" = true ]; then
    echo "✅ VS Code HTTP API Extension: Installed"
else
    echo "❌ VS Code HTTP API Extension: Installation failed"
fi
echo "✅ Configuration: Applied"
echo ""

print_status "Next Steps:"
echo "1. Restart VS Code if it's currently running"
echo "2. Open Command Palette (Ctrl+Shift+P) and type 'GhostLink' to see available commands"
echo "3. Test the integration by running: 'GhostLink: Show System Health'"
echo ""

print_status "Configuration Details:"
echo "- HTTP API Port: 8765"
echo "- API Key: ghostlink_secure_key_2025"
echo "- Project Root: $(pwd)"
echo ""

print_status "🎉 VS Code integration setup complete!"
print_warning "Please restart VS Code to activate the extensions."</content>
<parameter name="filePath">/Users/ghost-link-labs/ghostlinklabs/setup_vscode_integration.sh
#!/bin/bash

# 🚀 GHOSTLINK VS CODE EXTENSIONS INSTALLATION SCRIPT
# Automated installation of GhostLink VS Code extensions
# Date: December 8, 2025

set -e  # Exit on any error

echo "🚀 GHOSTLINK VS CODE EXTENSIONS INSTALLATION"
echo "==========================================="
echo "Date: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to install VS Code extension
install_vscode_extension() {
    local extension_path="$1"
    local extension_name="$2"

    echo ""
    echo -e "${BLUE}🔌 INSTALLING: ${extension_name}${NC}"
    echo -e "${BLUE}📁 Path: ${extension_path}${NC}"
    echo ""

    if [ -f "$extension_path" ]; then
        log "Installing $extension_name..."

        # Try to install the extension
        if code --install-extension "$extension_path" --force; then
            echo -e "${GREEN}✅ SUCCESS: $extension_name installed${NC}"
            log "$extension_name installed successfully"
            return 0
        else
            echo -e "${RED}❌ FAILED: $extension_name installation failed${NC}"
            log "ERROR: $extension_name installation failed"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠️  WARNING: Extension file not found: $extension_path${NC}"
        log "WARNING: $extension_path not found"
        return 1
    fi
}

# Function to verify VS Code CLI availability
check_vscode_cli() {
    echo -e "${BLUE}🔍 CHECKING VS CODE CLI AVAILABILITY${NC}"

    if command -v code &> /dev/null; then
        VS_CODE_VERSION=$(code --version 2>/dev/null | head -n 1)
        echo -e "${GREEN}✅ VS Code CLI available: $VS_CODE_VERSION${NC}"
        return 0
    else
        echo -e "${RED}❌ ERROR: VS Code CLI (code command) not found${NC}"
        echo -e "${YELLOW}💡 Please ensure VS Code is installed and CLI is available${NC}"
        echo -e "${YELLOW}   On macOS: Add 'Visual Studio Code.app/Contents/Resources/app/bin' to PATH${NC}"
        return 1
    fi
}

# Function to start VS Code HTTP API service
start_http_api_service() {
    echo ""
    echo -e "${BLUE}🌐 STARTING VS CODE HTTP API SERVICE${NC}"

    # Check if the service is already running
    if pgrep -f "vscode-http-api" > /dev/null; then
        echo -e "${GREEN}✅ VS Code HTTP API service is already running${NC}"
        return 0
    fi

    # Try to start the HTTP API service
    local api_dir="/Users/ghost-link-labs/ghostlinklabs/vscode-extensions/vscode-http-api"

    if [ -d "$api_dir" ]; then
        cd "$api_dir"
        log "Starting VS Code HTTP API service..."

        # Start the service in background
        npm start &
        local service_pid=$!

        # Wait a moment for service to start
        sleep 3

        if kill -0 $service_pid 2>/dev/null; then
            echo -e "${GREEN}✅ VS Code HTTP API service started (PID: $service_pid)${NC}"
            log "VS Code HTTP API service started successfully"
            return 0
        else
            echo -e "${RED}❌ FAILED: VS Code HTTP API service failed to start${NC}"
            log "ERROR: VS Code HTTP API service failed to start"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠️  WARNING: VS Code HTTP API directory not found${NC}"
        return 1
    fi
}

# Function to verify extension installation
verify_extension_installation() {
    local extension_id="$1"
    local extension_name="$2"

    echo -e "${YELLOW}🔍 VERIFYING: $extension_name installation${NC}"

    # Check if extension is installed
    if code --list-extensions | grep -q "$extension_id"; then
        echo -e "${GREEN}✅ VERIFIED: $extension_name is installed${NC}"
        return 0
    else
        echo -e "${RED}❌ VERIFICATION FAILED: $extension_name not found${NC}"
        return 1
    fi
}

# Pre-installation checks
echo -e "${BLUE}🔍 PERFORMING PRE-INSTALLATION CHECKS${NC}"
echo ""

# Check VS Code CLI
if ! check_vscode_cli; then
    echo -e "${RED}❌ Cannot proceed without VS Code CLI. Please install VS Code and ensure CLI is available.${NC}"
    exit 1
fi

# Check extension files exist
GHOSTLINK_EXTENSION="/Users/ghost-link-labs/ghostlinklabs/vscode-extensions/ghostlink-vscode/ghostlink-vscode-1.0.0.vsix"
HTTP_API_EXTENSION="/Users/ghost-link-labs/ghostlinklabs/vscode-extensions/vscode-http-api/vscode-http-api-0.0.1.vsix"

if [ ! -f "$GHOSTLINK_EXTENSION" ]; then
    echo -e "${RED}❌ ERROR: GhostLink VS Code extension not found: $GHOSTLINK_EXTENSION${NC}"
    exit 1
fi

if [ ! -f "$HTTP_API_EXTENSION" ]; then
    echo -e "${RED}❌ ERROR: VS Code HTTP API extension not found: $HTTP_API_EXTENSION${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All extension files found${NC}"

echo ""
echo -e "${GREEN}🎯 STARTING EXTENSION INSTALLATION${NC}"
echo "====================================="

# Track installation results
TOTAL_EXTENSIONS=2
SUCCESS_COUNT=0
FAILED_EXTENSIONS=""

# 1. Install GhostLink VS Code Extension
if install_vscode_extension "$GHOSTLINK_EXTENSION" "GhostLink VS Code Extension"; then
    ((SUCCESS_COUNT++))
    verify_extension_installation "undefined_publisher.ghostlink-vscode" "GhostLink VS Code Extension"
else
    FAILED_EXTENSIONS="$FAILED_EXTENSIONS GhostLink_VS_Code_Extension"
fi

# 2. Install VS Code HTTP API Extension
if install_vscode_extension "$HTTP_API_EXTENSION" "VS Code HTTP API Extension"; then
    ((SUCCESS_COUNT++))
    verify_extension_installation "undefined_publisher.vscode-http-api" "VS Code HTTP API Extension"
else
    FAILED_EXTENSIONS="$FAILED_EXTENSIONS VS_Code_HTTP_API_Extension"
fi

# 3. Start VS Code HTTP API Service
if start_http_api_service; then
    ((SUCCESS_COUNT++))
else
    FAILED_EXTENSIONS="$FAILED_EXTENSIONS HTTP_API_Service"
fi

echo ""
echo "====================================="
echo -e "${GREEN}🎯 INSTALLATION COMPLETE${NC}"
echo "====================================="

# Results summary
echo ""
echo -e "${BLUE}📊 INSTALLATION RESULTS:${NC}"
echo "Total Components: 3 (2 extensions + 1 service)"
echo -e "Successful Installations: ${GREEN}$SUCCESS_COUNT${NC}"
echo -e "Failed Installations: ${RED}$((3 - SUCCESS_COUNT))${NC}"

if [ -n "$FAILED_EXTENSIONS" ]; then
    echo -e "${RED}Failed Components: $FAILED_EXTENSIONS${NC}"
fi

# Success rate calculation
SUCCESS_RATE=$((SUCCESS_COUNT * 100 / 3))
echo -e "Success Rate: ${GREEN}$SUCCESS_RATE%${NC}"

# Post-installation instructions
echo ""
echo -e "${BLUE}📋 POST-INSTALLATION STEPS:${NC}"
echo "1. Restart VS Code completely (close and reopen)"
echo "2. Check VS Code extensions panel to verify installations"
echo "3. Test GhostLink integration with a simple command"
echo "4. Verify HTTP API service is accessible"

# Final status
echo ""
if [ $SUCCESS_COUNT -eq 3 ]; then
    echo -e "${GREEN}🎉 COMPLETE SUCCESS: All VS Code extensions installed and service started!${NC}"
    echo -e "${GREEN}🚀 GhostLink ↔ VS Code bidirectional communication is now active${NC}"
    echo ""
    echo -e "${GREEN}🎯 NEXT STEPS:${NC}"
    echo "• Test integration: Try a GhostLink command in VS Code"
    echo "• Monitor logs: Check VS Code developer console for any issues"
    echo "• Update TODO: Mark VS Code extension installation as complete"
    exit 0
elif [ $SUCCESS_COUNT -ge 2 ]; then
    echo -e "${YELLOW}⚠️  PARTIAL SUCCESS: $SUCCESS_COUNT/3 components installed${NC}"
    echo -e "${YELLOW}🔄 Manual intervention may be required for remaining components${NC}"
    exit 1
else
    echo -e "${RED}❌ INSTALLATION FAILED: Only $SUCCESS_COUNT/3 components installed${NC}"
    echo -e "${RED}🔧 Manual installation required${NC}"
    exit 1
fi
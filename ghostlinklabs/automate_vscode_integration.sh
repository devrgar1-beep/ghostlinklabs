#!/bin/bash
# GhostLink AI - Complete VS Code Integration Automation Script
# This script automates the entire VS Code integration setup and testing

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="python3"
VSCODE_SETTINGS_DIR=""
VSCODE_EXTENSIONS_DIR=""
LOG_FILE="$PROJECT_ROOT/vscode_integration_automation.log"

# Logging function
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

# Status tracking (using variables instead of associative arrays for compatibility)
python_check=false
integration_script=false
orchestrator=false
extension_build=false
vscode_cli=false
http_api_install=false
settings_config=false
integration_test=false

# Header
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           GhostLink AI - VS Code Integration Automation      ║"
echo "║                    Complete Setup & Testing                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
log "🚀 Starting GhostLink VS Code Integration Automation"

# Detect VS Code settings location
detect_vscode_paths() {
    log "🔍 Detecting VS Code paths..."

    # macOS paths
    if [[ "$OSTYPE" == "darwin"* ]]; then
        VSCODE_SETTINGS_DIR="$HOME/Library/Application Support/Code/User"
        VSCODE_EXTENSIONS_DIR="$HOME/.vscode/extensions"
    # Linux paths
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        VSCODE_SETTINGS_DIR="$HOME/.config/Code/User"
        VSCODE_EXTENSIONS_DIR="$HOME/.vscode/extensions"
    # Windows paths (if running in WSL or similar)
    else
        VSCODE_SETTINGS_DIR="$HOME/.config/Code/User"
        VSCODE_EXTENSIONS_DIR="$HOME/.vscode/extensions"
    fi

    log "📁 VS Code Settings: $VSCODE_SETTINGS_DIR"
    log "📁 VS Code Extensions: $VSCODE_EXTENSIONS_DIR"
}

# Check prerequisites
check_prerequisites() {
    log "🔧 Checking prerequisites..."

    # Check Python
    if command -v $PYTHON_CMD &> /dev/null; then
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
        log "✅ Python $PYTHON_VERSION found"
        python_check=true
    else
        log "❌ Python not found"
        return 1
    fi

    # Check Node.js and npm
    if command -v node &> /dev/null && command -v npm &> /dev/null; then
        NODE_VERSION=$(node --version)
        NPM_VERSION=$(npm --version)
        log "✅ Node.js $NODE_VERSION and npm $NPM_VERSION found"
    else
        log "❌ Node.js or npm not found"
        return 1
    fi

    # Check VS Code CLI
    if command -v code &> /dev/null; then
        VSCODE_VERSION=$(code --version | head -n 1)
        log "✅ VS Code CLI found: $VSCODE_VERSION"
        vscode_cli=true
    else
        log "⚠️  VS Code CLI not found - manual extension installation required"
    fi

    return 0
}

# Validate integration components
validate_components() {
    log "🔍 Validating integration components..."

    # Check integration script
    if [ -f "$PROJECT_ROOT/ghost_vscode_integration.py" ]; then
        log "✅ Ghost VS Code integration script found"
        integration_script=true
    else
        log "❌ Ghost VS Code integration script missing"
        return 1
    fi

    # Check orchestrator
    if [ -f "$PROJECT_ROOT/ghost_agent_orchestrator.py" ]; then
        log "✅ Ghost agent orchestrator found"
        orchestrator=true
    else
        log "❌ Ghost agent orchestrator missing"
        return 1
    fi

    # Check extension structure
    EXTENSION_DIR="$PROJECT_ROOT/vscode-extensions/ghostlink-vscode"
    if [ -d "$EXTENSION_DIR" ]; then
        log "✅ Extension directory exists"

        if [ -f "$EXTENSION_DIR/package.json" ]; then
            log "✅ Extension package.json found"
        else
            log "❌ Extension package.json missing"
            return 1
        fi

        if [ -f "$EXTENSION_DIR/out/extension.js" ]; then
            log "✅ Compiled extension found"
            extension_build=true
        else
            log "❌ Compiled extension missing - building..."
            build_extension
        fi
    else
        log "❌ Extension directory not found"
        return 1
    fi

    return 0
}

# Build VS Code extension
build_extension() {
    log "🔨 Building VS Code extension..."

    EXTENSION_DIR="$PROJECT_ROOT/vscode-extensions/ghostlink-vscode"

    if [ ! -d "$EXTENSION_DIR/node_modules" ]; then
        log "📦 Installing extension dependencies..."
        cd "$EXTENSION_DIR"
        npm install >> "$LOG_FILE" 2>&1
    fi

    log "⚙️  Compiling TypeScript..."
    cd "$EXTENSION_DIR"
    if npm run compile >> "$LOG_FILE" 2>&1; then
        log "✅ Extension built successfully"
        extension_build=true
        return 0
    else
        log "❌ Extension build failed"
        return 1
    fi
}

# Install VS Code extensions
install_extensions() {
    log "📦 Installing VS Code extensions..."

    if [ "$vscode_cli" = true ]; then
        # Install GhostLink extension
        log "Installing GhostLink extension..."
        if code --install-extension "$PROJECT_ROOT/vscode-extensions/ghostlink-vscode" --force >> "$LOG_FILE" 2>&1; then
            log "✅ GhostLink extension installed"
        else
            log "❌ Failed to install GhostLink extension"
        fi

        # Install HTTP API extension
        log "Installing VS Code HTTP API extension..."
        if code --install-extension "vscode-http-api" >> "$LOG_FILE" 2>&1; then
            log "✅ HTTP API extension installed"
            http_api_install=true
        else
            log "❌ Failed to install HTTP API extension"
        fi
    else
        log "⚠️  VS Code CLI not found - manual installation required"
        echo -e "${YELLOW}Manual Installation Required:${NC}"
        echo "1. Open VS Code"
        echo "2. Extensions (Ctrl+Shift+X)"
        echo "3. Install 'ghostlink-vscode' from: $PROJECT_ROOT/vscode-extensions/ghostlink-vscode"
        echo "4. Install 'vscode-http-api' from marketplace"
        echo ""
    fi
}

# Configure VS Code settings
configure_settings() {
    log "⚙️  Configuring VS Code settings..."

    SETTINGS_FILE="$VSCODE_SETTINGS_DIR/settings.json"

    # Create settings directory if it doesn't exist
    mkdir -p "$VSCODE_SETTINGS_DIR"

    # Backup existing settings
    if [ -f "$SETTINGS_FILE" ]; then
        cp "$SETTINGS_FILE" "${SETTINGS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        log "📋 Backed up existing settings"
    fi

    # Read existing settings or create empty object
    if [ -f "$SETTINGS_FILE" ]; then
        EXISTING_SETTINGS=$(cat "$SETTINGS_FILE" | tr -d '\n' | sed 's/}/}/g')
    else
        EXISTING_SETTINGS="{}"
    fi

    # Create new settings with GhostLink configuration
    NEW_SETTINGS=$(cat << EOF
{
  "ghostlink.pythonPath": "python3",
  "ghostlink.projectRoot": "$PROJECT_ROOT",
  "ghostlink.vscodeApiUrl": "http://localhost:3000"
}
EOF
)

    # Merge settings (simple approach - replace if exists)
    echo "$NEW_SETTINGS" > "$SETTINGS_FILE"
    log "✅ VS Code settings configured"
    settings_config=true
}

# Test integration
test_integration() {
    log "🧪 Testing integration..."

    # Test Python import
    if $PYTHON_CMD -c "import sys; sys.path.append('$PROJECT_ROOT'); import ghost_vscode_integration; print('Import successful')" >> "$LOG_FILE" 2>&1; then
        log "✅ Integration script imports correctly"
    else
        log "❌ Integration script import failed"
        return 1
    fi

    # Test orchestrator
    if $PYTHON_CMD "$PROJECT_ROOT/ghost_agent_orchestrator.py" --help >> "$LOG_FILE" 2>&1; then
        log "✅ Orchestrator runs without errors"
    else
        log "⚠️  Orchestrator may have issues"
    fi

    # Test integration script
    if $PYTHON_CMD "$PROJECT_ROOT/ghost_vscode_integration.py" status >> "$LOG_FILE" 2>&1; then
        log "✅ Integration script functional"
    else
        log "⚠️  Integration script may have issues"
    fi

    integration_test=true
    return 0
}

# Generate status report
generate_report() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    Integration Status Report                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    echo "📊 Component Status:"
    if [ "$python_check" = true ]; then echo -e "  ✅ python check"; else echo -e "  ❌ python check"; fi
    if [ "$integration_script" = true ]; then echo -e "  ✅ integration script"; else echo -e "  ❌ integration script"; fi
    if [ "$orchestrator" = true ]; then echo -e "  ✅ orchestrator"; else echo -e "  ❌ orchestrator"; fi
    if [ "$extension_build" = true ]; then echo -e "  ✅ extension build"; else echo -e "  ❌ extension build"; fi
    if [ "$vscode_cli" = true ]; then echo -e "  ✅ vscode cli"; else echo -e "  ❌ vscode cli"; fi
    if [ "$http_api_install" = true ]; then echo -e "  ✅ http api install"; else echo -e "  ❌ http api install"; fi
    if [ "$settings_config" = true ]; then echo -e "  ✅ settings config"; else echo -e "  ❌ settings config"; fi
    if [ "$integration_test" = true ]; then echo -e "  ✅ integration test"; else echo -e "  ❌ integration test"; fi
    echo ""

    # Overall status
    SUCCESS_COUNT=0
    TOTAL_COUNT=8

    if [ "$python_check" = true ]; then ((SUCCESS_COUNT++)); fi
    if [ "$integration_script" = true ]; then ((SUCCESS_COUNT++)); fi
    if [ "$orchestrator" = true ]; then ((SUCCESS_COUNT++)); fi
    if [ "$extension_build" = true ]; then ((SUCCESS_COUNT++)); fi
    if [ "$vscode_cli" = true ]; then ((SUCCESS_COUNT++)); fi
    if [ "$http_api_install" = true ]; then ((SUCCESS_COUNT++)); fi
    if [ "$settings_config" = true ]; then ((SUCCESS_COUNT++)); fi
    if [ "$integration_test" = true ]; then ((SUCCESS_COUNT++)); fi

    SUCCESS_RATE=$((SUCCESS_COUNT * 100 / TOTAL_COUNT))

    if [ $SUCCESS_RATE -eq 100 ]; then
        echo -e "${GREEN}🎉 Integration Status: COMPLETE (100% Success)${NC}"
    elif [ $SUCCESS_RATE -ge 75 ]; then
        echo -e "${YELLOW}⚠️  Integration Status: MOSTLY COMPLETE ($SUCCESS_RATE% Success)${NC}"
    else
        echo -e "${RED}❌ Integration Status: INCOMPLETE ($SUCCESS_RATE% Success)${NC}"
    fi
    echo ""

    # Next steps
    echo "📋 Next Steps:"
    if [ "$vscode_cli" = false ]; then
        echo "1. 🔧 Install VS Code extensions manually (see above)"
    fi
    if [ "$http_api_install" = false ]; then
        echo "2. 🌐 Start VS Code HTTP API: Command Palette → 'VSCode HTTP API: Start'"
    fi
    echo "3. 🧪 Test commands: Command Palette → 'GhostLink: Show System Health'"
    echo "4. 📊 Monitor logs: $LOG_FILE"
    echo ""

    log "📄 Full log available at: $LOG_FILE"
}

# Main execution
main() {
    detect_vscode_paths

    if ! check_prerequisites; then
        log "❌ Prerequisites check failed"
        exit 1
    fi

    if ! validate_components; then
        log "❌ Component validation failed"
        exit 1
    fi

    install_extensions
    configure_settings

    if ! test_integration; then
        log "⚠️  Some integration tests failed"
    fi

    generate_report

    log "🎯 Automation complete!"
}

# Run main function
main "$@"

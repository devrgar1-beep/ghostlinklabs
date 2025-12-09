#!/bin/bash
# IDE integration for GhostLink

# Create VS Code extension directory
mkdir -p "$HOME/.vscode/extensions/ghostlink-integration-1.0.0"

# Create package.json
cat > "$HOME/.vscode/extensions/ghostlink-integration-1.0.0/package.json" << 'PKG_EOF'
{
  "name": "ghostlink-integration",
  "displayName": "GhostLink AI Integration",
  "description": "Deep integration with GhostLink AI",
  "version": "1.0.0",
  "engines": { "vscode": "^1.74.0" },
  "activationEvents": ["onStartupFinished"],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "ghostlink.analyzeCode",
        "title": "GhostLink: Analyze Code"
      },
      {
        "command": "ghostlink.optimizeCode",
        "title": "GhostLink: Optimize Code"
      }
    ],
    "keybindings": [
      {
        "command": "ghostlink.analyzeCode",
        "key": "ctrl+alt+g a"
      }
    ]
  }
}
PKG_EOF

# Create extension source
mkdir -p "$HOME/.vscode/extensions/ghostlink-integration-1.0.0/src"
cat > "$HOME/.vscode/extensions/ghostlink-integration-1.0.0/src/extension.js" << 'EXT_EOF'
// GhostLink VS Code Extension
const vscode = require('vscode');

function activate(context) {
    console.log('GhostLink extension active');

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('ghostlink.analyzeCode', () => {
            vscode.window.showInformationMessage('GhostLink: Analyzing code...');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('ghostlink.optimizeCode', () => {
            vscode.window.showInformationMessage('GhostLink: Optimizing code...');
        })
    );
}

function deactivate() {}

module.exports = { activate, deactivate };
EXT_EOF

# Create VS Code settings
mkdir -p "$HOME/Library/Application Support/Code/User"
cat >> "$HOME/Library/Application Support/Code/User/settings.json" << 'SET_EOF'

// GhostLink IDE Integration
"ghostlink.api.url": "http://localhost:8080",
"ghostlink.api.key": "ghostlink_secure_key_2025",
"ghostlink.autoAnalyze": true,
SET_EOF

echo "✅ IDE integration complete!"
echo "Restart VS Code to activate extension"

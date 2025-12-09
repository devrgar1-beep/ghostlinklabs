#!/bin/bash
# ==========================================
# GHOSTLINK IDE INTEGRATION SCRIPT
# ==========================================
# Deep IDE integration for GhostLink AI
# Creates VS Code extensions, keybindings, and custom commands

set -e

# Configuration
GHOSTLINK_ROOT="/Users/ghost-link-labs/ghostlinklabs"
VSCODE_USER_DIR="$HOME/Library/Application Support/Code/User"
VSCODE_EXTENSIONS_DIR="$HOME/.vscode/extensions"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
}

# Error handling
error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    log "ERROR: $1"
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
    log "SUCCESS: $1"
}

# Info message
info() {
    echo -e "${BLUE}INFO: $1${NC}"
    log "INFO: $1"
}

# Create VS Code extension directory
create_extension_dir() {
    info "Creating VS Code GhostLink extension..."

    EXTENSION_DIR="$VSCODE_EXTENSIONS_DIR/ghostlink.ghostlink-integration-1.0.0"

    mkdir -p "$EXTENSION_DIR"

    # Create package.json
    cat > "$EXTENSION_DIR/package.json" << 'EOF'
{
  "name": "ghostlink-integration",
  "displayName": "GhostLink AI Integration",
  "description": "Deep integration with GhostLink AI for automated development",
  "version": "1.0.0",
  "engines": {
    "vscode": "^1.74.0"
  },
  "categories": [
    "Other",
    "Snippets",
    "Programming Languages"
  ],
  "activationEvents": [
    "onStartupFinished",
    "onCommand:ghostlink.analyzeCode",
    "onCommand:ghostlink.optimizeCode",
    "onCommand:ghostlink.runAutomation",
    "onCommand:ghostlink.showDashboard",
    "onCommand:ghostlink.startMonitoring"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "ghostlink.analyzeCode",
        "title": "GhostLink: Analyze Code",
        "category": "GhostLink"
      },
      {
        "command": "ghostlink.optimizeCode",
        "title": "GhostLink: Optimize Code",
        "category": "GhostLink"
      },
      {
        "command": "ghostlink.runAutomation",
        "title": "GhostLink: Run Automation",
        "category": "GhostLink"
      },
      {
        "command": "ghostlink.showDashboard",
        "title": "GhostLink: Show Dashboard",
        "category": "GhostLink"
      },
      {
        "command": "ghostlink.startMonitoring",
        "title": "GhostLink: Start Monitoring",
        "category": "GhostLink"
      }
    ],
    "keybindings": [
      {
        "command": "ghostlink.analyzeCode",
        "key": "ctrl+alt+g a",
        "mac": "cmd+alt+g a",
        "when": "editorTextFocus"
      },
      {
        "command": "ghostlink.optimizeCode",
        "key": "ctrl+alt+g o",
        "mac": "cmd+alt+g o",
        "when": "editorTextFocus"
      },
      {
        "command": "ghostlink.runAutomation",
        "key": "ctrl+alt+g r",
        "mac": "cmd+alt+g r",
        "when": "editorTextFocus"
      }
    ],
    "menus": {
      "editor/context": [
        {
          "command": "ghostlink.analyzeCode",
          "when": "editorTextFocus",
          "group": "ghostlink@1"
        },
        {
          "command": "ghostlink.optimizeCode",
          "when": "editorTextFocus",
          "group": "ghostlink@2"
        },
        {
          "command": "ghostlink.runAutomation",
          "when": "editorTextFocus",
          "group": "ghostlink@3"
        }
      ],
      "commandPalette": [
        {
          "command": "ghostlink.analyzeCode",
          "when": "editorTextFocus"
        },
        {
          "command": "ghostlink.optimizeCode",
          "when": "editorTextFocus"
        },
        {
          "command": "ghostlink.runAutomation"
        },
        {
          "command": "ghostlink.showDashboard"
        },
        {
          "command": "ghostlink.startMonitoring"
        }
      ]
    },
    "configuration": {
      "title": "GhostLink AI Integration",
      "properties": {
        "ghostlink.api.url": {
          "type": "string",
          "default": "http://localhost:8080",
          "description": "GhostLink API URL"
        },
        "ghostlink.api.key": {
          "type": "string",
          "default": "ghostlink_secure_key_2025",
          "description": "GhostLink API Key"
        },
        "ghostlink.autoAnalyze": {
          "type": "boolean",
          "default": true,
          "description": "Automatically analyze code on save"
        },
        "ghostlink.autoOptimize": {
          "type": "boolean",
          "default": false,
          "description": "Automatically optimize code on save"
        },
        "ghostlink.monitoring.enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable real-time monitoring"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./",
    "pretest": "npm run compile && npm run lint",
    "lint": "eslint src --ext ts",
    "test": "node ./out/test/runTest.js"
  },
  "devDependencies": {
    "@types/vscode": "^1.74.0",
    "@types/node": "16.x",
    "eslint": "^8.28.0",
    "typescript": "^4.9.4"
  },
  "dependencies": {
    "axios": "^1.2.2"
  }
}
EOF

    success "VS Code extension package.json created"
}

# Create extension TypeScript source
create_extension_source() {
    info "Creating extension source code..."

    mkdir -p "$EXTENSION_DIR/src"
    mkdir -p "$EXTENSION_DIR/out"

    # Create extension.ts
    cat > "$EXTENSION_DIR/src/extension.ts" << 'EOF'
import * as vscode from 'vscode';
import axios from 'axios';

let statusBarItem: vscode.StatusBarItem;
let monitoringTimer: NodeJS.Timeout | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('GhostLink AI Integration extension is now active!');

    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'ghostlink.showDashboard';
    context.subscriptions.push(statusBarItem);
    updateStatusBar();

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('ghostlink.analyzeCode', analyzeCode),
        vscode.commands.registerCommand('ghostlink.optimizeCode', optimizeCode),
        vscode.commands.registerCommand('ghostlink.runAutomation', runAutomation),
        vscode.commands.registerCommand('ghostlink.showDashboard', showDashboard),
        vscode.commands.registerCommand('ghostlink.startMonitoring', startMonitoring)
    );

    // Auto-analyze on save if enabled
    if (vscode.workspace.getConfiguration('ghostlink').get('autoAnalyze', true)) {
        context.subscriptions.push(
            vscode.workspace.onDidSaveTextDocument((document) => {
                if (document.languageId !== 'log' && document.languageId !== 'json') {
                    analyzeCode();
                }
            })
        );
    }

    // Start monitoring if enabled
    if (vscode.workspace.getConfiguration('ghostlink').get('monitoring.enabled', true)) {
        startMonitoring();
    }
}

export function deactivate() {
    if (monitoringTimer) {
        clearInterval(monitoringTimer);
    }
    if (statusBarItem) {
        statusBarItem.dispose();
    }
}

async function getApiConfig() {
    const config = vscode.workspace.getConfiguration('ghostlink');
    return {
        baseURL: config.get('api.url', 'http://localhost:8080'),
        headers: {
            'Authorization': `Bearer ${config.get('api.key', 'ghostlink_secure_key_2025')}`,
            'Content-Type': 'application/json'
        }
    };
}

async function analyzeCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor');
        return;
    }

    const document = editor.document;
    const code = document.getText();
    const language = document.languageId;

    try {
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'GhostLink AI Analysis',
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 0, message: 'Analyzing code...' });

            const config = await getApiConfig();
            const response = await axios.post(`${config.baseURL}/analyze/code`, {
                code: code,
                language: language,
                filename: document.fileName
            }, { headers: config.headers });

            progress.report({ increment: 100, message: 'Analysis complete' });

            const result = response.data;

            // Show results in output channel
            const outputChannel = vscode.window.createOutputChannel('GhostLink Analysis');
            outputChannel.clear();
            outputChannel.appendLine('🔍 GhostLink Code Analysis Results');
            outputChannel.appendLine('=' .repeat(50));
            outputChannel.appendLine(`Language: ${language}`);
            outputChannel.appendLine(`File: ${document.fileName}`);
            outputChannel.appendLine('');

            if (result.suggestions && result.suggestions.length > 0) {
                outputChannel.appendLine('💡 Suggestions:');
                result.suggestions.forEach((suggestion: string, index: number) => {
                    outputChannel.appendLine(`  ${index + 1}. ${suggestion}`);
                });
                outputChannel.appendLine('');
            }

            if (result.metrics) {
                outputChannel.appendLine('📊 Metrics:');
                Object.entries(result.metrics).forEach(([key, value]) => {
                    outputChannel.appendLine(`  ${key}: ${value}`);
                });
                outputChannel.appendLine('');
            }

            outputChannel.show();

            // Show notification
            const score = result.overall_score || 0;
            if (score >= 80) {
                vscode.window.showInformationMessage(`✅ Code analysis complete! Score: ${score}/100`);
            } else if (score >= 60) {
                vscode.window.showWarningMessage(`⚠️ Code analysis complete. Score: ${score}/100 - Review suggestions`);
            } else {
                vscode.window.showErrorMessage(`❌ Code analysis complete. Score: ${score}/100 - Major improvements needed`);
            }

        });
    } catch (error) {
        vscode.window.showErrorMessage(`GhostLink analysis failed: ${error}`);
    }
}

async function optimizeCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor');
        return;
    }

    const document = editor.document;
    const code = document.getText();
    const language = document.languageId;

    try {
        const optimized = await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'GhostLink AI Optimization',
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 0, message: 'Optimizing code...' });

            const config = await getApiConfig();
            const response = await axios.post(`${config.baseURL}/optimize/code`, {
                code: code,
                language: language,
                filename: document.fileName
            }, { headers: config.headers });

            progress.report({ increment: 100, message: 'Optimization complete' });
            return response.data;
        });

        if (optimized.optimized_code && optimized.optimized_code !== code) {
            // Show diff
            const originalUri = document.uri;
            const optimizedUri = vscode.Uri.parse(`ghostlink-optimized:${document.fileName}`);

            const optimizedDoc = await vscode.workspace.openTextDocument({
                content: optimized.optimized_code,
                language: language
            });

            await vscode.commands.executeCommand('vscode.diff', originalUri, optimizedUri, 'Original ↔ Optimized');

            // Ask to apply changes
            const apply = await vscode.window.showInformationMessage(
                'Optimized code generated. Apply changes?',
                'Apply',
                'Cancel'
            );

            if (apply === 'Apply') {
                const edit = new vscode.WorkspaceEdit();
                const fullRange = new vscode.Range(
                    document.positionAt(0),
                    document.positionAt(document.getText().length)
                );
                edit.replace(document.uri, fullRange, optimized.optimized_code);
                await vscode.workspace.applyEdit(edit);
                vscode.window.showInformationMessage('✅ Code optimized successfully!');
            }
        } else {
            vscode.window.showInformationMessage('ℹ️ No optimizations available for this code');
        }

    } catch (error) {
        vscode.window.showErrorMessage(`GhostLink optimization failed: ${error}`);
    }
}

async function runAutomation() {
    const taskName = await vscode.window.showInputBox({
        prompt: 'Enter automation task name',
        placeHolder: 'e.g., code-review, test-run, deploy'
    });

    if (!taskName) return;

    const paramsInput = await vscode.window.showInputBox({
        prompt: 'Enter task parameters (JSON)',
        placeHolder: '{"key": "value"}'
    });

    let parameters = {};
    if (paramsInput) {
        try {
            parameters = JSON.parse(paramsInput);
        } catch (error) {
            vscode.window.showErrorMessage('Invalid JSON parameters');
            return;
        }
    }

    try {
        const result = await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'GhostLink Automation',
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 0, message: `Running ${taskName}...` });

            const config = await getApiConfig();
            const response = await axios.post(`${config.baseURL}/automation/execute`, {
                task: taskName,
                parameters: parameters,
                context: {
                    vscode: true,
                    workspace: vscode.workspace.name,
                    activeFile: vscode.window.activeTextEditor?.document.fileName
                }
            }, { headers: config.headers });

            progress.report({ increment: 100, message: 'Task completed' });
            return response.data;
        });

        // Show results
        const outputChannel = vscode.window.createOutputChannel('GhostLink Automation');
        outputChannel.clear();
        outputChannel.appendLine(`🤖 Automation Task: ${taskName}`);
        outputChannel.appendLine('=' .repeat(50));

        if (result.output) {
            outputChannel.appendLine('📤 Output:');
            outputChannel.appendLine(result.output);
        }

        if (result.metrics) {
            outputChannel.appendLine('📊 Metrics:');
            Object.entries(result.metrics).forEach(([key, value]) => {
                outputChannel.appendLine(`  ${key}: ${value}`);
            });
        }

        outputChannel.show();

        vscode.window.showInformationMessage(`✅ Automation task '${taskName}' completed successfully!`);

    } catch (error) {
        vscode.window.showErrorMessage(`Automation failed: ${error}`);
    }
}

async function showDashboard() {
    try {
        const config = await getApiConfig();
        const response = await axios.get(`${config.baseURL}/dashboard`, {
            headers: config.headers
        });

        const dashboardData = response.data;

        // Create webview panel
        const panel = vscode.window.createWebviewPanel(
            'ghostlinkDashboard',
            'GhostLink Dashboard',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                localResourceRoots: []
            }
        );

        panel.webview.html = getDashboardHtml(dashboardData);

    } catch (error) {
        vscode.window.showErrorMessage(`Failed to load dashboard: ${error}`);
    }
}

function getDashboardHtml(data: any): string {
    return `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>GhostLink Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .metric { background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .metric h3 { margin: 0 0 5px 0; color: #007acc; }
        .metric .value { font-size: 24px; font-weight: bold; }
        .status { padding: 5px 10px; border-radius: 3px; color: white; }
        .status.active { background: #28a745; }
        .status.inactive { background: #dc3545; }
    </style>
</head>
<body>
    <h1>🔗 GhostLink AI Dashboard</h1>

    <div class="metric">
        <h3>System Status</h3>
        <span class="status ${data.status === 'active' ? 'active' : 'inactive'}">${data.status}</span>
    </div>

    <div class="metric">
        <h3>Active Tasks</h3>
        <div class="value">${data.active_tasks || 0}</div>
    </div>

    <div class="metric">
        <h3>CPU Usage</h3>
        <div class="value">${data.cpu_usage || 0}%</div>
    </div>

    <div class="metric">
        <h3>Memory Usage</h3>
        <div class="value">${data.memory_usage || 0}%</div>
    </div>

    <div class="metric">
        <h3>Automation Tasks Completed</h3>
        <div class="value">${data.completed_tasks || 0}</div>
    </div>
</body>
</html>`;
}

async function startMonitoring() {
    if (monitoringTimer) {
        clearInterval(monitoringTimer);
    }

    monitoringTimer = setInterval(async () => {
        try {
            const config = await getApiConfig();
            const response = await axios.get(`${config.baseURL}/health`, {
                headers: config.headers
            });

            updateStatusBar(response.data);
        } catch (error) {
            updateStatusBar({ status: 'disconnected' });
        }
    }, 30000); // Update every 30 seconds

    vscode.window.showInformationMessage('GhostLink monitoring started');
}

function updateStatusBar(data?: any) {
    if (!statusBarItem) return;

    const status = data?.status || 'unknown';
    const tasks = data?.active_tasks || 0;

    statusBarItem.text = `$(robot) GhostLink: ${status} (${tasks})`;
    statusBarItem.tooltip = `GhostLink AI - Status: ${status}, Active Tasks: ${tasks}`;
    statusBarItem.show();
}
EOF

    # Create tsconfig.json
    cat > "$EXTENSION_DIR/tsconfig.json" << 'EOF'
{
  "compilerOptions": {
    "module": "commonjs",
    "target": "ES2020",
    "outDir": "out",
    "lib": ["ES2020"],
    "sourceMap": true,
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "exclude": [
    "node_modules",
    "**/*.test.ts"
  ]
}
EOF

    success "Extension source code created"
}

# Create VS Code snippets
create_snippets() {
    info "Creating VS Code snippets..."

    # Python snippets
    cat > "$VSCODE_USER_DIR/snippets/python-ghostlink.json" << 'EOF'
{
  "GhostLink Function Template": {
    "prefix": "gl-func",
    "body": [
      "def ${1:function_name}(${2:parameters}):",
      "    \"\"\"",
      "    ${3:Description}",
      "    ",
      "    Args:",
      "        ${2}: ${4:Parameter description}",
      "    ",
      "    Returns:",
      "        ${5:Return type}: ${6:Return description}",
      "    \"\"\"",
      "    # GhostLink AI analyzed - ${7:analysis_date}",
      "    ${8:pass}",
      "",
      "    return ${9:result}"
    ],
    "description": "GhostLink-optimized Python function template"
  },

  "GhostLink Class Template": {
    "prefix": "gl-class",
    "body": [
      "class ${1:ClassName}:",
      "    \"\"\"",
      "    ${2:Description}",
      "    ",
      "    Attributes:",
      "        ${3:attribute}: ${4:Attribute description}",
      "    \"\"\"",
      "",
      "    def __init__(self, ${5:parameters}):",
      "        \"\"\"Initialize ${1}.\"\"\"",
      "        # GhostLink AI analyzed - ${6:analysis_date}",
      "        ${7:self.attribute = parameter}",
      "",
      "    def ${8:method_name}(self, ${9:parameters}):",
      "        \"\"\"${10:Method description}\"\"\"",
      "        # GhostLink AI optimized",
      "        ${11:pass}",
      "",
      "        return ${12:result}"
    ],
    "description": "GhostLink-optimized Python class template"
  },

  "GhostLink Async Function": {
    "prefix": "gl-async",
    "body": [
      "async def ${1:function_name}(${2:parameters}):",
      "    \"\"\"",
      "    ${3:Description - GhostLink AI optimized for async operations}",
      "    \"\"\"",
      "    try:",
      "        # GhostLink AI analyzed - ${4:analysis_date}",
      "        ${5:async_operation}",
      "        return ${6:result}",
      "    except Exception as e:",
      "        # GhostLink AI error handling",
      "        logger.error(f\"${1} failed: {e}\")",
      "        raise"
    ],
    "description": "GhostLink-optimized async function template"
  }
}
EOF

    # JavaScript/TypeScript snippets
    cat > "$VSCODE_USER_DIR/snippets/javascript-ghostlink.json" << 'EOF'
{
  "GhostLink Function": {
    "prefix": "gl-func",
    "body": [
      "/**",
      " * ${1:function description}",
      " * @param {${2:type}} ${3:param} - ${4:param description}",
      " * @returns {${5:type}} ${6:return description}",
      " * @analyzed-by GhostLink AI - ${7:analysis_date}",
      " */",
      "function ${8:functionName}(${3}) {",
      "    // GhostLink AI optimized",
      "    ${9:implementation}",
      "    return ${10:result};",
      "}"
    ],
    "description": "GhostLink-optimized JavaScript function"
  },

  "GhostLink Async Function": {
    "prefix": "gl-async",
    "body": [
      "/**",
      " * ${1:function description}",
      " * @param {${2:type}} ${3:param} - ${4:param description}",
      " * @returns {Promise<${5:type}>} ${6:return description}",
      " * @analyzed-by GhostLink AI - ${7:analysis_date}",
      " */",
      "async function ${8:functionName}(${3}) {",
      "    try {",
      "        // GhostLink AI optimized async operation",
      "        ${9:await operation;}",
      "        return ${10:result};",
      "    } catch (error) {",
      "        // GhostLink AI error handling",
      "        console.error(`${8:functionName} failed:`, error);",
      "        throw error;",
      "    }",
      "}"
    ],
    "description": "GhostLink-optimized async JavaScript function"
  },

  "GhostLink React Component": {
    "prefix": "gl-component",
    "body": [
      "import React, { useState, useEffect } from 'react';",
      "",
      "/**",
      " * ${1:Component description}",
      " * @analyzed-by GhostLink AI - ${2:analysis_date}",
      " */",
      "const ${3:ComponentName} = ({ ${4:props} }) => {",
      "    // GhostLink AI optimized state management",
      "    const [${5:state}, set${6:State}] = useState(${7:initialValue});",
      "",
      "    useEffect(() => {",
      "        // GhostLink AI optimized effect",
      "        ${8:effect logic}",
      "    }, [${9:dependencies}]);",
      "",
      "    const ${10:handlerName} = () => {",
      "        // GhostLink AI optimized handler",
      "        ${11:handler logic}",
      "    };",
      "",
      "    return (",
      "        <div className=\"${12:component-class}\">",
      "            {/* GhostLink AI optimized JSX */}",
      "            <h1>${3:ComponentName}</h1>",
      "            ${13:jsx content}",
      "        </div>",
      "    );",
      "};",
      "",
      "export default ${3:ComponentName};"
    ],
    "description": "GhostLink-optimized React component template"
  }
}
EOF

    success "VS Code snippets created"
}

# Create custom keybindings
create_keybindings() {
    info "Creating custom keybindings..."

    cat > "$VSCODE_USER_DIR/keybindings.json" << 'EOF'
// GhostLink AI Integration Keybindings
[
  // GhostLink Commands
  {
    "key": "ctrl+alt+g a",
    "command": "ghostlink.analyzeCode",
    "when": "editorTextFocus",
    "args": null
  },
  {
    "key": "ctrl+alt+g o",
    "command": "ghostlink.optimizeCode",
    "when": "editorTextFocus",
    "args": null
  },
  {
    "key": "ctrl+alt+g r",
    "command": "ghostlink.runAutomation",
    "when": "editorTextFocus",
    "args": null
  },
  {
    "key": "ctrl+alt+g d",
    "command": "ghostlink.showDashboard",
    "args": null
  },
  {
    "key": "ctrl+alt+g m",
    "command": "ghostlink.startMonitoring",
    "args": null
  },

  // Enhanced Development Workflow
  {
    "key": "ctrl+alt+g s",
    "command": "workbench.action.files.save",
    "when": "editorTextFocus",
    "args": null
  },
  {
    "key": "ctrl+alt+g t",
    "command": "workbench.action.tasks.runTask",
    "when": "editorTextFocus",
    "args": "test"
  },
  {
    "key": "ctrl+alt+g b",
    "command": "workbench.action.tasks.runTask",
    "when": "editorTextFocus",
    "args": "build"
  },

  // Quick Navigation
  {
    "key": "ctrl+alt+g p",
    "command": "workbench.action.quickOpen",
    "args": ">ghostlink"
  },
  {
    "key": "ctrl+alt+g l",
    "command": "workbench.action.showCommands",
    "args": null
  }
]
EOF

    success "Custom keybindings created"
}

# Create custom settings
create_custom_settings() {
    info "Creating custom VS Code settings..."

    # Read existing settings
    if [ -f "$VSCODE_USER_DIR/settings.json" ]; then
        cp "$VSCODE_USER_DIR/settings.json" "$VSCODE_USER_DIR/settings.json.backup"
    fi

    # Add GhostLink-specific settings
    cat >> "$VSCODE_USER_DIR/settings.json" << 'EOF'

// ==========================================
// GHOSTLINK IDE INTEGRATION SETTINGS
// ==========================================

  // GhostLink Extension Configuration
  "ghostlink.api.url": "http://localhost:8080",
  "ghostlink.api.key": "ghostlink_secure_key_2025",
  "ghostlink.autoAnalyze": true,
  "ghostlink.autoOptimize": false,
  "ghostlink.monitoring.enabled": true,

  // Enhanced Editor Experience
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit",
    "source.organizeImports": "explicit",
    "ghostlink.optimizeCode": "explicit"
  },
  "editor.quickSuggestions": {
    "other": true,
    "comments": true,
    "strings": true
  },
  "editor.suggestOnTriggerCharacters": true,

  // AI-Powered IntelliSense
  "editor.inlineSuggest.enabled": true,
  "editor.suggest.preview": true,
  "editor.acceptSuggestionOnEnter": "smart",

  // Enhanced File Watching
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/.git/subtree-cache/**": true,
    "**/node_modules/**": true,
    "**/__pycache__/**": true,
    "**/.venv/**": true,
    "**/ghostlink_cache/**": true
  },

  // GhostLink Task Integration
  "task.autoDetect": "on",
  "task.problemMatchers.neverPrompt": true,
  "task.saveBeforeRun": "always",

  // Enhanced Git Integration
  "git.autofetch": true,
  "git.autostash": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true,

  // GhostLink Language Support
  "python.analysis.autoImportCompletions": true,
  "python.analysis.typeCheckingMode": "basic",
  "typescript.suggest.autoImports": true,
  "javascript.suggest.autoImports": true,

  // Enhanced Terminal Integration
  "terminal.integrated.shellIntegration.enabled": true,
  "terminal.integrated.automationProfile.osx": "zsh",
  "terminal.integrated.defaultProfile.osx": "zsh",

  // GhostLink Workspace Trust
  "security.workspace.trust.enabled": false,
  "security.workspace.trust.untrustedFiles": "open",

  // Performance Optimizations
  "workbench.editor.enablePreview": false,
  "workbench.quickOpen.closeOnFocusLost": false,
  "window.newWindowProfile": "Default"
}
EOF

    success "Custom VS Code settings added"
}

# Create tasks.json for automation
create_tasks() {
    info "Creating VS Code tasks for GhostLink automation..."

    mkdir -p "$VSCODE_USER_DIR"

    cat > "$VSCODE_USER_DIR/tasks.json" << 'EOF'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "GhostLink: Analyze Current File",
      "type": "shell",
      "command": "cd '${workspaceFolder}' && python3 -c \"import requests; requests.post('http://localhost:8080/analyze/file', json={'file': '${file}', 'language': '${languageId}'}).raise_for_status()\"",
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "silent",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    },
    {
      "label": "GhostLink: Optimize Workspace",
      "type": "shell",
      "command": "cd '${workspaceFolder}' && python3 -c \"import requests; requests.post('http://localhost:8080/optimize/workspace', json={'path': '${workspaceFolder}'}).raise_for_status()\"",
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    },
    {
      "label": "GhostLink: Run Tests",
      "type": "shell",
      "command": "cd '${workspaceFolder}' && python3 -c \"import requests; requests.post('http://localhost:8080/automation/execute', json={'task': 'run-tests', 'parameters': {'path': '${workspaceFolder}'}}).raise_for_status()\"",
      "group": "test",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    },
    {
      "label": "GhostLink: Deploy",
      "type": "shell",
      "command": "cd '${workspaceFolder}' && python3 -c \"import requests; requests.post('http://localhost:8080/automation/execute', json={'task': 'deploy', 'parameters': {'environment': 'production'}}).raise_for_status()\"",
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    },
    {
      "label": "GhostLink: Security Scan",
      "type": "shell",
      "command": "cd '${workspaceFolder}' && python3 -c \"import requests; requests.post('http://localhost:8080/security/scan', json={'target': '${workspaceFolder}'}).raise_for_status()\"",
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    },
    {
      "label": "GhostLink: Performance Analysis",
      "type": "shell",
      "command": "cd '${workspaceFolder}' && python3 -c \"import requests; requests.post('http://localhost:8080/performance/analyze', json={'target': '${workspaceFolder}'}).raise_for_status()\"",
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    },
    {
      "label": "GhostLink: Health Check",
      "type": "shell",
      "command": "curl -s http://localhost:8080/health | jq .",
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    }
  ]
}
EOF

    success "VS Code tasks created"
}

# Install and compile extension
install_extension() {
    info "Installing and compiling VS Code extension..."

    cd "$EXTENSION_DIR"

    # Install dependencies
    if command -v npm &> /dev/null; then
        npm install
        npm run compile
        success "VS Code extension compiled successfully"
    else
        warning "npm not found. Please install Node.js and run 'npm install && npm run compile' in $EXTENSION_DIR"
    fi
}

# Main installation function
main() {
    log "Starting GhostLink IDE integration installation"

    create_extension_dir
    create_extension_source
    create_snippets
    create_keybindings
    create_custom_settings
    create_tasks
    install_extension

    success "GhostLink IDE integration completed successfully!"
    info "Restart VS Code to activate the extension"
    info "Use Ctrl+Alt+G (Cmd+Alt+G on Mac) for GhostLink commands"
    info "Check Command Palette for 'GhostLink:' commands"

    log "GhostLink IDE integration installation completed"
}

# Run main function
main "$@"
EOF

    chmod +x /Users/ghost-link-labs/ghostlinklabs/ghostlink_ide_integration.sh
    success "IDE integration script created"
}

# Create container integration
create_container_integration() {
    info "Creating container integration..."

    cat > /Users/ghost-link-labs/ghostlinklabs/ghostlink_container_integration.sh << 'EOF'
#!/bin/bash
# ==========================================
# GHOSTLINK CONTAINER INTEGRATION
# ==========================================
# Deep container integration for GhostLink AI

set -e

# Configuration
GHOSTLINK_ROOT="/Users/ghost-link-labs/ghostlinklabs"
CONTAINER_NAME="ghostlink-ai"
IMAGE_NAME="ghostlink/ghostlink-ai:latest"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
}

success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

info() {
    echo -e "${BLUE}INFO: $1${NC}"
}

error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

# Create Dockerfile
create_dockerfile() {
    info "Creating GhostLink Dockerfile..."

    cat > "$GHOSTLINK_ROOT/Dockerfile.ghostlink" << EOF
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    wget \\
    git \\
    build-essential \\
    nodejs \\
    npm \\
    jq \\
    htop \\
    iotop \\
    sysstat \\
    && rm -rf /var/lib/apt/lists/*

# Create ghostlink user
RUN useradd -m -s /bin/bash ghostlink

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install Node.js dependencies for VS Code integration
RUN npm install -g @vscode/vsce typescript eslint

# Create necessary directories
RUN mkdir -p /var/log/ghostlink \\
    /etc/ghostlink \\
    /opt/ghostlink \\
    /app/data \\
    /app/cache

# Set permissions
RUN chown -R ghostlink:ghostlink /app /var/log/ghostlink /etc/ghostlink /opt/ghostlink

# Switch to ghostlink user
USER ghostlink

# Environment variables
ENV GHOSTLINK_API_URL=http://localhost:8080
ENV GHOSTLINK_API_KEY=ghostlink_secure_key_2025
ENV GHOSTLINK_PROJECT_ROOT=/app
ENV PYTHONPATH=/app:\$PYTHONPATH
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8080/health || exit 1

# Expose ports
EXPOSE 8080 3000 8765

# Start command
CMD ["python3", "ghostlink_api_server.py"]
EOF

    success "Dockerfile created"
}

# Create docker-compose file
create_docker_compose() {
    info "Creating docker-compose configuration..."

    cat > "$GHOSTLINK_ROOT/docker-compose.ghostlink.yml" << EOF
version: '3.8'

services:
  ghostlink-api:
    build:
      context: .
      dockerfile: Dockerfile.ghostlink
    container_name: ghostlink-ai
    ports:
      - "8080:8080"    # API server
      - "3000:3000"    # Web dashboard
      - "8765:8765"    # VS Code HTTP API
    volumes:
      - ./data:/app/data
      - ./cache:/app/cache
      - ./logs:/var/log/ghostlink
      - ./config:/etc/ghostlink
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - GHOSTLINK_API_URL=http://localhost:8080
      - GHOSTLINK_API_KEY=ghostlink_secure_key_2025
      - GHOSTLINK_CONTAINERIZED=true
      - DOCKER_HOST=unix:///var/run/docker.sock
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - ghostlink-network

  ghostlink-monitor:
    image: ghostlink/ghostlink-monitor:latest
    container_name: ghostlink-monitor
    depends_on:
      ghostlink-api:
        condition: service_healthy
    volumes:
      - ./logs:/var/log/ghostlink
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - GHOSTLINK_API_URL=http://ghostlink-api:8080
      - MONITOR_INTERVAL=30
    restart: unless-stopped
    networks:
      - ghostlink-network

  ghostlink-vscode:
    image: ghostlink/vscode-integration:latest
    container_name: ghostlink-vscode
    depends_on:
      ghostlink-api:
        condition: service_healthy
    ports:
      - "8443:8443"  # VS Code server
    volumes:
      - ./workspace:/home/coder/workspace
      - ./vscode-data:/home/coder/.local/share/code-server
    environment:
      - GHOSTLINK_API_URL=http://ghostlink-api:8080
      - PASSWORD=ghostlink2025
    restart: unless-stopped
    networks:
      - ghostlink-network

  ghostlink-database:
    image: postgres:15-alpine
    container_name: ghostlink-db
    environment:
      - POSTGRES_DB=ghostlink
      - POSTGRES_USER=ghostlink
      - POSTGRES_PASSWORD=ghostlink_secure_2025
    volumes:
      - ghostlink_db_data:/var/lib/postgresql/data
      - ./sql:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - ghostlink-network

  ghostlink-redis:
    image: redis:7-alpine
    container_name: ghostlink-redis
    ports:
      - "6379:6379"
    volumes:
      - ghostlink_redis_data:/data
    restart: unless-stopped
    networks:
      - ghostlink-network

networks:
  ghostlink-network:
    driver: bridge

volumes:
  ghostlink_db_data:
  ghostlink_redis_data:
EOF

    success "Docker Compose configuration created"
}

# Create Kubernetes manifests
create_kubernetes_manifests() {
    info "Creating Kubernetes manifests..."

    mkdir -p "$GHOSTLINK_ROOT/k8s"

    # Namespace
    cat > "$GHOSTLINK_ROOT/k8s/namespace.yaml" << EOF
apiVersion: v1
kind: Namespace
metadata:
  name: ghostlink
  labels:
    name: ghostlink
    app: ghostlink-ai
EOF

    # ConfigMap
    cat > "$GHOSTLINK_ROOT/k8s/configmap.yaml" << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: ghostlink-config
  namespace: ghostlink
data:
  GHOSTLINK_API_URL: "http://ghostlink-api.ghostlink.svc.cluster.local:8080"
  GHOSTLINK_API_KEY: "ghostlink_secure_key_2025"
  GHOSTLINK_PROJECT_ROOT: "/app"
  PYTHONPATH: "/app"
  NODE_ENV: "production"
EOF

    # Secret
    cat > "$GHOSTLINK_ROOT/k8s/secret.yaml" << EOF
apiVersion: v1
kind: Secret
metadata:
  name: ghostlink-secret
  namespace: ghostlink
type: Opaque
data:
  api-key: $(echo -n "ghostlink_secure_key_2025" | base64)
  db-password: $(echo -n "ghostlink_secure_2025" | base64)
EOF

    # Deployment
    cat > "$GHOSTLINK_ROOT/k8s/deployment.yaml" << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ghostlink-api
  namespace: ghostlink
  labels:
    app: ghostlink-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ghostlink-api
  template:
    metadata:
      labels:
        app: ghostlink-api
    spec:
      containers:
      - name: ghostlink-api
        image: ghostlink/ghostlink-ai:latest
        ports:
        - containerPort: 8080
          name: api
        - containerPort: 3000
          name: dashboard
        envFrom:
        - configMapRef:
            name: ghostlink-config
        - secretRef:
            name: ghostlink-secret
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: ghostlink-data
          mountPath: /app/data
        - name: ghostlink-cache
          mountPath: /app/cache
      volumes:
      - name: ghostlink-data
        persistentVolumeClaim:
          claimName: ghostlink-data-pvc
      - name: ghostlink-cache
        emptyDir: {}
EOF

    # Service
    cat > "$GHOSTLINK_ROOT/k8s/service.yaml" << EOF
apiVersion: v1
kind: Service
metadata:
  name: ghostlink-api
  namespace: ghostlink
  labels:
    app: ghostlink-api
spec:
  selector:
    app: ghostlink-api
  ports:
  - name: api
    port: 8080
    targetPort: 8080
  - name: dashboard
    port: 3000
    targetPort: 3000
  type: ClusterIP
EOF

    # Ingress
    cat > "$GHOSTLINK_ROOT/k8s/ingress.yaml" << EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ghostlink-ingress
  namespace: ghostlink
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: ghostlink.local
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: ghostlink-api
            port:
              number: 8080
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ghostlink-api
            port:
              number: 3000
EOF

    # PVC
    cat > "$GHOSTLINK_ROOT/k8s/pvc.yaml" << EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ghostlink-data-pvc
  namespace: ghostlink
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
EOF

    success "Kubernetes manifests created"
}

# Create container management scripts
create_container_scripts() {
    info "Creating container management scripts..."

    # Build script
    cat > "$GHOSTLINK_ROOT/build-container.sh" << EOF
#!/bin/bash
# Build GhostLink container

set -e

echo "🏗️ Building GhostLink container..."

# Build the image
docker build -f Dockerfile.ghostlink -t $IMAGE_NAME .

echo "✅ Container built successfully"
echo "Run './start-container.sh' to start the container"
EOF

    # Start script
    cat > "$GHOSTLINK_ROOT/start-container.sh" << EOF
#!/bin/bash
# Start GhostLink container

set -e

echo "🚀 Starting GhostLink container..."

# Stop existing container if running
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Start new container
docker run -d \\
    --name $CONTAINER_NAME \\
    -p 8080:8080 \\
    -p 3000:3000 \\
    -p 8765:8765 \\
    -v "$GHOSTLINK_ROOT/data:/app/data" \\
    -v "$GHOSTLINK_ROOT/cache:/app/cache" \\
    -v "$GHOSTLINK_ROOT/logs:/var/log/ghostlink" \\
    -v "$GHOSTLINK_ROOT/config:/etc/ghostlink" \\
    -v /var/run/docker.sock:/var/run/docker.sock \\
    -e GHOSTLINK_API_URL=http://localhost:8080 \\
    -e GHOSTLINK_API_KEY=ghostlink_secure_key_2025 \\
    -e GHOSTLINK_CONTAINERIZED=true \\
    --restart unless-stopped \\
    $IMAGE_NAME

echo "✅ Container started successfully"
echo "API available at: http://localhost:8080"
echo "Dashboard available at: http://localhost:3000"
EOF

    # Stop script
    cat > "$GHOSTLINK_ROOT/stop-container.sh" << EOF
#!/bin/bash
# Stop GhostLink container

echo "🛑 Stopping GhostLink container..."

docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

echo "✅ Container stopped"
EOF

    # Logs script
    cat > "$GHOSTLINK_ROOT/container-logs.sh" << EOF
#!/bin/bash
# View GhostLink container logs

echo "📋 GhostLink container logs:"

docker logs -f $CONTAINER_NAME
EOF

    # Make scripts executable
    chmod +x "$GHOSTLINK_ROOT/build-container.sh"
    chmod +x "$GHOSTLINK_ROOT/start-container.sh"
    chmod +x "$GHOSTLINK_ROOT/stop-container.sh"
    chmod +x "$GHOSTLINK_ROOT/container-logs.sh"

    success "Container management scripts created"
}

# Main function
main() {
    log "Starting GhostLink container integration"

    create_dockerfile
    create_docker_compose
    create_kubernetes_manifests
    create_container_scripts

    success "GhostLink container integration completed!"
    info "Run './build-container.sh' to build the container"
    info "Run './start-container.sh' to start GhostLink in a container"
    info "Use 'docker-compose -f docker-compose.ghostlink.yml up' for full stack"

    log "GhostLink container integration completed"
}

main "\$@"
EOF

    chmod +x /Users/ghost-link-labs/ghostlinklabs/ghostlink_container_integration.sh
    success "Container integration script created"
}

# Create cloud integration
create_cloud_integration() {
    info "Creating cloud integration..."

    cat > /Users/ghost-link-labs/ghostlinklabs/ghostlink_cloud_integration.sh << 'EOF'
#!/bin/bash
# ==========================================
# GHOSTLINK CLOUD INTEGRATION
# ==========================================
# Deep cloud integration for GhostLink AI

set -e

# Configuration
GHOSTLINK_ROOT="/Users/ghost-link-labs/ghostlinklabs"
PROJECT_NAME="ghostlink-ai"
REGION="us-east-1"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
}

success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

info() {
    echo -e "${BLUE}INFO: $1${NC}"
}

error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

# AWS Integration
create_aws_integration() {
    info "Creating AWS integration..."

    mkdir -p "$GHOSTLINK_ROOT/cloud/aws"

    # CloudFormation template
    cat > "$GHOSTLINK_ROOT/cloud/aws/cloudformation.yaml" << EOF
AWSTemplateFormatVersion: '2010-09-09'
Description: 'GhostLink AI Cloud Infrastructure'

Parameters:
  ProjectName:
    Type: String
    Default: ghostlink-ai
  Environment:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]

Resources:
  # VPC
  GhostLinkVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${ProjectName}-${Environment}-vpc'

  # Subnets
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref GhostLinkVPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true

  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref GhostLinkVPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: !Select [0, !GetAZs '']

  # Security Groups
  ALBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow HTTP/HTTPS traffic
      VpcId: !Ref GhostLinkVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0

  ECSSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: ECS service security group
      VpcId: !Ref GhostLinkVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          SourceSecurityGroupId: !Ref ALBSecurityGroup

  # ECS Cluster
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub '${ProjectName}-${Environment}'

  # ECR Repository
  ECRRepository:
    Type: AWS::ECR::Repository
    Properties:
      RepositoryName: !Sub '${ProjectName}/ghostlink-api'
      ImageScanningConfiguration:
        ScanOnPush: true

  # RDS Database
  GhostLinkDB:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceClass: db.t3.micro
      Engine: postgres
      EngineVersion: '15.4'
      DBInstanceIdentifier: !Sub '${ProjectName}-${Environment}-db'
      MasterUsername: ghostlink
      MasterUserPassword: !Ref DBPassword
      AllocatedStorage: '20'
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref DBInstanceSecurityGroup

  DBSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupDescription: Subnet group for GhostLink database
      SubnetIds:
        - !Ref PrivateSubnet1

  DBInstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Database security group
      VpcId: !Ref GhostLinkVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          SourceSecurityGroupId: !Ref ECSSecurityGroup

  # ElastiCache Redis
  RedisCluster:
    Type: AWS::ElastiCache::CacheCluster
    Properties:
      CacheNodeType: cache.t3.micro
      Engine: redis
      EngineVersion: '7.0'
      NumCacheNodes: 1
      ClusterName: !Sub '${ProjectName}-${Environment}-redis'
      VpcSecurityGroupIds:
        - !Ref RedisSecurityGroup

  RedisSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Redis security group
      VpcId: !Ref GhostLinkVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 6379
          ToPort: 6379
          SourceSecurityGroupId: !Ref ECSSecurityGroup

Outputs:
  ECRRepositoryUri:
    Description: ECR Repository URI
    Value: !GetAtt ECRRepository.RepositoryUri
    Export:
      Name: !Sub '${ProjectName}-${Environment}-ecr-uri'

  ECSClusterName:
    Description: ECS Cluster Name
    Value: !Ref ECSCluster
    Export:
      Name: !Sub '${ProjectName}-${Environment}-cluster'
EOF

    # AWS Lambda function for serverless integration
    cat > "$GHOSTLINK_ROOT/cloud/aws/lambda_function.py" << 'EOF'
import json
import boto3
import requests
from datetime import datetime

def lambda_handler(event, context):
    """GhostLink AWS Lambda integration"""

    # Initialize AWS clients
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')

    # GhostLink API configuration
    ghostlink_url = "https://api.ghostlink.ai"
    api_key = "ghostlink_secure_key_2025"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        # Process different event types
        if 'Records' in event:
            for record in event['Records']:
                if record.get('eventSource') == 'aws:s3':
                    # S3 event processing
                    bucket = record['s3']['bucket']['name']
                    key = record['s3']['object']['key']

                    # Analyze file with GhostLink
                    analysis_request = {
                        "file_url": f"s3://{bucket}/{key}",
                        "analysis_type": "security",
                        "metadata": {
                            "source": "aws_lambda",
                            "bucket": bucket,
                            "key": key
                        }
                    }

                    response = requests.post(
                        f"{ghostlink_url}/analyze/file",
                        json=analysis_request,
                        headers=headers
                    )

                    if response.status_code == 200:
                        result = response.json()

                        # Store results in DynamoDB
                        table = dynamodb.Table('ghostlink-analysis-results')
                        table.put_item(Item={
                            'id': f"{bucket}-{key}-{datetime.now().isoformat()}",
                            'bucket': bucket,
                            'key': key,
                            'analysis_result': result,
                            'timestamp': datetime.now().isoformat()
                        })

                elif record.get('eventSource') == 'aws:codecommit':
                    # CodeCommit event processing
                    repository_name = record['eventSourceARN'].split(':')[-1]

                    # Trigger code analysis
                    analysis_request = {
                        "repository": repository_name,
                        "commit_id": record.get('customData', {}).get('commitId'),
                        "analysis_type": "code-review",
                        "source": "aws_codecommit"
                    }

                    requests.post(
                        f"{ghostlink_url}/automation/execute",
                        json={"task": "code-review", "parameters": analysis_request},
                        headers=headers
                    )

        # CloudWatch scheduled event
        elif event.get('source') == 'aws.events':
            # Periodic health check and maintenance
            health_response = requests.get(f"{ghostlink_url}/health", headers=headers)

            if health_response.status_code == 200:
                # Trigger maintenance tasks
                requests.post(
                    f"{ghostlink_url}/automation/execute",
                    json={"task": "system-maintenance", "parameters": {}},
                    headers=headers
                )

        return {
            'statusCode': 200,
            'body': json.dumps('GhostLink Lambda integration completed successfully')
        }

    except Exception as e:
        print(f"Error in GhostLink Lambda integration: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
EOF

    success "AWS integration created"
}

# Azure Integration
create_azure_integration() {
    info "Creating Azure integration..."

    mkdir -p "$GHOSTLINK_ROOT/cloud/azure"

    # ARM template
    cat > "$GHOSTLINK_ROOT/cloud/azure/azuredeploy.json" << EOF
{
  "\$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "projectName": {
      "type": "string",
      "defaultValue": "ghostlink-ai",
      "metadata": {
        "description": "Name of the project"
      }
    },
    "environment": {
      "type": "string",
      "defaultValue": "dev",
      "allowedValues": ["dev", "staging", "prod"],
      "metadata": {
        "description": "Environment name"
      }
    }
  },
  "variables": {
    "location": "[resourceGroup().location]",
    "resourceGroupName": "[resourceGroup().name]",
    "storageAccountName": "[concat(parameters('projectName'), parameters('environment'), 'storage')]",
    "appServicePlanName": "[concat(parameters('projectName'), '-', parameters('environment'), '-plan')]",
    "webAppName": "[concat(parameters('projectName'), '-', parameters('environment'), '-api')]",
    "acrName": "[concat(parameters('projectName'), parameters('environment'), 'acr')]"
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2021-09-01",
      "name": "[variables('storageAccountName')]",
      "location": "[variables('location')]",
      "sku": {
        "name": "Standard_LRS"
      },
      "kind": "StorageV2",
      "properties": {
        "allowBlobPublicAccess": false,
        "minimumTlsVersion": "TLS1_2"
      }
    },
    {
      "type": "Microsoft.ContainerRegistry/registries",
      "apiVersion": "2021-09-01",
      "name": "[variables('acrName')]",
      "location": "[variables('location')]",
      "sku": {
        "name": "Basic"
      },
      "properties": {
        "adminUserEnabled": true
      }
    },
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2021-03-01",
      "name": "[variables('appServicePlanName')]",
      "location": "[variables('location')]",
      "sku": {
        "name": "B1",
        "tier": "Basic",
        "size": "B1",
        "family": "B",
        "capacity": 1
      },
      "kind": "linux",
      "properties": {
        "reserved": true
      }
    },
    {
      "type": "Microsoft.Web/sites",
      "apiVersion": "2021-03-01",
      "name": "[variables('webAppName')]",
      "location": "[variables('location')]",
      "dependsOn": [
        "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]",
        "[resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))]"
      ],
      "kind": "app,linux,container",
      "properties": {
        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]",
        "siteConfig": {
          "linuxFxVersion": "[concat('DOCKER|', reference(resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))).loginServer, '/ghostlink-api:latest')]",
          "alwaysOn": true,
          "appSettings": [
            {
              "name": "DOCKER_REGISTRY_SERVER_URL",
              "value": "[concat('https://', reference(resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))).loginServer)]"
            },
            {
              "name": "DOCKER_REGISTRY_SERVER_USERNAME",
              "value": "[listCredentials(resourceId('Microsoft.ContainerRegistry/registries', variables('acrName')), '2021-09-01').username]"
            },
            {
              "name": "DOCKER_REGISTRY_SERVER_PASSWORD",
              "value": "[listCredentials(resourceId('Microsoft.ContainerRegistry/registries', variables('acrName')), '2021-09-01').passwords[0].value]"
            }
          ]
        }
      }
    }
  ],
  "outputs": {
    "acrLoginServer": {
      "type": "string",
      "value": "[reference(resourceId('Microsoft.ContainerRegistry/registries', variables('acrName'))).loginServer]"
    },
    "webAppUrl": {
      "type": "string",
      "value": "[concat('https://', reference(resourceId('Microsoft.Web/sites', variables('webAppName'))).defaultHostName)]"
    }
  }
}
EOF

    success "Azure integration created"
}

# Google Cloud Integration
create_gcp_integration() {
    info "Creating Google Cloud integration..."

    mkdir -p "$GHOSTLINK_ROOT/cloud/gcp"

    # Terraform configuration
    cat > "$GHOSTLINK_ROOT/cloud/gcp/main.tf" << EOF
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

# VPC Network
resource "google_compute_network" "ghostlink_vpc" {
  name                    = "ghostlink-\${var.environment}-vpc"
  auto_create_subnetworks = false
}

# Subnets
resource "google_compute_subnetwork" "ghostlink_subnet" {
  name          = "ghostlink-\${var.environment}-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.ghostlink_vpc.id
}

# GKE Cluster
resource "google_container_cluster" "ghostlink_cluster" {
  name               = "ghostlink-\${var.environment}-cluster"
  location           = var.region
  initial_node_count = 1

  node_config {
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

# Cloud SQL Database
resource "google_sql_database_instance" "ghostlink_db" {
  name             = "ghostlink-\${var.environment}-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "ghostlink_database" {
  name     = "ghostlink"
  instance = google_sql_database_instance.ghostlink_db.name
}

# Cloud Storage Bucket
resource "google_storage_bucket" "ghostlink_storage" {
  name          = "ghostlink-\${var.environment}-\${var.project_id}"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}

# Cloud Run Service
resource "google_cloud_run_service" "ghostlink_api" {
  name     = "ghostlink-\${var.environment}-api"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/\${var.project_id}/ghostlink-api:latest"
        env {
          name  = "GHOSTLINK_API_KEY"
          value = "ghostlink_secure_key_2025"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# IAM Service Account
resource "google_service_account" "ghostlink_sa" {
  account_id   = "ghostlink-\${var.environment}-sa"
  display_name = "GhostLink Service Account"
}

# Cloud Functions
resource "google_cloudfunctions_function" "ghostlink_function" {
  name        = "ghostlink-\${var.environment}-function"
  description = "GhostLink AI integration function"
  runtime     = "python39"

  source_archive_bucket = google_storage_bucket.ghostlink_storage.name
  source_archive_object = google_storage_bucket_object.function_code.name

  entry_point = "ghostlink_handler"

  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = google_storage_bucket.ghostlink_storage.name
  }
}

resource "google_storage_bucket_object" "function_code" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.ghostlink_storage.name
  source = "\${path.module}/function-source.zip"
}
EOF

    # Cloud Function source
    cat > "$GHOSTLINK_ROOT/cloud/gcp/main.py" << 'EOF'
import functions_framework
from google.cloud import storage, firestore
import requests
from datetime import datetime

def ghostlink_handler(event, context):
    """GhostLink Google Cloud Function integration"""

    # Initialize clients
    storage_client = storage.Client()
    db = firestore.Client()

    # GhostLink API configuration
    ghostlink_url = "https://api.ghostlink.ai"
    api_key = "ghostlink_secure_key_2025"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        # Process Cloud Storage events
        if event.get('bucket') and event.get('name'):
            bucket_name = event['bucket']
            file_name = event['name']

            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(file_name)

            # Analyze file with GhostLink
            analysis_request = {
                "file_url": f"gs://{bucket_name}/{file_name}",
                "analysis_type": "security",
                "metadata": {
                    "source": "gcp_function",
                    "bucket": bucket_name,
                    "file": file_name,
                    "size": blob.size,
                    "content_type": blob.content_type
                }
            }

            response = requests.post(
                f"{ghostlink_url}/analyze/file",
                json=analysis_request,
                headers=headers
            )

            if response.status_code == 200:
                result = response.json()

                # Store results in Firestore
                doc_ref = db.collection('analysis_results').document()
                doc_ref.set({
                    'bucket': bucket_name,
                    'file': file_name,
                    'analysis_result': result,
                    'timestamp': datetime.now()
                })

        return 'GhostLink analysis completed'

    except Exception as e:
        print(f"Error in GhostLink function: {str(e)}")
        return f'Error: {str(e)}'

@functions_framework.http
def health_check(request):
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'ghostlink-gcp-integration'}
EOF

    success "Google Cloud integration created"
}

# Create cloud deployment scripts
create_cloud_scripts() {
    info "Creating cloud deployment scripts..."

    # AWS deployment script
    cat > "$GHOSTLINK_ROOT/cloud/deploy-aws.sh" << EOF
#!/bin/bash
# Deploy GhostLink to AWS

set -e

echo "🚀 Deploying GhostLink to AWS..."

# Build and push Docker image
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
docker build -f Dockerfile.ghostlink -t ghostlink-api .
docker tag ghostlink-api:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ghostlink-api:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ghostlink-api:latest

# Deploy CloudFormation stack
aws cloudformation deploy \\
    --template-file cloud/aws/cloudformation.yaml \\
    --stack-name ghostlink-ai-stack \\
    --parameter-overrides ProjectName=$PROJECT_NAME Environment=dev \\
    --capabilities CAPABILITY_IAM

echo "✅ GhostLink deployed to AWS successfully"
EOF

    # Azure deployment script
    cat > "$GHOSTLINK_ROOT/cloud/deploy-azure.sh" << EOF
#!/bin/bash
# Deploy GhostLink to Azure

set -e

echo "🚀 Deploying GhostLink to Azure..."

# Login to Azure
az login --use-device-code

# Create resource group
az group create --name ghostlink-rg --location eastus

# Deploy ARM template
az deployment group create \\
    --resource-group ghostlink-rg \\
    --template-file cloud/azure/azuredeploy.json \\
    --parameters projectName=$PROJECT_NAME environment=dev

echo "✅ GhostLink deployed to Azure successfully"
EOF

    # GCP deployment script
    cat > "$GHOSTLINK_ROOT/cloud/deploy-gcp.sh" << EOF
#!/bin/bash
# Deploy GhostLink to Google Cloud

set -e

echo "🚀 Deploying GhostLink to Google Cloud..."

# Authenticate
gcloud auth login
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudfunctions.googleapis.com

# Build and push Docker image
gcloud builds submit --tag gcr.io/$PROJECT_ID/ghostlink-api

# Deploy to Cloud Run
gcloud run deploy ghostlink-api \\
    --image gcr.io/$PROJECT_ID/ghostlink-api \\
    --platform managed \\
    --region us-central1 \\
    --allow-unauthenticated

echo "✅ GhostLink deployed to Google Cloud successfully"
EOF

    chmod +x "$GHOSTLINK_ROOT/cloud/deploy-aws.sh"
    chmod +x "$GHOSTLINK_ROOT/cloud/deploy-azure.sh"
    chmod +x "$GHOSTLINK_ROOT/cloud/deploy-gcp.sh"

    success "Cloud deployment scripts created"
}

# Main function
main() {
    log "Starting GhostLink cloud integration"

    create_aws_integration
    create_azure_integration
    create_gcp_integration
    create_cloud_scripts

    success "GhostLink cloud integration completed!"
    info "Run './cloud/deploy-aws.sh' to deploy to AWS"
    info "Run './cloud/deploy-azure.sh' to deploy to Azure"
    info "Run './cloud/deploy-gcp.sh' to deploy to Google Cloud"

    log "GhostLink cloud integration completed"
}

main "$@"
EOF

    chmod +x /Users/ghost-link-labs/ghostlinklabs/ghostlink_cloud_integration.sh
    success "Cloud integration script created"
}

# Run all integrations
run_integrations() {
    info "Running all GhostLink deep integrations..."

    # Make scripts executable
    chmod +x "$GHOSTLINK_ROOT/ghostlink_system_integration.sh"
    chmod +x "$GHOSTLINK_ROOT/ghostlink_ide_integration.sh"
    chmod +x "$GHOSTLINK_ROOT/ghostlink_container_integration.sh"
    chmod +x "$GHOSTLINK_ROOT/ghostlink_cloud_integration.sh"

    # Run system integration
    if [ ! -f "/usr/local/bin/ghostlink-monitor" ]; then
        info "Running system integration..."
        "$GHOSTLINK_ROOT/ghostlink_system_integration.sh"
    else
        info "System integration already installed"
    fi

    # Run IDE integration
    if [ ! -d "$HOME/.vscode/extensions/ghostlink.ghostlink-integration-1.0.0" ]; then
        info "Running IDE integration..."
        "$GHOSTLINK_ROOT/ghostlink_ide_integration.sh"
    else
        info "IDE integration already installed"
    fi

    # Run container integration
    if [ ! -f "$GHOSTLINK_ROOT/build-container.sh" ]; then
        info "Running container integration..."
        "$GHOSTLINK_ROOT/ghostlink_container_integration.sh"
    else
        info "Container integration already configured"
    fi

    # Run cloud integration
    if [ ! -d "$GHOSTLINK_ROOT/cloud" ]; then
        info "Running cloud integration..."
        "$GHOSTLINK_ROOT/ghostlink_cloud_integration.sh"
    else
        info "Cloud integration already configured"
    fi

    success "All GhostLink deep integrations completed!"
    info "GhostLink is now deeply integrated across all levels:"
    info "  🔧 System Level: Monitoring, automation, services"
    info "  💻 IDE Level: VS Code extension, snippets, keybindings"
    info "  🐳 Container Level: Docker, Kubernetes, orchestration"
    info "  ☁️ Cloud Level: AWS, Azure, GCP integration"
    info ""
    info "Use 'gl-status' to check GhostLink status"
    info "Use 'gl-exec <task>' to run automation tasks"
    info "Use Ctrl+Alt+G in VS Code for GhostLink commands"
}

# Main execution
main() {
    echo "🔗 Deep GhostLink Integration Setup"
    echo "=================================="
    echo ""

    run_integrations
}

main "$@"
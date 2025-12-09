# Claude Code Setup for GhostLink Labs

This guide helps you set up Claude Code for optimal development with the GhostLink project.

## Overview

Claude Code is Anthropic's agentic coding tool that integrates with your terminal and IDE to help you build features, debug issues, and navigate codebases faster.

## Installation Options

### Option 1: CLI (Recommended for Terminal Users)

**macOS/Linux via Homebrew:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Start using Claude Code:**
```bash
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/ghostlinklabs
claude
```

You'll be prompted to log in on first use with your [Claude.ai](https://claude.ai/) account.

### Option 2: VS Code Extension (Beta)

**Requirements:**
- VS Code 1.98.0 or higher

**Installation:**
1. Open VS Code
2. Install from [Visual Studio Code Extension Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)
3. Click the Spark icon in the sidebar to access Claude Code

**Features:**
- Native IDE experience with dedicated sidebar panel
- Plan mode with editing preview
- Auto-accept edits mode
- Extended thinking toggle
- @-mention files or attach via file picker
- MCP server usage (configured via CLI)
- Conversation history
- Multiple simultaneous sessions
- Keyboard shortcuts and slash commands

## GhostLink Project Configuration

### Environment Setup

The GhostLink project uses a Python virtual environment at `.venv/`. Ensure Claude Code uses this environment:

**VS Code Settings (already configured):**
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

### VS Code Tasks

All VS Code tasks now use the workspace venv Python to avoid path issues:
- Link: Start/Stop/Status
- Link: Health Check/View Errors/Fix Common Issues
- Link: Start Monitoring/System Info
- Git: Auto Pull/Auto Sync/Status/Abort Merge
- Link: Add Task/List Tasks/View History
- Link: Set Context/List Context

### CLI Integration

When running `claude` from VS Code's integrated terminal, the legacy CLI integration automatically activates:
- Selection context sharing (current selection/tab shared with Claude)
- Diff viewing in IDE instead of terminal
- File reference shortcuts (Cmd+Option+K on Mac, Alt+Ctrl+K on Windows/Linux)
- Automatic diagnostic sharing (lint and syntax errors)

To manually connect external terminal to VS Code:
```bash
claude
/ide
```

## Security Considerations

When using Claude Code in VS Code with auto-edit permissions:
- Consider enabling [VS Code Restricted Mode](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) for untrusted workspaces
- Use manual approval mode for edits when working with sensitive code
- Take extra care to ensure Claude is only used with trusted prompts

Claude Code may modify IDE configuration files that can be automatically executed, which could bypass permission prompts for bash execution.

## Third-Party Providers (Optional)

If using Amazon Bedrock, Microsoft Foundry, or Google Vertex AI instead of Claude.ai:

**Configure via VS Code Settings:**
1. Open VS Code settings
2. Search for "Claude Code: Environment Variables"
3. Add required environment variables:

**Amazon Bedrock:**
```
CLAUDE_CODE_USE_BEDROCK=1
AWS_REGION=us-east-2
AWS_PROFILE=your-profile
```

**Google Vertex AI:**
```
CLAUDE_CODE_USE_VERTEX=1
CLOUD_ML_REGION=global
ANTHROPIC_VERTEX_PROJECT_ID=your-project-id
```

**Microsoft Foundry:**
```
CLAUDE_CODE_USE_FOUNDRY=1
ANTHROPIC_FOUNDRY_RESOURCE=your-resource
ANTHROPIC_FOUNDRY_API_KEY=your-api-key
```

For detailed setup: [Third-Party Provider Documentation](https://code.claude.com/docs/en/third-party-integrations)

## Model Context Protocol (MCP)

Claude Code supports MCP servers for extended functionality. Configure MCP servers through the CLI:

```bash
claude
/mcp
```

Once configured, MCP servers work in both CLI and VS Code extension. Learn more: [MCP Documentation](https://code.claude.com/docs/en/mcp)

## Common Workflows

### Build Features
```bash
claude -p "Build a health monitoring endpoint that exposes metrics in Prometheus format"
```

### Debug Issues
```bash
claude -p "The Link service is failing to start with exit code 127. Diagnose and fix."
```

### Navigate Codebase
```bash
claude -p "Explain the PipelineOrchestrator class and how it handles retries"
```

### Automate Tasks
```bash
claude -p "Fix all lint issues in ghostlink/ directory"
```

### Unix-style Composition
```bash
tail -f app.log | claude -p "Alert if you see any critical errors"
```

## Troubleshooting

### Claude Code Never Responds
1. Check internet connection
2. Start a new conversation
3. Try the CLI for detailed error messages: `claude`
4. [File a bug report](https://github.com/anthropics/claude-code/issues)

### VS Code Extension Not Installing
- Ensure VS Code 1.98.0+
- Check extension install permissions
- Install directly from Marketplace website

### Legacy Integration Not Working
- Run from VS Code's integrated terminal
- Ensure `code` command is installed:
  - Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux)
  - Search: "Shell Command: Install 'code' command in PATH"

### Task Exit Code 127
This usually means the Python interpreter isn't found. We've fixed all tasks to use `${workspaceFolder}/.venv/bin/python` instead of system `python`.

## Additional Resources

- [Quickstart Guide](https://code.claude.com/docs/en/quickstart)
- [Common Workflows](https://code.claude.com/docs/en/common-workflows)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Settings](https://code.claude.com/docs/en/settings)
- [Security Best Practices](https://code.claude.com/docs/en/security)
- [Privacy & Data Usage](https://code.claude.com/docs/en/data-usage)

## Quick Start for GhostLink Development

```bash
# Navigate to project
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/ghostlinklabs

# Activate venv (if needed manually)
source .venv/bin/activate

# Start Claude Code
claude

# Example prompts:
# "Run the health check and show me the results"
# "Add a test for the git sync command in tests/test_cli_integration.py"
# "Fix the remaining bandit security warnings"
# "Add orchestrator retry failure tests with timeout scenarios"
```

---

**Note:** Claude Code is in active development. Check [documentation](https://code.claude.com/docs) for latest features and updates.

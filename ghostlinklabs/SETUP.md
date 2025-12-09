# GhostLink Setup Guide

Complete setup instructions for the GhostLink repository and Link agent.

## Prerequisites

The repository maintenance has identified that you need to install development tools:

### 1. Install Python 3.8+

**Option A: Microsoft Store (Recommended for Windows)**
```powershell
# Windows will prompt you to install from Microsoft Store when you run:
python
```

**Option B: Official Python Installer**
- Download from: https://www.python.org/downloads/
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Verify: `python --version` (should show Python 3.8 or higher)

### 2. Install Node.js and npm

**Download from**: https://nodejs.org/
- Install LTS version (Long Term Support)
- npm is included with Node.js
- Verify installations:
  ```powershell
  node --version
  npm --version
  ```

## Installation Steps

### 1. Install Python Dependencies

```powershell
# Navigate to repository root
cd c:\Users\devrg\ghostlinklabs

# Install development dependencies (includes linting tools)
pip install -e ".[dev]"

# OR install just the base package
pip install -e .
```

### 2. Build VS Code Extension

```powershell
# Navigate to extension directory
cd .vscode\link-agent

# Install Node.js dependencies
npm install

# Compile TypeScript
npm run compile
```

### 3. Install Pre-commit Hooks (Optional but Recommended)

```powershell
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install
```

## Verification

### Test Python Installation

```powershell
# Verify Link can be imported
python -c "from ghostlink import Link; print('✓ Link imported successfully')"

# Test CLI
link --help
link status
```

### Test VS Code Extension

1. Open repository in VS Code
2. Press `F5` to launch Extension Development Host
3. In the new VS Code window, open GitHub Copilot Chat
4. Type: `@link hello`
5. Link should respond

### Run Linting

```powershell
# Run all linters
make lint

# Auto-format code
make format

# Type check
make check
```

## Current Errors

After running the maintenance task, the following issues remain:

### TypeScript Extension Errors (6 errors)

**Root Cause**: Missing `node_modules` - dependencies not installed

**Files Affected**: 
- `.vscode/link-agent/tsconfig.json` (2 errors)
- `.vscode/link-agent/src/extension.ts` (6 errors)

**Errors**:
- Cannot find type definition file for 'node'
- Cannot find type definition file for 'vscode'
- Cannot find module 'child_process'
- Cannot find module 'vscode'
- Cannot find name 'Buffer' (2 instances)
- Cannot find name 'console' (2 instances)

**Resolution**: Run `npm install` in `.vscode/link-agent/` (requires Node.js/npm installation first)

### Python Import Validation

**Status**: ✓ All Python imports are valid
- `ghostlink/link.py` - No errors
- `ghostlink/link_agent.py` - No errors  
- `ghostlink/link_cli.py` - No errors

## What Was Fixed

During the maintenance task, the following were corrected:

### TypeScript Type Annotations (9 fixes)
1. ✅ Import order - moved ChildProcess/spawn before vscode import
2. ✅ Buffer type annotations - added `data: Buffer` to stdout/stderr handlers
3. ✅ Explicit parameter types - added `vscode.ChatRequest`, `vscode.ChatContext`, `vscode.ChatResponseStream`, `vscode.CancellationToken`

### .gitignore Improvements
1. ✅ Changed `/.vscode/` to `/.vscode/settings.json` - keep extension code tracked
2. ✅ Added Node.js patterns: `node_modules/`, `.vscode/link-agent/node_modules/`, `.vscode/link-agent/out/`
3. ✅ Added Link patterns: `link_memory.json`, `*.bak`, `*.tmp`
4. ✅ Improved Python patterns: `__pycache__/`, `*.py[cod]`, `.pytest_cache/`

## Next Steps

1. **Install Python 3.8+** - Required for all Python functionality
2. **Install Node.js/npm** - Required to build VS Code extension
3. **Run installation steps** - Install dependencies and verify
4. **Test all components** - CLI, Python API, VS Code extension
5. **Run linting** - Ensure code quality standards

## Link Agent Interfaces

Once setup is complete, you can interact with Link through:

### 1. Command Line Interface
```powershell
link start                    # Start Link agent
link status                   # View agent status
link task add "description"   # Add a task
link task list                # List all tasks
link context set key=value    # Set context
link learn "preference"       # Teach Link
link history                  # View task history
link reset                    # Reset memory
```

### 2. Python API
```python
from ghostlink import Link, get_link, chat_with_link

# Get singleton instance
link = get_link()

# Add tasks
await link.add_task("Build feature X", priority=TaskPriority.HIGH)

# Chat interface
response = await chat_with_link("What tasks are pending?")
print(response)
```

### 3. GitHub Copilot Chat (VS Code)
```
@link hello
@link add task: implement authentication
@link what's my status?
@link remember I prefer async/await
```

### 4. GitHub Custom Agent
Link is registered as a GitHub custom agent in `.github/agents/LINK.agent.md`

## Documentation

- **Link Overview**: `LINK.md`
- **Chat Agent**: `LINK_CHAT_AGENT.md`
- **IDE Integration**: `.vscode/LINK_INTEGRATION.md`
- **Linting Setup**: `LINTING.md`
- **Open Source**: `OPEN_SOURCE.md`
- **Consolidated README**: `CONSOLIDATED_README.md`

## Troubleshooting

### Python not found
```
Python was not found; run without arguments to install from the Microsoft Store
```
**Solution**: Install Python from Microsoft Store or python.org

### npm not recognized
```
npm : The term 'npm' is not recognized as the name of a cmdlet
```
**Solution**: Install Node.js from nodejs.org (includes npm)

### Import errors in Python
```
ModuleNotFoundError: No module named 'click'
```
**Solution**: Run `pip install -e ".[dev]"` to install all dependencies

### Extension doesn't activate
**Solution**: 
1. Ensure TypeScript compiled successfully: `npm run compile`
2. Check for compilation errors in `.vscode/link-agent/out/extension.js`
3. View extension logs: `View > Output > Select "Link Agent"`

## Support

For issues or questions:
- Check documentation in repo root
- Review `.github/agents/LINK.agent.md` for agent capabilities
- Examine error logs in VS Code Output panel

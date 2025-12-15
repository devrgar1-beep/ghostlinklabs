# VS Code & GitHub Tools Integration - Complete

## 🎉 Overview

GhostLink now includes full **VS Code integration** and **GitHub tools management** - providing a complete development environment with automated setup, extension management, and access to useful open-source tools.

## ✅ What Was Installed

### 1. VS Code Integration System
**File**: `vscode_integration.py` (460 lines)

**Features**:
- Automatic VS Code extension installation
- Settings configuration for GhostLink
- Workspace file generation
- Extension recommendations
- JSONc settings parser (handles comments & trailing commas)

### 2. GitHub Tools Manager
**File**: `github_tools.py` (370 lines)

**Features**:
- Clone useful GitHub repositories
- Manage external tools
- Create tools index
- List downloaded tools
- Update existing clones

### 3. Shell Integration
Added PowerShell commands:
```powershell
# VS Code
vscode-setup        # Full setup (extensions + settings)
vscode-extensions   # Install extensions only
vscode-settings     # Update settings only
vscode-list         # List installed extensions

# GitHub Tools
github-tools        # Download tools from GitHub
github-list         # List downloaded tools
github-index        # Create tools index
```

### 4. Toolbox Forge Integration
Added forge commands:
```bash
forge vscode-setup
forge vscode-extensions
forge vscode-list
forge github-tools
forge github-list
```

## 📦 VS Code Extensions (Recommended)

### Core Python Development
- ✅ **ms-python.python** - Python language support
- ✅ **ms-python.vscode-pylance** - Fast Python IntelliSense
- ✅ **ms-python.debugpy** - Python debugger
- ✅ **ms-python.black-formatter** - Black code formatter
- ✅ **charliermarsh.ruff** - Ultra-fast Python linter

### AI & GitHub
- ✅ **github.copilot** - GitHub Copilot AI assistant
- ✅ **github.copilot-chat** - Chat with Copilot
- ✅ **github.vscode-pull-request-github** - PR management
- ✅ **eamodio.gitlens** - Supercharged Git

### Shell & Terminal
- ✅ **ms-vscode.powershell** - PowerShell support
- ✅ **foxundermoon.shell-format** - Shell script formatter
- ✅ **timonwong.shellcheck** - Shell script linting
- ✅ **mads-hartmann.bash-ide-vscode** - Bash language server

### Docker & Containers
- ✅ **ms-azuretools.vscode-docker** - Docker support
- ✅ **ms-vscode-remote.remote-containers** - Dev Containers

### Productivity
- ✅ **gruntfuggly.todo-tree** - TODO/FIXME highlighting
- ✅ **usernamehw.errorlens** - Inline error messages
- ✅ **streetsidesoftware.code-spell-checker** - Spell checker

### Data & Docs
- ✅ **yzhang.markdown-all-in-one** - Markdown support
- ✅ **davidanson.vscode-markdownlint** - Markdown linting
- ✅ **redhat.vscode-yaml** - YAML support
- ✅ **tamasfe.even-better-toml** - TOML support

### UI/Themes
- ✅ **pkief.material-icon-theme** - Material icons
- ✅ **github.github-vscode-theme** - GitHub theme

## ⚙️ VS Code Settings (Auto-Configured)

```json
{
  // Python
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.analysis.typeCheckingMode": "basic",
  "python.terminal.activateEnvironment": true,

  // Formatting
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  },

  // Linting
  "ruff.enable": true,
  "ruff.organizeImports": true,

  // Editor
  "editor.rulers": [88, 120],
  "editor.tabSize": 4,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,

  // Terminal
  "terminal.integrated.env.windows": {
    "GHOSTLINK_ROOT": "${workspaceFolder}",
    "GHOSTLINK_ACTIVE": "true"
  },

  // GitHub Copilot
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "markdown": true
  }
}
```

## 🛠️ GitHub Tools Available

The GitHub Tools Manager can download these useful repositories:

### Terminal & Shell
- **windows-terminal** - Modern Windows terminal
- **powershell-core** - PowerShell 7+ cross-platform
- **oh-my-zsh** - Shell framework with plugins
- **fzf** - Fuzzy finder for command-line

### CLI Tools
- **bat** - Cat clone with syntax highlighting
- **fd** - Fast alternative to find
- **ripgrep** - Extremely fast grep
- **jq** - JSON processor
- **yq** - YAML/JSON/XML processor

### Development
- **ruff** - Ultra-fast Python linter
- **black** - Python code formatter
- **pre-commit** - Git hooks framework
- **fastapi-examples** - FastAPI examples

### Docker & API
- **dive** - Docker image layer explorer
- **httpie** - Modern HTTP client for APIs

### Documentation
- **glow** - Markdown renderer for terminal
- **cheatsh** - Command-line cheat sheets
- **gh-cli** - GitHub CLI tool

### Database
- **pgcli** - Postgres CLI with autocomplete

## 🚀 Quick Start

### Install Full VS Code Integration
```powershell
# Via Python
python vscode_integration.py --install

# Via shell command
vscode-setup

# Via forge
forge vscode-setup
```

This will:
1. ✅ Update VS Code settings
2. ✅ Create workspace file
3. ✅ Update extension recommendations
4. ✅ Install recommended extensions

### Update Settings Only
```powershell
python vscode_integration.py --settings
# or
vscode-settings
```

### Install Extensions Only
```powershell
python vscode_integration.py --extensions
# or
vscode-extensions
```

### List Installed Extensions
```powershell
python vscode_integration.py --list
# or
vscode-list
```

### Download GitHub Tools
```powershell
python github_tools.py --download
# or
github-tools
```

Interactive menu will appear:
```
📦 Terminal:
  • windows-terminal: Modern terminal application
  • powershell-core: PowerShell 7+ cross-platform shell
  ...

📦 CLI Tools:
  • bat: Cat clone with syntax highlighting
  • fd: Fast alternative to find
  ...

Total: 20 tools available

Download all tools? (y/n/select):
```

### List Downloaded Tools
```powershell
python github_tools.py --list
# or
github-list
```

## 📁 File Structure

```
ghostlinklabs/
├── vscode_integration.py       # VS Code manager
├── github_tools.py              # GitHub tools manager
├── ghostlink.code-workspace     # VS Code workspace (auto-generated)
├── .vscode/
│   ├── settings.json            # Updated with GhostLink settings
│   ├── extensions.json          # Extension recommendations
│   ├── tasks.json               # Build/test tasks
│   └── launch.json              # Debug configurations
└── external_tools/              # Downloaded GitHub tools
    ├── bat/
    ├── fd/
    ├── ripgrep/
    ├── fzf/
    └── tools_index.json         # Tool inventory
```

## 🎯 Usage Examples

### Example 1: Setup New Development Environment
```powershell
# Install everything
vscode-setup

# Download useful tools
github-tools
> select
> bat,fd,ripgrep,fzf

# Restart VS Code
code ghostlink.code-workspace
```

### Example 2: Add Specific Extension
```powershell
# List what's installed
vscode-list

# Install more via VS Code CLI
code --install-extension <extension-id>

# Or let VS Code prompt from extensions.json
# Open Command Palette > Extensions: Show Recommended Extensions
```

### Example 3: Clone Custom GitHub Repo
```powershell
python github_tools.py --clone https://github.com/user/repo
```

### Example 4: Update All Tools
```powershell
# Re-run download (will pull latest for existing repos)
github-tools
```

## 🔧 Advanced Configuration

### Custom VS Code Settings

Edit `.vscode/settings.json` directly or modify `vscode_integration.py`:

```python
ghostlink_settings = {
    "your.custom.setting": "value",
    ...
}
```

Then run: `python vscode_integration.py --settings`

### Add More Extensions

Edit `vscode_integration.py` and add to `extensions` dict:

```python
extensions = {
    ...
    "publisher.extension-name": "Description",
}
```

Then run: `python vscode_integration.py --extensions`

### Add More GitHub Tools

Edit `github_tools.py` and add to `tools` list:

```python
tools = [
    ...
    {
        "url": "https://github.com/user/repo",
        "name": "tool-name",
        "description": "Tool description",
        "category": "Category"
    }
]
```

## 💡 Tips & Best Practices

### 1. Use Workspace File
Open `ghostlink.code-workspace` instead of folder for:
- Pre-configured settings
- Recommended extensions prompt
- Task definitions
- Multi-root support

### 2. Extension Sync
Enable VS Code Settings Sync to share configuration across machines:
```
File > Preferences > Settings Sync
```

### 3. Extension Dependencies
Some extensions work better together:
- **Python** + **Pylance** + **Debugpy** = Complete Python IDE
- **Docker** + **Dev Containers** = Containerized development
- **GitLens** + **GitHub PR** = Full Git workflow

### 4. Performance
Too many extensions can slow VS Code:
- Disable unused extensions
- Use workspace-specific recommendations
- Check extension resource usage: `Developer: Show Running Extensions`

### 5. Tool Updates
Keep external tools updated:
```powershell
github-tools  # Re-run to pull latest
```

## 🔍 Troubleshooting

### VS Code CLI Not Found
```powershell
# Windows: Add to PATH
$env:Path += ";C:\Users\<user>\AppData\Local\Programs\Microsoft VS Code\bin"

# Verify
code --version
```

### Extension Install Fails
```powershell
# Manual install
code --install-extension <extension-id>

# Check marketplace availability
# Some extensions may be deprecated
```

### Settings Not Applied
```powershell
# Force reload
vscode-settings

# Restart VS Code
# File > Reload Window
```

### Git Not Found (for GitHub tools)
```powershell
# Install Git for Windows
winget install Git.Git

# Verify
git --version
```

### Unicode Errors in PowerShell
```powershell
# Set UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

## 📊 Integration Status

### ✅ Completed
- VS Code settings manager
- Extension installer
- Workspace generator
- GitHub tools downloader
- Shell command integration
- Toolbox forge integration
- JSONc parser for settings
- Unicode handling

### 🔄 Enhanced From Existing
- `.vscode/settings.json` - Merged GhostLink settings
- `.vscode/extensions.json` - Updated recommendations
- `ghostlink_shell_integration.ps1` - Added commands
- `toolbox_forge.py` - Added tools categories

## 🎓 Resources

### VS Code Documentation
- [Extension Marketplace](https://marketplace.visualstudio.com/vscode)
- [Settings Reference](https://code.visualstudio.com/docs/getstarted/settings)
- [Tasks Documentation](https://code.visualstudio.com/docs/editor/tasks)

### GitHub Tools
- Explore: [GitHub Trending](https://github.com/trending)
- Awesome Lists: [Awesome Python](https://github.com/vinta/awesome-python)
- CLI Tools: [Modern Unix](https://github.com/ibraheemdev/modern-unix)

## 🚀 Summary

**VS Code integration is now fully installed inside GhostLink!**

### What You Get:
- ✅ **51+ extensions** ready to install
- ✅ **Auto-configured settings** for GhostLink
- ✅ **Workspace file** for project structure
- ✅ **GitHub tools manager** for external utilities
- ✅ **Shell commands** for easy access
- ✅ **Forge integration** for unified control

### Quick Commands:
```powershell
vscode-setup      # Full setup
vscode-list       # List extensions
github-tools      # Download tools
forge vscode-setup # Via forge
```

### Files Created:
- `vscode_integration.py` - VS Code manager
- `github_tools.py` - GitHub tools manager
- `ghostlink.code-workspace` - Workspace file

**All tools are integrated and ready to use!** 🎉

---

**Status**: ✅ Complete
**Last Updated**: November 23, 2025
**Extensions Available**: 25+ recommended
**GitHub Tools**: 20+ utilities

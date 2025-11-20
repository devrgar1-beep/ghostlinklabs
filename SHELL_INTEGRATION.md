# Shell Integration Setup for GhostLink

GhostLink now includes **full shell integration** with VS Code, providing enhanced terminal capabilities, command tracking, and AI-assisted shell operations.

## 🚀 Features Enabled

### Shell Integration
- ✅ **Command Decoration** - Visual indicators for command success/failure
- ✅ **Command History** - 100 commands preserved with shell integration
- ✅ **Intelligent Suggestions** - Context-aware command completions
- ✅ **Persistent Sessions** - Terminal state preserved across restarts
- ✅ **Link Agent Environment** - `GHOSTLINK_LINK_ENABLED=true` in all terminals

### Installed Extensions (All Open Source)

```vscode-extensions
ms-vscode.powershell,foxundermoon.shell-format,timonwong.shellcheck,mads-hartmann.bash-ide-vscode
```

## 📦 Installed Extensions

### 1. **PowerShell** (`ms-vscode.powershell`)
- **License**: MIT
- **Features**:
  - Syntax highlighting and IntelliSense
  - Script debugging
  - Script analysis (PSScriptAnalyzer)
  - Integrated console
- **Status**: ✅ Installed

### 2. **shell-format** (`foxundermoon.shell-format`)
- **License**: MIT
- **Features**:
  - Format shell scripts (bash, sh, zsh)
  - Format Dockerfile, gitignore, .env files
  - Automatic formatting on save
- **Status**: ✅ Installed
- **Config**: 2-space indentation, compact if statements

### 3. **ShellCheck** (`timonwong.shellcheck`)
- **License**: GPL-3.0 (open source)
- **Features**:
  - Real-time shell script linting
  - Best practice recommendations
  - Error detection and fixes
- **Status**: ✅ Installed
- **Config**: See `.shellcheckrc`

### 4. **Bash IDE** (`mads-hartmann.bash-ide-vscode`)
- **License**: MIT
- **Features**:
  - Language server for Bash
  - Go-to-definition
  - Symbol highlighting
  - Code completion
- **Status**: ✅ Installed

## 🔧 Configuration

### Shell Integration Settings

```json
{
  "terminal.integrated.shellIntegration.enabled": true,
  "terminal.integrated.shellIntegration.decorationsEnabled": "both",
  "terminal.integrated.shellIntegration.history": 100,
  "terminal.integrated.shellIntegration.suggestEnabled": true,
  "terminal.integrated.enablePersistentSessions": true
}
```

### ShellCheck Configuration (`.shellcheckrc`)

```bash
# Disable SC1091 (not following included files)
disable=SC1091
enable=all
shell=bash
```

### Shell Format Configuration

```json
{
  "shellformat.flag": "-i 2 -ci"  // 2-space indent, compact if
}
```

## 🎯 Terminal Profiles

Three custom terminal profiles available:

### 1. GhostLink - PowerShell
- **Icon**: 🔷 PowerShell
- **Color**: Magenta
- **Environment**: `GHOSTLINK_LINK_ENABLED=true`

### 2. Link Agent
- **Icon**: 🤖 Robot
- **Color**: Cyan
- **Command**: Launches `link start` automatically
- **Purpose**: Dedicated Link agent terminal

### 3. Python
- **Icon**: 🔷 Keyword
- **Color**: Yellow
- **Environment**: `PYTHONPATH` set to workspace root
- **Purpose**: Python REPL and script execution

## 📋 Usage

### Open Terminal Profiles

**Method 1**: Command Palette
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: "Terminal: Select Default Profile"
3. Choose your profile

**Method 2**: Terminal Dropdown
1. Click the `+` dropdown in terminal panel
2. Select profile from list

**Method 3**: Keyboard Shortcut
- ``Ctrl+` `` - Open default terminal
- `Ctrl+Shift+` ` - Open new terminal

### Shell Integration Commands

Shell integration adds these capabilities:

**Command Navigation**:
- `Ctrl+Up/Down` - Navigate between commands
- `Ctrl+Shift+Up/Down` - Select command output

**Command Actions**:
- Click decoration to see command details
- Right-click command for actions (copy, rerun, etc.)

**Link Integration**:
```powershell
# Link is available in all terminals
link status
link task add "Deploy feature X"
link context set project=ghostlink
```

## 🧪 Testing Shell Integration

### Test 1: Command Decoration
```powershell
echo "Success test"  # Should show ✓ decoration
false               # Should show ✗ decoration (on Unix/WSL)
```

### Test 2: Command History
```powershell
# Run several commands, then press:
# Ctrl+R to search history (in PowerShell 7+)
# Or use Up/Down arrows
```

### Test 3: Link Agent Terminal
```powershell
# Open "Link Agent" terminal profile
# Should auto-start: link start
```

### Test 4: Shell Formatting
1. Create a file: `test.sh`
2. Add unformatted content:
   ```bash
   if [ -f file.txt ]; then
   echo "exists"
   fi
   ```
3. Save - should auto-format to:
   ```bash
   if [ -f file.txt ]; then
     echo "exists"
   fi
   ```

### Test 5: ShellCheck Linting
1. Create a file: `test.sh`
2. Add problematic code:
   ```bash
   echo $undefined_var
   ```
3. Should see warning about unquoted variable

## 🔗 Link Agent + Shell Integration

Link now leverages shell integration for enhanced capabilities:

### Context Awareness
Link can detect:
- Current working directory
- Last command executed
- Command exit codes
- Terminal environment variables

### Smart Task Creation
```powershell
# In terminal:
git status  # Shows uncommitted changes

# Then in Copilot Chat:
@link The git status shows changes. Create a task to commit them.
# Link creates task: "Commit pending changes" with context
```

### Command Suggestions
```powershell
@link How do I run the linter?
# Link responds with: make lint
# Click to execute directly in terminal
```

## 🛠️ Troubleshooting

### Shell Integration Not Working

**PowerShell**:
1. Ensure PowerShell 7+ is installed
2. Check: `$PSVersionTable.PSVersion`
3. Update if needed: `winget install Microsoft.PowerShell`

**Bash/WSL**:
1. Shell integration requires bash 4.0+
2. Check: `bash --version`
3. Update via package manager if needed

### ShellCheck Errors

**"shellcheck executable not found"**:
```powershell
# Windows (via Chocolatey)
choco install shellcheck

# Windows (via Scoop)
scoop install shellcheck

# WSL/Linux
sudo apt install shellcheck  # Debian/Ubuntu
sudo yum install ShellCheck  # RHEL/CentOS
brew install shellcheck      # macOS
```

**Alternative**: Disable ShellCheck in settings:
```json
{
  "shellcheck.enable": false
}
```

### Shell Format Issues

**"shfmt not found"**:
```powershell
# Windows (via Scoop)
scoop install shfmt

# Windows (via Chocolatey)
choco install shfmt

# Or download from: https://github.com/mvdan/sh/releases
```

**Alternative**: Use PowerShell formatter only:
```json
{
  "[shellscript]": {
    "editor.formatOnSave": false
  }
}
```

## 📚 Additional Resources

- **PowerShell Extension**: https://github.com/PowerShell/vscode-powershell
- **ShellCheck**: https://github.com/koalaman/shellcheck
- **shell-format**: https://github.com/foxundermoon/vs-shell-format
- **Bash IDE**: https://github.com/bash-lsp/bash-language-server
- **VS Code Shell Integration**: https://code.visualstudio.com/docs/terminal/shell-integration

## 🎉 Benefits

With shell integration enabled, you get:

1. **Visual Feedback** - Instant success/failure indicators
2. **Command History** - Persistent, searchable command log
3. **Link Awareness** - Link knows what you're doing in terminal
4. **Better Debugging** - Clear command output boundaries
5. **Productivity Boost** - Quick command re-execution and navigation
6. **Professional Linting** - Catch shell script issues early
7. **Consistent Formatting** - Auto-format shell scripts on save

## 🔐 Security & Privacy

All installed extensions are open source:
- ✅ MIT License: PowerShell, shell-format, Bash IDE
- ✅ GPL-3.0 License: ShellCheck (copyleft open source)
- ✅ No telemetry by default (VS Code respects `telemetry.telemetryLevel`)
- ✅ No proprietary dependencies
- ✅ Local-only processing (no cloud services)

---

**Shell integration is now fully enabled! 🚀**

Try opening a terminal and running some Link commands to see it in action.

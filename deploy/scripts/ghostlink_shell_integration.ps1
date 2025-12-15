# GhostLink Shell Integration for PowerShell
# This script enables deep shell integration for GhostLink system

# Set encoding for Unicode support
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# GhostLink Environment Variables
$env:GHOSTLINK_ROOT = "D:\ghostlinklabs"
$env:GHOSTLINK_ACTIVE = "true"
$env:GHOSTLINK_SHELL = "powershell"

# Add GhostLink to PATH
$env:Path = "$env:GHOSTLINK_ROOT;$env:GHOSTLINK_ROOT\ghostlink;$env:Path"

# GhostLink Command Aliases
function gl { python -m ghostlink.link_cli @args }
function link { python -m ghostlink.link_cli @args }
function ghost { python -m ghostlink.link_cli @args }
function void { python "$env:GHOSTLINK_ROOT\void_activation.py" @args }
function glctl { python -m ghostlink.link_cli @args }

# Quick Commands
function gl-start { python -m ghostlink.link_cli start @args }
function gl-stop { python -m ghostlink.link_cli stop }
function gl-status { python -m ghostlink.link_cli status }
function gl-health { python -m ghostlink.link_cli diagnostics health }
function gl-audit { python "$env:GHOSTLINK_ROOT\ghostlink_audit.py" @args }
function gl-server { python -m uvicorn ghostlink.main:app --host 127.0.0.1 --port 8001 @args }

# BIOS/Hardware Commands
function gl-bios { python "$env:GHOSTLINK_ROOT\void_activation.py" --admin-override --bridge-bios }
function gl-hardware { python "$env:GHOSTLINK_ROOT\void_activation.py" --admin-override }
function gl-void { python "$env:GHOSTLINK_ROOT\void_activation.py" --admin-override @args }

# Git Integration
function gl-sync { python -m ghostlink.link_cli git sync }
function gl-pull { python -m ghostlink.link_cli git pull }
function gl-git { python -m ghostlink.link_cli git @args }

# Task Management
function gl-task { python -m ghostlink.link_cli task @args }
function gl-tasks { python -m ghostlink.link_cli task list }
function gl-add { python -m ghostlink.link_cli task add @args }

# Context Management
function gl-ctx { python -m ghostlink.link_cli context @args }
function gl-set { python -m ghostlink.link_cli context set @args }
function gl-get { python -m ghostlink.link_cli context list }

# Toolbox Forge - Unified Command Center
function forge { python "$env:GHOSTLINK_ROOT\toolbox_forge.py" @args }
function gl-forge { python "$env:GHOSTLINK_ROOT\toolbox_forge.py" @args }
function toolbox { python "$env:GHOSTLINK_ROOT\toolbox_forge.py" @args }

# Groq Integration - Internal Communication AI
function groq-test { python "$env:GHOSTLINK_ROOT\groq_integration.py" }
function groq-comm {
    param([string]$sender, [string]$receiver, [string]$message)
    python -c "from groq_integration import GroqClient; c = GroqClient(); print(c.internal_communication('$sender', '$receiver', '$message'))"
}
function groq-chat {
    param([string]$prompt)
    python -c "from groq_integration import GroqClient; c = GroqClient(); print(c.simple_chat('$prompt', 'You are GhostLink internal communication AI.'))"
}

# Lattice - Unified Component Bridge
function lattice { python "$env:GHOSTLINK_ROOT\ghostlink_lattice.py" @args }
function lattice-demo { python "$env:GHOSTLINK_ROOT\ghostlink_lattice.py" --demo }
function lattice-state { python "$env:GHOSTLINK_ROOT\ghostlink_lattice.py" --state }
function lattice-interactive { python "$env:GHOSTLINK_ROOT\ghostlink_lattice.py" --interactive }
function lattice-visual { python "$env:GHOSTLINK_ROOT\lattice_visualizer.py" }

# VS Code Integration
function vscode-setup { python "$env:GHOSTLINK_ROOT\vscode_integration.py" --install }
function vscode-extensions { python "$env:GHOSTLINK_ROOT\vscode_integration.py" --extensions }
function vscode-settings { python "$env:GHOSTLINK_ROOT\vscode_integration.py" --settings }
function vscode-list { python "$env:GHOSTLINK_ROOT\vscode_integration.py" --list }

# GitHub Tools
function github-tools { python "$env:GHOSTLINK_ROOT\github_tools.py" --download }
function github-list { python "$env:GHOSTLINK_ROOT\github_tools.py" --list }
function github-index { python "$env:GHOSTLINK_ROOT\github_tools.py" --index }

# Prompt Enhancement
function prompt {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal] $identity
    $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

    $ghostlink_status = if ($env:GHOSTLINK_ACTIVE -eq "true") { "👻" } else { "" }
    $admin_indicator = if ($isAdmin) { "[ADMIN] " } else { "" }

    $location = Get-Location
    "$admin_indicator$ghostlink_status PS $location> "
}

# Tab Completion for GhostLink Commands
Register-ArgumentCompleter -CommandName gl, link, ghost, glctl -ScriptBlock {
    param($commandName, $wordToComplete, $commandAst, $fakeBoundParameters)

    $commands = @(
        'start', 'stop', 'status', 'health', 'diagnostics',
        'task', 'context', 'git', 'history'
    )

    $commands | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
    }
}

# Auto-start message
Write-Host "🧠 GhostLink Shell Integration Loaded" -ForegroundColor Cyan
Write-Host "   Commands: gl, link, ghost, void, gl-status, gl-server" -ForegroundColor Gray
Write-Host "   Quick: gl-start, gl-stop, gl-health, gl-bios" -ForegroundColor Gray

# Check if running as admin
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal] $identity
if ($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "   Status: ⚡ Administrator Mode" -ForegroundColor Green
} else {
    Write-Host "   Status: 👤 User Mode (run as admin for full hardware access)" -ForegroundColor Yellow
}

# PSReadLine enhancements if available
if (Get-Module -ListAvailable -Name PSReadLine) {
    Import-Module PSReadLine
    try {
        Set-PSReadLineOption -EditMode Windows -ErrorAction SilentlyContinue
        Set-PSReadLineOption -HistorySearchCursorMovesToEnd -ErrorAction SilentlyContinue
    } catch {
        # Older PSReadLine version, skip advanced options
    }
    Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
    Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
}

# Change to GhostLink directory if not already there
if ($PWD.Path -ne $env:GHOSTLINK_ROOT) {
    Set-Location $env:GHOSTLINK_ROOT
    Write-Host "   Location: $env:GHOSTLINK_ROOT" -ForegroundColor Gray
}

Write-Host ""

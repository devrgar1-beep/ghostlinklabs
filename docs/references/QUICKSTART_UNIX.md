# !/usr/bin/env bash

# Quick Start: Full Unix Integration

## What Was Installed

Complete Unix/Linux system integration for GhostLink with:

✅ Universal command: `ghostlink`
✅ Shell completions (bash + zsh)
✅ Manual pages
✅ Systemd services (Linux)
✅ XDG Base Directory compliance
✅ Automatic configuration
✅ Logging infrastructure
✅ Installation automation

## Immediate Usage

### Direct Commands

From project directory:

```bash
cd /path/to/ghostlinklabs

# Check status
./bin/ghostlink status

# List tasks
./bin/ghostlink task list

# Show help
./bin/ghostlink help
```

### Add to PATH

Make available system-wide:

```bash
# Option 1: Create symlink (recommended)
sudo ln -s /path/to/ghostlinklabs/bin/ghostlink /usr/local/bin/

# Option 2: Add to shell profile
export PATH="/path/to/ghostlinklabs/bin:$PATH"
```

### Shell Integration

Add to ~/.bashrc or ~/.zshrc:

```bash
source /path/to/ghostlinklabs/etc/ghostlink-shell-init.sh
```

Then reload shell and use aliases:

```bash
gl status           # Shorter alias
glask task list     # Task commands
glgit status        # Git commands
gldiag health       # Diagnostics
```

## Installation

### Automated (Recommended)

```bash
cd /path/to/ghostlinklabs
bash scripts/install-ghostlink.sh
```

This installs:

- Commands to `/usr/local/bin/`
- Completions
- Man pages
- Configuration templates
- User-level systemd services

### Manual

Already done for you:

- ✅ `bin/ghostlink` - Main command (executable)
- ✅ Shell completions created
- ✅ Man pages created
- ✅ Systemd units created
- ✅ Shell init script created

## Available Commands

```bash
# Global
ghostlink status              # Check status
ghostlink start               # Start Link
ghostlink stop                # Stop Link
ghostlink version             # Show version
ghostlink help                # Show help

# Tasks
ghostlink task list           # List all tasks
ghostlink task add "desc"     # Add new task
ghostlink task complete <id>  # Complete task

# Git
ghostlink git status          # Git status
ghostlink git sync            # Sync with remote
ghostlink git pull            # Pull changes

# Diagnostics
ghostlink diagnostics health  # Health check
ghostlink diagnostics errors  # View errors
ghostlink diagnostics monitor # Monitor system

# Context & Learning
ghostlink context list        # List context
ghostlink context set K V     # Set variable
ghostlink learn list          # Show preferences
ghostlink history             # Show history

# System
ghostlink daemon start        # Start daemon
ghostlink daemon stop         # Stop daemon
```

## Configuration

Auto-created at: `~/.config/ghostlink/ghostlink.conf`

Edit with your settings:

```bash
nano ~/.config/ghostlink/ghostlink.conf
```

## Data Locations (XDG Standard)

```
~/.config/ghostlink/              # Configuration
~/.local/share/ghostlink/         # Data & logs
~/.local/share/ghostlink/logs/    # Log files
~/.cache/ghostlink/               # Cache
```

## Systemd (Linux Only)

Enable auto-start at login:

```bash
systemctl --user enable ghostlink.service
systemctl --user start ghostlink.service
systemctl --user status ghostlink.service
```

View logs:

```bash
journalctl --user -u ghostlink -f
```

## Shell Aliases (After Shell Init)

```bash
gl              # ghostlink
glctx           # context
glask           # tasks
glgit           # git
gldiag          # diagnostics
gllearn         # learning
glhistory       # history

# Functions
gl-status       # Quick status
gl-quick        # Quick reference
```

## Verification

Test everything works:

```bash
ghostlink version     # Should show 0.1.0
ghostlink status      # Should show status
ghostlink task list   # Should show tasks
ghostlink help        # Should show commands
```

## Next Steps

1. **Source shell init (optional):**

   ```bash
   echo 'source /path/to/ghostlinklabs/etc/ghostlink-shell-init.sh' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Try commands:**

## Prerequisites & Security Notes

- Install Python 3.8+ and pip, or the containerized mode
- If using the venv runner, ensure `tmux` is installed (recommended) to run long-lived processes
- For Docker deployments, mount TLS certs at `/run/ghostlink` and use `GL_TLS_CERT`, `GL_TLS_KEY`, `GL_TLS_CA` environment variables if you enable TLS
- If you use Docker's host networking mode, services may be exposed on all host interfaces; confirm firewall rules and limit to loopback if necessary


   ```bash
   gl status
   gl task add "My first task"
   gl task list
   ```

3. **Enable daemon (Linux):**

   ```bash
   systemctl --user enable ghostlink
   systemctl --user start ghostlink
   ```

4. **Read documentation:**

   ```bash
   man ghostlink        # Full manual
   ghostlink help       # Quick help
   cat UNIX_INTEGRATION.md
   ```

## Platform Support

| Feature | macOS | Linux | BSD |
|---------|-------|-------|-----|
| Commands | ✅ | ✅ | ✅ |
| Completions | ⚠️ | ✅ | ✅ |
| Man pages | ✅ | ✅ | ✅ |
| Systemd | ❌ | ✅ | ❌ |

## Files Created/Modified

✅ bin/ghostlink - Main command wrapper
✅ bin/ghostlink.bash-completion.sh - Bash completions
✅ bin/_ghostlink - Zsh completions
✅ man/man1/ghostlink.1 - Manual page
✅ systemd/*.service - Systemd units (Linux)
✅ etc/ghostlink-shell-init.sh - Shell integration
✅ scripts/install-ghostlink.sh - Installation script
✅ UNIX_INTEGRATION.md - Comprehensive guide
✅ UNIX_ALIGNMENT_COMPLETE.md - Completion report

## Troubleshooting

### Command not found

```bash
# Add to PATH
export PATH="/path/to/ghostlinklabs/bin:$PATH"
```

### Config not created

```bash
# Manually create
mkdir -p ~/.config/ghostlink ~/.local/share/ghostlink/logs
```

### Completions not working

```bash
# Reload shell
exec bash -l  # for bash
exec zsh -l   # for zsh
```

### Need help

```bash
ghostlink help
man ghostlink
cat UNIX_INTEGRATION.md
```

## Support

- Documentation: `man ghostlink`
- GitHub: <https://github.com/devrgar1-beep/ghostlinklabs>
- Issues: Report on GitHub

---

**Status:** ✅ Complete and Ready for Use
**Version:** 0.1.0
**Date:** December 3, 2025

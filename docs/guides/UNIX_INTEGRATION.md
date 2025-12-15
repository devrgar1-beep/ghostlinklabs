# Unix Integration & System Setup

Complete Unix alignment and integration for GhostLink framework.

## Overview

GhostLink has been fully integrated with Unix/Linux systems following:
- XDG Base Directory Specification
- systemd standards
- Unix conventions and best practices
- POSIX compliance

## Installation

### Automated Installation

```bash
cd /path/to/ghostlinklabs
bash scripts/install-ghostlink.sh
```

### Manual Installation

1. **Make executable:**
   ```bash
   chmod +x bin/ghostlink
   chmod +x scripts/install-ghostlink.sh
   ```

2. **Create symlink (optional):**
   ```bash
   sudo ln -s /path/to/bin/ghostlink /usr/local/bin/ghostlink
   ```

3. **Install completions:**
   ```bash
   # Bash
   sudo cp bin/ghostlink.bash-completion.sh /etc/bash_completion.d/ghostlink

   # Zsh
   sudo cp bin/_ghostlink /usr/share/zsh/site-functions/
   ```

4. **Install man page:**
   ```bash
   sudo mkdir -p /usr/local/share/man/man1
   sudo cp man/man1/ghostlink.1 /usr/local/share/man/man1/
   ```

## Shell Integration

### Bash

Add to `~/.bashrc`:

```bash
# GhostLink initialization
source /path/to/ghostlinklabs/etc/ghostlink-shell-init.sh
```

Then reload:
```bash
source ~/.bashrc
```

### Zsh

Add to `~/.zshrc`:

```bash
# GhostLink initialization
source /path/to/ghostlinklabs/etc/ghostlink-shell-init.sh
```

Then reload:
```bash
source ~/.zshrc
```

## Available Commands

### Global
```bash
ghostlink status          # Check status
ghostlink start          # Start Link
ghostlink stop           # Stop Link
ghostlink help           # Show help
ghostlink version        # Show version
```

### Tasks
```bash
ghostlink task list           # List tasks
ghostlink task add "desc"     # Add task
ghostlink task status <id>    # Show task
ghostlink task complete <id>  # Complete task
```

### Git Operations
```bash
ghostlink git status     # Git status
ghostlink git sync       # Sync with remote
ghostlink git pull       # Pull changes
ghostlink git abort      # Abort merge
```

### Diagnostics
```bash
ghostlink diagnostics health      # Health check
ghostlink diagnostics errors      # View errors
ghostlink diagnostics fix-common  # Auto-fix issues
ghostlink diagnostics monitor     # Monitor system
ghostlink diagnostics sysinfo     # System info
```

### Context & Learning
```bash
ghostlink context list                # List context
ghostlink context set KEY VALUE       # Set variable
ghostlink learn list                  # Show preferences
ghostlink learn add KEY VALUE         # Add preference
ghostlink history                     # Show history
```

### Shell Aliases (after sourcing ghostlink-shell-init.sh)
```bash
gl               # ghostlink
glctx            # context commands
glask            # task commands
glgit            # git commands
gldiag           # diagnostics
gllearn          # learning commands
glhistory        # history
gl-status        # Quick status check
gl-quick         # Show quick reference
```

## Configuration

### Config Directories (XDG Standard)

```
~/.config/ghostlink/              # Configuration
~/.local/share/ghostlink/         # Data & logs
~/.cache/ghostlink/               # Temporary files
/run/user/$(id -u)/ghostlink/     # Runtime files
```

### Configuration File

Located at: `~/.config/ghostlink/ghostlink.conf`

```conf
# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Performance
WORKERS=auto
TIMEOUT=30

# Networking
BIND_HOST=127.0.0.1
BIND_PORT=8000
```

## Systemd Integration (Linux)

### User-Level Service

```bash
# Enable automatic start at login
systemctl --user enable ghostlink.service

# Start the service
systemctl --user start ghostlink.service

# Check status
systemctl --user status ghostlink.service

# View logs
journalctl --user -u ghostlink

# Follow logs
journalctl --user -u ghostlink -f

# Stop the service
systemctl --user stop ghostlink.service
```

### Available Units

- `ghostlink.service` - Main daemon
- `ghostlink.socket` - Socket activation
- `ghostlink-health.service` - Health check
- `ghostlink-health.timer` - Health check scheduler

### Health Checks

The system automatically runs health checks every 5 minutes:

```bash
# View last health check
journalctl --user -u ghostlink-health.service -n 20

# Run manual health check
ghostlink diagnostics health
```

## Environment Variables

### XDG Base Directory

```bash
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_CACHE_HOME="$HOME/.cache"
```

### GhostLink Specific

```bash
export GHOSTLINK_HOME="/path/to/ghostlinklabs"
export GHOSTLINK_CONFIG_DIR="$HOME/.config/ghostlink"
export GHOSTLINK_DATA_DIR="$HOME/.local/share/ghostlink"
export GHOSTLINK_LOG_DIR="$HOME/.local/share/ghostlink/logs"
export GHOSTLINK_RUNTIME_DIR="/run/user/$(id -u)/ghostlink"
```

## Logging

### Log Files

```bash
# Main logs
~/.local/share/ghostlink/logs/

# Daemon logs
journalctl --user -u ghostlink -f

# Health check logs
journalctl --user -u ghostlink-health -f
```

### Log Rotation

Configure in `/etc/logrotate.d/ghostlink`:

```
~/.local/share/ghostlink/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

## Platform-Specific Notes

### macOS

- Systemd not available (use launchd instead)
- All XDG directories work normally
- Shell completions installed to Homebrew locations if available

### Linux (systemd)

- Full systemd integration available
- User-level units (no elevated privileges needed)
- Socket activation supported

### BSD

- Basic POSIX compliance
- No systemd services (use rc.d instead)
- XDG directories work normally

## Troubleshooting

### Command Not Found

Ensure `$GHOSTLINK_HOME/bin` is in PATH:

```bash
export PATH="$GHOSTLINK_HOME/bin:$PATH"
```

### Systemd Service Won't Start

Check logs:
```bash
journalctl --user -u ghostlink -n 50
```

### Config Not Found

Verify config directory:
```bash
ghostlink context list  # Will show where config is expected
```

### Permission Issues

Ensure proper directory ownership:
```bash
chmod 700 ~/.config/ghostlink
chmod 700 ~/.local/share/ghostlink
```

## Verification

### Test Installation

```bash
# Check version
ghostlink version

# Run health check
ghostlink diagnostics health

# List tasks
ghostlink task list

# View help
ghostlink help
```

### Check Integration

```bash
# Verify shell integration
echo $GHOSTLINK_HOME

# Check aliases
alias gl

# Test completion (in Bash/Zsh)
ghostlink task <TAB>
```

## Advanced Usage

### Custom Installation Directory

```bash
INSTALL_PREFIX=$HOME/.local bash scripts/install-ghostlink.sh
```

### Custom Config Location

```bash
export GHOSTLINK_CONFIG_DIR="/etc/ghostlink"
ghostlink status
```

### Daemon Mode

```bash
# Start as background daemon
ghostlink daemon start

# Stop daemon
ghostlink daemon stop

# Check daemon logs
tail -f ~/.local/share/ghostlink/logs/daemon.log
```

### Integration with Other Tools

```bash
# Use in scripts
if ghostlink task list | grep -q "deploy"; then
    echo "Deploy task found"
fi

# Pipe output
ghostlink task list | jq '.tasks[] | .id'

# Combine with git
ghostlink git sync && ghostlink task list
```

## Performance Tuning

### System Limits

Adjust if needed:
```bash
# Increase file descriptors
ulimit -n 65535

# Adjust in systemd unit if needed
# Edit ~/.config/systemd/user/ghostlink.service
# Add: LimitNOFILE=65535
```

### Resource Management

Monitor resource usage:
```bash
ghostlink diagnostics monitor
```

## Uninstallation

### Full Uninstall

```bash
bash scripts/install-ghostlink.sh uninstall
```

Or manually:
```bash
# Remove commands
rm /usr/local/bin/ghostlink /usr/local/bin/glctl

# Remove completions
rm /etc/bash_completion.d/ghostlink
rm /usr/share/zsh/site-functions/_ghostlink

# Remove man pages
rm /usr/local/share/man/man1/ghostlink.1

# Disable services
systemctl --user disable ghostlink.service

# Remove config (optional - keeps user data)
rm -rf ~/.config/ghostlink
rm -rf ~/.local/share/ghostlink
```

## Next Steps

1. **Configure shell** - Add init script to shell profile
2. **Enable systemd** - Enable auto-start at login
3. **Add to PATH** - Ensure commands are accessible
4. **Test commands** - Verify integration with `ghostlink status`
5. **Setup aliases** - Use shorter command names

## Support

- Documentation: `man ghostlink`
- GitHub: https://github.com/devrgar1-beep/ghostlinklabs
- Issues: https://github.com/devrgar1-beep/ghostlinklabs/issues

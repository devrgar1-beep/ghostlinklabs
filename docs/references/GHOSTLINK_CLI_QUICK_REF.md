# GhostLink CLI - Quick Reference

## Installation & Setup

```bash
# Install from source
cd ~/ghostlinklabs
./scripts/install-ghostlink.sh

# Verify installation
ghostlink --version
```

## Core Commands

### Status & Control

```bash
# Check Link status
ghostlink status

# Start Link (autonomous operation)
ghostlink start --name "MyBrain"

# Stop Link
ghostlink stop

# Reset memory
ghostlink reset --confirm
```

### Task Management

```bash
# Add a task
ghostlink task add "Fix bug in core module" --priority high

# List all tasks
ghostlink task list

# Filter by status
ghostlink task list --status pending
```

### Context & Learning

```bash
# Set context variable
ghostlink context set user_role "developer"

# Get context variable
ghostlink context get user_role

# List all context
ghostlink context list

# Teach preference
ghostlink learn set style "async_preferred"

# List learned preferences
ghostlink learn list
```

### System Diagnostics

```bash
# Get health status
ghostlink health check

# Monitor in real-time
ghostlink health monitor --duration 60 --interval 5

# Export health data
ghostlink health export --output ~/health.json

# Full system audit
ghostlink audit run

# View audit report
ghostlink audit view

# Show detailed findings
ghostlink audit run --show-findings
```

### Git Operations

```bash
# Auto pull latest
ghostlink git pull

# Auto sync (pull + push)
ghostlink git sync

# Check git status
ghostlink git status

# Abort merge
ghostlink git abort
```

### History & Learning

```bash
# View execution history
ghostlink history

# List recent tasks
ghostlink task list --status completed
```

## Advanced Usage

### Monitoring & Alerts

```bash
# Start 24-hour health monitoring
ghostlink health monitor --duration 86400 --interval 300

# Get comprehensive report
ghostlink audit run --show-findings
```

### Pipeline Operations

```bash
# Create pipeline
ghostlink pipeline create my-pipeline --description "CI/CD Pipeline"

# Execute pipeline
ghostlink pipeline execute my-pipeline

# List pipelines
ghostlink pipeline list
```

## Shell Aliases (if installed)

```bash
gl status              # Quick status
glctx                  # List context
glask                  # Add task
glgit status           # Git status
gldiag                 # Health check
gllearn                # List learned
glhistory              # View history
```

## Common Workflows

### Daily Status Check

```bash
ghostlink status
ghostlink health check
ghostlink audit run
ghostlink task list
```

### Monitor & Learn

```bash
# Start monitoring
ghostlink health monitor --duration 3600 &

# Do work...

# Review what was learned
ghostlink learn list
ghostlink context list
```

### Team Coordination

```bash
# Share context
ghostlink context set team_project "v2.0"
ghostlink context set sprint_number "23"

# Auto sync with team
ghostlink git sync
```

## Report Formats

### Health Check Output

```
Status: HEALTHY
CPU: 25.5% (healthy)
Memory: 45.2% (healthy)
Disk: 62.1% (healthy)
```

### Audit Summary

```
Status: HEALTHY
Findings: 0 total
  ✅ No issues found
```

### Task List

```
[PENDING] Task 1
[COMPLETED] Task 2
[FAILED] Task 3
```

## Environment Variables

```bash
# GhostLink directories
export XDG_CONFIG_HOME=~/.config
export XDG_DATA_HOME=~/.local/share
export XDG_CACHE_HOME=~/.cache

# Service port
export GHOSTLINK_PORT=8000

# Log level
export GHOSTLINK_LOG_LEVEL=INFO
```

## Troubleshooting

### Command Not Found

```bash
# Ensure it's installed
which ghostlink

# Or run directly
~/.local/bin/ghostlink status

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Service Won't Start

```bash
# Check systemd status
systemctl --user status ghostlink

# View logs
journalctl --user-unit ghostlink -f

# Restart service
systemctl --user restart ghostlink
```

### Permission Issues

```bash
# Fix directory permissions
chmod 750 ~/.config/ghostlink
chmod 750 ~/.local/share/ghostlink
chmod 750 ~/.cache/ghostlink
```

## Configuration

### Main Config File

Location: `~/.config/ghostlink/config.json`

```json
{
  "name": "Link",
  "api_port": 8000,
  "log_level": "INFO",
  "memory_path": "~/.local/share/ghostlink/memory.json"
}
```

### Health Check Config

Location: `~/.config/ghostlink/health.json`

```json
{
  "check_interval": 300,
  "thresholds": {
    "cpu_warning": 75,
    "cpu_critical": 90,
    "memory_warning": 80,
    "memory_critical": 95
  }
}
```

## Files & Locations

```
~/.config/ghostlink/          # Configuration
~/.local/share/ghostlink/     # Data, reports, memory
~/.cache/ghostlink/           # Runtime data, cache
/usr/local/bin/ghostlink      # Executable (system install)
/usr/local/share/man/man1/    # Manual pages
/etc/systemd/user-units/      # Systemd services
```

## Getting Help

```bash
# Main help
ghostlink --help

# Command help
ghostlink audit --help
ghostlink health --help
ghostlink task --help

# Man page
man ghostlink

# Documentation
cat SYSTEM_AUDIT_ORCHESTRATION.md
cat UNIX_INTEGRATION.md
cat QUICKSTART_UNIX.md
```

## Performance Tips

1. **Batch Operations**: Use `ghostlink task add` multiple times before running
2. **Scheduled Monitoring**: Run health monitoring during off-peak hours
3. **Cleanup History**: Regularly export and archive old reports
4. **Context Efficiency**: Keep context variables minimal and focused
5. **Task Priorities**: Mark critical tasks as high priority for better resource allocation

## Security Notes

- Reports stored in user home directory only
- No sensitive data in logs
- Configuration files 0600 permissions
- Audit trails preserved for compliance
- All operations are user-level (no root required)

## Related Documentation

- Full documentation: `SYSTEM_AUDIT_ORCHESTRATION.md`
- Unix integration: `UNIX_INTEGRATION.md`
- Setup guide: `QUICKSTART_UNIX.md`
- Architecture: `UNIX_ALIGNMENT_COMPLETE.md`

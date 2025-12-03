# GhostLink Toolbox Forge

Unified command center and toolkit for all GhostLink operations.

## Quick Start

```bash
# Interactive mode
python toolbox_forge.py

# Or use the shortcut
forge

# Command mode
forge status
forge build
forge start-server
```

## Available Tools

### System Tools
- `status` - Get comprehensive system status
- `health` - Run health diagnostics
- `audit [target]` - Run system audit

### Server Tools
- `start-server [--port PORT] [--host HOST]` - Start FastAPI server
- `stop-server` - Stop running servers

### Hardware Tools
- `void` - Run void activation with admin override
- `bios-bridge` - Bridge BIOS and hardware to GhostLink

### Link Orchestrator Tools
- `link-start` - Start Link orchestrator
- `link-stop` - Stop Link orchestrator
- `link-status` - Get Link status

### Git Tools
- `git-sync` - Sync with git repository
- `git-status` - Get git status
- `git-pull` - Pull from git

### Build Tools
- `build` - Build all components
- `clean` - Clean build artifacts

### Development Tools
- `test` - Run all tests
- `lint` - Run linting
- `format` - Format code with black

### Utility Tools
- `shell` - Enable shell integration
- `history` - Show action history
- `info` - Show toolbox information

## Interactive Mode

Run without arguments to enter interactive mode:

```bash
python toolbox_forge.py
```

In interactive mode, you can:
- Type commands without the `forge` prefix
- Use `help` to see available commands
- Use `exit` or `quit` to exit

## PowerShell Integration

After enabling shell integration, you can use these shortcuts:

```powershell
forge status           # System status
forge build           # Build all
forge start-server    # Start server
forge void            # Void activation
forge health          # Health check
```

## History Tracking

All actions are logged with timestamps:

```bash
forge history
```

## Configuration

Configuration is stored in `.ghostlink_forge_config.json` and includes:
- Tool shortcuts
- Action history
- Custom settings

## Examples

```bash
# Check system status
forge status

# Build and start server
forge build
forge start-server --port 8001

# Hardware integration
forge void
forge bios-bridge

# Development workflow
forge clean
forge build
forge test
forge lint

# Git workflow
forge git-status
forge git-pull
forge git-sync
```

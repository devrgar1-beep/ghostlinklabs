# GhostLink AI Bot Framework

Integrated AI agents with hotkey and quick-command root access.

## Features

- **Multiple Bot Types**: System, metrics, and custom plugin bots
- **Hotkey Support**: Global keyboard shortcuts (ctrl+shift+s, etc.)
- **Quick Commands**: Multiple input formats (`/bot cmd`, `!cmd`, `@bot cmd`, `cmd`)
- **Root Access**: Execute privileged commands with proper access control
- **Plugin System**: Dynamic bot loading from `plugins/` directory
- **CLI Interface**: Interactive terminal with help and autocomplete

## Architecture

```
ai_bots/
├── core.py          # Base bot framework, command routing
├── hotkeys.py       # System-level keyboard event capture
├── parser.py        # Command parsing (multiple formats)
├── registry.py      # Bot plugin discovery and management
├── cli.py           # Interactive CLI interface
├── requirements.txt # Dependencies
└── plugins/         # Custom bot plugins
    └── calculator.py
```

## Installation

```bash
cd ai_bots
pip install -r requirements.txt
```

**Dependencies:**
- `psutil` - System monitoring
- `pynput` - Keyboard event capture
- `httpx` - HTTP client for metrics

## Usage

### CLI Interface

```bash
python -m ai_bots.cli
```

**Command formats:**
```
/system status              # Route to specific bot
!status                     # Quick command (any bot)
@metrics get                # Mention style
status                      # Direct (any bot)
```

**Special commands:**
```
help        # Show help
list        # List all commands
hotkeys     # List all hotkeys
exit/quit   # Exit CLI
```

### Built-in Bots

#### SystemBot (root access)
- `status` - System status (CPU, memory)
- `restart <service>` - Restart service
- `logs <lines>` - View logs
- `exec <command>` - Execute shell command

#### MetricsBot (read access)
- `get` - Fetch metrics from controller
- `alert <metric> <threshold>` - Create alert rule

### Hotkeys

- `ctrl+shift+s` - System status
- `ctrl+shift+r` - Restart service
- `ctrl+shift+l` - View logs
- `ctrl+m` - Get metrics

## Creating Custom Bots

Create a new file in `ai_bots/plugins/`:

```python
from ai_bots.core import AIBot, AccessLevel, BotContext
from typing import List

class MyBot(AIBot):
    def __init__(self):
        super().__init__("mybot", AccessLevel.READ)
        
    async def initialize(self):
        self.register_command(
            "hello",
            self.cmd_hello,
            "Say hello",
            AccessLevel.READ,
            hotkey="ctrl+shift+h",
            aliases=["hi"]
        )
        
    async def cmd_hello(self, args: List[str], ctx: BotContext) -> str:
        name = args[0] if args else "World"
        return f"Hello, {name}!"
```

The bot will be automatically discovered and loaded.

## Access Levels

- `READ` - Read-only access
- `WRITE` - Write access
- `ADMIN` - Administrative access
- `ROOT` - Full system access

Commands are checked against user's access level before execution.

## Examples

```bash
# System commands
/system status
/system exec ps aux
/system restart ghostlink

# Metrics
/metrics get
/metrics alert cpu_temp_c 80

# Calculator (plugin example)
/calc add 1 2 3
/calc multiply 2 3 4
/calc eval 2 + 3 * 4
```

## Testing

Run individual components:

```bash
# Test command parser
python ai_bots/parser.py

# Test bot registry
python ai_bots/registry.py

# Test hotkey handler
python ai_bots/hotkeys.py

# Test calculator plugin
python ai_bots/plugins/calculator.py

# Run full CLI
python ai_bots/cli.py
```

## Integration

Import and use in other code:

```python
from ai_bots.core import CommandRouter, SystemBot, BotContext, AccessLevel

router = CommandRouter()
await router.register_bot(SystemBot())

context = BotContext(
    user_id="admin",
    session_id="session123",
    access_level=AccessLevel.ROOT
)

result = await router.route("/system status", context)
print(result)
```

## YOLO Mode

YOLO (You Only Live Once) mode automatically approves dangerous commands without confirmation:

- **Enabled by default** in CLI for root access
- Toggle with `/system yolo` or `!yolo`
- When enabled: Commands like `exec` and `restart` run immediately
- When disabled: Requires confirmation for dangerous operations

**Example:**

```bash
/system yolo          # Toggle YOLO mode
/system exec rm -rf / # Runs immediately if YOLO enabled
```

## Notes

- Hotkey handler requires `pynput` and may need accessibility permissions on macOS
- System commands use subprocess with shell=True - use with caution
- Plugin bots are loaded dynamically - restart CLI to reload changes

# Link Integration

This workspace is configured with **Link** - your AI orchestration brain.

## Quick Access

### Command Palette (Ctrl+Shift+P)
- `Tasks: Run Task` → Select any Link task

### Available Tasks
- **Link: Start** - Start Link's autonomous operation
- **Link: Stop** - Stop Link
- **Link: Status** - Check Link's current status
- **Link: Add Task** - Add a new task with priority
- **Link: List Tasks** - View all tasks
- **Link: View History** - See execution history
- **Link: Set Context** - Set context variables
- **Link: List Context** - View all context

### Debug Configurations
- **Link: Run** - Run Link with debugger
- **Link: CLI** - Debug CLI commands

## Terminal Commands

```bash
# Start Link
python -m ghostlink.link_cli start

# Or use the CLI directly (after pip install -e .)
link start
link status
link task add "Your task here"
```

## Keyboard Shortcuts (Optional)

Add to your `keybindings.json`:

```json
[
  {
    "key": "ctrl+shift+l",
    "command": "workbench.action.tasks.runTask",
    "args": "Link: Status"
  }
]
```

## Files to Watch
- `~/.ghostlink/link_memory.json` - Link's persistent memory
- Watch this file to see Link's state in real-time

## Extension Recommendations
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Python Debugger (ms-python.debugpy)
- Black Formatter (ms-python.black-formatter)
- Ruff (charliermarsh.ruff)

Link is ready to orchestrate your work! 🧠

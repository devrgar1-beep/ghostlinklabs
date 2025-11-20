# Link Agent - GitHub Copilot Chat Integration

This directory contains the VS Code extension that integrates Link as a custom chat participant in GitHub Copilot Chat.

## What is Link Agent?

Link Agent brings your AI orchestration brain directly into GitHub Copilot Chat. You can chat with Link naturally using `@link` in any chat conversation.

## Features

- **Natural Conversation**: Chat with Link using natural language
- **Task Management**: Add, view, and manage tasks through chat
- **Context Awareness**: Link remembers your project context
- **Intelligent Responses**: Link provides contextual, helpful responses
- **Command Support**: Use `/status`, `/tasks`, `/context`, `/learn` commands

## Usage in Chat

```
@link what's your status?
@link add task: Review the authentication module (urgent)
@link show my tasks
@link remember that this project is called GhostLink
@link what have you learned about my preferences?
```

## Commands

- `@link /status` - Check Link's current status
- `@link /tasks` - View or manage tasks
- `@link /context` - View or set context
- `@link /learn` - View or teach preferences
- `@link /help` - Get help

## Keyboard Shortcuts

- `Ctrl+Shift+L` (Windows/Linux) or `Cmd+Shift+L` (Mac) - Open chat with Link

## Configuration

Settings available in VS Code settings:

- `link.enabled` - Enable/disable Link agent (default: true)
- `link.autoStart` - Automatically start Link on workspace open (default: false)
- `link.pythonPath` - Path to Python interpreter (default: "python")

## Development

### Building the Extension

```bash
cd .vscode/link-agent
npm install
npm run compile
```

### Testing Locally

1. Open this folder in VS Code
2. Press F5 to launch Extension Development Host
3. Open any workspace with GhostLink installed
4. Open GitHub Copilot Chat
5. Type `@link hello!`

### Publishing

```bash
npm install -g @vscode/vsce
vsce package
# Creates link-agent-0.1.0.vsix
```

Then install manually or publish to marketplace.

## Architecture

```
User in VS Code Chat
    ↓
@link participant
    ↓
TypeScript Extension
    ↓
Python Link Agent (ghostlink/link_agent.py)
    ↓
Link Core (ghostlink/link.py)
    ↓
GhostLink Components
```

## Requirements

- VS Code 1.80+
- Python 3.8+
- GhostLink installed (`pip install -e .`)
- GitHub Copilot Chat enabled

## Example Conversations

**User:** `@link what are you doing?`
**Link:** 🧠 Link Status Report...

**User:** `@link add task: Fix the login bug (critical)`
**Link:** ✅ Task added: Fix the login bug (Priority: CRITICAL)...

**User:** `@link show my tasks`
**Link:** 📋 Current Tasks...

## Extension API

The extension exposes these commands:

- `link.chat` - Open chat with Link
- `link.addTask` - Quick add task dialog
- `link.showStatus` - Show Link's status

Use them in keybindings or other extensions.

## Troubleshooting

### Link doesn't respond
- Check Python path in settings
- Verify GhostLink is installed: `pip list | grep ghostlink`
- Check extension logs: Output > Link Agent

### Commands not working
- Ensure GitHub Copilot Chat is enabled
- Restart VS Code after installing extension
- Check that `@link` participant is registered

## Contributing

Link Agent is part of the GhostLink open source project. Contributions welcome!

---

**Link Agent** - Your AI brain, now in your chat! 🧠💬

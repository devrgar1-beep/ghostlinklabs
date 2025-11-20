# Link as a Custom Chat Agent

Link is now available as a **custom chat agent** for GitHub Copilot and AI chat interfaces!

## Quick Start

### In GitHub Copilot Chat

```
@link what's your status?
@link add task: Review the auth module (urgent)
@link show my tasks
@link remember that project_name is GhostLink
```

### In Python Code

```python
from ghostlink import chat_with_link
import asyncio

response = await chat_with_link("What's your status?")
print(response)
```

## Installation as Chat Agent

### Option 1: VS Code Extension (Recommended)

1. Navigate to `.vscode/link-agent/`
2. Run: `npm install && npm run compile`
3. Press F5 to launch Extension Development Host
4. Open GitHub Copilot Chat
5. Type `@link hello!`

### Option 2: Direct Python Usage

```python
from ghostlink import LinkAgent, get_link_agent

agent = get_link_agent()
response = await agent.invoke("Show my tasks")
print(response)
```

## Chat Commands

Link understands natural language and these commands:

- **Status**: `@link status`, `@link what are you doing?`
- **Tasks**: `@link show tasks`, `@link add task: [description]`
- **Context**: `@link what do you remember?`, `@link remember [key] is [value]`
- **Learning**: `@link what have you learned?`, `@link learn that I prefer [something]`
- **Help**: `@link help`, `@link what can you do?`

## Features

### Natural Language Understanding

Link parses your intent from natural language:

```
@link add task: Fix the login bug (this is urgent!)
→ Creates CRITICAL priority task

@link show me what's in my queue
→ Lists all pending tasks

@link do you remember my project name?
→ Shows stored context
```

### Intelligent Responses

Link provides contextual, helpful responses:

```
@link what are you doing?
→ 🧠 Link Status Report
  • Active: Yes
  • Pending Tasks: 3
  • Completed: 12
  ...
```

### Priority Detection

Link automatically detects priority from your language:

- **CRITICAL**: urgent, critical, asap, emergency
- **HIGH**: important, high priority, soon
- **LOW**: low priority, later, whenever, nice to have
- **NORMAL**: everything else

### Context Awareness

Link remembers your environment:

```
@link remember that this is the authentication module
@link remember my coding style is concise
@link what do you remember about this project?
```

## Architecture

```
GitHub Copilot Chat
    ↓
@link participant
    ↓
VS Code Extension (TypeScript)
    ↓
LinkAgent (Python)
    ↓
Link Core
    ↓
GhostLink Components
```

## API Reference

### LinkAgent Class

```python
from ghostlink import LinkAgent

agent = LinkAgent()

# Invoke with message
response = await agent.invoke(
    message="Add task: Review code",
    context={"project": "GhostLink"}
)
```

### Helper Function

```python
from ghostlink import chat_with_link

# Quick chat interface
response = await chat_with_link(
    "What's my status?",
    context={"session_id": "123"}
)
```

### GitHub Copilot Integration

```python
from ghostlink.link_agent import LinkCopilotAgent

# Register as Copilot agent
agent_info = LinkCopilotAgent.register_as_copilot_agent()

# Handle chat request
response = await LinkCopilotAgent.handle_chat_request({
    "prompt": "Show my tasks",
    "context": {}
})
```

## Examples

### Task Management Conversation

```
You: @link hey, can you help me organize my work?
Link: 🧠 Of course! I'm Link, your AI orchestration brain...

You: @link add task: Implement user authentication
Link: ✅ Task added: Implement user authentication (Priority: NORMAL)

You: @link actually that's urgent
Link: 📝 I'll update the priority...

You: @link show my tasks
Link: 📋 Current Tasks
      • Implement user authentication (CRITICAL)
      ...
```

### Context Building

```
You: @link remember that this is the backend API
Link: 📝 Context set: project_type = backend API

You: @link remember my preferred language is Python
Link: 📚 Learned: preferred_language = Python

You: @link what do you know about my project?
Link: 🔍 What I Remember:
      • project_type: backend API
      • preferred_language: Python
```

## Configuration

### VS Code Settings

```json
{
  "link.enabled": true,
  "link.autoStart": false,
  "link.pythonPath": "python"
}
```

### Environment Variables

```bash
export GHOSTLINK_LINK_ENABLED=true
```

## Keyboard Shortcuts

- `Ctrl+Shift+L`: Open chat with Link
- Can be customized in VS Code keybindings

## Advanced Usage

### Custom Handler Registration

```python
from ghostlink import get_link_agent

agent = get_link_agent()

async def custom_analyzer(task):
    # Your custom logic
    return {"analysis": "complete"}

agent.link.register_handler("analysis", custom_analyzer)
```

### Conversation Context

```python
context = {
    "session_id": "abc123",
    "user_name": "Ghost",
    "project": "GhostLink"
}

response = await chat_with_link("Status?", context)
```

## Troubleshooting

### Agent doesn't respond in chat
- Verify Python path in settings
- Check GhostLink is installed: `pip list | grep ghostlink`
- Restart VS Code

### Commands not recognized
- Update to latest Link version
- Check GitHub Copilot Chat is enabled
- Review extension logs

## Future Enhancements

- [ ] Multi-turn conversation memory
- [ ] LLM integration for smarter responses
- [ ] Voice command support
- [ ] Team collaboration features
- [ ] Web UI dashboard
- [ ] Slack/Discord integrations

## Contributing

Link Agent is open source! Contributions welcome:
- Add new command parsers
- Enhance natural language understanding
- Integrate with more chat platforms
- Improve response generation

---

**Link** - Now in your chat, orchestrating everything! 🧠💬

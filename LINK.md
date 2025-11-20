# Link - Your AI Brain

**Link** is your autonomous AI orchestration brain built into GhostLink. He coordinates all operations, manages tasks, learns your preferences, and serves as your personal AI assistant.

## What is Link?

Link is an intelligent agent that:
- **Orchestrates** all GhostLink components autonomously
- **Manages** tasks with priority-based scheduling
- **Learns** your preferences and working style
- **Remembers** context across sessions
- **Coordinates** complex multi-step workflows
- **Integrates** with external LLMs (optional)

Think of Link as your digital brain that handles the orchestration while you focus on what matters.

## Quick Start

### CLI Usage

```bash
# Start Link
link start

# Add a task
link task add "Analyze the codebase for improvements" --priority high

# Check status
link status

# Set context
link context set project_name "MyProject"

# Teach preferences
link learn set coding_style "concise"

# View history
link history

# Stop Link
link stop
```

### Python API

```python
import asyncio
from ghostlink import Link, TaskPriority

async def main():
    # Create Link instance
    link = Link(name="Link")
    
    # Start autonomous operation
    await link.start()
    
    # Add tasks
    link.add_task(
        "Build feature X",
        "Implement the new feature according to specs",
        priority=TaskPriority.HIGH,
        metadata={"type": "development"}
    )
    
    # Set context for Link to remember
    link.set_context("user_name", "Ghost")
    link.set_context("project_path", "/path/to/project")
    
    # Learn preferences
    link.learn_preference("output_format", "markdown")
    link.learn_preference("code_style", "black")
    
    # Wait for tasks
    await asyncio.sleep(10)
    
    # Check status
    status = link.get_status()
    print(f"Pending: {status['pending_tasks']}")
    print(f"Completed: {status['completed_tasks']}")
    
    # Stop when done
    await link.stop()

asyncio.run(main())
```

## Features

### 1. Autonomous Task Orchestration

Link manages tasks with intelligent scheduling:

```bash
# Critical tasks run first
link task add "Fix security vulnerability" --priority critical

# Normal priority for routine work
link task add "Update documentation" --priority normal

# Low priority for nice-to-haves
link task add "Refactor old code" --priority low
```

### 2. Persistent Memory

Link remembers everything across sessions:
- All tasks and their status
- Context variables
- Your preferences
- Execution history

Memory is stored in `~/.ghostlink/link_memory.json`

### 3. Context Awareness

Teach Link about your environment:

```bash
# Set project context
link context set project_name "GhostLink"
link context set language "Python"
link context set environment "production"

# Get context
link context get project_name
# Output: project_name = GhostLink

# List all context
link context list
```

### 4. Learning & Preferences

Link learns how you work:

```bash
# Teach preferences
link learn set output_format "json"
link learn set verbosity "low"
link learn set notification_style "minimal"

# View learned preferences
link learn list
```

### 5. Custom Task Handlers

Register custom handlers for specific task types:

```python
from ghostlink import get_link

link = get_link()

async def handle_analysis(task):
    """Custom handler for analysis tasks."""
    # Your analysis logic here
    return {"status": "analyzed", "findings": [...]}

# Register handler
link.register_handler("analysis", handle_analysis)

# Add task with type
link.add_task(
    "Analyze security",
    "Run security analysis on codebase",
    type="analysis"
)
```

## CLI Commands

### Core Commands

```bash
link start                    # Start Link
link stop                     # Stop Link
link status                   # Show status
link history                  # View execution history
link reset --confirm          # Reset memory (careful!)
```

### Task Management

```bash
link task add "description" [--name NAME] [--priority PRIORITY]
link task list [--status STATUS]
```

Priorities: `low`, `normal`, `high`, `critical`

### Context Management

```bash
link context set KEY VALUE    # Set context variable
link context get KEY          # Get context variable
link context list             # List all context
```

### Learning

```bash
link learn set KEY VALUE      # Teach preference
link learn list               # List preferences
```

## Integration with GhostLink

Link coordinates with all GhostLink components:

- **TOOL_CHAIN_ORCHESTRATOR** - Workflow coordination
- **SYMBOLIC_TASK_SCHEDULER** - Task scheduling
- **AUTO_TRIGGER_ENGINE** - Automatic triggers
- **LATTICE_WATCHDOG** - System monitoring
- **RUNTIME_STATE_MANAGER** - State management

## Architecture

```
Link (Your AI Brain)
├── Task Queue (Priority-based)
├── Memory (Persistent)
│   ├── Tasks
│   ├── Context
│   ├── Preferences
│   └── History
├── Orchestrator
│   ├── Task Execution
│   ├── Component Coordination
│   └── Error Handling
└── Handlers (Custom)
    ├── Analysis
    ├── Development
    ├── Monitoring
    └── Custom...
```

## Advanced Usage

### Running as Daemon

```bash
# Start in background
nohup link start > link.log 2>&1 &

# Or use systemd (Linux)
# Create /etc/systemd/system/link.service
```

### Custom Task Types

```python
# Register multiple handlers
link.register_handler("build", handle_build)
link.register_handler("test", handle_test)
link.register_handler("deploy", handle_deploy)

# Add typed tasks
link.add_task("Build project", "...", type="build")
link.add_task("Run tests", "...", type="test")
link.add_task("Deploy to prod", "...", type="deploy")
```

### Monitoring

```python
# Check what Link is doing
status = link.get_status()

print(f"Active: {status['active']}")
print(f"Queue: {status['pending_tasks']} pending")
print(f"Done: {status['completed_tasks']} completed")
print(f"Failed: {status['failed_tasks']} failed")
```

## LLM Integration (Optional)

Link can integrate with open source LLMs for natural language interaction:

```python
from ghostlink import Link
from ghostlink.config import config

# Configure LLM (Ollama, LocalAI, etc.)
link = Link()
llm_config = config.get_llm_config()

if llm_config["enabled"]:
    # Link can now use LLM for natural language tasks
    link.add_task(
        "Summarize codebase",
        "Generate a high-level summary of the project structure",
        type="llm_task"
    )
```

## Examples

### Personal Assistant

```python
# Morning routine
link.add_task("Check system health", "Run diagnostics", priority=TaskPriority.HIGH)
link.add_task("Update dependencies", "Check for updates", priority=TaskPriority.NORMAL)
link.add_task("Generate report", "Daily metrics report", priority=TaskPriority.LOW)
```

### Development Workflow

```bash
# Setup development session
link context set current_branch "feature/new-api"
link context set ticket_id "GHOST-123"

# Add development tasks
link task add "Review code changes" --priority high
link task add "Run test suite" --priority high
link task add "Update documentation" --priority normal
```

### Project Management

```python
# Set project context
link.set_context("sprint", "Sprint 23")
link.set_context("team", "Backend")

# Add sprint tasks
for task in sprint_backlog:
    link.add_task(
        task["name"],
        task["description"],
        priority=task["priority"],
        metadata={"sprint": "Sprint 23", "story_points": task["points"]}
    )
```

## Best Practices

1. **Use Priority Wisely** - Reserve CRITICAL for actual emergencies
2. **Set Context Early** - Help Link understand your environment
3. **Teach Preferences** - Link learns and adapts to your style
4. **Custom Handlers** - Implement task-specific logic for best results
5. **Check Status Regularly** - Monitor Link's progress
6. **Review History** - Learn from past executions

## Troubleshooting

### Link won't start
- Check Python version (3.8+)
- Verify dependencies: `pip install -e ".[dev]"`
- Check memory file permissions: `~/.ghostlink/`

### Tasks not executing
- Verify Link is active: `link status`
- Check task queue: `link task list`
- Review error logs in memory file

### Memory issues
- Check disk space
- Verify write permissions
- Reset if needed: `link reset --confirm`

## Roadmap

Future enhancements for Link:

- [ ] Multi-agent coordination
- [ ] Natural language task input via LLM
- [ ] Web UI dashboard
- [ ] Team collaboration features
- [ ] Plugin system for extensions
- [ ] Advanced scheduling algorithms
- [ ] Predictive task management
- [ ] Integration with external tools (GitHub, Slack, etc.)

## Contributing

Link is part of the open source GhostLink project. Contributions welcome!

---

**Link** - Your autonomous AI brain, coordinating everything while you focus on what matters.

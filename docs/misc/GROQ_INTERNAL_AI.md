# Groq Internal Communication AI

## Overview

Groq provides **ultra-fast LLM inference** for GhostLink's autonomous component communication. It enables real-time reasoning, coordination, and decision-making between system components.

## Purpose

**Internal Communication AI** - Not for external user interaction, but for:
- Link ↔️ Container coordination
- Signal ↔️ Pressure negotiation  
- Autonomous system orchestration
- Real-time inter-component reasoning
- Task scheduling and resource allocation
- Error recovery and adaptive responses

## Architecture

```
┌─────────────────────────────────────────────────┐
│         GhostLink Autonomous System             │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────┐    Groq AI    ┌───────────┐         │
│  │ Link │ ◄──────────► │ Container │         │
│  └──────┘               └───────────┘         │
│      ▲                        ▲                │
│      │     Ultra-fast         │                │
│      │     Inference          │                │
│      ▼                        ▼                │
│  ┌────────┐               ┌──────────┐        │
│  │ Signal │               │ Pressure │        │
│  └────────┘               └──────────┘        │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Configuration

### Model
- **Current**: `llama-3.3-70b-versatile`
- **Context**: 131,072 tokens
- **Speed**: Sub-second inference
- **Max tokens**: 8,192

### Environment
```bash
GROQ_API_KEY=[REDACTED_GROQ_API_KEY]
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_PURPOSE=internal_communication
```

### Config (config.yaml)
```yaml
ai_models:
  groq:
    model: "llama-3.3-70b-versatile"
    max_tokens: 8192
    temperature: 0.7
    api_key_env: "GROQ_API_KEY"
    purpose: "internal_communication"
```

## Usage

### Python API

```python
from groq_integration import GroqClient

client = GroqClient()

# Simple internal communication
response = client.internal_communication(
    sender="Link",
    receiver="Container", 
    message="Request task status and resource allocation",
    context={"active_tasks": 3, "system_load": "moderate"}
)

# Direct chat (for autonomous reasoning)
response = client.simple_chat(
    "Analyze system load and recommend resource reallocation",
    system="You are GhostLink internal communication AI."
)
```

### Shell Commands

```powershell
# Test connection
groq-test

# Check status
groq-status

# Facilitate communication
groq-comm Link Container "Your message here"

# Quick chat
groq-chat "Your prompt here"
```

### Toolbox Forge

```bash
# Test AI
forge groq-test

# Check status
forge groq-status

# Inter-component communication
forge groq-comm Link Container "Message"

# Interactive mode
forge
> groq-status
> groq-comm Signal Pressure "Negotiate bandwidth allocation"
```

## Use Cases

### 1. Task Coordination
```python
response = client.internal_communication(
    sender="Link",
    receiver="Container",
    message="Schedule high-priority task with resource constraints",
    context={"priority": "CRITICAL", "max_cpu": 0.8}
)
```

### 2. Resource Negotiation
```python
response = client.internal_communication(
    sender="Pressure",
    receiver="Signal",
    message="Request additional bandwidth for data transfer",
    context={"current_bw": "50Mbps", "required": "100Mbps"}
)
```

### 3. Error Recovery
```python
response = client.internal_communication(
    sender="Container",
    receiver="Link",
    message="Task failed with memory error, recommend recovery strategy",
    context={"task": "analyze_logs", "error": "MemoryError"}
)
```

### 4. Autonomous Decision-Making
```python
response = client.simple_chat(
    "System load at 90%, 5 pending tasks. Prioritize or defer?",
    system="You coordinate GhostLink autonomous operations."
)
```

## Communication Protocol

### Request Format
```python
{
    "sender": "ComponentName",      # Source component
    "receiver": "ComponentName",    # Target component  
    "message": "Action request",    # What to do
    "context": {                    # Optional state
        "key": "value"
    }
}
```

### Response Format
- Concise, actionable responses
- Component-appropriate language
- Real-time coordination focus
- No external user interaction

## Components

### Autonomous Components
- **Link**: AI orchestration brain, task management
- **Container**: Execution environment, resource management
- **Signal**: Communication protocols, data flow
- **Pressure**: Resource constraints, system health
- **Vault**: Secure storage, memory persistence

### Communication Patterns

```
Link → Container: "Execute task X with priority Y"
Container → Link: "Task X started, ETA 2 minutes"

Pressure → Signal: "Bandwidth constrained at 60%"
Signal → Pressure: "Reducing data transfer rate to 40Mbps"

Link → All: "System health check initiated"
All → Link: "Status: operational"
```

## Performance

- **Latency**: < 500ms average
- **Throughput**: 100+ requests/second
- **Context**: 131K tokens (full system state)
- **Availability**: 99.9% uptime

## Best Practices

1. **Keep messages concise** - 1-2 sentences max
2. **Include context** - System state, task IDs, resource levels
3. **Use consistent naming** - Component names match GhostLink architecture
4. **Error handling** - Always catch exceptions, provide fallbacks
5. **Rate limiting** - Batch communications when possible

## Testing

```bash
# Full test suite
python groq_integration.py

# Status check
forge groq-status

# Interactive testing
forge
> groq-comm Link Container "Test message"
```

## Monitoring

```python
# Check available models
models = client.list_models()
print(f"Models: {len(models)}")

# Verify connection
try:
    response = client.simple_chat("ping")
    print("✅ Groq AI operational")
except Exception as e:
    print(f"❌ Groq AI error: {e}")
```

## Troubleshooting

### Connection Errors
```bash
# Verify API key
echo $env:GROQ_API_KEY

# Test connection
groq-test

# Check model availability
groq-status
```

### Rate Limits
- Groq has generous free tier: 14,400 requests/day
- Implement request queuing if hitting limits
- Use caching for repeated queries

### Model Issues
```bash
# List available models
python -c "from groq_integration import GroqClient; c = GroqClient(); print([m['id'] for m in c.list_models()])"

# Update model in ghostlink.env
GROQ_MODEL=llama-3.3-70b-versatile
```

## Integration Points

- ✅ Shell integration (`ghostlink_shell_integration.ps1`)
- ✅ Toolbox Forge (`toolbox_forge.py`)
- ✅ Environment config (`ghostlink.env`, `config.yaml`)
- ✅ Python API (`groq_integration.py`)
- 🔄 Link CLI (pending)
- 🔄 Container orchestrator (pending)
- 🔄 Signal processor (pending)

## Roadmap

- [ ] Streaming responses for long-running coordination
- [ ] Multi-turn conversations for complex negotiations
- [ ] Context persistence across component sessions
- [ ] Automated error recovery with AI reasoning
- [ ] Performance analytics and optimization
- [ ] Integration with other GhostLink AI models

## Security

- ✅ API key stored in `.env` (not committed)
- ✅ Internal-only communication (no external exposure)
- ✅ No sensitive data in prompts
- ⚠️ Rate limiting to prevent abuse
- ⚠️ Request logging for audit trail

## Summary

Groq is GhostLink's **internal communication AI** - enabling autonomous components to coordinate, reason, and adapt in real-time with ultra-fast inference. It's the nervous system that connects Link, Container, Signal, Pressure, and other components for intelligent orchestration.

**Not for external use** - purely for internal system communication and autonomous operations.

---

**Last Updated**: November 23, 2025  
**Model**: llama-3.3-70b-versatile  
**Status**: ✅ Operational

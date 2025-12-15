# GhostLink Automation System

## Overview

GhostLink now includes a comprehensive automation system that allows components to operate autonomously with configurable approval and experimental feature gates.

## Configuration

All automation settings can be controlled via environment variables:

### Core Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTOMATE_ALL` | `true` | Enable automatic execution of supported operations without manual confirmation |
| `AUTO_APPROVE` | `true` | Automatically approve actions that normally require confirmation |
| `EXPERIMENTAL_MODE` | `full` | Control experimental feature access: `off`, `partial`, or `full` |

### Example Configurations

**Development (fully automated):**
```bash
export AUTOMATE_ALL=true
export AUTO_APPROVE=true
export EXPERIMENTAL_MODE=full
```

**Staging (selective automation):**
```bash
export AUTOMATE_ALL=true
export AUTO_APPROVE=false
export EXPERIMENTAL_MODE=partial
```

**Production (conservative):**
```bash
export AUTOMATE_ALL=false
export AUTO_APPROVE=false
export EXPERIMENTAL_MODE=off
```

## Usage

### In Components

Components should import the policy helpers to check automation settings:

```python
from ghostlink.automation import policy

# Check if automation is enabled
if policy.automate_all():
    # Run autonomously
    execute_operation()
else:
    # Require manual confirmation
    request_approval()

# Check if auto-approval is enabled
if policy.auto_approve():
    # Proceed without confirmation
    dangerous_operation()
else:
    # Request explicit approval
    await_approval()

# Check experimental features
if policy.experimental_enabled():
    level = policy.experimental_level()
    if level == "full":
        # Run all experimental features
        run_experimental_feature()
```

### Command Line Tools

**Check current settings:**
```bash
python -m ghostlink.automation.check_settings
```

**Run automation demonstration:**
```bash
python -m ghostlink.automation.demo_automation
```

**View via API:**
```bash
curl http://127.0.0.1:8000/status
```

## API Endpoints

### GET /status

Returns current system status and automation configuration:

```json
{
  "service": "GhostLink",
  "status": "running",
  "automation": {
    "automate_all": true,
    "auto_approve": true,
    "experimental_mode": "full",
    "experimental_enabled": true
  },
  "config": {
    "debug": false,
    "database_url": "./ghostlink.db"
  }
}
```

## Policy Module

The `ghostlink.automation.policy` module provides helper functions:

- `automate_all()` → `bool`: Check if automation is enabled
- `auto_approve()` → `bool`: Check if auto-approval is enabled
- `experimental_level()` → `str`: Get experimental mode level
- `experimental_enabled()` → `bool`: Check if any experimental features are enabled

## Safety Considerations

**⚠️ Important:** 
- `AUTO_APPROVE=true` should be used with caution in production
- Always review what operations will be automated before enabling
- Use `EXPERIMENTAL_MODE=off` in production unless features are thoroughly tested
- Consider using `partial` mode for gradual rollout of experimental features

## Configuration File

See `.env.example` for a complete configuration template with all available options.

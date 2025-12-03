# Automatic Troubleshooting and Error Correction

GhostLink now includes **automatic troubleshooting** and **error correction** capabilities powered by the Link agent.

## 🚀 Features

### Automatic Error Detection & Classification
- **Real-time error analysis** - Categorizes errors into: Import, Syntax, Runtime, Configuration, Dependency, Network, Filesystem, Permission, Memory
- **Severity assessment** - Assigns severity levels: INFO, WARNING, ERROR, CRITICAL
- **Context-aware diagnostics** - Captures error context, traceback, and system state

### Autonomous Error Correction
- **Auto-fix common issues** - Automatically resolves import errors, missing dependencies, configuration problems
- **Retry failed tasks** - Re-attempts tasks after successful fixes
- **Learning system** - Tracks fix history to improve future corrections

### Proactive Health Monitoring
- **System resource monitoring** - Tracks CPU, memory, disk usage
- **Dependency checking** - Validates Python packages, Node.js, npm
- **Configuration validation** - Checks .env files, pyproject.toml
- **Permission auditing** - Verifies file/directory access

### Intelligent Diagnostics
- **Error history tracking** - Maintains detailed error logs
- **Fix suggestions** - Provides actionable recommendations
- **System information** - Comprehensive platform and resource details
- **Export reports** - JSON reports for debugging and analysis

## 📦 Components

### 1. AutoTroubleshooter (`ghostlink/troubleshooter.py`)

Analyzes errors and applies automatic fixes:

```python
from ghostlink import handle_error

try:
    # Your code here
    import some_missing_module
except Exception as e:
    # Automatic analysis and fix attempt
    report = await handle_error(e, auto_fix=True)
    if report.fix_applied:
        print("✓ Error auto-fixed!")
```

**Features**:
- Error classification and severity detection
- Suggested fixes generation
- Automatic fix application
- Fix handler registration system

### 2. HealthMonitor (`ghostlink/health_monitor.py`)

Monitors system health proactively:

```python
from ghostlink import get_health_monitor

monitor = get_health_monitor()
status = await monitor.check_health()

if status.overall_status == "critical":
    print(f"Issues: {status.issues}")
    print(f"Recommendations: {status.recommendations}")
```

**Checks**:
- System resources (CPU, RAM, disk)
- Python installation and version
- Required and optional dependencies
- Configuration files (.env, pyproject.toml)
- File permissions

### 3. Diagnostics CLI (`ghostlink/diagnostics_cli.py`)

Command-line tools for troubleshooting:

```bash
# Check system health
link diagnostics health

# View system information
link diagnostics sysinfo

# View error history
link diagnostics errors

# Enable/disable auto-fix
link diagnostics autofix --enable

# Start continuous monitoring
link diagnostics monitor 60

# Fix common issues automatically
link diagnostics fix-common
```

## 🎯 Usage

### Integrated with Link Agent

Link automatically uses troubleshooting when errors occur:

```python
from ghostlink import get_link

link = get_link()

# Enable auto-fix (default: enabled)
link.auto_fix_enabled = True

# Enable proactive monitoring
link.proactive_monitoring = True

await link.start()
```

### Manual Error Handling

```python
from ghostlink.troubleshooter import get_troubleshooter, handle_error

# Get troubleshooter instance
troubleshooter = get_troubleshooter()

# Analyze an error
try:
    dangerous_operation()
except Exception as e:
    report = troubleshooter.analyze_error(e, context={"operation": "test"})
    
    print(f"Category: {report.category.value}")
    print(f"Severity: {report.severity.name}")
    print(f"Suggestions: {report.suggested_fixes}")
    
    # Attempt auto-fix
    if await troubleshooter.auto_fix(report):
        print("✓ Fixed!")
```

### Health Monitoring

```python
from ghostlink.health_monitor import get_health_monitor

monitor = get_health_monitor()

# One-time check
status = await monitor.check_health()
print(f"Status: {status.overall_status}")
print(f"CPU: {status.cpu_usage}%")
print(f"Memory: {status.memory_usage}%")

# Continuous monitoring
await monitor.start_monitoring()
# ... monitoring runs in background ...
await monitor.stop_monitoring()
```

## 🔧 CLI Commands

### Health Check
```bash
link diagnostics health
```
**Output**:
```
============================================================
System Health: HEALTHY
============================================================

CPU Usage: 15.2%
Memory Usage: 42.8%
Disk Usage: 67.3%

✓ All systems operational
```

### System Information
```bash
link diagnostics sysinfo --output sysinfo.json
```
Exports comprehensive system details including platform, Python version, resources, and workspace info.

### Error History
```bash
link diagnostics errors --output error_report.json
```
**Output**:
```
============================================================
Error Diagnostics
============================================================

Total Errors: 12
Auto-fixes Applied: 8
Auto-fix Enabled: True

Errors by Category:
  import: 5
  configuration: 3
  dependency: 4

Recent Errors:
  [import] ERROR
  No module named 'requests'
  ✓ Auto-fixed: pip install requests
```

### Enable Auto-fix
```bash
link diagnostics autofix --enable
```

### Continuous Monitoring
```bash
link diagnostics monitor 60
```
Checks system health every 60 seconds and logs warnings/critical issues.

### Fix Common Issues
```bash
link diagnostics fix-common
```
**Automatically fixes**:
- Missing .env file (copies from .env.example)
- Missing Python dependencies (runs pip install)
- Basic configuration issues

## 🛠️ Customization

### Register Custom Fix Handlers

```python
from ghostlink.troubleshooter import get_troubleshooter, ErrorCategory

def my_custom_fix(report):
    """Custom fix handler."""
    if "my_specific_error" in report.message:
        # Apply fix
        return True
    return False

troubleshooter = get_troubleshooter()
troubleshooter.register_fix_handler(ErrorCategory.RUNTIME, my_custom_fix)
```

### Configure Monitoring Interval

```python
from ghostlink.health_monitor import get_health_monitor

monitor = get_health_monitor()
monitor.check_interval = 30  # Check every 30 seconds
await monitor.start_monitoring()
```

### Export Custom Reports

```python
from ghostlink.troubleshooter import get_troubleshooter
from pathlib import Path

troubleshooter = get_troubleshooter()
report_json = troubleshooter.export_report(Path("my_report.json"))
```

## 📊 Error Categories

| Category | Auto-Fixable | Example |
|----------|--------------|---------|
| **IMPORT** | ✅ Yes | `ModuleNotFoundError: No module named 'requests'` |
| **DEPENDENCY** | ✅ Yes | `npm: command not found` |
| **CONFIGURATION** | ✅ Yes | `.env file missing` |
| **SYNTAX** | ✅ Yes | `SyntaxError: invalid syntax` |
| **PERMISSION** | ⚠️ Partial | `PermissionError: Access denied` |
| **RUNTIME** | ❌ No | `ValueError: invalid literal` |
| **NETWORK** | ❌ No | `ConnectionError: Network unreachable` |
| **FILESYSTEM** | ❌ No | `FileNotFoundError: file.txt` |
| **MEMORY** | ❌ No | `MemoryError` |

## 🔒 Security & Privacy

- **All processing is local** - No external services
- **No telemetry** - Error reports stay on your machine
- **Opt-in auto-fix** - You control when fixes are applied
- **Audit trail** - All fixes are logged with timestamps

## 🎓 Examples

### Example 1: Import Error Auto-Fix

```python
# This will fail initially
import some_package_not_installed

# Link detects the error, analyzes it, installs the package,
# and retries the import automatically
```

### Example 2: Configuration Auto-Fix

```python
# Missing .env file
from ghostlink import config

# Link detects missing .env, copies from .env.example,
# and reloads configuration
```

### Example 3: Health Monitoring Alert

```bash
# Start monitoring
link diagnostics monitor 60

# Output when issues detected:
# WARNING: High memory usage: 87%
# WARNING: High disk usage: 92%
# CRITICAL: Missing required package 'fastapi'
```

## 🚦 Integration with VS Code

Auto-troubleshooting works seamlessly with VS Code:

1. **Terminal Integration** - Errors in terminal are auto-detected
2. **Task Failures** - Failed tasks trigger auto-fix attempts
3. **Extension Errors** - Link extension errors are logged and analyzed
4. **Chat Integration** - Ask Link about errors: `@link what errors have occurred?`

## 📈 Statistics & Monitoring

View troubleshooting statistics:

```python
troubleshooter = get_troubleshooter()
diagnostics = troubleshooter.get_diagnostics()

print(f"Total errors: {diagnostics['error_count']}")
print(f"Fixes applied: {diagnostics['fixes_applied']}")
print(f"Success rate: {diagnostics['fixes_applied'] / diagnostics['error_count'] * 100}%")
```

## 🔄 Continuous Improvement

The troubleshooter learns from:
- **Fix success rates** - Tracks which fixes work
- **Error patterns** - Identifies recurring issues
- **System configurations** - Adapts to your environment

---

**Automatic troubleshooting is enabled by default in Link agent.**

For more information, see:
- `ghostlink/troubleshooter.py` - Auto-troubleshooting implementation
- `ghostlink/health_monitor.py` - Health monitoring system
- `ghostlink/diagnostics_cli.py` - CLI commands

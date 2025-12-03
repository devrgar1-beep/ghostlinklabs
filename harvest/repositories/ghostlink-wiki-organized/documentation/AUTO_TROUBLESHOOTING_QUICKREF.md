# Automatic Troubleshooting and Error Correction - Quick Reference

## ⚡ Quick Start

### Check System Health
```bash
link diagnostics health
```

### View Error History
```bash
link diagnostics errors
```

### Enable Auto-Fix
```bash
link diagnostics autofix --enable
```

### Fix Common Issues
```bash
link diagnostics fix-common
```

### Start Monitoring
```bash
link diagnostics monitor 60  # Check every 60 seconds
```

## 🎯 Key Features

| Feature | Command | Auto-fixable |
|---------|---------|--------------|
| **Import Errors** | Detects ModuleNotFoundError | ✅ Yes - pip install |
| **Missing Dependencies** | Detects missing packages | ✅ Yes - auto-install |
| **Config Issues** | Detects missing .env | ✅ Yes - copy from example |
| **Syntax Errors** | Detects Python syntax issues | ✅ Yes - auto-format |
| **Permission Errors** | Detects access denied | ⚠️ Partial |
| **Resource Issues** | Monitors CPU/RAM/disk | ⚠️ Alerts only |

## 📋 CLI Commands

```bash
link diagnostics health          # Check system health
link diagnostics sysinfo         # Show system info
link diagnostics errors          # View error history
link diagnostics autofix         # Enable/disable auto-fix
link diagnostics monitor 60      # Start monitoring
link diagnostics fix-common      # Fix common issues
```

## 🔧 Python API

```python
from ghostlink import handle_error, get_health_monitor

# Auto-fix an error
try:
    risky_operation()
except Exception as e:
    report = await handle_error(e, auto_fix=True)
    if report.fix_applied:
        print("Fixed!")

# Check health
monitor = get_health_monitor()
status = await monitor.check_health()
print(f"Status: {status.overall_status}")
```

## 📊 Error Categories

- `IMPORT` - Missing modules (auto-fixable)
- `DEPENDENCY` - Missing tools/packages (auto-fixable)
- `CONFIGURATION` - Config issues (auto-fixable)
- `SYNTAX` - Python syntax errors (auto-fixable)
- `PERMISSION` - Access issues (partial fix)
- `RUNTIME` - Logic errors (manual fix)
- `NETWORK` - Connection errors (manual fix)
- `FILESYSTEM` - File not found (manual fix)
- `MEMORY` - Out of memory (manual fix)

## 🎛️ Configuration

Enable in Link agent:
```python
from ghostlink import get_link

link = get_link()
link.auto_fix_enabled = True           # Enable auto-fix
link.proactive_monitoring = True       # Enable monitoring
await link.start()
```

## 📈 Common Issues Fixed Automatically

1. **Missing Python package** → `pip install <package>`
2. **Missing .env file** → Copy from `.env.example`
3. **Syntax errors** → Run Black formatter
4. **Missing requirements** → `pip install -r requirements.txt`
5. **Wrong file permissions** → `chmod 644`

## 🔔 Health Monitoring

Monitors:
- CPU usage (warn >70%, critical >90%)
- Memory usage (warn >75%, critical >90%)
- Disk usage (warn >85%, critical >95%)
- Python version (requires 3.8+)
- Required dependencies
- Configuration files

## 📝 Export Reports

```bash
# Export system info
link diagnostics sysinfo --output system.json

# Export error report
link diagnostics errors --output errors.json
```

## ⚙️ Integration

Works with:
- ✅ Link agent (automatic)
- ✅ CLI commands
- ✅ Python API
- ✅ VS Code extension
- ✅ Terminal integration

---

**For complete documentation:** See `AUTO_TROUBLESHOOTING.md`

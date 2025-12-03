# GhostLink Labs - 100% Local Sovereign AI Framework

A completely local AI orchestration system with symbolic reasoning, hardware binding, and autonomous operation. Zero external dependencies - runs on any platform with Python 3.8+.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (built-in on most systems)
- That's it - no external dependencies, no package managers, no virtual environments

### Installation
```bash
# Copy files to your system
# No installation required - just run directly
```

### Basic Usage
```bash
# Start the Link AI brain
python main.py

# Or use the CLI
python -m ghostlink.link_cli start

# Access web interface at http://localhost:8000
```

### Advanced Usage
```bash
# Hardware-bound operation (requires admin privileges)
python -m ghostlink.link_cli start --hardware --confirm-hardware

# Lattice component coordination
python ghostlink_lattice.py --demo

# Symbolic reasoning demo
python gdl_example.gdl
```

## 🔒 Security & Sovereignty

- **100% Local**: No external dependencies or cloud services required
- **Hardware Binding**: Direct BIOS/firmware interaction when needed
- **VM Detection**: Prevents unsafe operations in virtual environments
- **Optional Web Backup**: Web connectivity only for backup/sync (disabled by default)
- **Platform Agnostic**: Runs on Windows, macOS, Linux, BSD, etc.

## 📚 Core Components

### Link AI Brain
- Task management and orchestration
- Context learning and adaptation
- Autonomous decision making

### Lattice Mesh Network
- Component communication and coordination
- Self-healing network topology
- Real-time state synchronization

### Symbolic Reasoning Engine (GDL)
- Cellular automata-based reasoning
- Pattern recognition and prediction
- Hardware-accelerated when available

### Hardware Bridge
- Direct BIOS/firmware access (admin required)
- Physical device binding and control
- Manufacturer tool integration

## 🤖 AI Integration

### Internal AI
- Groq-based ultra-fast inference
- Component coordination
- Real-time decision making

### Local AI Support
- Compatible with LM Studio, Ollama
- No cloud dependencies required
- Runs entirely offline

## 🔧 Platform Support

GhostLink runs on any platform with Python 3.8+:

- **Windows**: Native support, hardware binding available
- **macOS**: Full compatibility, hardware binding via system APIs
- **Linux**: Native performance, full hardware access
- **BSD variants**: Compatible with standard library
- **Embedded systems**: Minimal resource requirements

## 📁 File Structure

```
ghostlink/
├── main.py                 # Main entry point
├── ghostlink_lattice.py    # Mesh network coordinator
├── link_cli.py            # Command line interface
├── groq_integration.py    # Internal AI client
├── bios_bridge.py         # Hardware interface
├── gdl_example.gdl        # Symbolic reasoning demo
└── config.yaml            # Local configuration
```

## 🔄 Updates & Backup

### Offline Updates
- Manual file replacement
- Configuration preservation
- No automatic update mechanisms

### Optional Web Backup
```bash
# Enable web backup (optional)
python -m ghostlink.link_cli backup enable --endpoint https://your-backup-server

# Sync to backup
python -m ghostlink.link_cli backup sync
```

## 📄 License

Proprietary - See LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues
- **Hardware Binding Fails**: Ensure admin/root privileges and physical hardware
- **Lattice Communication**: Check component health with `python ghostlink_lattice.py --state`
- **Web Server Issues**: Verify port 8000 is available
- **Permission Errors**: Run with appropriate privileges for hardware operations

### Logs
- All output goes to terminal/console
- No external logging services
- Self-contained operation logs

### Platform-Specific Notes
- **Windows**: May require UAC elevation for hardware operations
- **macOS**: May require sudo for system-level access
- **Linux**: Full root access available for hardware binding

---

**Built for complete local sovereignty - no external dependencies, no cloud requirements, no package managers. Just Python and your hardware.**

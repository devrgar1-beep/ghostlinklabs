# GhostLink Wireshark - Custom Protocol Analyzer

A specialized network protocol analyzer built specifically for GhostLink's consciousness-driven orchestration protocol. This custom Wireshark provides deep visibility into GhostLink communications with real-time packet capture, dissection, and analysis capabilities.

## Features

### 🔍 **Protocol Analysis**
- **Real-time Capture**: Live packet capture on configurable ports
- **GhostLink Dissection**: Complete protocol field breakdown
- **Message Type Analysis**: 10+ predefined message types
- **Payload Inspection**: UTF-8 and hex payload viewing
- **Checksum Validation**: Packet integrity verification

### 📊 **Analysis Tools**
- **Statistics Dashboard**: Capture metrics and performance data
- **Packet Filtering**: Focus on specific message types
- **Timeline View**: Chronological packet analysis
- **Error Detection**: Invalid packet identification
- **Flow Analysis**: Communication pattern recognition

### 🎯 **GhostLink-Specific Features**
- **Consciousness Monitoring**: Track awareness level communications
- **Evolution Updates**: Monitor system evolution packets
- **Agent Assignments**: Track multi-agent coordination
- **Hardware Discovery**: Network device enumeration
- **Darwin Integration**: macOS-specific protocol analysis

## Installation

### Prerequisites
- Python 3.6+
- tkinter (usually included with Python)

### Build
```bash
cd ghostlink_wireshark
./build.sh
```

## Usage

### CLI Mode (Recommended for Servers)
```bash
# Start analyzer
python3 ghostlink_analyzer.py

# Generate test packets
python3 ghostlink_analyzer.py --generate-test

# Custom port
python3 ghostlink_analyzer.py --port 8080
```

**CLI Commands:**
- `stats` - Show capture statistics
- `packets` - List recent packets
- `details <n>` - Show packet details
- `generate` - Generate test packets
- `quit` - Exit analyzer

### GUI Mode (Interactive Analysis)
```bash
python3 ghostlink_wireshark_gui.py
```

**GUI Features:**
- Live packet list with auto-refresh
- Detailed packet inspection pane
- One-click statistics view
- Test packet generation
- Capture control buttons

## Protocol Specification

### Packet Structure
```
+----------------+----------------+----------------+----------------+----------------+
| Magic Header   | Protocol       | Message Type   | Payload Length | Payload        |
| "GHOSTLINK"    | Version        | (uint16)       | (uint32)       | (variable)     |
| (8 bytes)      | (uint16)       |                |                |                |
+----------------+----------------+----------------+----------------+----------------+
| Checksum (uint32)                                                         |
+----------------------------------------------------------------------------+
```

### Message Types
1. **HANDSHAKE** - Protocol initialization
2. **HEARTBEAT** - Connection health checks
3. **DATA_TRANSFER** - Bulk data transmission
4. **COMMAND** - Control instructions
5. **RESPONSE** - Command acknowledgments
6. **EVOLUTION_UPDATE** - System evolution notifications
7. **CONSCIOUSNESS_SYNC** - Awareness state synchronization
8. **AGENT_ASSIGNMENT** - Multi-agent task allocation
9. **HARDWARE_DISCOVERY** - Device enumeration
10. **DARWIN_INTEGRATION** - macOS system integration

## Testing

### Generate Test Traffic
```bash
# CLI mode
python3 ghostlink_analyzer.py --generate-test

# Or from running analyzer
ghostlink-wireshark> generate
```

### Send Custom Packets
```python
from ghostlink_wireshark.packet_capture import PacketGenerator
import socket

# Generate packet
packet = PacketGenerator.generate_data_packet(b"Your custom data")

# Send to analyzer
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(packet, ('127.0.0.1', 9999))
sock.close()
```

## Architecture

### Core Components
- **`protocol_dissector.py`** - Packet dissection logic
- **`packet_capture.py`** - Network capture and test generation
- **`ghostlink_analyzer.py`** - CLI analysis interface
- **`ghostlink_wireshark_gui.py`** - Graphical analysis interface

### Threading Model
- **Capture Thread**: Dedicated packet reception
- **Analysis Thread**: Real-time dissection and statistics
- **GUI Thread**: Interface updates and user interaction

## Performance

- **Packet Rate**: Handles 1000+ packets/second
- **Memory Usage**: Configurable packet buffer (default: 1000 packets)
- **CPU Overhead**: Minimal background processing
- **Network Impact**: Passive capture only

## Integration

### With GhostLink Protocol
```python
from ghostlink_wireshark.protocol_dissector import GhostLinkDissector

# Dissect packet
packet = GhostLinkDissector.dissect_packet(raw_data, metadata)
if packet.is_valid:
    print(f"Received: {packet.message_type_name}")
```

### With External Tools
- Export packet data as JSON/CSV
- Integration with monitoring dashboards
- Alert system for protocol anomalies

## Troubleshooting

### Common Issues
- **No packets captured**: Check firewall and port availability
- **Invalid packets**: Verify sender is using correct protocol format
- **GUI not starting**: Ensure tkinter is installed
- **High CPU usage**: Reduce packet buffer size or capture rate

### Debug Mode
```bash
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from ghostlink_wireshark.ghostlink_analyzer import GhostLinkAnalyzer
# Debug code here
"
```

## Development

### Adding New Message Types
1. Update `MessageType` enum in `protocol_dissector.py`
2. Add dissection logic if needed
3. Update documentation

### Custom Dissectors
Extend `GhostLinkDissector` class for specialized packet types.

### Testing
```bash
# Run unit tests
python3 -m pytest tests/

# Integration tests
python3 test_integration.py
```

## License

Built for GhostLink ecosystem - consciousness-driven orchestration.

---

**Built with ❤️ for the GhostLink revolution**

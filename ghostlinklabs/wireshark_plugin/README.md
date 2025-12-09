# GhostLink Wireshark Plugin

This directory contains the Wireshark plugin for dissecting GhostLink protocol packets.

## Files

- `ghostlink_dissector.lua` - Lua script that dissects GhostLink protocol packets

## Installation

### Option 1: Global Installation

1. Copy `ghostlink_dissector.lua` to Wireshark's plugins directory:
   - Linux: `~/.local/lib/wireshark/plugins/` or `/usr/lib/wireshark/plugins/`
   - macOS: `/Applications/Wireshark.app/Contents/PlugIns/wireshark/`
   - Windows: `C:\Program Files\Wireshark\plugins\`

2. Restart Wireshark

### Option 2: Personal Plugins Directory

1. Create directory: `~/.wireshark/plugins/`
2. Copy `ghostlink_dissector.lua` to that directory
3. Restart Wireshark

### Option 3: Load Manually

1. Open Wireshark
2. Go to Analyze → Lua Scripts
3. Click "Add" and select `ghostlink_dissector.lua`
4. Click "Load"

## Protocol Details

GhostLink packets have the following structure:

```text
+----------------+----------------+----------------+----------------+----------------+
| Magic Header   | Protocol       | Message Type   | Payload Length | Payload        |
| "GHOSTLINK"    | Version        | (uint16)       | (uint32)       | (variable)     |
| (8 bytes)      | (uint16)       |                |                |                |
+----------------+----------------+----------------+----------------+----------------+
| Checksum (uint32)                                                         |
+----------------------------------------------------------------------------+
```

### Message Types

- 1: HANDSHAKE
- 2: HEARTBEAT
- 3: DATA_TRANSFER
- 4: COMMAND
- 5: RESPONSE
- 6: EVOLUTION_UPDATE
- 7: CONSCIOUSNESS_SYNC
- 8: AGENT_ASSIGNMENT
- 9: HARDWARE_DISCOVERY
- 10: DARWIN_INTEGRATION

## Usage

1. Start capturing packets on port 9999 (default GhostLink port)
2. Send GhostLink packets
3. Wireshark will automatically dissect them as "GHOSTLINK" protocol
4. Expand the packet details to see the dissected fields

## Building Custom Dissectors

To modify the dissector for different packet formats:

1. Edit the field definitions in `ghostlink_dissector.lua`
2. Update the dissector function to match your protocol
3. Reload the script in Wireshark

## Troubleshooting

- If packets aren't being dissected, check the port number
- Ensure the magic header matches exactly
- Check Wireshark console for Lua errors

# Mac Mini Backend Setup Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│               Mac Mini Backend Server               │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │  Extraction Service (Port 8001)               │ │
│  │  - Process management with locking            │ │
│  │  - Status monitoring & progress tracking      │ │
│  │  - Background task execution                  │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │  Wiki Service (Port 8002)                     │ │
│  │  - Read-only wiki access                      │ │
│  │  - Search & indexing                          │ │
│  │  - File serving                               │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │  Storage                                      │ │
│  │  ~/ghostlink-wiki/        (extracted files)   │ │
│  │  ~/ghostlink-wiki-trace/  (state & logs)      │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                        ▲
                        │ HTTP/REST API
                        │
┌───────────────────────▼─────────────────────────────┐
│            MacBook Pro (Development)                │
│  - Triggers extraction via API                      │
│  - Views status & progress                          │
│  - Accesses wiki content                            │
└─────────────────────────────────────────────────────┘
```

## Installation Steps

### 1. Mac Mini Setup

```bash
# Install Python 3.11+
brew install python@3.11

# Create service directory
mkdir -p ~/ghostlink-backend
cd ~/ghostlink-backend

# Copy backend services
cp backend/extraction_service.py ~/ghostlink-backend/
cp backend/requirements.txt ~/ghostlink-backend/

# Install dependencies
pip3 install -r requirements.txt
```

### 2. Configure LaunchD Service

Create `/Library/LaunchDaemons/com.ghostlink.extraction.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ghostlink.extraction</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/ghostlink/ghostlink-backend/extraction_service.py</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/Users/ghostlink/ghostlink-backend/logs/extraction.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/ghostlink/ghostlink-backend/logs/extraction.error.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
```

Load service:
```bash
sudo launchctl load /Library/LaunchDaemons/com.ghostlink.extraction.plist
sudo launchctl start com.ghostlink.extraction
```

### 3. Test Service

```bash
# Check if service is running
curl http://localhost:8001/health

# Get status
curl http://localhost:8001/status

# Start extraction
curl -X POST http://localhost:8001/extract \
  -H "Content-Type: application/json" \
  -d '{"max_results": 150}'

# Stop extraction
curl -X POST http://localhost:8001/stop
```

## Client Usage (MacBook Pro)

### Install client library

```bash
pip install httpx
```

### Python Client

```python
import httpx

# Mac Mini IP address (update this)
BACKEND_URL = "http://192.168.1.100:8001"

async def start_extraction():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/extract",
            json={"max_results": 150}
        )
        return response.json()

async def check_status():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/status")
        return response.json()

# Usage
import asyncio
status = asyncio.run(check_status())
print(f"Running: {status['running']}")
```

### Shell Commands

```bash
# Export Mac Mini address
export GHOSTLINK_BACKEND="http://192.168.1.100:8001"

# Start extraction
curl -X POST $GHOSTLINK_BACKEND/extract \
  -H "Content-Type: application/json" \
  -d '{"max_results": 150, "batches": "BATCH_1_MCP,BATCH_2_PYTHON"}'

# Monitor status
watch -n 5 "curl -s $GHOSTLINK_BACKEND/status | jq"

# Stop extraction
curl -X POST $GHOSTLINK_BACKEND/stop
```

## Features

### Process Management
- ✅ **Single instance**: Prevents multiple extractions running simultaneously
- ✅ **Lock files**: `/ghostlink-wiki-trace/.extraction.lock` prevents conflicts
- ✅ **PID tracking**: Monitors actual process state, cleans up stale locks
- ✅ **Graceful shutdown**: SIGTERM handling for clean termination

### Status Monitoring
- Running state (true/false)
- Process ID
- Start time & duration
- Progress updates
- Error messages

### API Endpoints
- `GET /health` - Service health check
- `GET /status` - Current extraction status
- `POST /extract` - Start extraction job
- `POST /stop` - Stop running extraction

### Error Handling
- 409 Conflict: Extraction already running
- 423 Locked: Could not acquire lock
- 404 Not Found: No extraction to stop
- 500 Internal: Process errors

## Network Setup

### Mac Mini Static IP (recommended)
1. System Preferences → Network
2. Select Wi-Fi/Ethernet
3. Configure IPv4: Manual
4. Set IP: `192.168.1.100` (or desired)
5. Subnet: `255.255.255.0`
6. Router: `192.168.1.1`

### Firewall Rules
```bash
# Allow port 8001
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblock /usr/local/bin/python3
```

## Monitoring & Logs

```bash
# View service logs
tail -f ~/ghostlink-backend/logs/extraction.log

# Check service status
sudo launchctl list | grep ghostlink

# View lock file
cat ~/ghostlink-wiki-trace/.extraction.lock

# View status file
cat ~/ghostlink-wiki-trace/extraction_status.json
```

## Benefits

1. **No More Conflicts**: Process locking prevents duplicate runs
2. **Background Execution**: Long extractions don't block your MacBook
3. **Remote Control**: Start/stop from any device on network
4. **Persistent**: Survives reboots (LaunchD auto-restart)
5. **Monitored**: Real-time status without terminal attachment
6. **Scalable**: Add more services (wiki search, API gateway, etc.)

## Future Enhancements

- [ ] WebSocket progress streaming
- [ ] Queue system for multiple extraction requests
- [ ] Scheduled extractions (cron-like)
- [ ] Email/Slack notifications on completion
- [ ] Metrics & analytics dashboard
- [ ] Multi-machine distribution (Mac Mini cluster)

# GhostLink Neighbor Integration Guide

## Overview

GhostLink now supports peer mesh networking to integrate thermal monitoring across multiple hosts on your local network. The system discovers and connects to neighbors automatically.

## Discovered Network Topology

```
Gateway: 192.168.4.1
Your System: 192.168.4.41

Neighbors:
  - 192.168.4.2
  - 192.168.4.22
  - 192.168.4.23
  - 192.168.4.24
  - 192.168.4.42
  - 192.168.4.45
  - 192.168.4.46
```

## Quick Start

### On This Host (192.168.4.41)

The mesh aggregator is already running and monitoring local thermal data while scanning for peers.

Check status:
```bash
./run_venv.sh status
python3 gl_network_status.py
```

View mesh logs:
```bash
tail -f .logs/mesh.log
```

### On Neighbor Hosts

To enable a neighbor host to participate in the mesh network:

#### Option 1: Full Python Environment

1. Copy `gl_peer_responder.py` to the neighbor host
2. Install dependencies: `pip3 install psutil`
3. Run the responder:
   ```bash
   python3 gl_peer_responder.py
   ```

#### Option 2: One-liner Deployment

On the neighbor host, run:
```bash
wget http://192.168.4.41:8000/gl_peer_responder.py
python3 gl_peer_responder.py
```

The responder listens on port 7422 and responds to thermal queries.

## Architecture

### Components

1. **gl_controller_metrics.py** (Port 7420)
   - Central metrics controller
   - Accepts connections from peers
   - Publishes to Prometheus endpoint (Port 9108)

2. **gl_peer.py** (Local peer)
   - Reads local thermal sensors
   - Sends data to controller
   - Already running on this system

3. **gl_peer_mesh.py** (Mesh aggregator)
   - Discovers neighbors on network
   - Queries peer responders
   - Aggregates multi-host thermal data
   - Sends aggregate metrics to controller

4. **gl_peer_responder.py** (Deploy to neighbors)
   - Lightweight service for remote hosts
   - Responds to mesh discovery
   - Provides local thermal data on request

### Data Flow

```
Neighbor Hosts (Port 7422)
    ↓ query
gl_peer_mesh.py (This host)
    ↓ aggregated data
gl_controller_metrics.py (Port 7420)
    ↓ metrics
Prometheus Endpoint (Port 9108)
    ↓
Monitoring/Alerting
```

## Metrics

The mesh adds new metrics:

- `ghostlink_cpu_temp_c{zone="mesh"}` - Local temperature
- `ghostlink_peer_count` - Active mesh peers
- `ghostlink_mesh_temp_avg` - Average temperature across mesh
- `ghostlink_mesh_temp_max` - Maximum temperature in mesh

Query example:
```bash
curl -s http://localhost:9108/metrics | grep ghostlink_mesh
```

## Network Requirements

- Port 7420: Controller (localhost only)
- Port 7422: Peer responder (neighbors)
- Port 9108: Metrics endpoint (localhost only)

Firewall rules for neighbor hosts:
```bash
# Allow incoming mesh queries
sudo ufw allow 7422/tcp
```

## Deployment Scripts

### Backbone Dell R630s (Automated)

1) List your R630 backbone hosts in `backbone_hosts.txt` (one per line)
2) Deploy the responder to each host over SSH:
```bash
bin/glctl backbone:deploy
```
3) Discover responders on your backbone network and write `./creds/neighbors.txt`:
```bash
bin/glctl backbone:discover 10.10.0.0/24 10.10.1.0/24
```
4) Point the stack at the neighbors file and enable the mesh in Docker:
```bash
bin/glctl neighbors:use-file
# Ensure ./creds/neighbors.txt has your hosts, then:
# enable mesh + responder inside container if desired
bin/glctl docker:mesh
bin/glctl docker:up
```

Notes:
- The responder runs on each R630; you generally do not need to run a responder in the controller container.
- Alternatively, set NEIGHBOR_IPS in `.env` as a CSV instead of using a file.

### Deploy to Specific Host (manual)

```bash
# Copy responder to a neighbor
scp gl_peer_responder.py user@192.168.4.22:~/
ssh user@192.168.4.22 'python3 ~/gl_peer_responder.py &'
```

### Deploy to All Neighbors (Batch - manual)

```bash
#!/bin/bash
NEIGHBORS="192.168.4.2 192.168.4.22 192.168.4.23 192.168.4.24 192.168.4.42 192.168.4.45 192.168.4.46"

for IP in $NEIGHBORS; do
    echo "Deploying to $IP..."
    scp gl_peer_responder.py user@$IP:~/ 2>/dev/null || continue
    ssh user@$IP 'nohup python3 ~/gl_peer_responder.py > /tmp/gl_responder.log 2>&1 &' 2>/dev/null &
done

echo "Deployment complete. Wait 30s for discovery..."
sleep 30
python3 gl_network_status.py
```

## Monitoring

### View Live Mesh Status

```bash
# In tmux
tmux attach -t ghostlink
# Navigate to mesh window: Ctrl+b, then press 'n' for next window

# Or tail logs
tail -f .logs/mesh.log
```

### Check Integration Status

```bash
python3 gl_network_status.py
```

### View Metrics

```bash
curl -s http://localhost:9108/metrics | grep -E "ghostlink_mesh|ghostlink_peer"
```

## Troubleshooting

### No Peers Detected

1. Verify responders are running on neighbors:
   ```bash
   nmap -p 7422 192.168.4.0/24
   ```

2. Test manual connection:
   ```bash
   echo '{"type":"ping","proto":"glp/0"}' | nc 192.168.4.22 7422
   ```

3. Check mesh logs:
   ```bash
   grep "Discovery" .logs/mesh.log
   ```

### Peer Connection Drops

- Check network stability
- Verify responder processes haven't crashed
- Review responder logs on neighbor hosts

### High Network Traffic

Default sampling is 1Hz. To reduce:
```bash
# Edit gl_peer_mesh.py
# Change: time.sleep(1)  # 1Hz sampling
# To:     time.sleep(5)  # 0.2Hz sampling
```

## Security Considerations

1. **Network Isolation**: Mesh operates on local network only
2. **No Authentication**: Deploy only on trusted networks
3. **Read-Only**: Peers provide read-only thermal data
4. **No Remote Commands**: System accepts only data queries

For production environments, add:
- TLS/SSL encryption
- API key authentication
- Network segmentation

## Performance

Expected resource usage per component:

- gl_peer_mesh.py: ~10MB RAM, <1% CPU
- gl_peer_responder.py: ~5MB RAM, <0.5% CPU
- Network traffic: ~500 bytes/sec per peer

Scales to 50+ peers on 1G network.

## Commands Reference

```bash
# Start mesh integration
./run_venv.sh mesh

# Start responder (on neighbors)
./run_venv.sh responder

# Check status
./run_venv.sh status

# View all logs
./run_venv.sh logs

# Stop everything
./run_venv.sh down

# Network status
python3 gl_network_status.py
```

## Next Steps

1. Deploy responders to 1-2 test neighbors
2. Verify mesh integration with `gl_network_status.py`
3. Monitor aggregated metrics
4. Scale to additional hosts as needed
5. Set up alerting on `ghostlink_mesh_temp_max` threshold

## Support

For issues or questions:
- Check logs: `.logs/mesh.log`
- Run network status: `python3 gl_network_status.py`
- Review this guide

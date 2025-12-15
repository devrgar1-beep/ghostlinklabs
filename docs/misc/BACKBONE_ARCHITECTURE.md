# GhostLink Backbone Architecture

## Overview

Complete infrastructure control plane for Dell R630 backbone integration with GhostLink monitoring and management system.

## Network Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                     GHOSTLINK CONTROL PLANE                      │
│                   (Controller Host: 192.168.4.41)                │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │ gl_controller    │  │  gl_peer_mesh    │  │ gl_idrac       │ │
│  │   _metrics.py    │  │     .py          │  │  _monitor.py   │ │
│  │                  │  │                  │  │                │ │ │
│  │ Port 7420        │←─│ Aggregates mesh  │  │ Polls iDRACs   │ │
│  │ Metrics: 9108    │  │ samples          │  │ every 30s      │ │
│  └──────────────────┘  └──────────────────┘  └────────────────┘ │
│           ↑                    ↑                      ↑           │
│           │                    │                      │           │
└───────────┼────────────────────┼──────────────────────┼───────────┘
            │                    │                      │
            │ GLP/0              │ Port 7422            │ Redfish HTTPS
            │ Port 7420          │ TCP queries          │ Port 443
            │                    │                      │
  ┌─────────┴────────────────────┴──────────────────────┴─────────┐
  │                    BACKBONE NETWORK                            │
  │                  Dell R630 Server Rack                         │
  └────────────────────────────────────────────────────────────────┘
            │                    │                      │
    ┌───────┴──────┐     ┌───────┴──────┐      ┌───────┴──────┐
    │   R630-01    │     │   R630-02    │      │   R630-03    │
    │              │     │              │      │              │
    │ Data Network │     │ Data Network │      │ Data Network │
    │ 10.10.0.21   │     │ 10.10.0.22   │      │ 10.10.0.23   │
    │              │     │              │      │              │
    │ gl_peer_     │     │ gl_peer_     │      │ gl_peer_     │
    │ responder.py │     │ responder.py │      │ responder.py │
    │ Port 7422    │     │ Port 7422    │      │ Port 7422    │
    │              │     │              │      │              │
    ├──────────────┤     ├──────────────┤      ├──────────────┤
    │ iDRAC Mgmt   │     │ iDRAC Mgmt   │      │ iDRAC Mgmt   │
    │ 10.10.100.21 │     │ 10.10.100.22 │      │ 10.10.100.23 │
    │              │     │              │      │              │
    │ Redfish API  │     │ Redfish API  │      │ Redfish API  │
    │ HTTPS :443   │     │ HTTPS :443   │      │ HTTPS :443   │
    └──────────────┘     └──────────────┘      └──────────────┘
```

## Network Segments

### Data Network (10.10.0.0/24)
- **Purpose**: OS-level communication, GhostLink responders
- **Services**: 
  - `gl_peer_responder.py` on port 7422 (TCP)
  - SSH access for deployment and management
- **Protocol**: GLP/0 (GhostLink Protocol)
- **Traffic**: Low bandwidth, ~500 bytes/sec per peer

### Management Network (10.10.100.0/24)
- **Purpose**: Out-of-band management via iDRAC
- **Services**: Dell iDRAC9 Redfish API (HTTPS port 443)
- **Functions**:
  - Power control (on/off/cycle/reset)
  - Thermal monitoring (CPU, ambient, exhaust temps + fans)
  - Health status (PSU, SEL, firmware)
  - Virtual media mounting
  - Boot order configuration (PXE, HDD)
- **Authentication**: Username/password (stored in `creds/idrac_creds.json`)
- **Traffic**: Moderate, polls every 30s, ~2KB per poll

## Data Flow

### 1. Thermal Mesh Flow
```
R630 OS sensors → gl_peer_responder.py (port 7422)
                       ↓
          gl_peer_mesh.py queries (TCP)
                       ↓
          Aggregates temperatures
                       ↓
          gl_controller_metrics.py (port 7420)
                       ↓
          Prometheus /metrics (port 9108)
```

### 2. iDRAC Health Flow
```
iDRAC Redfish API (HTTPS :443) ← gl_idrac_monitor.py polls
                       ↓
    Parallel queries (16 workers)
                       ↓
    Aggregate: temps, fans, PSU, health
                       ↓
    gl_controller_metrics.py (port 7420)
                       ↓
    Prometheus /metrics (port 9108)
```

### 3. Power Control Flow
```
User/Script → glctl idrac:power-on <host>
                  ↓
         scripts/idrac_ctl.sh
                  ↓
         gl_idrac.py (Redfish client)
                  ↓
         iDRAC Redfish API
                  ↓
         Power state change
```

## Components

### Controller Host (192.168.4.41)

#### Core Services
- **gl_controller_metrics.py**: Central metrics aggregator
  - Listens on port 7420 (GLP/0 protocol)
  - Exposes Prometheus endpoint on port 9108
  - Receives samples from peers and mesh aggregator
  - Stores time-windowed metrics with sigma-fraction calculations

- **gl_peer_mesh.py**: Mesh network aggregator
  - Discovers and queries peer responders on data network
  - Aggregates thermal data across multiple R630s
  - Sends consolidated "mesh" samples to controller
  - Configurable via `NEIGHBOR_IPS` (CSV) or `NEIGHBORS_FILE`

- **gl_idrac_monitor.py**: iDRAC health monitoring daemon
  - Polls all iDRACs in `idrac_inventory.txt` every 30s
  - Gathers thermal, PSU, health, and SEL data
  - Sends aggregate "idrac_health" samples to controller
  - Parallel polling with configurable workers (default: 16)

#### Management Tools
- **gl_idrac.py**: Redfish API client library
  - Full Redfish wrapper for Dell iDRAC9
  - Power control, thermal, health, SEL, firmware, network, virtual media
  - Credential management via `creds/idrac_creds.json`

- **scripts/idrac_ctl.sh**: CLI wrapper for common iDRAC operations
  - Power on/off/cycle/reset
  - Boot order (PXE, HDD)
  - Thermal and health queries
  - Virtual media mount/unmount

- **scripts/discover_idrac.py**: Network scanner
  - Probes management network for iDRAC endpoints
  - Validates Redfish availability
  - Writes discovered hosts to `idrac_inventory.txt`

- **bin/glctl**: Unified orchestration tool
  - Local runtime (tmux-based)
  - Docker workflows
  - Backbone deploy/discover
  - iDRAC operations (idrac:discover, idrac:status, idrac:power-on, etc.)

### Backbone R630 Servers

#### OS-Level Service
- **gl_peer_responder.py**: Lightweight mesh responder
  - Listens on port 7422 (TCP)
  - Responds to ping/query messages with thermal data
  - Optional iDRAC integration via `IDRAC_HOST` env var
  - Sources:
    - OS sensors (psutil or /sys/class/thermal)
    - iDRAC Redfish (if configured)
  - Resource usage: ~5MB RAM, <0.5% CPU

#### Out-of-Band Management
- **Dell iDRAC9**: Hardware management controller
  - Always available (independent of OS state)
  - Redfish API on HTTPS port 443
  - Provides:
    - Power control
    - Thermal monitoring (CPU, ambient, exhaust, fans)
    - Health status (PSU, memory, storage)
    - System Event Log (SEL)
    - Virtual media for remote installation
    - Boot order and PXE control

## Deployment Workflow

### 1. Initial Setup

```bash
# Clone and configure controller host
cd /path/to/ghostlinklabs

# Populate backbone inventory
# Edit backbone_hosts.txt with R630 data IPs
# Edit idrac_inventory.txt with management IPs

# Configure credentials
# Edit creds/idrac_creds.json with iDRAC passwords
```

### 2. Discovery Phase

```bash
# Discover responders on data network
bin/glctl backbone:discover 10.10.0.0/24

# Discover iDRACs on management network
bin/glctl idrac:discover 10.10.100.0/24

# Verify discoveries
cat creds/neighbors.txt        # Data network responders
cat idrac_inventory.txt        # Management network iDRACs
```

### 3. Deploy Responders

```bash
# Deploy gl_peer_responder.py to all R630s
BACKBONE_USER=admin bin/glctl backbone:deploy

# Verify deployment (should see port 7422 open)
nmap -p 7422 10.10.0.0/24
```

### 4. Start Monitoring

```bash
# Configure neighbor discovery
bin/glctl neighbors:use-file

# Start controller and mesh
bash run_venv.sh up

# Start iDRAC health monitoring
python3 gl_idrac_monitor.py &

# Verify metrics
curl -s http://127.0.0.1:9108/metrics | grep -E 'ghostlink_mesh|ghostlink_peer|idrac'
```

### 5. Power Management

```bash
# Check status of an R630
bin/glctl idrac:status 10.10.100.21

# Power on a server
bin/glctl idrac:power-on 10.10.100.22

# Configure PXE boot and power on
bin/glctl idrac:power-on 10.10.100.23
scripts/idrac_ctl.sh boot-pxe 10.10.100.23

# Check thermal status
bin/glctl idrac:thermal 10.10.100.21

# View health and recent alerts
bin/glctl idrac:health 10.10.100.22
```

## Security Model

### Authentication
- **iDRAC**: Username/password (HTTPS with self-signed certs)
  - Credentials stored in `creds/idrac_creds.json` (git-ignored)
  - Default user: `root`
  - SSL verification disabled by default (set `IDRAC_VERIFY_SSL=1` to enable)

- **Responder**: No authentication (trusted network)
  - GLP/0 protocol is plaintext
  - Designed for isolated/private networks only

### Network Isolation
- **Data network**: GhostLink peer communication
- **Management network**: iDRAC-only, isolated from data plane
- **Controller host**: Dual-homed, accesses both networks

### Secrets Management
- `creds/idrac_creds.json`: iDRAC passwords
- `creds/*.key`, `creds/*.pem`: TLS certificates (future)
- All credential files are git-ignored

### Best Practices
1. Use separate VLANs for data and management networks
2. Restrict iDRAC access to controller host only (firewall rules)
3. Use strong iDRAC passwords (min 12 chars, mixed case + symbols)
4. Enable iDRAC SSL cert verification in production (`IDRAC_VERIFY_SSL=1`)
5. Rotate iDRAC credentials quarterly
6. Review iDRAC SEL logs weekly for hardware alerts

## Performance Characteristics

### Network Traffic
- **Per responder**: ~500 bytes/sec (1Hz polling)
- **Per iDRAC**: ~2KB every 30s (health poll)
- **Backbone total** (50 R630s): ~25KB/sec + ~3.3KB/sec = ~30KB/sec

### Resource Usage (Controller Host)
- `gl_controller_metrics.py`: ~50MB RAM, <2% CPU
- `gl_peer_mesh.py`: ~10MB RAM, <1% CPU
- `gl_idrac_monitor.py`: ~30MB RAM, <5% CPU (with 16 workers)
- Total: ~90MB RAM, <10% CPU

### Resource Usage (R630)
- `gl_peer_responder.py`: ~5MB RAM, <0.5% CPU

### Scalability
- **Mesh peers**: Tested up to 50, scales to 100+ on 1G network
- **iDRAC polling**: 16 parallel workers can poll 100+ hosts in <10s
- **Controller capacity**: Handles 1000+ samples/sec with <100ms latency

## Monitoring Metrics

### Prometheus Endpoints
All metrics available at `http://127.0.0.1:9108/metrics`

#### Core Metrics
- `ghostlink_sigma_fraction{zone}`: Anomaly detection score
- `ghostlink_samples_total{zone}`: Sample counter
- `ghostlink_window_samples{zone}`: Samples in current window

#### Mesh Metrics
- `ghostlink_peer_count`: Active mesh peers
- `ghostlink_mesh_temp_avg`: Average temperature across mesh
- `ghostlink_mesh_temp_max`: Maximum temperature in mesh

#### iDRAC Metrics (planned)
- `ghostlink_idrac_temp_avg_c{hostname}`: Average CPU temp per host
- `ghostlink_idrac_power_w{hostname}`: Total PSU power output
- `ghostlink_idrac_health{hostname,status}`: Health status gauge

## Troubleshooting

### Responder Not Responding
```bash
# Verify responder is running on R630
ssh user@10.10.0.21 'ps aux | grep gl_peer_responder'

# Test TCP connectivity
nc -zv 10.10.0.21 7422

# Manual query test
echo '{"type":"ping","proto":"glp/0"}' | nc 10.10.0.21 7422
```

### iDRAC Unreachable
```bash
# Ping management IP
ping -c 3 10.10.100.21

# Test HTTPS port
curl -k -m 5 https://10.10.100.21/redfish/v1/

# Check credentials
bin/glctl idrac:status 10.10.100.21
```

### Mesh Not Discovering Peers
```bash
# Check neighbor configuration
grep NEIGHBOR .env
cat creds/neighbors.txt

# Verify mesh aggregator is running
ps aux | grep gl_peer_mesh

# Check mesh logs
tail -f .logs/mesh.log
```

### iDRAC Monitor Failing
```bash
# Check inventory file
cat idrac_inventory.txt

# Check credentials file
cat creds/idrac_creds.json

# Run monitor in foreground for debugging
python3 gl_idrac_monitor.py
```

## Files and Directories

### Configuration
- `backbone_hosts.txt`: Data network host inventory
- `idrac_inventory.txt`: Management network (iDRAC) inventory
- `creds/idrac_creds.json`: iDRAC authentication credentials
- `creds/neighbors.txt`: Discovered responder IPs
- `.env`: Environment defaults (NEIGHBOR_IPS, RUN_* flags)

### Source Code
- `gl_controller_metrics.py`: Central metrics controller
- `gl_peer.py`: Local thermal peer
- `gl_peer_mesh.py`: Mesh aggregator
- `gl_peer_responder.py`: Responder for R630s
- `gl_idrac.py`: Redfish API client library
- `gl_idrac_monitor.py`: iDRAC health polling daemon

### Scripts
- `scripts/deploy_responder.sh`: Deploy responders via SSH
- `scripts/discover_backbone.py`: Discover responders on data network
- `scripts/discover_idrac.py`: Discover iDRACs on management network
- `scripts/idrac_ctl.sh`: iDRAC CLI wrapper

### Orchestration
- `bin/glctl`: Unified control tool (local, Docker, backbone, iDRAC)
- `Makefile`: Quick commands (up/down, deploy, discover, idrac-*)
- `run_venv.sh`: Tmux-based local runtime

## Next Steps

1. **Fill Inventory Files**
   - Add your R630 data IPs to `backbone_hosts.txt`
   - Add iDRAC management IPs to `idrac_inventory.txt`
   - Add iDRAC credentials to `creds/idrac_creds.json`

2. **Run Discovery**
   - `bin/glctl backbone:discover 10.10.0.0/24`
   - `bin/glctl idrac:discover 10.10.100.0/24`

3. **Deploy and Test**
   - Deploy responders: `bin/glctl backbone:deploy`
   - Start controller: `bash run_venv.sh up`
   - Start iDRAC monitor: `python3 gl_idrac_monitor.py &`
   - Verify metrics: `curl http://127.0.0.1:9108/metrics`

4. **Power Management Test**
   - Check status: `bin/glctl idrac:status 10.10.100.21`
   - Power cycle one R630: `bin/glctl idrac:reset 10.10.100.21`
   - Verify thermal data flows through mesh and iDRAC monitors

5. **Production Deployment**
   - Configure Prometheus to scrape `127.0.0.1:9108`
   - Set up Grafana dashboards for mesh and iDRAC metrics
   - Configure alerting on temp thresholds and health status
   - Schedule iDRAC credential rotation

## References

- Neighbor Integration Guide: [NEIGHBOR_INTEGRATION.md](./NEIGHBOR_INTEGRATION.md)
- Integration Summary: [INTEGRATION_SUMMARY.txt](./INTEGRATION_SUMMARY.txt)
- Dell iDRAC9 Redfish API: https://www.dell.com/support/manuals/idrac9-lifecycle-controller

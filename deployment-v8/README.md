# GhostLink v8 - Distributed AI Coordination Protocol

**Production-Grade Implementation of 64-Agent FCC Lattice with CMFL Reasoning**

[![Version](https://img.shields.io/badge/version-8.0.0-blue.svg)](https://github.com/devrgar-cyber/ghostlinklabs)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production-brightgreen.svg)](https://github.com/devrgar-cyber/ghostlinklabs)

> *"Treating computational variance as meta-information rather than noise to eliminate."*  
> — Robert Christopher George (Ghost)

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Core Innovation](#core-innovation)
- [Quick Start](#quick-start)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

GhostLink v8 is a production-grade distributed AI coordination system that implements a 64-agent Face-Centered Cubic (FCC) lattice topology with CMFL (Collapse→Mirror→Forge→Link) reasoning cycles and stigmergic coordination mechanisms.

### Key Features

- **64-Agent FCC Lattice**: Spatially-distributed agents in 4D coordinate space
- **CMFL Reasoning Cycles**: Four-phase coordination pattern inspired by quantum collapse
- **Stigmergic Coordination**: Indirect agent communication via pheromone trails
- **Variance-as-Signal**: Treats disagreement between AI providers as meta-information
- **Byzantine Fault Tolerance**: Zero-failure operational requirements from emergency vehicle systems
- **Multi-Provider Integration**: Coordinates across 8+ major AI providers
- **Real-Time Monitoring**: React dashboard with WebSocket integration
- **Production-Ready**: Docker orchestration, health checks, graceful degradation

### Use Cases

- **Distributed AI Reasoning**: Coordinate multiple AI models for complex problem-solving
- **Variance Analysis**: Identify patterns in where different AI systems disagree
- **Meta-Learning Systems**: Extract insights from coordination patterns
- **Byzantine-Tolerant AI**: Mission-critical applications requiring zero-failure operation
- **Research Platform**: Study emergent behaviors in distributed AI systems

## Architecture

GhostLink v8 implements a five-layer architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING LAYER                              │
│         React Dashboard • WebSocket Updates • Metrics            │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION LAYER                             │
│     Python • 64-Agent FCC Lattice • CMFL Cycle Manager          │
│     FastAPI • Asyncio • Agent Lifecycle Management              │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                   MCP SERVER LAYER                               │
│   Node.js • Model Context Protocol • Tool Coordinators          │
│   Filesystem • HTTP • Database • GitHub Connectors               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                 COORDINATION LAYER                               │
│        Redis (Stigmergy) • PostgreSQL (Agent State)             │
│        Pheromone Trails • CMFL Cycle Records                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                INFRASTRUCTURE LAYER                              │
│     Docker Compose • Networking • Health Checks                  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Python Orchestrator (`/python/ghostlink/`)
- **Purpose**: Manages 64-agent FCC lattice and CMFL coordination
- **Technology**: Python 3.9+, FastAPI, asyncio, NumPy
- **Responsibilities**:
  - Agent lifecycle management (birth, heartbeat, death)
  - CMFL cycle execution (Collapse→Mirror→Forge→Link)
  - Lattice topology maintenance
  - Variance analysis across AI providers
  - Health monitoring and metrics export

#### 2. MCP Server Coordinator (`/node/src/`)
- **Purpose**: Model Context Protocol server cluster for tool execution
- **Technology**: Node.js 18+, TypeScript, Express
- **Responsibilities**:
  - Filesystem operations (read/write/list)
  - HTTP request proxying
  - Database query execution
  - GitHub integration
  - Pheromone trail deposition/sensing

#### 3. React Dashboard (`/node/dashboard/`)
- **Purpose**: Real-time monitoring and visualization
- **Technology**: React 18, TypeScript, Tailwind CSS, Vite
- **Features**:
  - Live agent status grid
  - CMFL phase distribution charts
  - Coordination metrics graphs
  - Pheromone trail heat maps
  - System health indicators

#### 4. Database Layer
- **PostgreSQL**: Agent state, CMFL cycles, variance analysis
- **Redis**: Stigmergic pheromone trails with TTL-based evaporation
- **Schema**: Optimized for spatial queries with GIN indexes

#### 5. Infrastructure
- **Docker Compose**: PostgreSQL, Redis, Grafana containers
- **Health Checks**: Comprehensive checks across all layers
- **Logging**: Centralized aggregation to `/logs` directory

## Core Innovation

### Variance-as-Signal Methodology

Traditional AI coordination treats disagreement between models as error to be minimized through consensus mechanisms. GhostLink inverts this paradigm:

```
Traditional Approach:
  AI Model A → Response A ┐
  AI Model B → Response B ├─→ Consensus Algorithm → Single Response
  AI Model C → Response C ┘

GhostLink Approach:
  AI Model A → Response A ┐
  AI Model B → Response B ├─→ Variance Analysis → Meta-Information
  AI Model C → Response C ┘                     → Uncertainty Boundaries
                                                → Knowledge Gaps
```

**Key Insight**: The *patterns of disagreement* reveal information about:
- Uncertainty boundaries in the problem space
- Knowledge gaps in training data
- Reasoning approach differences
- Confidence calibration across models

### CMFL Reasoning Cycle

The four-phase CMFL cycle coordinates agents without central control:

1. **Collapse**: Agent reduces uncertainty into discrete options by sensing local pheromones
2. **Mirror**: Agent reflects its state to neighbors via pheromone deposition
3. **Forge**: Agent synthesizes new understanding from variance patterns
4. **Link**: Agent coordinates final response and records cycle completion

Each agent executes independently at 500ms intervals, with coordination emerging from stigmergic coupling.

### Stigmergic Coordination

Agents communicate *indirectly* through pheromone trails in Redis:

```python
# Agent deposits pheromone at lattice position
pheromone = {
    'agent_id': '0a1b2c3d',
    'trail_type': 'mirror',
    'concentration': 0.85,
    'position': [2, 1, 3, 0]  # 4D FCC coordinates
}
redis.setex(f"pheromone:{position}", ttl=10, value)

# Neighboring agents sense pheromones
nearby_pheromones = redis.get(f"pheromone:{position}")
if concentration > STIGMERGY_THRESHOLD:
    adjust_coordination_weight(concentration)
```

Pheromones evaporate via Redis TTL, preventing stale coordination signals.

## Quick Start

### Prerequisites

```bash
# Verify system requirements
docker --version    # Docker 20.10+
docker-compose --version  # Docker Compose 2.0+
python3 --version   # Python 3.9+
node --version      # Node.js 18+
```

### Installation (5 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/devrgar-cyber/ghostlinklabs.git
cd ghostlinklabs

# 2. Initialize system
./ghostlink-boot.sh init

# 3. Configure environment
cp .env.example .env
nano .env  # Add your API keys

# 4. Start all services
./ghostlink-boot.sh start
```

### Access Points

After successful startup:

- **Dashboard**: http://localhost:5173
- **Orchestrator API**: http://localhost:8000
- **MCP Servers**: http://localhost:3000
- **Grafana**: http://localhost:3001 (admin/ghostlink)

## System Requirements

### Minimum Requirements

- **OS**: Ubuntu 20.04+ / macOS 12+ / Windows 10+ with WSL2
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Disk**: 20 GB free space
- **Network**: 10 Mbps+ (for AI provider API calls)

### Recommended Production

- **OS**: Ubuntu 22.04 LTS
- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **Disk**: 100+ GB SSD
- **Network**: 100 Mbps+, low latency to AI provider endpoints

### Required Services

- Docker Engine 20.10+
- Docker Compose 2.0+
- Python 3.9+
- Node.js 18+
- PostgreSQL 15+ (via Docker)
- Redis 7+ (via Docker)

## Installation

### Method 1: Automated Boot Script (Recommended)

```bash
# Full initialization and startup
chmod +x ghostlink-boot.sh
./ghostlink-boot.sh init
./ghostlink-boot.sh start
```

### Method 2: Manual Component Installation

```bash
# Infrastructure
cd docker
docker-compose up -d postgres redis

# Python Orchestrator
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ghostlink.orchestrator --port 8000

# MCP Servers
cd node
npm install
npm run start:mcp

# Dashboard
cd node/dashboard
npm install
npm run dev
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required: AI Provider Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Optional: Additional Providers
MISTRAL_API_KEY=...
COHERE_API_KEY=...
TOGETHER_API_KEY=...

# Core Settings
GHOSTLINK_LATTICE_SIZE=64
CMFL_CYCLE_INTERVAL=500
STIGMERGY_THRESHOLD=0.7

# Database
DATABASE_URL=postgresql://ghostlink:ghostlink@localhost:5432/ghostlink
REDIS_URL=redis://localhost:6379/0
```

### Lattice Configuration

Modify lattice parameters in `python/ghostlink/orchestrator.py`:

```python
# FCC Lattice Constants
FCC_LATTICE_SIZE = 64        # Number of agents
FCC_DIMENSIONS = 4           # Coordinate space dimensions
FCC_EDGE_LENGTH = 4          # Lattice edge length

# CMFL Cycle Configuration
CMFL_CYCLE_INTERVAL_MS = 500
STIGMERGY_THRESHOLD = 0.7
PHEROMONE_EVAPORATION_RATE = 0.1
```

### Port Configuration

Default ports (configurable in `.env`):

- **3000**: MCP Servers
- **5173**: React Dashboard
- **8000**: Python Orchestrator
- **5432**: PostgreSQL
- **6379**: Redis
- **3001**: Grafana

## Deployment

### Development Deployment

```bash
# Start with development settings
GHOSTLINK_ENV=dev ./ghostlink-boot.sh start

# Enable debug logging
DEBUG_MODE=true ./ghostlink-boot.sh start

# Mock AI providers for testing
MOCK_AI_PROVIDERS=true ./ghostlink-boot.sh start
```

### Production Deployment

```bash
# 1. Configure for production
export GHOSTLINK_ENV=production
export ENABLE_AUTH=true
export ENABLE_METRICS=true

# 2. Generate secure secrets
export JWT_SECRET=$(openssl rand -hex 32)
export ADMIN_API_KEY=$(openssl rand -hex 32)

# 3. Start with production settings
./ghostlink-boot.sh start

# 4. Verify health
./ghostlink-boot.sh status
```

### Docker Deployment

```bash
# Build production image
docker build -t ghostlink:8.0.0 .

# Run with compose
docker-compose -f docker-compose.prod.yml up -d

# Scale MCP servers
docker-compose -f docker-compose.prod.yml up -d --scale mcp-servers=3
```

### Cloud Deployment (Cloudflare Workers)

```bash
# Enable Cloudflare Workers
export CLOUDFLARE_WORKERS_ENABLED=true
export CLOUDFLARE_ACCOUNT_ID=your-account-id
export CLOUDFLARE_API_TOKEN=your-api-token

# Deploy to edge locations
wrangler deploy
```

## Monitoring

### Dashboard Overview

The React dashboard (`http://localhost:5173`) provides:

- **System Health**: Overall status and uptime
- **Agent Status**: 64-agent grid with CMFL phase indicators
- **Coordination Metrics**: Variance scores, coordination weights
- **Pheromone Activity**: Active stigmergic trail count
- **CMFL Cycles**: Total cycles completed across all agents

### API Health Checks

```bash
# Orchestrator health
curl http://localhost:8000/health

# MCP servers health
curl http://localhost:3000/health

# Agent status
curl http://localhost:8000/agents/status

# Coordination metrics
curl http://localhost:8000/metrics/coordination
```

### Log Aggregation

Logs are centralized in `/opt/ghostlink/logs/`:

```bash
# View all logs
./ghostlink-boot.sh logs all

# View specific component
./ghostlink-boot.sh logs orchestrator
./ghostlink-boot.sh logs mcp
./ghostlink-boot.sh logs dashboard

# Tail live logs
tail -f /opt/ghostlink/logs/orchestrator.log
```

### Grafana Dashboards

Access Grafana at `http://localhost:3001` (admin/ghostlink):

- **System Overview**: CPU, memory, network metrics
- **Agent Performance**: CMFL cycle times, variance scores
- **Coordination Health**: Pheromone trail activity, agent connectivity
- **Database Metrics**: Query performance, connection pool status

## API Documentation

### Python Orchestrator API

**Base URL**: `http://localhost:8000`

#### Health Check

```http
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "8.0.0",
  "lattice_size": 64,
  "active_agents": 64,
  "uptime_seconds": 3600.5
}
```

#### Agent Status

```http
GET /agents/status
```

Response:
```json
{
  "total_agents": 64,
  "active_count": 64,
  "inactive_count": 0,
  "agents_by_phase": {
    "collapse": 16,
    "mirror": 16,
    "forge": 16,
    "link": 16
  }
}
```

#### Coordination Metrics

```http
GET /metrics/coordination
```

Response:
```json
{
  "stigmergy_trails_active": 42,
  "cmfl_cycles_completed": 15234,
  "average_variance_score": 0.342,
  "average_coordination_weight": 1.125
}
```

### MCP Server API

**Base URL**: `http://localhost:3000`

#### List Tools

```http
GET /tools
```

#### Execute Tool

```http
POST /execute/:toolName
Content-Type: application/json

{
  "param1": "value1",
  "param2": "value2"
}
```

## Development

### Project Structure

```
ghostlinklabs/
├── ghostlink-boot.sh          # Master boot orchestrator
├── .env.example               # Configuration template
├── README.md                  # This file
│
├── python/                    # Python orchestrator
│   ├── ghostlink/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   └── orchestrator.py    # Main orchestration logic
│   └── requirements.txt       # Python dependencies
│
├── node/                      # Node.js MCP servers
│   ├── src/
│   │   └── mcp-coordinator.ts # MCP server coordinator
│   ├── dashboard/             # React monitoring dashboard
│   │   ├── src/
│   │   │   ├── App.tsx        # Main dashboard component
│   │   │   └── main.tsx       # Entry point
│   │   └── package.json
│   ├── package.json
│   └── tsconfig.json
│
└── docker/                    # Infrastructure
    ├── docker-compose.yml
    └── init-db.sql            # Database initialization
```

### Running Tests

```bash
# Python tests
cd python
pytest tests/ --cov=ghostlink

# Node.js tests
cd node
npm test

# Integration tests
./run-integration-tests.sh
```

### Building Documentation

```bash
# Python docs
cd python
sphinx-build -b html docs/ docs/_build/

# Node.js docs
cd node
npm run docs
```

## Troubleshooting

### Common Issues

#### 1. Agents Not Starting

```bash
# Check database connection
PGPASSWORD=ghostlink psql -h localhost -U ghostlink -d ghostlink -c "SELECT COUNT(*) FROM agents;"

# Verify Redis
redis-cli ping

# Check orchestrator logs
tail -f /opt/ghostlink/logs/orchestrator.log
```

#### 2. MCP Servers Unhealthy

```bash
# Check port availability
lsof -i :3000

# Restart MCP servers
cd /opt/ghostlink/node
npm run start:mcp
```

#### 3. Dashboard Not Loading

```bash
# Check dashboard build
cd /opt/ghostlink/node/dashboard
npm run build

# Verify ports
curl http://localhost:5173
```

#### 4. High Variance Scores

High variance is expected and indicates rich meta-information. However, consistently maximal variance (>0.9) may indicate:

- API key issues
- Provider rate limiting
- Network connectivity problems
- Ambiguous prompts requiring more context

### Debug Mode

Enable comprehensive debugging:

```bash
# Set debug flags
export DEBUG_MODE=true
export GHOSTLINK_DEBUG=1
export LOG_LEVEL=DEBUG

# Restart services
./ghostlink-boot.sh restart

# Monitor debug logs
tail -f /opt/ghostlink/logs/*.log | grep DEBUG
```

### Health Check Failures

```bash
# Run comprehensive validation
./ghostlink-boot.sh validate

# Check individual components
curl http://localhost:8000/health
curl http://localhost:3000/health
docker-compose -f /opt/ghostlink/docker/docker-compose.yml ps
```

## Contributing

GhostLink v8 welcomes contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Implement changes with tests
4. Commit with descriptive messages (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

### Code Standards

- **Python**: Black formatting, type hints, comprehensive docstrings
- **TypeScript**: ESLint + Prettier, strict mode enabled
- **Commits**: Conventional Commits format
- **Tests**: 80%+ coverage required for new features

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Robert Christopher George (Ghost)**  
Senior Electrical Diagnostics Specialist → AI Coordination Research

- Email: ghost@ghostlinklabs.com
- GitHub: [@devrgar-cyber](https://github.com/devrgar-cyber)

## Acknowledgments

- Inspired by termite mound coordination and mycelial networks
- Built on 18+ years of Byzantine fault tolerance experience in emergency vehicle systems
- Over 500 research sessions consolidated into production-ready implementation

## Citation

If you use GhostLink v8 in research, please cite:

```bibtex
@software{ghostlink2024,
  author = {George, Robert Christopher},
  title = {GhostLink v8: Distributed AI Coordination Protocol},
  year = {2024},
  url = {https://github.com/devrgar-cyber/ghostlinklabs},
  version = {8.0.0}
}
```

---

**Built with precision. Deployed with confidence. Coordinated with stigmergy.**

*GhostLink v8 - Where variance becomes signal.*

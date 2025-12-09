# GhostLink Hybrid Triad

🧬 **GhostLink AI Ecosystem - Absorptive Architecture**

A sovereign, local-first AI framework that operates independently of external services while maintaining hybrid capabilities for enhanced functionality through **Triad Synergy** - seamless integration between Python, Mathematica, and Docker components.

## Triad Synergy Overview

GhostLink implements a revolutionary **Hybrid Triad Mode** that combines three powerful components:

### 🐍 **Python Core** (Local Foundation)
- **Sovereign Operation**: Fully functional with Python stdlib only
- **Fallback Mode**: Graceful degradation when dependencies unavailable
- **Local-First**: All operations prioritize local execution
- **Autonomous Agents**: Task planning and execution without external APIs

### 🔢 **Mathematica Layer** (Symbolic Enhancement)
- **Symbolic Computation**: Advanced mathematical analysis and processing
- **AI Enhancement**: Symbolic reasoning for improved AI capabilities
- **Knowledge Representation**: Mathematical modeling of complex systems
- **Hybrid Intelligence**: Combines neural and symbolic approaches

### 🐳 **Docker Infrastructure** (Deployment & Scaling)
- **Containerization**: Portable deployment across environments
- **Service Orchestration**: Multi-component coordination
- **Network Isolation**: Sovereign communication channels
- **Scalable Architecture**: From single-node to cluster deployments

## Quick Start

### Sovereign Mode (Python Stdlib Only)
```bash
git clone https://github.com/ghostlink/hybrid-triad.git
cd hybrid-triad
python3 -m pip install -e .
ghostlink
```

### Hybrid Triad Mode (Full Synergy)
```bash
# Activate complete triad synergy
./activate_triad_synergy.sh

# Or manually:
pip install -e ".[full]"
docker-compose up -d
ghostlink --triad-synergy
```

### Experimental Triad Mode
```bash
# Enable all experimental features
export GHOSTLINK_EXPERIMENTAL=true
export GHOSTLINK_HYBRID_MODE=true
export GHOSTLINK_SOVEREIGN=true

ghostlink --experimental
```

## Triad Synergy Features

### 🔗 **Seamless Component Integration**
- **Python ↔ Mathematica**: Symbolic computation bridge
- **Python ↔ Docker**: Containerized deployment
- **Mathematica ↔ Docker**: Symbolic processing in containers
- **Cross-Component Communication**: Unified API across all components

### ⚡ **Synergy Operations**
```bash
# Triad analysis
ghostlink triad analyze

# Symbolic computation
ghostlink triad symbolic "Solve[x^2 + 3x + 2 == 0, x]"

# Hybrid AI processing
ghostlink triad hybrid "Explain neural networks mathematically"

# Container operations
ghostlink triad container build
ghostlink triad container deploy
```

### 🌐 **Network Endpoints**
- **GhostLink API**: `http://localhost:8000`
- **Triad Synergy Hub**: `http://localhost:7422`
- **Mathematica Kernel**: `localhost:31415`
- **Health Checks**: `http://localhost:8000/health`

## Architecture

### Hybrid Triad Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Python Core   │◄──►│ Triad Synergy    │◄──►│  Mathematica    │
│                 │    │ Orchestrator     │    │   Engine        │
│ • Stdlib Only   │    │                  │    │                 │
│ • Fallback Mode │    │ • Python Bridge  │    │ • Symbolic AI   │
│ • Local First   │    │ • Docker Bridge  │    │ • Math Engine   │
└─────────────────┘    │ • Math Bridge    │    └─────────────────┘
                       └──────────────────┘             │
                              ▲                        │
                              │                        │
                       ┌─────────────────┐             │
                       │   Docker        │◄────────────┘
                       │   Infrastructure│
                       │                 │
                       │ • Containers    │
                       │ • Orchestration │
                       │ • Networking    │
                       └─────────────────┘
```

### Sovereign Operation Principles
1. **Local-First**: All operations work without network dependencies
2. **Graceful Degradation**: System adapts to available components
3. **Optional Enhancement**: External dependencies provide bonuses, not requirements
4. **Network Sovereignty**: No mandatory external service connections

## Installation

### Minimal Installation (Sovereign)
```bash
pip install -e .
```

### Standard Installation (Hybrid)
```bash
pip install -e ".[ml,data,web,config]"
```

### Full Installation (Triad)
```bash
pip install -e ".[full]"
```

### Docker Deployment
```bash
docker-compose up -d
```

## Usage

### Command Line Interface
```bash
# Basic operation
ghostlink

# Triad synergy mode
ghostlink --triad-synergy

# Symbolic computation
ghostlink --symbolic-compute "D[Sin[x], x]"

# Hybrid AI
ghostlink --hybrid-ai "What is machine learning?"

# Terminal interface
ghostlink --terminal-90s
```

### Programmatic Usage
```python
from triad_synergy import triad_synergy
import asyncio

async def main():
    # Initialize synergy
    await triad_synergy.initialize_synergy()

    # Execute symbolic computation
    result = await triad_synergy.execute_synergy_task({
        "type": "symbolic_computation",
        "expression": "Integrate[Exp[-x^2], {x, -Infinity, Infinity}]"
    })

    # Execute hybrid AI
    result = await triad_synergy.execute_synergy_task({
        "type": "hybrid_ai",
        "prompt": "Explain quantum entanglement"
    })

asyncio.run(main())
```

### Mathematica Integration
```mathematica
(* Load GhostLink package *)
Get["GhostLink`"];

(* Create model *)
model = GhostLinkModel[];

(* Generate response *)
response = GenerateResponse[model, "How does symbolic computation help AI?"];

(* Learn from interaction *)
model = LearnFromInteraction[model, "Question", "Answer"];
```

## Configuration

### Environment Variables
```bash
# Core Settings
GHOSTLINK_EXPERIMENTAL=true          # Enable experimental features
GHOSTLINK_HYBRID_MODE=true           # Enable hybrid triad mode
GHOSTLINK_LOCAL_FIRST=true           # Prioritize local operations
GHOSTLINK_SOVEREIGN=true             # Maintain network sovereignty

# Triad Components
MATHEMATICA_KERNEL_URL=http://localhost:31415
DOCKER_SOCKET=/var/run/docker.sock
TRIAD_SYNERGY_PORT=7421
```

### Configuration File
See `triad_synergy.ini` for detailed configuration options.

## Development

### Prerequisites
- Python 3.8+
- Docker (optional)
- Wolfram Mathematica/Engine (optional)
- Git

### Development Setup
```bash
git clone https://github.com/ghostlink/hybrid-triad.git
cd hybrid-triad
./activate_triad_synergy.sh
```

### Testing
```bash
# Run all tests
pytest

# Test triad synergy
python3 triad_synergy.py

# Test symbolic computation
python3 triad_synergy.py --expression "2 + 2"
```

## API Reference

### REST API Endpoints
- `GET /health` - System health check
- `POST /api/generate` - Generate AI response
- `POST /triad/synergy` - Execute triad synergy task
- `GET /api/status` - System status

### Triad Synergy Tasks
- `symbolic_computation` - Execute Mathematica expressions
- `hybrid_ai` - Combined Python + Mathematica AI processing
- `containerized_deployment` - Docker container operations
- `triad_analysis` - Comprehensive system analysis

## Deployment

### Docker Compose
```yaml
version: '3.8'
services:
  ghostlink:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GHOSTLINK_HYBRID_MODE=true
  triad-synergy-hub:
    build:
      context: .
      dockerfile: Dockerfile.synergy
    ports:
      - "7422:7422"
```

### Kubernetes
```bash
kubectl apply -f infrastructure/ghostlink-cluster.yaml
```

## Security

- **No Hardcoded Secrets**: Environment-based configuration only
- **Sovereign Operation**: No mandatory external dependencies
- **Optional Encryption**: Configurable security features
- **Network Isolation**: Container-level network segmentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement triad synergy enhancements
4. Add comprehensive tests
5. Submit a pull request

### Development Guidelines
- Maintain sovereign operation capability
- Add optional dependencies as enhancements
- Include triad synergy integration
- Follow black code formatting
- Add tests for all components

## License

MIT License - see LICENSE file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/ghostlink/hybrid-triad/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ghostlink/hybrid-triad/discussions)
- **Documentation**: [Read the Docs](https://ghostlink.readthedocs.io/)

---

**🧬 GhostLink: Where Python meets Mathematica in Docker's embrace**

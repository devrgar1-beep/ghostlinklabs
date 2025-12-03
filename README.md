# GhostLink AI Ecosystem

A comprehensive, modular AI ecosystem with multi-provider support, autonomous agents, and free API integration. Now includes **local AI models** - no API keys required!

## Features

- **🔧 Local AI First**: Ollama integration for running AI models locally (no API keys needed!)
- **🌐 Multi-Provider AI**: Claude, ChatGPT, Grok, and Gemini with automatic failover
- **🤖 Autonomous Agents**: Self-directing AI agents with memory and coordination
- **🎮 90s Terminal UI**: Retro cyberpunk interface with animated loading
- **📡 Free API Integration**: 200+ public APIs for real-time data
- **🏗️ Modular Architecture**: Clean separation of concerns
- **⚡ Production Ready**: Comprehensive error handling and logging

## Quick Start

### Option 1: Local AI (Recommended - No API Keys Needed!)

1. **Setup local AI:**
   ```bash
   # Linux/macOS
   bash setup_local_ai.sh

   # Windows
   setup_local_ai.bat
   ```

2. **Test it:**
   ```bash
   python main.py ask "Hello local AI!"
   ```

## Docker (optional)

Run GhostLink components in containers. This is handy for servers and quick setups.

### Prerequisites
- Docker Engine 24+ or Docker Desktop
- Optional: `docker compose` plugin

### Build image
```bash
docker build -t ghostlink:latest .
```

### Run with Docker Compose (recommended)
By default only the controller runs and exposes Prometheus metrics on 9108 (host network).
```bash
docker compose up -d
```

Enable additional components by toggling environment flags in `docker-compose.yml`:
- `RUN_PEER=1`         read local sensors (mounts `/sys/class/thermal`)
- `RUN_MESH=1`         run mesh aggregator (connects to controller)
- `RUN_RESPONDER=1`    run peer responder on port 7422
- `RUN_BRIDGE=1`       run OpenAI bridge (requires `OPENAI_API_KEY`)

Example: controller + mesh + responder
```bash
docker compose up -d --build
```

Check metrics
```bash
curl -s http://127.0.0.1:9108/metrics | head
```

Stop
```bash
docker compose down
```
### Option 2: API Providers (Requires API Keys)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Test with API providers:**
   ```bash
   python main.py ask "Hello API AI!" --provider anthropic
   ```

## Usage Examples

### Local AI Conversations
```bash
python main.py ask "What is the meaning of life?"
python main.py ask "Write a Python function to calculate fibonacci" --provider ollama
```

### API Data Analysis
```bash
python main.py api jokes --question "Rate this joke's humor"
python main.py api iss_location --question "Where is the ISS right now?"
```

### Autonomous Agent
```bash
python main.py agent "Analyze current market trends" --agent-role analyst
```

### Cyberpunk Interface
```bash
python main.py --terminal-90s
```

## Architecture

```
ghostlink/
├── core/           # Core business logic
│   ├── ai_providers.py     # AI provider management (Ollama + APIs)
│   ├── api_integration.py  # Free API integration
│   └── autonomous_agents.py # Agent orchestration
├── interfaces/     # User interfaces
│   ├── cli.py             # Command-line interface
│   ├── terminal_90s.py    # Retro terminal UI
│   └── web.py             # Web interface (future)
├── utils/          # Utilities
│   ├── config.py          # Configuration management
│   ├── logging.py         # Logging setup
│   └── error_handling.py  # Error handling
└── tests/          # Test suite
```

## Configuration

The system uses a hierarchical configuration system:

1. **Environment variables** (highest priority)
2. **YAML config file** (`config.yaml`)
3. **Default values** (lowest priority)

### Default Setup (Local AI)
- **Default Provider**: `ollama` (local models)
- **No API Keys Required**: Works out of the box with local models
- **Fallback**: Automatically uses API providers if available

### API Provider Setup (Optional)
Set these in your `.env` file for API provider access:

```bash
ANTHROPIC_API_KEY=your_actual_anthropic_key
OPENAI_API_KEY=your_actual_openai_key
GROK_API_KEY=your_actual_grok_key
GOOGLE_API_KEY=your_actual_google_key
```

## Local AI Models

GhostLink supports local AI models through Ollama:

### Popular Models to Try
```bash
# Fast and capable (recommended)
ollama pull mistral

# Code-focused
ollama pull codellama

# General purpose
ollama pull llama2:13b

# Creative writing
ollama pull llama2:70b
```

### Switching Models
```bash
# Use different models
python main.py ask "Hello!" --provider ollama

# Configure default model in config.yaml
ai:
  providers:
    ollama:
      model: mistral  # Change from default llama2
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
black ghostlink/          # Format code
flake8 ghostlink/         # Lint code
mypy ghostlink/           # Type checking
```

### Adding New Features

1. **New AI Provider**: Add to `ghostlink/core/ai_providers.py`
2. **New API**: Add to `ghostlink/core/api_integration.py`
3. **New Interface**: Add to `ghostlink/interfaces/`
4. **New Utility**: Add to `ghostlink/utils/`

## Documentation

Comprehensive documentation is available in the `docs/` directory:

### 📚 Quick Links
- **[Documentation Index](docs/INDEX.md)** - Complete documentation overview
- **[Quick Reference](docs/reference/QUICK_REFERENCE.md)** - Common commands and operations
- **[Deployment Guide](docs/deployment/GHOSTLINK_DEPLOYMENT.md)** - Production deployment
- **[Mesh Network Integration](NEIGHBOR_INTEGRATION.md)** - Distributed monitoring setup

### 📖 Architecture & Theory
- [Theoretical Foundations](docs/architecture/01-THEORETICAL-FOUNDATIONS.md) - Core concepts and math
- [64-Agent Array](docs/architecture/02-64-AGENT-ARRAY.md) - Distributed architecture
- [Pipelines & Sharding](docs/architecture/03-PIPELINES-SHARDS-MIRRORS.md) - Data flow patterns
- [DAK Infrastructure](docs/architecture/04-DAK-SOVEREIGNTY-INFRA.md) - Autonomous systems
- [Advanced Implementation](docs/architecture/05-ADVANCED-IMPLEMENTATION.md) - Optimization strategies

### 🔬 Research & Applications
- [Research Applications](docs/research/06-RESEARCH-APPLICATIONS.md) - Research methodologies

### 📋 Reference & Operations
- [Code Reference](docs/reference/07-CODE-REFERENCE.md) - Complete API documentation
- [Testing & Deployment](docs/deployment/08-TESTING-DEPLOYMENT-OPS.md) - Operations guide
- [Deployment Summary](docs/deployment/DEPLOYMENT_SUMMARY.txt) - Deployment checklist

## Mesh Network Monitoring

GhostLink includes distributed thermal monitoring with mesh networking:

### Quick Start Mesh Network
```bash
# Start core services
./run_venv.sh up

# Start mesh aggregator
./run_venv.sh mesh

# Check integration status
python3 gl_integration_summary.py

# View network status
python3 gl_network_status.py
```

### Mesh Components
- **gl_controller_metrics.py** - Central metrics controller (Port 7420)
- **gl_peer_mesh.py** - Mesh aggregator for multi-host monitoring
- **gl_peer_responder.py** - Lightweight peer service for neighbors
- **gl_network_status.py** - Network discovery and status tool

See [NEIGHBOR_INTEGRATION.md](NEIGHBOR_INTEGRATION.md) for complete mesh setup guide.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the logs in `logs/ghostlink.log`
- Run `python main.py status` for system diagnostics

---

**Built with ❤️ for the future of AI ecosystems - Local First! 🧠⚡🎮**

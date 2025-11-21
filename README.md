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

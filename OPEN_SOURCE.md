# GhostLink - Open Source AI Framework

GhostLink is now **100% open source** and depends only on open source components.

## Open Source Dependencies

All dependencies are open source with permissive licenses:

- **FastAPI** (MIT) - Web framework
- **httpx** (BSD) - HTTP client
- **matplotlib** (PSF/BSD) - Plotting library
- **numpy** (BSD) - Numerical computing
- **pydantic** (MIT) - Data validation
- **python-dotenv** (BSD) - Environment management
- **sqlalchemy** (MIT) - Database toolkit
- **pytest** (MIT) - Testing framework
- **black** (MIT) - Code formatter
- **ruff** (MIT) - Linter

## LLM Integration (Optional)

GhostLink supports **any OpenAI-compatible API**, allowing you to use open source LLM solutions:

### Recommended Open Source LLM Platforms

1. **Ollama** - Run LLMs locally
   - https://ollama.ai
   - Supports Llama 2, Mistral, CodeLlama, and more
   - Easy installation and management

2. **LocalAI** - OpenAI-compatible API for local models
   - https://localai.io
   - Runs on CPU and GPU
   - Compatible with many model formats

3. **LM Studio** - Desktop app for running LLMs
   - https://lmstudio.ai
   - User-friendly GUI
   - Local inference

4. **vLLM** - High-throughput LLM serving
   - https://github.com/vllm-project/vllm
   - Production-ready
   - Optimized performance

5. **Text Generation WebUI** - Gradio web UI for LLMs
   - https://github.com/oobabooga/text-generation-webui
   - Multiple model support
   - API compatibility

### Configuration Example

```bash
# Using Ollama (recommended for local development)
LLM_API_URL=http://localhost:11434/api/generate
LLM_MODEL=llama2

# Using LocalAI
LLM_API_URL=http://localhost:8080/v1/completions
LLM_MODEL=gpt-3.5-turbo  # LocalAI model name
LLM_API_KEY=your-optional-key

# Using LM Studio
LLM_API_URL=http://localhost:1234/v1/completions
LLM_MODEL=local-model
```

## Running Without LLM Integration

GhostLink's core functionality works without any LLM integration. The bridge component is **completely optional** and only needed if you want external language model capabilities.

## License

MIT License - See LICENSE file for full text.

## Contributing

As an open source project, contributions are welcome! Please ensure all contributions:
- Use only open source dependencies
- Include appropriate tests
- Follow the existing code style
- Are compatible with the MIT license

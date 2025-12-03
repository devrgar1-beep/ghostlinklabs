# AI Orchestration Setup

Free AI API keys for internal orchestration with Copilot as oracle.

## Quick Start

1. **Get API Keys** (all free tier)

- **Groq** (fastest, recommended): https://console.groq.com/keys
- **Together AI**: https://api.together.xyz/settings/api-keys
- **Hugging Face**: https://huggingface.co/settings/tokens
- **OpenRouter** (optional): https://openrouter.ai/keys

2. **Configure**

```bash
# Copy template
cp .env.example .env

# Edit .env and add your keys
nano .env
```

3. **Install dependencies**

```bash
pip install --user httpx python-dotenv
```

4. **Test**

```bash
# Load env vars
export $(cat .env | xargs)

# Run the AI bot
python3 ai_bots/run.py
```

## Usage

In the bot CLI:

```bash
# Ask AI (via Groq)
ai ask what is quantum computing?
!ask explain docker compose

# Ask Copilot oracle
ai oracle how do I optimize this code?
@ai copilot what's the best approach here?

# Check providers
ai providers

# List models
ai models
```

## Hotkeys

- `ctrl+shift+a` - Ask AI
- `ctrl+shift+o` - Ask Copilot oracle

## Free Tier Limits

- **Groq**: 14,400 requests/day (very generous)
- **Together AI**: $25 free credit monthly
- **Hugging Face**: Rate-limited but free
- **Copilot Oracle**: Uses your GitHub Copilot subscription

## Architecture

```
User Query
    ↓
AI Orchestration Bot
    ↓
    ├─→ Groq API (fast inference)
    ├─→ Together AI (multiple models)
    ├─→ Hugging Face (open models)
    └─→ Copilot Oracle (VS Code integration)
```

## Copilot Oracle

The oracle mode uses GitHub Copilot as a privileged AI advisor:

- **Current**: Placeholder that prompts you to use Copilot Chat
- **Future**: Direct API integration when GitHub releases Copilot API
- **Workaround**: Use `@workspace` or `@terminal` in VS Code Copilot Chat

## Example: Multi-Provider Strategy

```python
# Fast queries → Groq
ai ask what is the capital of France?

# Complex reasoning → Copilot oracle
ai oracle analyze this distributed system design

# Code generation → Copilot oracle
ai oracle write a binary search tree in Rust
```

## Security

- Store API keys in `.env` (never commit)
- `.env` is gitignored by default
- Use read-only access level for AI bot
- Consider using separate keys for dev/prod

## Troubleshooting

**"Groq API key not configured"**
- Check `.env` file exists
- Ensure `GROQ_API_KEY` is set
- Load env: `export $(cat .env | xargs)`

**"httpx not installed"**
```bash
pip install --user httpx
```

**"Copilot oracle not enabled"**
- Set `COPILOT_ORACLE_ENABLED=true` in `.env`
- Ensure GitHub Copilot is active in VS Code

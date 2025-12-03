#!/usr/bin/env python3
"""
API Keys Setup - Multi-Provider AI System
==========================================
Manage API keys for all supported AI providers: Claude, ChatGPT, Grok, and Gemini.
"""

import os


def main():
    print("🔐 AI PROVIDER API KEYS SETUP")
    print("=============================")
    print("Setting up API keys for multi-provider AI system.\n")

    providers = {
        "anthropic": {
            "name": "Claude (Anthropic)",
            "env_vars": ["ANTHROPIC_API_KEY"],
            "url": "https://console.anthropic.com/",
            "models": ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"],
            "format": "sk-ant-api03-...",
        },
        "openai": {
            "name": "ChatGPT (OpenAI)",
            "env_vars": ["OPENAI_API_KEY"],
            "url": "https://platform.openai.com/api-keys",
            "models": ["gpt-4o", "gpt-4o-mini", "chatgpt-4o-latest"],
            "format": "sk-...",
        },
        "grok": {
            "name": "Grok (X.AI)",
            "env_vars": ["XAI_API_KEY", "GROK_API_KEY"],
            "url": "https://console.x.ai/",
            "models": ["grok-beta", "grok-2-1212", "grok-vision-beta"],
            "format": "xai-...",
        },
        "google": {
            "name": "Gemini (Google)",
            "env_vars": ["GOOGLE_API_KEY"],
            "url": "https://aistudio.google.com/app/apikey",
            "models": ["gemini-1.5-pro-latest", "gemini-pro"],
            "format": "AI...",
        },
    }

    configured_count = 0

    for provider_id, info in providers.items():
        print(f"🤖 {info['name']}")
        print("-" * (len(info["name"]) + 3))

        # Check if already configured
        configured = any(os.getenv(env_var) for env_var in info["env_vars"])

        if configured:
            key_source = None
            for env_var in info["env_vars"]:
                if os.getenv(env_var):
                    key_source = env_var
                    break

            print(f"✅ CONFIGURED via {key_source}")
            configured_count += 1
        else:
            print("❌ NOT CONFIGURED")
            print(f"   Get API key: {info['url']}")
            print(f"   Set environment variable(s): {', '.join(info['env_vars'])}")
            print(f"   Key format: {info['format']}")

        print(f"   Top models: {', '.join(info['models'][:2])}")
        print()

    # Summary
    print("📊 CONFIGURATION SUMMARY")
    print("========================")
    print(f"Configured providers: {configured_count}/{len(providers)}")

    if configured_count > 0:
        print("✅ Ready to use multi-AI system!")
        print("\nTest with:")
        print("  python claude_cli.py --interactive")
        print("  python claude_cli.py --list-models")
    else:
        print("⚠️  No providers configured. Set at least one API key to get started.")

    print("\n🚀 QUICK SETUP COMMANDS (Windows PowerShell):")
    print("=" * 50)

    if not any(
        os.getenv(env_var)
        for provider_id, info in providers.items()
        for env_var in info["env_vars"]
    ):
        print("# Set your API keys (replace with actual keys)")
        for provider_id, info in providers.items():
            env_var = info["env_vars"][0]  # Use primary env var
            print(f'$env:{env_var} = "{info["format"]}"')

        print("\n# Or add to PowerShell profile for persistence:")
        print("notepad $PROFILE")
        print("# Add the $env: lines above to the profile file")

    print("\n💡 USAGE EXAMPLES:")
    print("=" * 18)
    print("# Interactive mode with auto-provider selection")
    print("python claude_cli.py --interactive")
    print()
    print("# Use specific provider")
    print('python claude_cli.py --provider grok --message "Hello from Grok!"')
    print()
    print("# Use specific model")
    print('python claude_cli.py --model gpt-4o --message "Hello ChatGPT-4o!"')
    print()
    print("# List all available models")
    print("python claude_cli.py --list-models")


if __name__ == "__main__":
    main()

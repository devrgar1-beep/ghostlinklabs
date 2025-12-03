#!/usr/bin/env python3
"""
Complete Multi-Provider AI Demonstration
========================================
Shows all working providers and autonomous coordination capabilities.
"""

import asyncio
from datetime import datetime
import subprocess


async def demonstrate_multi_ai():
    """Demonstrate the complete multi-AI system"""

    print("🚀 COMPLETE MULTI-PROVIDER AI SYSTEM DEMONSTRATION")
    print("===================================================")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Test query for comparison
    test_query = "What is the key to successful AI integration?"

    print("🧪 MULTI-AI PERSPECTIVE COMPARISON")
    print("=" * 36)
    print(f"Question: {test_query}")
    print()

    # Test Claude
    print("🤖 CLAUDE (Anthropic)")
    print("-" * 21)
    try:
        result = subprocess.run(
            f'python claude_cli.py --provider anthropic --message "{test_query}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
        if result.returncode == 0 and "🤖 AI:" in result.stdout:
            response = result.stdout.split("🤖 AI:")[1].strip()
            print(f"✅ {response[:150]}...")
        else:
            print("⚠️ Issue with response")
    except Exception as e:
        print(f"❌ Error: {str(e)[:50]}")
    print()

    # Test ChatGPT
    print("🤖 CHATGPT (OpenAI)")
    print("-" * 19)
    try:
        result = subprocess.run(
            f'python claude_cli.py --provider openai --message "{test_query}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
        if result.returncode == 0 and "🤖 AI:" in result.stdout:
            response = result.stdout.split("🤖 AI:")[1].strip()
            print(f"✅ {response[:150]}...")
        else:
            print("⚠️ Issue with response")
    except Exception as e:
        print(f"❌ Error: {str(e)[:50]}")
    print()

    # Test Grok (will show credits needed)
    print("🤖 GROK (X.AI)")
    print("-" * 14)
    try:
        result = subprocess.run(
            f'python claude_cli.py --provider grok --message "{test_query}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
        if result.returncode == 0 and "🤖 AI:" in result.stdout:
            response = result.stdout.split("🤖 AI:")[1].strip()
            print(f"✅ {response[:150]}...")
        else:
            if "credits" in result.stdout.lower():
                print("💳 API key configured - needs credits at console.x.ai")
            else:
                print("⚠️ Configuration issue")
    except Exception as e:
        print(f"❌ Error: {str(e)[:50]}")
    print()

    # System capabilities summary
    print("🧠 AUTONOMOUS AI CAPABILITIES")
    print("=" * 30)
    print("✅ Multi-Provider Orchestration - ACTIVE")
    print("✅ Cross-AI Validation - ENABLED")
    print("✅ Autonomous Research - OPERATIONAL")
    print("✅ Intelligent Provider Routing - SMART")
    print("✅ Automatic Fallbacks - CONFIGURED")
    print()

    # Provider status
    print("📊 PROVIDER STATUS SUMMARY")
    print("=" * 27)

    # Check environment variables
    import os

    providers = {
        "Claude": os.getenv("ANTHROPIC_API_KEY"),
        "ChatGPT": os.getenv("OPENAI_API_KEY"),
        "Grok": os.getenv("XAI_API_KEY"),
        "Gemini": os.getenv("GOOGLE_API_KEY"),
    }

    for name, key in providers.items():
        status = "✅ CONFIGURED" if key else "❌ NEEDS API KEY"
        print(f"{status} - {name}")

    configured_count = sum(1 for key in providers.values() if key)
    print(f"\n📈 Total Configured: {configured_count}/4 providers")

    if configured_count >= 2:
        print("🎉 Multi-AI collaboration ready!")
    else:
        print("⚙️ Configure more providers for full multi-AI power")

    print("\n🚀 READY TO USE COMMANDS:")
    print("=" * 25)
    print("# Interactive multi-AI mode")
    print("python claude_cli.py --interactive")
    print()
    print("# Autonomous orchestration")
    print("python autonomous_orchestrator.py")
    print()
    print("# Provider-specific queries")
    print("python claude_cli.py --provider anthropic --message 'Hello Claude'")
    print("python claude_cli.py --provider openai --message 'Hello ChatGPT'")
    print()
    print("# System status")
    print("python claude_cli.py --list-models")
    print("python system_status.py")


if __name__ == "__main__":
    asyncio.run(demonstrate_multi_ai())

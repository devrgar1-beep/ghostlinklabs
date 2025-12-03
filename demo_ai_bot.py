#!/usr/bin/env python3
"""Quick demo of AI bot commands"""
import asyncio
import os
import sys

sys.path.insert(0, '.')

from ai_bots.core import (  # noqa: E402
    CommandRouter,
    SystemBot,
    MetricsBot,
    BotContext,
    AccessLevel
)
from ai_bots.plugins.ai_orchestration import AIOrchestrationBot  # noqa: E402
from ai_bots.plugins.calculator import CalculatorBot  # noqa: E402


async def demo():
    # Check for required API key
    if not os.environ.get('GROQ_API_KEY'):
        print("❌ Error: GROQ_API_KEY environment variable not set")
        print("Please set it before running: "
              "export GROQ_API_KEY='your-key-here'")
        sys.exit(1)

    router = CommandRouter()
    
    # Register all bots
    system_bot = SystemBot()
    metrics_bot = MetricsBot()
    ai_bot = AIOrchestrationBot()
    calc_bot = CalculatorBot()
    
    await router.register_bot(system_bot)
    await router.register_bot(metrics_bot)
    await router.register_bot(ai_bot)
    await router.register_bot(calc_bot)
    
    ctx = BotContext('admin', 'demo', AccessLevel.ROOT, yolo_mode=True)
    
    commands = [
        ("/ai ask explain docker compose", "🐳 Docker Compose"),
        ("/ai ask what is machine learning?", "🤖 Machine Learning"),
        ("/ai providers", "📋 Providers"),
        ("/system status", "💻 System Status"),
        ("/system yolo", "🎯 YOLO Toggle"),
    ]
    
    print("=" * 60)
    print("GhostLink AI Bot Demo")
    print("=" * 60)
    print()
    
    for cmd, title in commands:
        print(f"\n{title}")
        print(f"Command: {cmd}")
        print("-" * 60)
        
        result = await router.route(cmd, ctx)
        
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            output = result.get('result', 'OK')
            print(output)
        
        print()
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(demo())

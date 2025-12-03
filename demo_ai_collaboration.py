#!/usr/bin/env python3
"""
Demo: AI-to-AI Collaboration
Shows agents working together on complex tasks
"""
import asyncio
import os
import sys

sys.path.insert(0, '.')

from ai_bots.ai_bus import ai_bus  # noqa: E402
from ai_bots.core import (  # noqa: E402
    SystemBot,
    MetricsBot,
    BotContext,
    AccessLevel
)
from ai_bots.plugins.calculator import CalculatorBot  # noqa: E402
from ai_bots.plugins.ai_orchestration import AIOrchestrationBot  # noqa: E402


async def demo():
    # Check for required API key
    if not os.environ.get('GROQ_API_KEY'):
        print("❌ Error: GROQ_API_KEY environment variable not set")
        print("Please set it before running: "
              "export GROQ_API_KEY='your-key-here'")
        sys.exit(1)

    # Setup agents
    system_bot = SystemBot()
    metrics_bot = MetricsBot()
    calc_bot = CalculatorBot()
    ai_bot = AIOrchestrationBot()
    
    await system_bot.initialize()
    await metrics_bot.initialize()
    await calc_bot.initialize()
    await ai_bot.initialize()
    
    ai_bus.register_agent(system_bot)
    ai_bus.register_agent(metrics_bot)
    ai_bus.register_agent(calc_bot)
    ai_bus.register_agent(ai_bot)
    
    ctx = BotContext(
        'admin',
        'collab_demo',
        AccessLevel.ROOT,
        yolo_mode=True
    )
    
    print("=" * 70)
    print("AI-to-AI Collaboration Demo")
    print("Agents: system, metrics, calc, ai")
    print("=" * 70)
    print()
    
    # Scenario 1: Intelligent delegation
    print("📋 Scenario 1: Intelligent Task Delegation")
    print("-" * 70)
    
    tasks = [
        "check system status",
        "what is the capital of France?",
        "multiply 7 times 8",
    ]
    
    for task in tasks:
        print(f"\n💬 Task: '{task}'")
        result = await ai_bus.delegate("user", task, ctx)
        output = result.get("result", result.get("error", "No result"))
        if isinstance(output, str) and len(output) > 150:
            output = output[:150] + "..."
        print(f"✓  {output}")
    
    # Scenario 2: AI orchestrating other agents
    print("\n\n📋 Scenario 2: AI Orchestrating Multiple Agents")
    print("-" * 70)
    print("\n💬 AI delegates to system bot for status...")
    
    result = await ai_bus.send(
        "ai", "system", "status", [], ctx
    )
    print(f"✓  {result.get('result')}")
    
    # Scenario 3: Broadcast
    print("\n\n📋 Scenario 3: Broadcast Query to All Agents")
    print("-" * 70)
    print("\n💬 Broadcasting 'status' command to all agents...")
    
    results = await ai_bus.broadcast("user", "status", [], ctx)
    for agent_name, result in results.items():
        output = result.get("result", result.get("error", "No response"))
        if isinstance(output, str) and len(output) > 80:
            output = output[:80] + "..."
        print(f"  {agent_name:10} → {output}")
    
    # Scenario 4: Chain of delegation
    print("\n\n📋 Scenario 4: Chain of Delegation")
    print("-" * 70)
    print("\n💬 AI uses delegate to route complex query...")
    
    result = await ai_bot.execute(
        "delegate",
        ["explain", "quantum", "computing"],
        ctx
    )
    output = result.get("result", result.get("error"))
    if isinstance(output, str) and len(output) > 200:
        output = output[:200] + "..."
    print(f"✓  {output}")
    
    # Show communication history
    print("\n\n📋 Communication History")
    print("-" * 70)
    history = ai_bus.get_history(limit=10)
    for msg in history:
        print(
            f"  {msg.sender:10} → {msg.receiver:10} : "
            f"{msg.task} {msg.args[:3] if msg.args else ''}"
        )
    
    print("\n" + "=" * 70)
    print("✓ AI-to-AI collaboration complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(demo())

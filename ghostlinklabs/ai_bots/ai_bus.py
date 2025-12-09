#!/usr/bin/env python3
"""
AI-to-AI Communication System
Enables bots to delegate tasks and collaborate
"""
import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ai_bots.core import AIBot, BotContext


@dataclass
class AIMessage:
    """Message passed between AI agents"""
    sender: str
    receiver: str
    task: str
    args: List[str]
    context: BotContext
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class AIBus:
    """Message bus for AI-to-AI communication"""
    
    def __init__(self):
        self.agents: Dict[str, AIBot] = {}
        self.message_queue: List[AIMessage] = []
        self.message_history: List[AIMessage] = []
        
    def register_agent(self, agent: AIBot):
        """Register an AI agent on the bus"""
        self.agents[agent.name] = agent
        
    def unregister_agent(self, name: str):
        """Unregister an agent"""
        if name in self.agents:
            del self.agents[name]
            
    async def send(
        self,
        sender: str,
        receiver: str,
        task: str,
        args: List[str],
        context: BotContext,
        priority: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a message from one AI to another"""
        message = AIMessage(
            sender=sender,
            receiver=receiver,
            task=task,
            args=args,
            context=context,
            priority=priority,
            metadata=metadata or {}
        )
        
        # Log to history
        self.message_history.append(message)
        
        # Route message
        if receiver not in self.agents:
            return {"error": f"Unknown agent: {receiver}"}
            
        agent = self.agents[receiver]
        result = await agent.execute(task, args, context)
        
        return result
        
    async def broadcast(
        self,
        sender: str,
        task: str,
        args: List[str],
        context: BotContext
    ) -> Dict[str, Dict[str, Any]]:
        """Broadcast message to all agents"""
        results = {}
        
        for name, agent in self.agents.items():
            if name == sender:
                continue
            result = await agent.execute(task, args, context)
            results[name] = result
            
        return results
        
    async def delegate(
        self,
        sender: str,
        task_description: str,
        context: BotContext
    ) -> Dict[str, Any]:
        """
        Intelligent delegation - route task to best agent
        Uses simple heuristics to pick the right agent
        """
        # Task routing heuristics
        task_lower = task_description.lower()
        
        # System operations
        if any(
            kw in task_lower
            for kw in ["status", "restart", "exec", "log", "system"]
        ):
            return await self.send(
                sender, "system", "status", [], context
            )
            
        # Metrics/monitoring
        if any(kw in task_lower for kw in ["metric", "monitor", "cpu", "memory"]):  # noqa: E501
            return await self.send(
                sender, "metrics", "get", [], context
            )
            
        # Math/calculation
        if any(
            kw in task_lower
            for kw in ["calculate", "add", "multiply", "math", "+", "*"]
        ):
            # Extract numbers if present
            words = task_description.split()
            return await self.send(
                sender, "calc", "add", words, context
            )
            
        # AI queries (everything else)
        if "ai" in self.agents:
            return await self.send(
                sender,
                "ai",
                "ask",
                [task_description],
                context
            )
            
        return {"error": "No suitable agent found for task"}
        
    def get_history(
        self,
        sender: Optional[str] = None,
        receiver: Optional[str] = None,
        limit: int = 10
    ) -> List[AIMessage]:
        """Get message history with optional filtering"""
        filtered = self.message_history
        
        if sender:
            filtered = [m for m in filtered if m.sender == sender]
        if receiver:
            filtered = [m for m in filtered if m.receiver == receiver]
            
        return filtered[-limit:]


# Global AI bus instance
ai_bus = AIBus()


if __name__ == "__main__":
    async def test():
        from ai_bots.core import SystemBot, MetricsBot, AccessLevel
        from ai_bots.plugins.calculator import CalculatorBot
        from ai_bots.plugins.ai_orchestration import AIOrchestrationBot
        
        # Setup
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
            user_id="test",
            session_id="demo",
            access_level=AccessLevel.ROOT,
            yolo_mode=True
        )
        
        print("AI-to-AI Communication Demo")
        print("=" * 60)
        
        # Test delegation
        tasks = [
            "check system status",
            "calculate 5 + 10",
            "what is docker?",
        ]
        
        for task in tasks:
            print(f"\nTask: {task}")
            print("-" * 60)
            result = await ai_bus.delegate("test", task, ctx)
            output = result.get("result", result.get("error", "No result"))
            print(output[:200] if len(str(output)) > 200 else output)
            
        # Show history
        print("\n\nMessage History:")
        print("-" * 60)
        for msg in ai_bus.get_history(limit=5):
            print(f"{msg.sender} → {msg.receiver}: {msg.task}")
            
    asyncio.run(test())

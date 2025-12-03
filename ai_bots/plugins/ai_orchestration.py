#!/usr/bin/env python3
"""
AI Orchestration Bot
Routes requests to free AI APIs and Copilot oracle
"""
import asyncio
import os
from typing import List

try:
    import httpx
except ImportError:
    httpx = None

from ai_bots.core import AIBot, AccessLevel, BotContext
from ai_bots.introspection import MetacognitiveAgent, ThoughtType
from ai_bots.ai_bus import ai_bus


class AIOrchestrationBot(AIBot):
    """Bot for AI orchestration with free APIs"""
    
    def __init__(self):
        super().__init__("ai", AccessLevel.READ)
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.together_api_key = os.getenv("TOGETHER_API_KEY")
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        
        # Introspection agent
        self.introspection = MetacognitiveAgent(
            name="AIOrchestrationBot",
            groq_api_key=self.groq_api_key,
            verbose=False
        )
        
    async def initialize(self):
        """Register AI commands"""
        self.register_command(
            "ask",
            self.cmd_ask,
            "Ask AI a question: ai ask <prompt>",
            AccessLevel.READ,
            hotkey="ctrl+shift+a",
            aliases=["query", "q"]
        )
        
        self.register_command(
            "oracle",
            self.cmd_oracle,
            "Ask Copilot oracle: ai oracle <question>",
            AccessLevel.READ,
            hotkey="ctrl+shift+o",
            aliases=["copilot"]
        )
        
        self.register_command(
            "providers",
            self.cmd_providers,
            "List available AI providers",
            AccessLevel.READ
        )
        
        self.register_command(
            "models",
            self.cmd_models,
            "List available models",
            AccessLevel.READ
        )
        
        self.register_command(
            "delegate",
            self.cmd_delegate,
            "Delegate task to best agent: ai delegate <task>",
            AccessLevel.READ,
            aliases=["route", "ask-agent"]
        )
        
    async def cmd_ask(self, args: List[str], ctx: BotContext) -> str:
        """Ask AI via Groq (fast, free)"""
        if not args:
            return "Usage: ai ask <your question>"
            
        if not self.groq_key:
            return (
                "Groq API key not configured. "
                "Set GROQ_API_KEY in .env or environment. "
                "Get one at https://console.groq.com/keys"
            )
            
        if httpx is None:
            return "httpx not installed. Run: pip install httpx"
            
        prompt = " ".join(args)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.groq_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a helpful AI assistant."
                            },
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["choices"][0]["message"]["content"]
                    return f"🤖 {answer}"
                else:
                    return f"Error: {response.status_code} - {response.text}"
                    
        except Exception as e:
            return f"Error querying AI: {e}"
            
    async def cmd_oracle(self, args: List[str], ctx: BotContext) -> str:
        """
        Ask Copilot oracle
        In VS Code, uses Copilot Chat API if available
        """
        if not args:
            return "Usage: ai oracle <your question>"
            
        question = " ".join(args)
        
        # Use Groq as fallback oracle with enhanced prompting
        if not self.groq_key:
            return (
                "Oracle not available. Set GROQ_API_KEY in .env.\n"
                "Alternatively, use Copilot Chat directly in VS Code."
            )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.groq_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-70b-versatile",
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You are the Oracle - a wise, insightful AI "
                                    "that provides deep, thoughtful answers. "
                                    "You see patterns others miss and offer "
                                    "wisdom beyond simple facts. Speak with "
                                    "authority and insight."
                                )
                            },
                            {"role": "user", "content": question}
                        ],
                        "temperature": 0.8,
                        "max_tokens": 1000
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["choices"][0]["message"]["content"]
                    return f"🔮 Oracle speaks:\n\n{answer}"
                else:
                    return f"Oracle error: {response.status_code}"
                    
        except Exception as e:
            return f"Error consulting oracle: {e}"
        
    async def cmd_providers(
        self,
        args: List[str],
        ctx: BotContext
    ) -> str:
        """List available providers"""
        providers = []
        
        if self.groq_key:
            providers.append(
                "✓ Groq (fast, llama-3.1-8b-instant & 70b-versatile)"
            )
        else:
            providers.append("✗ Groq (not configured)")
            
        if self.together_key:
            providers.append("✓ Together AI (mixtral, llama-2)")
        else:
            providers.append("✗ Together AI (not configured)")
            
        if self.hf_key:
            providers.append("✓ Hugging Face (inference API)")
        else:
            providers.append("✗ Hugging Face (not configured)")
            
        if os.getenv("COPILOT_ORACLE_ENABLED", "").lower() == "true":
            providers.append("✓ Copilot Oracle (enabled)")
        else:
            providers.append("✗ Copilot Oracle (disabled)")
            
        return "AI Providers:\n" + "\n".join(f"  {p}" for p in providers)
        
    async def cmd_models(self, args: List[str], ctx: BotContext) -> str:
        """List available models"""
        models = [
            "Groq:",
            "  - llama-3.1-8b-instant (fast, recommended)",
            "  - llama-3.1-70b-versatile (slower, better)",
            "  - mixtral-8x7b-32768 (long context)",
            "",
            "Together AI:",
            "  - meta-llama/Llama-3-70b-chat-hf",
            "  - mistralai/Mixtral-8x7B-Instruct-v0.1",
            "",
            "Hugging Face:",
            "  - meta-llama/Meta-Llama-3-8B-Instruct",
            "  - microsoft/phi-2",
            "",
            "Copilot Oracle:",
            "  - Uses your GitHub Copilot subscription",
        ]
        return "\n".join(models)
    
    async def cmd_delegate(
        self,
        args: List[str],
        ctx: BotContext
    ) -> str:
        """Delegate task to best agent via AI bus"""
        if not args:
            return "Usage: ai delegate <task description>"
        
        from ai_bots.ai_bus import ai_bus
        
        task = " ".join(args)
        result = await ai_bus.delegate("ai", task, ctx)
        
        if "error" in result:
            return f"❌ {result['error']}"
        
        return result.get("result", "Task delegated")


if __name__ == "__main__":
    async def test():
        bot = AIOrchestrationBot()
        await bot.initialize()
        
        ctx = BotContext(
            user_id="test",
            session_id="demo",
            access_level=AccessLevel.ROOT
        )
        
        print("AI Orchestration Bot Demo")
        print("=" * 50)
        
        # Test providers
        result = await bot.execute("providers", [], ctx)
        print(result.get("result", result.get("error")))
        
    asyncio.run(test())

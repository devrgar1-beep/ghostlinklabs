#!/usr/bin/env python3
"""
GhostLink Groq Integration - Internal Communication AI

Groq provides ultra-fast LLM inference for internal component communication:
- Link <-> Container coordination
- Signal <-> Pressure negotiation
- Autonomous decision-making
- Real-time system orchestration
- Inter-component reasoning
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

# Load environment variables
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / "ghostlink.env")


class GroqClient:
    """
    Internal Communication AI Client

    Groq provides ultra-fast inference for GhostLink's autonomous components
    to communicate, reason, and make decisions in real-time.
    """

    def __init__(self, api_key: Optional[str] = None):
        try:
            from groq import Groq

            self.api_key = api_key or os.getenv("GROQ_API_KEY")
            self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

            if not self.api_key:
                raise ValueError("GROQ_API_KEY not found in environment")

            self.client = Groq(api_key=self.api_key)
        except ImportError:
            raise ImportError("groq package not installed. Run: pip install groq")

    def create_headers(self) -> Dict[str, str]:
        """Create request headers (legacy, not needed with official SDK)"""
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """
        Create a chat completion

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (default from env)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response

        Returns:
            API response dict
        """
        completion = self.client.chat.completions.create(
            model=model or self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
        )

        if stream:
            return completion

        return {
            "id": completion.id,
            "model": completion.model,
            "choices": [
                {
                    "index": choice.index,
                    "message": {"role": choice.message.role, "content": choice.message.content},
                    "finish_reason": choice.finish_reason,
                }
                for choice in completion.choices
            ],
            "usage": {
                "prompt_tokens": completion.usage.prompt_tokens,
                "completion_tokens": completion.usage.completion_tokens,
                "total_tokens": completion.usage.total_tokens,
            },
        }

    def simple_chat(self, prompt: str, system: Optional[str] = None) -> str:
        """
        Simple chat interface

        Args:
            prompt: User prompt
            system: Optional system message

        Returns:
            Assistant response text
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.chat_completion(messages)
        return response["choices"][0]["message"]["content"]

    def internal_communication(
        self, sender: str, receiver: str, message: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Facilitate internal component communication

        Args:
            sender: Source component (e.g., 'Link', 'Container')
            receiver: Target component (e.g., 'Signal', 'Pressure')
            message: Communication payload
            context: Optional system context

        Returns:
            Receiver's response
        """
        system_prompt = f"""
You are the internal communication AI for GhostLink's autonomous system.
You facilitate real-time communication between components.

Current Context:
- Sender: {sender}
- Receiver: {receiver}
{f"- System State: {context}" if context else ""}

Provide concise, actionable responses for component coordination.
"""
        return self.simple_chat(message, system=system_prompt)

    def list_models(self) -> List[Dict[str, Any]]:
        """List available models"""
        models = self.client.models.list()
        return [
            {
                "id": model.id,
                "object": model.object,
                "created": model.created,
                "owned_by": model.owned_by,
            }
            for model in models.data
        ]


def test_groq_connection():
    """Test Groq API connection"""
    try:
        client = GroqClient()
        print("🚀 Testing Groq API Connection...\n")
        if client.api_key:
            print("API Key: [REDACTED] set")
        else:
            print("API Key: not set")
        print(f"Model: {client.model}\n")

        # Test internal communication
        print("Testing internal communication AI...")
        response = client.internal_communication(
            sender="Link",
            receiver="Container",
            message="Request status update and resource allocation for pending tasks",
            context={"active_tasks": 3, "system_load": "moderate"},
        )
        print(f"✅ Response: {response}\n")

        # List models
        print("Listing available models...")
        models = client.list_models()
        print(f"✅ Found {len(models)} models:")
        for model in models[:5]:  # Show first 5
            print(f"  • {model['id']}")

        print("\n🎉 Groq integration successful!")
        return True

    except ImportError as e:
        print(f"❌ Groq package not installed: {e}")
        print("\n📦 Install with: pip install groq")
        return False
    except Exception as e:
        print(f"❌ Groq integration failed: {e}")
        return False


if __name__ == "__main__":
    test_groq_connection()

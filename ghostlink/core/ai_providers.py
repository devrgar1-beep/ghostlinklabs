"""AI Provider Management for GhostLink"""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import requests

from ..utils.config import config


class AIProvider(ABC):
    """Abstract base class for AI providers"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model or self.get_default_model()

    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model for this provider"""
        pass

    @abstractmethod
    async def ask(self, question: str) -> str:
        """Ask a question and get response"""
        pass

    def get_models(self) -> list[str]:
        """Get available models"""
        return [self.model]


class OllamaProvider(AIProvider):
    """Local Ollama provider for running models locally"""

    def __init__(self, api_key: str = None, model: str = None):
        super().__init__(api_key, model)
        self.base_url = config.get("ai.providers.ollama.base_url", "http://localhost:11434")

    def get_default_model(self) -> str:
        return "llama2"  # Default fallback model

    async def ask(self, question: str) -> str:
        """Query local Ollama model"""
        try:
            payload = {"model": self.model, "prompt": question, "stream": False}

            # Run HTTP request in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(f"{self.base_url}/api/generate", json=payload, timeout=60),
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response from local model")
            else:
                raise Exception(f"Local model error: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to Ollama. Is it running? (ollama serve)")
        except Exception as e:
            raise Exception(f"Local model error: {str(e)}")

    def get_models(self) -> list:
        """Get available local models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return [self.model]
        except:
            return [self.model]


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider"""

    def get_default_model(self) -> str:
        return "claude-3-sonnet-20240229"

    async def ask(self, question: str) -> str:
        # Placeholder implementation
        return f"Claude response to: {question}"


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""

    def get_default_model(self) -> str:
        return "gpt-4"

    async def ask(self, question: str) -> str:
        # Placeholder implementation
        return f"GPT response to: {question}"


class GrokProvider(AIProvider):
    """xAI Grok provider"""

    def get_default_model(self) -> str:
        return "grok-1"

    async def ask(self, question: str) -> str:
        # Placeholder implementation
        return f"Grok response to: {question}"


class GoogleProvider(AIProvider):
    """Google Gemini provider"""

    def get_default_model(self) -> str:
        return "gemini-pro"

    async def ask(self, question: str) -> str:
        # Placeholder implementation
        return f"Gemini response to: {question}"


class AIProviderManager:
    """Manages multiple AI providers with failover"""

    def __init__(self):
        self.providers: Dict[str, Optional[AIProvider]] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all configured providers"""
        provider_configs = {
            "ollama": (OllamaProvider, None),  # Local provider, no API key needed
            "anthropic": (AnthropicProvider, "ai.providers.anthropic.api_key"),
            "openai": (OpenAIProvider, "ai.providers.openai.api_key"),
            "grok": (GrokProvider, "ai.providers.grok.api_key"),
            "google": (GoogleProvider, "ai.providers.google.api_key"),
        }

        for name, (provider_class, key_path) in provider_configs.items():
            if key_path is None:
                # Local provider (like Ollama)
                try:
                    self.providers[name] = provider_class()
                except Exception as e:
                    print(f"Failed to initialize {name}: {e}")
                    self.providers[name] = None
            else:
                # API-based provider
                api_key = config.get(key_path)
                if api_key:
                    try:
                        self.providers[name] = provider_class(api_key)
                    except Exception as e:
                        print(f"Failed to initialize {name}: {e}")
                        self.providers[name] = None
                else:
                    self.providers[name] = None

    async def ask(self, question: str, provider: Optional[str] = None) -> str:
        """Ask a question using specified or default provider with automatic failover"""
        if provider is None:
            provider = config.get("ai.default_provider", "ollama")

        # Try the specified/default provider first
        if provider in self.providers and self.providers[provider] is not None:
            try:
                return await self.providers[provider].ask(question)  # type: ignore
            except Exception as e:
                print(f"Provider {provider} failed: {e}")
                # Continue to fallback logic

        # Try failover to other available providers
        for p_name, p_instance in self.providers.items():
            if p_instance is not None and p_name != provider:
                try:
                    print(f"Trying fallback provider: {p_name}")
                    return await p_instance.ask(question)
                except Exception as e:
                    print(f"Fallback provider {p_name} also failed: {e}")
                    continue

        raise Exception("All AI providers failed. Please check your setup.")

    def get_provider_info(self, provider: str) -> Dict[str, Any]:
        """Get information about a provider"""
        p = self.providers.get(provider)
        if p:
            return {"name": provider, "models": p.get_models(), "status": "available"}
        return {"name": provider, "models": [], "status": "unavailable"}


# Global provider manager
ai_manager = AIProviderManager()

"""Free API Integration for GhostLink"""

import asyncio
from typing import Any, Dict

import requests

from ..core.ai_providers import ai_manager


class FreeAPIIntegration:
    """Integration with free public APIs"""

    def __init__(self):
        self.apis = self._get_api_catalog()

    def _get_api_catalog(self) -> Dict[str, Dict[str, Any]]:
        """Get catalog of available free APIs"""
        return {
            "jokes": {
                "url": "https://official-joke-api.appspot.com/random_joke",
                "description": "Random jokes API",
            },
            "advice": {
                "url": "https://api.adviceslip.com/advice",
                "description": "Random advice API",
            },
            "iss_location": {
                "url": "http://api.open-notify.org/iss-now.json",
                "description": "ISS location API",
            },
            "cat_facts": {"url": "https://catfact.ninja/fact", "description": "Random cat facts"},
            "dog_facts": {
                "url": "https://dog-api.kinduff.com/api/facts",
                "description": "Random dog facts",
            },
            "quotes": {"url": "https://api.quotable.io/random", "description": "Random quotes"},
            "numbers": {
                "url": "http://numbersapi.com/random/trivia",
                "description": "Numbers trivia",
            },
            "bored": {
                "url": "https://www.boredapi.com/api/activity",
                "description": "Random activities",
            },
            "weather": {"url": "https://wttr.in/?format=j1", "description": "Weather information"},
            "crypto": {
                "url": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
                "description": "Bitcoin price",
            },
        }

    async def query_api(self, api_name: str) -> Dict[str, Any]:
        """Query a specific API"""
        if api_name not in self.apis:
            raise ValueError(f"Unknown API: {api_name}")

        api_config = self.apis[api_name]

        try:
            # Run HTTP request in thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: requests.get(api_config["url"], timeout=10)
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "api": api_name}

    async def query_ai_with_api_data(self, question: str, api_data: Dict[str, Any]) -> str:
        """Query AI with API data context"""
        context = f"API Data: {api_data}\nQuestion: {question}"
        return await ai_manager.ask(context)

    def get_available_apis(self) -> Dict[str, str]:
        """Get list of available APIs with descriptions"""
        return {name: config["description"] for name, config in self.apis.items()}


# Global API integration instance
api_integration = FreeAPIIntegration()

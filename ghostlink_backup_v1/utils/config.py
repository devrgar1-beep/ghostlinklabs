"""Centralized Configuration Management for GhostLink"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()


class Config:
    """Centralized configuration management with hierarchical loading"""

    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from multiple sources"""
        # Start with defaults
        self._config = self._get_defaults()

        # Load from YAML file
        yaml_config = self._load_yaml_config()
        if yaml_config:
            self._deep_update(self._config, yaml_config)

        # Override with environment variables
        env_config = self._load_env_config()
        if env_config:
            self._deep_update(self._config, env_config)

    def _get_defaults(self) -> Dict[str, Any]:
        """Get default configuration values"""
        return {
            "system": {
                "name": "GhostLink",
                "version": "1.0.0",
                "debug": False,
            },
            "ai": {
                "default_provider": "ollama",  # Changed to local Ollama
                "timeout": 30,
                "max_retries": 3,
                "temperature": 0.7,
                "providers": {
                    "ollama": {
                        "base_url": "http://localhost:11434",
                        "model": "llama2",
                    }
                },
            },
            "api": {
                "timeout": 10,
                "max_retries": 2,
                "cache_ttl": 300,
            },
            "agent": {
                "max_memory_items": 100,
                "decision_timeout": 60,
                "auto_save": True,
            },
            "logging": {
                "level": "INFO",
                "directory": "logs",
                "filename": "ghostlink.log",
                "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
                "rotation": "10 MB",
                "retention": "1 week",
                "compression": "gz",
            },
            "interface": {
                "default": "cli",
                "theme": "cyberpunk",
            },
        }

    def _load_yaml_config(self) -> Optional[Dict[str, Any]]:
        """Load configuration from YAML file"""
        config_paths = [
            Path("config.yaml"),
            Path("config.yml"),
            Path.home() / ".ghostlink" / "config.yaml",
        ]

        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path) as f:
                        return yaml.safe_load(f)
                except Exception as e:
                    logger.warning(f"Failed to load config from {config_path}: {e}")

        return None

    def _load_env_config(self) -> Optional[Dict[str, Any]]:
        """Load configuration from environment variables"""
        env_mapping = {
            "ANTHROPIC_API_KEY": "ai.providers.anthropic.api_key",
            "OPENAI_API_KEY": "ai.providers.openai.api_key",
            "GROK_API_KEY": "ai.providers.grok.api_key",
            "GOOGLE_API_KEY": "ai.providers.google.api_key",
            "LOG_LEVEL": "logging.level",
            "DEBUG": "system.debug",
        }

        config = {}
        for env_var, config_path in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                self._set_nested(config, config_path.split("."), value)

        return config if config else None

    def _deep_update(self, base: Dict[str, Any], update: Dict[str, Any]):
        """Deep update nested dictionaries"""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value

    def _set_nested(self, config: Dict[str, Any], keys: list, value: Any):
        """Set nested dictionary value"""
        for key in keys[:-1]:
            config = config.setdefault(key, {})
        config[keys[-1]] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key"""
        keys = key.split(".")
        value = self._config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any):
        """Set configuration value by dot-separated key"""
        keys = key.split(".")
        self._set_nested(self._config, keys, value)

    def validate(self) -> bool:
        """Validate configuration - API keys are optional since we have local Ollama"""
        # Check if at least one provider is available
        providers = ["ollama"]  # Local provider is always available
        api_providers = ["anthropic", "openai", "grok", "google"]

        for provider in api_providers:
            key_path = f"ai.providers.{provider}.api_key"
            if self.get(key_path):
                providers.append(provider)

        if not providers:
            logger.error("No AI providers available (neither local Ollama nor API keys)")
            return False

        logger.info(f"Configuration validation passed - Available providers: {providers}")
        return True

    def reload(self):
        """Reload configuration"""
        self._load_config()
        logger.info("Configuration reloaded")


# Global config instance
config = Config()

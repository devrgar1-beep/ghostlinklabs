import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for GhostLink."""
    
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ghostlink.db")
    
    # External API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Security settings
    API_KEY_EXPIRATION_DAYS: int = int(os.getenv("API_KEY_EXPIRATION_DAYS", "365"))
    
    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    # Automation settings
    # When AUTOMATE_ALL is true, components that support automation should
    # run without manual confirmation where safe.
    AUTOMATE_ALL: bool = os.getenv("AUTOMATE_ALL", "true").lower() == "true"

    # If AUTO_APPROVE is true, actions that normally require approval
    # should be auto-approved. Use with caution in production.
    AUTO_APPROVE: bool = os.getenv("AUTO_APPROVE", "true").lower() == "true"

    # Experimental mode level: one of 'off', 'partial', 'full'.
    # 'full' enables all experimental features; 'partial' enables a subset.
    EXPERIMENTAL_MODE: str = os.getenv("EXPERIMENTAL_MODE", "full").lower()

    @classmethod
    def experimental_enabled(cls) -> bool:
        """Return True if experimental features are enabled.

        Use `EXPIRIMENTAL_MODE` to decide the level of feature exposure.
        """
        return cls.EXPERIMENTAL_MODE != "off"
    
    @classmethod
    def get_openai_api_key(cls) -> str:
        """Get OpenAI API key with validation."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI integration")
        return cls.OPENAI_API_KEY
    
    @classmethod
    def validate_required_config(cls) -> None:
        """Validate that all required configuration is present."""
        # Add validation logic here if needed
        pass

# Global config instance
config = Config()
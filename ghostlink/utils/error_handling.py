"""Error Handling Utilities for GhostLink"""

import functools
import traceback
from typing import Any, Callable, Dict

from loguru import logger


class GhostLinkError(Exception):
    """Base exception for GhostLink"""


class APIError(GhostLinkError):
    """API-related errors"""


class ConfigurationError(GhostLinkError):
    """Configuration-related errors"""


class AIProviderError(GhostLinkError):
    """AI provider-related errors"""


class ValidationError(GhostLinkError):
    """Data validation errors"""


def handle_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for comprehensive error handling"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except APIError as e:
            logger.error(f"API Error in {func.__name__}: {e}")
            raise
        except ConfigurationError as e:
            logger.error(f"Configuration Error in {func.__name__}: {e}")
            raise
        except AIProviderError as e:
            logger.error(f"AI Provider Error in {func.__name__}: {e}")
            raise
        except ValidationError as e:
            logger.error(f"Validation Error in {func.__name__}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            raise GhostLinkError(f"Unexpected error: {e}") from e

    return wrapper


def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for retrying operations on failure"""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            delay_val = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} failed, retrying in {delay_val}s: {e}"
                        )
                        import time

                        time.sleep(delay_val)
                        delay_val *= backoff  # Exponential backoff
                    else:
                        logger.error(f"All {max_retries} attempts failed")
            if last_exception:
                raise last_exception
            raise RuntimeError("Retry failed without exception")

        return wrapper

    return decorator


def validate_api_key(api_key: str, provider: str) -> bool:
    """Validate API key format"""
    if not api_key:
        raise ConfigurationError(f"Invalid {provider} API key")

    # Basic format validation
    min_length = 20
    if len(api_key) < min_length:
        raise ConfigurationError(f"{provider} API key too short")

    return True


def validate_input(data: Any, schema: Dict[str, Any]) -> Dict[str, Any]:
    """Validate input data against schema"""
    if not isinstance(data, dict):
        raise ValidationError("Input must be a dictionary")

    validated = {}
    for key, rules in schema.items():
        if key not in data and rules.get("required", False):
            raise ValidationError(f"Missing required field: {key}")

        if key in data:
            value = data[key]
            expected_type = rules.get("type")
            if expected_type and not isinstance(value, expected_type):
                raise ValidationError(f"Field {key} must be of type {expected_type.__name__}")

            min_length = rules.get("min_length")
            if min_length and isinstance(value, str) and len(value) < min_length:
                raise ValidationError(f"Field {key} must be at least {min_length} characters")

            validated[key] = value

    return validated

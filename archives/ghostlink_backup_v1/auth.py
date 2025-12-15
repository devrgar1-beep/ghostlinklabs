from functools import wraps
from typing import Optional
from fastapi import HTTPException, Request
from .database import Database, ApiKey

db = Database()

def get_api_key_from_request(request: Request) -> Optional[str]:
    """Extract API key from X-API-Key header."""
    return request.headers.get("X-API-Key")

def require_api_key(permission: str = "read"):
    """Decorator to require valid API key with specific permission."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Find the request parameter
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            for key, value in kwargs.items():
                if isinstance(value, Request):
                    request = value
                    break
            
            if not request:
                raise HTTPException(status_code=500, detail="Request object not found")
            
            api_key = get_api_key_from_request(request)
            if not api_key:
                raise HTTPException(status_code=401, detail="API key required")
            
            validated_key = db.validate_api_key(api_key, permission)
            if not validated_key:
                raise HTTPException(status_code=403, detail="Invalid or expired API key")
            
            # Add the validated API key to the request for use in endpoints
            request.state.api_key = validated_key
            return func(*args, **kwargs)
        return wrapper
    return decorator

def optional_api_key(permission: str = "read"):
    """Decorator for optional API key authentication."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Find the request parameter
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            for key, value in kwargs.items():
                if isinstance(value, Request):
                    request = value
                    break
            
            if not request:
                raise HTTPException(status_code=500, detail="Request object not found")
            
            api_key = get_api_key_from_request(request)
            validated_key = None
            
            if api_key:
                validated_key = db.validate_api_key(api_key, permission)
                if not validated_key:
                    raise HTTPException(status_code=403, detail="Invalid or expired API key")
            
            # Add the validated API key to the request (None if no key provided)
            request.state.api_key = validated_key
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_api_key_sync(key: str, permission: str = "read") -> Optional[ApiKey]:
    """Synchronous API key validation for direct use."""
    return db.validate_api_key(key, permission)
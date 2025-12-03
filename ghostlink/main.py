import datetime
import json
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel

from .auth import get_api_key_from_request
from .automation import policy
from .config import config
from .database import ApiKey, Database
from .net import backbone
from .reasoning import process_metaphors
from .storage import MockIPFS

app = FastAPI(title="GhostLink")

# Initialize components
_db = None
ipfs = MockIPFS()
items: list[dict] = []


def get_db() -> Database:
    """Get the database instance."""
    global _db
    if _db is None:
        _db = Database()
    return _db


def set_db(database: Database) -> None:
    """Set the database instance (for testing)."""
    global _db
    _db = database


class Item(BaseModel):
    name: str
    value: int


class TextInput(BaseModel):
    text: str


class DataInput(BaseModel):
    data: str


class ApiKeyCreate(BaseModel):
    user_id: str
    permissions: str = "read"
    expires_at: Optional[datetime.datetime] = None


class ApiKeyResponse(BaseModel):
    id: int
    key: str
    user_id: str
    permissions: str
    created_at: datetime.datetime
    expires_at: Optional[datetime.datetime]


# API Key Management Endpoints
@app.post("/api_keys", response_model=ApiKeyResponse)
def create_api_key(api_key_data: ApiKeyCreate, db: Database = Depends(get_db)) -> ApiKeyResponse:
    """Create a new API key. Admin endpoint."""
    created_key = db.create_api_key(
        user_id=api_key_data.user_id,
        permissions=api_key_data.permissions,
        expires_at=api_key_data.expires_at
    )
    return ApiKeyResponse(
        id=created_key.id,
        key=created_key.key,
        user_id=created_key.user_id,
        permissions=created_key.permissions,
        created_at=created_key.created_at,
        expires_at=created_key.expires_at
    )


@app.get("/api_keys/validate")
def validate_api_key(request: Request, db: Database = Depends(get_db)) -> dict:
    """Validate the provided API key."""
    api_key = get_api_key_from_request(request)
    if not api_key:
        raise HTTPException(status_code=400, detail="API key required in X-API-Key header")

    validated_key = db.validate_api_key(api_key, "read")
    if not validated_key:
        raise HTTPException(status_code=403, detail="Invalid or expired API key")

    return {
        "valid": True,
        "user_id": validated_key.user_id,
        "permissions": validated_key.permissions,
        "expires_at": validated_key.expires_at
    }


@app.get("/status")
def get_status() -> dict:
    """Get system status and configuration settings."""
    bb = backbone.get_backbone()
    return {
        "service": "GhostLink",
        "status": "running",
        "automation": {
            "automate_all": policy.automate_all(),
            "auto_approve": policy.auto_approve(),
            "experimental_mode": policy.experimental_level(),
            "experimental_enabled": policy.experimental_enabled(),
        },
        "backbone": {
            "class": bb.backbone_class.value,
            "primary_interface": bb.primary_iface,
            "linked_servers": len(bb.servers),
        },
        "config": {
            "debug": config.DEBUG,
            "database_url": config.DATABASE_URL.split("///")[-1] if "///" in config.DATABASE_URL else "configured",
        },
    }


@app.get("/backbone")
def get_backbone_info() -> dict:
    """Get backbone network topology and linked servers."""
    bb = backbone.get_backbone()
    return bb.get_topology()


@app.post("/backbone/link")
def link_to_backbone() -> dict:
    """Link this server to the backbone network."""
    result = backbone.link_local_server(api_port=8000)
    return result


@app.get("/backbone/discover")
def discover_peers() -> dict:
    """Discover other GhostLink nodes on the backbone."""
    bb = backbone.get_backbone()
    peers = bb.discover_peers(port=8000)
    return {
        "discovered": len(peers),
        "peers": peers,
    }


# Helper functions for authentication
def validate_optional_api_key(request: Request, db: Database, permission: str = "read") -> Optional[ApiKey]:
    """Helper to validate optional API key."""
    api_key = get_api_key_from_request(request)
    if api_key:
        validated_key = db.validate_api_key(api_key, permission)
        if not validated_key:
            raise HTTPException(status_code=403, detail="Invalid or expired API key")
        return validated_key
    return None


def require_valid_api_key(request: Request, db: Database, permission: str = "read") -> ApiKey:
    """Helper to require valid API key."""
    api_key = get_api_key_from_request(request)
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")

    validated_key = db.validate_api_key(api_key, permission)
    if not validated_key:
        raise HTTPException(status_code=403, detail="Invalid or expired API key")

    return validated_key


# Updated existing endpoints with optional API key authentication
@app.post("/items")
def create_item(request: Request, item: Item, db: Database = Depends(get_db)) -> dict:
    api_key = validate_optional_api_key(request, db, "write")

    data = item.model_dump()  # Fixed deprecation warning
    data_str = json.dumps(data)
    data_hash = ipfs.store(data_str)
    stored = {**data, "hash": data_hash}

    # Add API key info if present
    if api_key:
        stored["created_by"] = api_key.user_id

    items.append(stored)
    return stored


@app.get("/items")
def get_items(request: Request, db: Database = Depends(get_db)) -> list[dict]:
    validate_optional_api_key(request, db, "read")
    # Could filter based on API key permissions in the future
    return items


@app.post("/reasoning/")
def reasoning_endpoint(request: Request, text: TextInput, db: Database = Depends(get_db)) -> dict:
    validate_optional_api_key(request, db, "read")
    processed = process_metaphors(text.text)
    return {"processed": processed}


@app.post("/ipfs/store")
def ipfs_store(request: Request, data: DataInput, db: Database = Depends(get_db)) -> dict:
    api_key = validate_optional_api_key(request, db, "write")

    cid = ipfs.store(data.data)
    result = {"cid": cid}

    # Add API key info if present
    if api_key:
        result["stored_by"] = api_key.user_id

    return result


@app.get("/ipfs/{data_hash}")
def ipfs_get(request: Request, data_hash: str, db: Database = Depends(get_db)) -> dict:
    validate_optional_api_key(request, db, "read")

    data = ipfs.retrieve(data_hash)
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"data": data}


# Secured external API endpoint (requires API key)
@app.get("/external_api/data")
def external_api_data(request: Request, db: Database = Depends(get_db)) -> dict:
    """External API endpoint that requires valid API key authentication."""
    api_key = require_valid_api_key(request, db, "read")

    # Return filtered data based on API key permissions
    return {
        "message": "Secured data access",
        "user_id": api_key.user_id,
        "permissions": api_key.permissions,
        "items_count": len(items),
        "data": items if api_key.has_permission("admin") else [item for item in items if not item.get("sensitive", False)]
    }

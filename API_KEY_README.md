# GhostLink API Key Implementation

This document describes the API key functionality added to the GhostLink system.

## Overview

The GhostLink API now supports secure API key authentication with permission-based access control. This enables:

- **Secure external integrations** - Third-party systems can access GhostLink APIs using API keys
- **User tracking** - Actions are logged with the user who performed them
- **Permission-based access control** - Different API keys can have different permission levels
- **Protected endpoints** - Some endpoints require API key authentication

## Features Implemented

### ✅ Core Components

1. **Database Layer** (`ghostlink/database.py`)
   - SQLAlchemy-based `ApiKey` model
   - Secure token generation using `secrets.token_urlsafe(32)`
   - Permission checking and expiration support
   - Database operations for CRUD operations

2. **Authentication Layer** (`ghostlink/auth.py`)
   - Header-based authentication using `X-API-Key`
   - Optional vs required API key decorators
   - Permission validation

3. **Configuration Management** (`ghostlink/config.py`)
   - Environment variable support via `.env` files
   - External API key management (e.g., OpenAI)
   - Database configuration

### ✅ API Endpoints

#### API Key Management
- `POST /api_keys` - Create new API keys
- `GET /api_keys/validate` - Validate API keys

#### Protected Endpoints
- `GET /external_api/data` - Requires API key authentication

#### Enhanced Existing Endpoints
All original endpoints now support optional API key authentication:
- `POST /items` - Create items (tracks creator if API key provided)
- `GET /items` - List items 
- `POST /reasoning/` - Process text
- `POST /ipfs/store` - Store data (tracks creator if API key provided)
- `GET /ipfs/{hash}` - Retrieve data

### ✅ Permission System

Three permission levels are supported:
- **read** - Can access read-only endpoints
- **write** - Can access read and write endpoints  
- **admin** - Can access all endpoints including sensitive data

### ✅ Security Features

- **Secure token generation** - Uses cryptographically secure random tokens
- **Permission-based access** - Granular control over what each key can access
- **Expiration support** - Keys can have optional expiration dates
- **Header-based authentication** - Standard `X-API-Key` header format

## Usage Examples

### Creating API Keys

```bash
# Create a read-only API key
curl -X POST "http://localhost:8000/api_keys" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "external_app", "permissions": "read"}'

# Create an admin API key with expiration
curl -X POST "http://localhost:8000/api_keys" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "admin_user", "permissions": "read,write,admin", "expires_at": "2024-12-31T23:59:59"}'
```

### Using API Keys

```bash
# Access protected endpoint
curl -X GET "http://localhost:8000/external_api/data" \
     -H "X-API-Key: your-api-key-here"

# Create item with API key (will track creator)
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-api-key-here" \
     -d '{"name": "test item", "value": 42}'
```

### Validating API Keys

```bash
curl -X GET "http://localhost:8000/api_keys/validate" \
     -H "X-API-Key: your-api-key-here"
```

## Configuration

### Environment Variables

Create a `.env` file (see `.env.example`):

```env
# Database Configuration
DATABASE_URL=sqlite:///./ghostlink.db

# External API Keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# Security Settings
API_KEY_EXPIRATION_DAYS=365

# Application Settings
DEBUG=false
```

### Database Setup

The database tables are automatically created when the application starts. The `api_keys` table stores:

- `id` - Unique identifier
- `key` - The API key token
- `user_id` - User/system that owns the key
- `permissions` - Comma-separated permission list
- `created_at` - Creation timestamp
- `expires_at` - Optional expiration timestamp

## Running the Application

### Development Server

```bash
pip install fastapi uvicorn sqlalchemy python-dotenv
uvicorn ghostlink.main:app --reload
```

### Demo Script

Run the included demonstration:

```bash
python demo_api_keys.py
```

This will demonstrate all API key functionality including:
- Creating keys with different permissions
- Validating keys
- Using keys for authentication
- Permission-based access control

## Testing

The original tests continue to pass, ensuring backward compatibility:

```bash
pytest tests/test_app.py -v
```

Database functionality can be tested directly:

```bash
python -c "
from ghostlink.database import Database
db = Database('sqlite:///:memory:')
key = db.create_api_key('test_user', 'read,write')
print('Created key:', key.key)
print('Valid:', db.validate_api_key(key.key, 'read') is not None)
"
```

## Implementation Notes

### Backward Compatibility

All existing functionality continues to work without API keys. The API key system is additive and optional for most endpoints.

### Security Considerations

- API keys are stored as plain text in the database (consider hashing for production)
- Use HTTPS in production to protect API keys in transit
- Regularly rotate API keys
- Use minimal required permissions for each key

### Performance

- Database queries are optimized for key validation
- Keys are validated once per request
- Minimal overhead for endpoints that don't require authentication

## Future Enhancements

Potential improvements that could be added:

- API key hashing for security
- Rate limiting per API key
- Key usage analytics and logging
- Web UI for key management
- Key rotation functionality
- Webhook integration for key events

## Error Handling

The API provides clear error messages:

- `401 Unauthorized` - API key required but not provided
- `403 Forbidden` - Invalid or expired API key
- `400 Bad Request` - Malformed request

All errors include descriptive detail messages to aid in debugging.
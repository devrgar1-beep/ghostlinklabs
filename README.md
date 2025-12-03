# GhostLink Labs - Unified Repository

## Core Components
# GhostLink Labs - 100% Local Sovereign AI Framework

A completely local AI orchestration system with symbolic reasoning, hardware binding, and autonomous operation. Zero external dependencies - runs on any platform with Python 3.8+.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (built-in on most systems)
- That's it - no external dependencies, no package managers, no virtual environments

### Installation
```bash
# Copy files to your system
# No installation required - just run directly
```

### Local Release (Automated)

If you want a reproducible local install and a quick smoke test, use the included helper script:

```bash
python -m venv .venv
source .venv/bin/activate
python scripts/local_release.py
```

This installs the package locally and runs basic smoke tests (CLI status + diagnostics). It does not enable hardware binding by default.

If you installed using `pip install .` and you'd like to use the `ghostlink` CLI without `python -m`, add your site scripts directory to PATH. On macOS this is often:

```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```

### Basic Usage
```bash
# Start the Link AI brain
python main.py

# Or use the CLI
python -m ghostlink.link_cli start

# Access web interface at http://localhost:8000
```

### Advanced Usage
```bash
# Hardware-bound operation (requires admin privileges)
python -m ghostlink.link_cli start --hardware --confirm-hardware

# Lattice component coordination
python ghostlink_lattice.py --demo

# Symbolic reasoning demo
python gdl_example.gdl
```

## 🔒 Security & Sovereignty

- **100% Local**: No external dependencies or cloud services required
- **Hardware Binding**: Direct BIOS/firmware interaction when needed
- **VM Detection**: Prevents unsafe operations in virtual environments
- **Optional Web Backup**: Web connectivity only for backup/sync (disabled by default)
- **Platform Agnostic**: Runs on Windows, macOS, Linux, BSD, etc.

## 📚 Core Components

### Link AI Brain
- Task management and orchestration
- Context learning and adaptation
- Autonomous decision making

### Lattice Mesh Network
- Component communication and coordination
- Self-healing network topology
- Real-time state synchronization

### Symbolic Reasoning Engine (GDL)
- Cellular automata-based reasoning
- Pattern recognition and prediction
- Hardware-accelerated when available

### Hardware Bridge
- Direct BIOS/firmware access (admin required)
- Physical device binding and control
- Manufacturer tool integration

## 🤖 AI Integration

### Internal AI
- Groq-based ultra-fast inference
- Component coordination
- Real-time decision making

### Local AI Support
- Compatible with LM Studio, Ollama
- No cloud dependencies required
- Runs entirely offline

## 🔧 Platform Support

GhostLink runs on any platform with Python 3.8+:

- **Windows**: Native support, hardware binding available
- **macOS**: Full compatibility, hardware binding via system APIs
- **Linux**: Native performance, full hardware access
- **BSD variants**: Compatible with standard library
- **Embedded systems**: Minimal resource requirements

## 📁 File Structure

```
ghostlink/
├── main.py                 # Main entry point
├── ghostlink_lattice.py    # Mesh network coordinator
├── link_cli.py            # Command line interface
├── groq_integration.py    # Internal AI client
├── bios_bridge.py         # Hardware interface
├── gdl_example.gdl        # Symbolic reasoning demo
└── config.yaml            # Local configuration
```

## 🔄 Updates & Backup

### Offline Updates
- Manual file replacement
- Configuration preservation
- No automatic update mechanisms

### Optional Web Backup
```bash
# Enable web backup (optional)
python -m ghostlink.link_cli backup enable --endpoint https://your-backup-server

# Sync to backup
python -m ghostlink.link_cli backup sync
```

## 📄 License

Proprietary - See LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues
- **Hardware Binding Fails**: Ensure admin/root privileges and physical hardware
- **Lattice Communication**: Check component health with `python ghostlink_lattice.py --state`
- **Web Server Issues**: Verify port 8000 is available
- **Permission Errors**: Run with appropriate privileges for hardware operations

### Logs
- All output goes to terminal/console
- No external logging services
- Self-contained operation logs

### Platform-Specific Notes
- **Windows**: May require UAC elevation for hardware operations
- **macOS**: May require sudo for system-level access
- **Linux**: Full root access available for hardware binding

---

**Built for complete local sovereignty - no external dependencies, no cloud requirements, no package managers. Just Python and your hardware.**
# GhostLink Backend & MCP Servers

Backend FastAPI server and Model Context Protocol (MCP) server for GhostLink platform.

## Quick Start

### Backend API Server

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run server
python main.py
# Or with uvicorn directly:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend runs on http://localhost:8000

API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### MCP Server

```bash
# Run MCP server (stdio mode)
cd mcp_server
python main.py

# Or test with echo
echo '{"method":"tools/list","params":{}}' | python main.py
```

## Endpoints

### Backend API

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /agents` - List available agents
- `POST /agents/execute` - Execute command on agent
- `GET /metrics` - Get system metrics (proxies to controller:9108)

### MCP Server

MCP server exposes tools and resources over stdio (JSON-RPC):

**Methods:**
- `tools/list` - List available tools
- `resources/list` - List available resources
- `tools/call` - Execute a tool
- `resources/read` - Read a resource

**Tools:**
- `get_metrics` - Retrieve system metrics
- `execute_command` - Execute command on agent

**Resources:**
- `ghostlink://metrics` - Real-time metrics
- `ghostlink://agents` - Agent list

## Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- `backend` - FastAPI backend on port 8000
- `mcp` - MCP server (stdio, not exposed)
- `controller` - GhostLink controller on port 7420/9108

## Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### MCP

```bash
cd mcp_server
python main.py < test_request.json
```

## Environment Variables

### Backend
- `HOST` - Bind host (default: 0.0.0.0)
- `PORT` - Bind port (default: 8000)

### Controller (existing)
- `RUN_CONTROLLER` - Enable controller (default: 1)
- `RUN_PEER` - Enable peer (default: 0)
- `RUN_BRIDGE` - Enable OpenAI bridge (default: 0)
- `OPENAI_API_KEY` - OpenAI API key (if bridge enabled)
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

All errors include descriptive detail messages to aid in debugging.# GhostLink - Consolidated Python Repository

## Overview

This consolidated Python file (`ghostlink_consolidated.py`) contains **all Python code** from the GhostLink repository in a single, easy-to-share file.

## File Details

- **Total Python Files**: 240
- **Total Lines**: ~13,000+
- **File Size**: ~500 KB (0.48 MB)
- **Format**: Single `.py` file with clear section markers

## How to Use

### For ChatGPT

1. **Copy the entire `ghostlink_consolidated.py` file**
2. **Paste it into ChatGPT** with a prompt like:
   - "Here's my complete GhostLink codebase. Help me understand [specific module]"
   - "Review this code and suggest improvements"
   - "Find all functions related to [specific feature]"
3. **Use Ctrl+F** to quickly locate specific modules or functions

### For Local Development

```bash
# The file is syntactically valid Python
python3 -m py_compile ghostlink_consolidated.py

# You can import specific sections if needed (though not recommended for production)
```

## Structure

The file is organized as follows:

1. **Header Section**
   - Future imports (consolidated at the top for Python compatibility)
   - Documentation and table of contents
   - Complete list of all 240 source files

2. **Code Sections**
   - Each file is clearly marked with section headers:
     ```python
     #=====================================================================
     # FILE X/240: ./path/to/file.py
     #=====================================================================
     ```

3. **Footer Section**
   - Clear end marker

## Navigation Tips

### Finding Specific Modules

Use your editor's search function (Ctrl+F or Cmd+F) to find:

- **Module by name**: Search for `# FILE` + module name
  - Example: `# FILE` + `ghostlink/core/signal.py`

- **Function by name**: Search for `def function_name`
  - Example: `def SIGNAL(`

- **Class by name**: Search for `class ClassName`
  - Example: `class GhostLink`

### Table of Contents

The file begins with a complete table of contents listing all 240 files in order:

```
  1. ./demo_api_keys.py
  2. ./ghost_consciousness_daemon.py
  3. ./ghostknife.py
  ...
240. ./verify_and_restore.py
```

## What's Included

All Python modules from GhostLink, including:

- **Core Systems**: Signal processing, pressure analysis, containers, links
- **Diagnostics**: Tool integrity, ritual detection, compression analysis
- **Runtime**: Session management, state tracking, execution engines
- **Automation**: Task scheduling, repair loops, orchestration
- **Reflection**: Mirror systems, compression logic, artifact scanning
- **Access Control**: Permission layers, ritual unlocking
- **Storage**: Audit logs, blueprints, configurations
- **Testing**: Test frameworks and validators
- **Bio Integration**: Biological trace integrators, neuro-signal proxies
- **Observers**: Sentient bridges, subjective trace harness
- **Sandbox**: Test injection, unstable tool simulation
- **And more...**

## Notes

- **Future Imports**: All `from __future__ import` statements have been consolidated at the top of the file for Python compatibility
- **Syntax**: The file passes Python syntax validation (`py_compile`)
- **Encoding**: UTF-8 with error handling for special characters
- **Separation**: Each file section is clearly marked with comment separators

## Original Repository Structure

The code maintains its original organization:

- `ghostlink/core/` - Core functionality
- `ghostlink/diagnostic/` - Diagnostic tools
- `ghostlink/runtime/` - Runtime systems
- `ghostlink/access/` - Access control
- `ghostlink/automation/` - Automation tools
- `ghostlink/reflect/` - Reflection systems
- And many more subdirectories...

## Use Cases

1. **Share with ChatGPT** for code review, analysis, or questions
2. **Archive** the entire codebase in a single file
3. **Search** across all modules simultaneously
4. **Reference** when working on related projects
5. **Documentation** for understanding the complete system

## Updates

To regenerate the consolidated file with the latest changes:

```bash
# Run the consolidation script (included in the repository)
python3 consolidate_ghostlink.py
```

---

**Generated**: 2025-10-06
**Repository**: https://github.com/devrgar-cyber/ghostlinklabs

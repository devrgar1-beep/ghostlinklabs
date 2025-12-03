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

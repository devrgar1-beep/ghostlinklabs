# GhostLink Phase 5 - API, Dashboard, and Containerization

## Overview
This phase adds a simple FastAPI backend, a small dashboard UI, and Dockerization to run the evolution engine as a service.

## Run locally (optional manual install)
> Note: Docker-based deployment is the recommended and primary setup. Local installs are kept for development convenience.

1. Install dependencies (recommended in a venv):

```bash
# Optional local install for development only
python3 -m pip install -r requirements/api.txt --user
```

2. Start the API server (dev mode - local):

```bash
cd /path/to/projects/ghostlinklabs
python3 -m uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload
```

3. Open the dashboard (static file - local):

```bash
cd ui/dashboard
python3 -m http.server 3000 --bind 127.0.0.1
# Visit http://localhost:3000/index.html
```

4. Use the VS Code extension to call commands, or run `ghost_vscode_integration.py` directly for CLI commands.

## Docker-first (recommended)
1. Ensure Docker and Docker Compose are installed
2. From the repository root, run:

```bash
# Build and start the stack
./scripts/run_docker.sh

# Stop the stack
cd docker && docker compose down
```

This launches:
- Evolution API: http://localhost:8000
- Dashboard: http://localhost:3000

## Run via Docker Compose
1. Ensure Docker and Docker Compose are installed
2. From `docker`, run:

```bash
docker-compose up --build -d
```

3. Access the API at `http://localhost:8000` and the dashboard at `http://localhost:3000` (if served).

## Tests
Install `pytest` and run tests:

```bash
python3 -m pip install pytest --user
pytest -q tests/test_api.py
```

## Notes
- The API provides endpoints:
  - `GET /status` - get evolution status
  - `POST /evolve` - trigger a single evolution generation
  - `POST /start-loop` - start background cycles
  - `POST /stop-loop` - stop background cycles

- The VS Code extension includes a new command `GhostLink: API Status` to query the API directly.

## Next Steps
- Create a real React dashboard and integrate authentication
- Improve containerization for monitoring, metrics and persistence
- Add CI/CD to build Docker images and run tests automatically

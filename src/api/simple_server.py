#!/usr/bin/env python3
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path

# Ensure src root on path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Robust src path discovery: try common locations and fall back to walking parents
candidate_paths = [
    PROJECT_ROOT,
    PROJECT_ROOT / "projects" / "ghostlinklabs",
    PROJECT_ROOT / "projects" / "ghostlinklabs" / "src",
    PROJECT_ROOT / "src",
]


def add_path(p: Path):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)


for p in candidate_paths:
    add_path(p)

# Last resort: search upwards for a folder containing evolutionary_intelligence.py
try:
    for parent in [PROJECT_ROOT] + list(PROJECT_ROOT.parents):
        maybe = parent / "src" / "evolutionary_intelligence.py"
        if maybe.exists():
            add_path(parent / "src")
            break
except Exception:
    pass

try:
    # Prefer absolute package import if available
    from src.evolutionary_intelligence import EvolutionaryIntelligence
except Exception:
    from evolutionary_intelligence import EvolutionaryIntelligence

WORKSPACE_PATH = (
    "/Users/ghostlinklabs/Library/Mobile Documents/com~apple~CloudDocs/projects/ghostlinklabs"
)
ei = EvolutionaryIntelligence(workspace_path=WORKSPACE_PATH)

# Micro-cache for status to reduce repeated computation overhead
_STATUS_CACHE = {"value": None, "ts": 0.0}
_STATUS_TTL = 0.3  # seconds


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/status":
            data = ei.get_evolution_status()
            self._send_json(data)
        elif parsed.path == "/status_fast":
            import time

            now = time.time()
            if _STATUS_CACHE["value"] is None or (now - _STATUS_CACHE["ts"]) > _STATUS_TTL:
                _STATUS_CACHE["value"] = ei.get_evolution_status()
                _STATUS_CACHE["ts"] = now
            self._send_json({"cached": True, "ttl": _STATUS_TTL, "status": _STATUS_CACHE["value"]})
        else:
            self._send_json({"error": "not found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/evolve":
            # Run evolution synchronously
            import asyncio

            ok = asyncio.run(ei.evolve_generation())
            data = {"success": ok, "status": ei.get_evolution_status()}
            self._send_json(data, status=200 if ok else 500)
        else:
            self._send_json({"error": "not found"}, status=404)

    def log_message(self, format, *args):
        # Reduce noise
        pass


if __name__ == "__main__":
    import os

    host = os.environ.get("HOST", "127.0.0.1")
    try:
        port = int(os.environ.get("PORT", "8000"))
    except ValueError:
        port = 8000
    httpd = HTTPServer((host, port), Handler)
    print(f"🚀 Simple Evolution API running on http://{host}:{port}")
    print("Endpoints: GET /status, GET /status_fast, POST /evolve")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  Stopping server")

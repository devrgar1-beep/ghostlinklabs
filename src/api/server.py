from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from pathlib import Path
from typing import Dict
import sys

# Ensure the parent src is in sys.path so src modules import properly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Initialize logging
logging.getLogger("uvicorn.error")

# Import the EvolutionaryIntelligence class
from evolutionary_intelligence import EvolutionaryIntelligence

# Default workspace path used across the project
WORKSPACE_PATH = (
    "/Users/ghostlinklabs/Library/Mobile Documents/com~apple~CloudDocs/projects/ghostlinklabs"
)

app = FastAPI(title="GhostLink Evolution API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the Evolutionary Intelligence instance
ei = EvolutionaryIntelligence(workspace_path=WORKSPACE_PATH)

background_task_running = False


@app.get("/status")
async def get_status() -> Dict:
    """Return the current evolution status."""
    return ei.get_evolution_status()


@app.post("/evolve")
async def trigger_evolution(background_tasks: BackgroundTasks) -> Dict:
    """Trigger a single autonomous evolution generation."""
    # Run evolve_generation and return status
    success = await ei.evolve_generation()
    return {"success": success, "status": ei.get_evolution_status()}


async def continuous_loop(max_cycles: int = 0, delay_seconds: int = 1):
    global background_task_running
    if background_task_running:
        return
    background_task_running = True
    cycle_count = 0
    while max_cycles == 0 or cycle_count < max_cycles:
        cycle_count += 1
        try:
            await ei.evolve_generation()
            await asyncio.sleep(delay_seconds)
        except Exception as e:
            logging.exception("Background evolution failed: %s", e)
            break
    background_task_running = False


@app.post("/start-loop")
async def start_loop(background_tasks: BackgroundTasks, max_cycles: int = 0):
    """Start continuous background evolution loop (max_cycles=0 -> unlimited)."""
    background_tasks.add_task(continuous_loop, max_cycles, 1)
    return {"started": True, "max_cycles": max_cycles}


@app.post("/stop-loop")
async def stop_loop() -> Dict:
    """Stop the background loop by setting a flag via the global variable."""
    global background_task_running
    background_task_running = False
    return {"stopped": True}


@app.on_event("startup")
async def startup_event():
    # Ensure workspace path exists
    Path(WORKSPACE_PATH).mkdir(parents=True, exist_ok=True)
    # Optionally start a background loop with a small warm-up
    # background_tasks.add_task(continuous_loop, 0, 5)  # disabled by default
    logging.info("GhostLink Evolution API started")

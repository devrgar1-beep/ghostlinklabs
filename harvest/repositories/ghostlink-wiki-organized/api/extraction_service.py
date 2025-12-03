#!/usr/bin/env python3
"""
GhostLink Extraction Service
Backend service for managing wiki extraction jobs with process management.
Designed to run on Mac Mini backend server.
"""

import asyncio
from datetime import datetime
import json
import logging
import os
from pathlib import Path
import signal
import sys
from typing import Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
import psutil
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="GhostLink Extraction Service")

# Global state
EXTRACTION_STATE = {
    "running": False,
    "pid": None,
    "start_time": None,
    "last_update": None,
    "progress": {},
    "error": None
}

LOCK_FILE = Path.home() / "ghostlink-wiki-trace" / ".extraction.lock"
STATUS_FILE = Path.home() / "ghostlink-wiki-trace" / "extraction_status.json"


class ExtractionRequest(BaseModel):
    """Request to start extraction"""
    batches: Optional[str] = None
    max_results: int = 150
    force: bool = False


class ExtractionStatus(BaseModel):
    """Current extraction status"""
    running: bool
    pid: Optional[int]
    start_time: Optional[str]
    duration_seconds: Optional[float]
    progress: dict
    error: Optional[str]


def is_extraction_running() -> bool:
    """Check if extraction process is actually running"""
    if not LOCK_FILE.exists():
        return False
    
    try:
        lock_data = json.loads(LOCK_FILE.read_text())
        pid = lock_data.get("pid")
        
        if pid and psutil.pid_exists(pid):
            try:
                proc = psutil.Process(pid)
                # Check if it's actually our extraction script
                if "extraction_script.py" in " ".join(proc.cmdline()):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Stale lock file
        LOCK_FILE.unlink()
        return False
    except Exception as e:
        logger.error(f"Error checking lock file: {e}")
        return False


def acquire_lock() -> bool:
    """Acquire extraction lock"""
    if is_extraction_running():
        return False
    
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    lock_data = {
        "pid": os.getpid(),
        "start_time": datetime.utcnow().isoformat(),
        "hostname": os.uname().nodename
    }
    
    LOCK_FILE.write_text(json.dumps(lock_data, indent=2))
    return True


def release_lock():
    """Release extraction lock"""
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()


def save_status():
    """Save current status to file"""
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATUS_FILE.write_text(json.dumps(EXTRACTION_STATE, indent=2, default=str))


async def run_extraction(batches: Optional[str], max_results: int):
    """Run extraction script as subprocess with monitoring"""
    script_path = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Desktop/Desktop - Ghost's MacBook Pro/ghostlinklabs-main/wiki-extraction/extraction_script.py"
    
    if not script_path.exists():
        raise FileNotFoundError(f"Extraction script not found: {script_path}")
    
    # Build command
    cmd = [sys.executable, str(script_path), "--max-results", str(max_results)]
    if batches:
        cmd.extend(["--batches", batches])
    
    logger.info(f"Starting extraction: {' '.join(cmd)}")
    
    # Start process
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    EXTRACTION_STATE["running"] = True
    EXTRACTION_STATE["pid"] = process.pid
    EXTRACTION_STATE["start_time"] = datetime.utcnow().isoformat()
    EXTRACTION_STATE["error"] = None
    save_status()
    
    try:
        # Monitor process
        stdout, stderr = await process.communicate()
        
        EXTRACTION_STATE["running"] = False
        EXTRACTION_STATE["pid"] = None
        
        if process.returncode == 0:
            logger.info("Extraction completed successfully")
            EXTRACTION_STATE["progress"]["status"] = "completed"
        else:
            error_msg = stderr.decode() if stderr else "Unknown error"
            logger.error(f"Extraction failed: {error_msg}")
            EXTRACTION_STATE["error"] = error_msg
            EXTRACTION_STATE["progress"]["status"] = "failed"
        
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        EXTRACTION_STATE["running"] = False
        EXTRACTION_STATE["pid"] = None
        EXTRACTION_STATE["error"] = str(e)
        EXTRACTION_STATE["progress"]["status"] = "error"
    
    finally:
        release_lock()
        save_status()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "extraction", "timestamp": datetime.utcnow().isoformat()}


@app.get("/status", response_model=ExtractionStatus)
async def get_status():
    """Get current extraction status"""
    # Verify running state
    if EXTRACTION_STATE["running"]:
        if not is_extraction_running():
            EXTRACTION_STATE["running"] = False
            EXTRACTION_STATE["pid"] = None
            save_status()
    
    duration = None
    if EXTRACTION_STATE["start_time"] and EXTRACTION_STATE["running"]:
        start = datetime.fromisoformat(EXTRACTION_STATE["start_time"])
        duration = (datetime.utcnow() - start).total_seconds()
    
    return ExtractionStatus(
        running=EXTRACTION_STATE["running"],
        pid=EXTRACTION_STATE["pid"],
        start_time=EXTRACTION_STATE["start_time"],
        duration_seconds=duration,
        progress=EXTRACTION_STATE["progress"],
        error=EXTRACTION_STATE["error"]
    )


@app.post("/extract")
async def start_extraction(request: ExtractionRequest, background_tasks: BackgroundTasks):
    """Start extraction job"""
    # Check if already running
    if EXTRACTION_STATE["running"] or is_extraction_running():
        if not request.force:
            raise HTTPException(
                status_code=409,
                detail="Extraction already running. Use force=true to override."
            )
        else:
            # Kill existing process
            if EXTRACTION_STATE["pid"]:
                try:
                    os.kill(EXTRACTION_STATE["pid"], signal.SIGTERM)
                    await asyncio.sleep(2)
                except ProcessLookupError:
                    pass
            release_lock()
    
    # Acquire lock
    if not acquire_lock():
        raise HTTPException(
            status_code=423,
            detail="Could not acquire extraction lock"
        )
    
    # Start extraction in background
    background_tasks.add_task(
        run_extraction,
        batches=request.batches,
        max_results=request.max_results
    )
    
    return {
        "status": "started",
        "message": "Extraction job started",
        "batches": request.batches,
        "max_results": request.max_results
    }


@app.post("/stop")
async def stop_extraction():
    """Stop running extraction"""
    if not EXTRACTION_STATE["running"]:
        raise HTTPException(status_code=404, detail="No extraction running")
    
    if EXTRACTION_STATE["pid"]:
        try:
            os.kill(EXTRACTION_STATE["pid"], signal.SIGTERM)
            EXTRACTION_STATE["running"] = False
            EXTRACTION_STATE["pid"] = None
            EXTRACTION_STATE["progress"]["status"] = "stopped"
            save_status()
            release_lock()
            
            return {"status": "stopped", "message": "Extraction stopped"}
        except ProcessLookupError:
            raise HTTPException(status_code=404, detail="Process not found")
        except PermissionError:
            raise HTTPException(status_code=403, detail="Permission denied")
    
    raise HTTPException(status_code=500, detail="No PID available")


@app.on_event("startup")
async def startup_event():
    """Initialize service on startup"""
    logger.info("GhostLink Extraction Service starting...")
    
    # Clean up stale locks
    if LOCK_FILE.exists() and not is_extraction_running():
        logger.info("Cleaning up stale lock file")
        release_lock()
    
    # Load last status if exists
    if STATUS_FILE.exists():
        try:
            saved_state = json.loads(STATUS_FILE.read_text())
            # Only restore if process is still running
            if saved_state.get("pid") and psutil.pid_exists(saved_state["pid"]):
                EXTRACTION_STATE.update(saved_state)
                logger.info(f"Restored extraction state: PID {saved_state['pid']}")
        except Exception as e:
            logger.error(f"Error loading saved state: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("GhostLink Extraction Service shutting down...")
    save_status()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )

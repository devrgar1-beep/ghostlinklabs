#!/usr/bin/env python3
"""
GhostLink Main Application
Sovereign Computing System - Container Entry Point
"""

import os
import sys
import json
import signal
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# GhostLink Core Imports
from .core.controller import GhostLinkController
from .neural.neural_node import NeuralNode
from .wired.wired_core import WiredCore
from .bridge.bridge_service import BridgeService
from .security.sovereignty_gate import SovereigntyGate
from .utils.config_manager import ConfigManager
from .utils.logger import setup_logging

# Configuration Models
@dataclass
class GhostLinkConfig:
    mode: str = "controller"
    host: str = "0.0.0.0"
    port: int = 8080
    data_path: str = "/data"
    neural_mode: str = "offline_local"
    sovereignty_gate: str = "closed"
    log_level: str = "INFO"

class HealthResponse(BaseModel):
    status: str
    mode: str
    version: str
    uptime: float
    components: Dict[str, str]

class SystemStatus(BaseModel):
    controller: str
    neural: str
    wired: str
    bridge: str
    sovereignty_gate: str

# Global application state
app_state = {
    "controller": None,
    "neural": None,
    "wired": None,
    "bridge": None,
    "sovereignty_gate": None,
    "start_time": None
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    app_state["start_time"] = asyncio.get_event_loop().time()
    logger = logging.getLogger("ghostlink.main")
    
    try:
        logger.info("Starting GhostLink components...")
        await initialize_components()
        logger.info("GhostLink components initialized successfully")
        yield
    finally:
        # Shutdown
        logger.info("Shutting down GhostLink components...")
        await shutdown_components()
        logger.info("GhostLink shutdown complete")

# FastAPI application
app = FastAPI(
    title="GhostLink Sovereign Computing System",
    description="Autonomous AI system with sovereignty controls",
    version="7.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def initialize_components():
    """Initialize GhostLink components based on mode"""
    config = load_config()
    
    # Initialize sovereignty gate first
    app_state["sovereignty_gate"] = SovereigntyGate(
        mode=config.sovereignty_gate,
        data_path=config.data_path
    )
    
    # Initialize components based on mode
    if config.mode in ["controller", "all"]:
        app_state["controller"] = GhostLinkController(config)
        await app_state["controller"].start()
    
    if config.mode in ["neural", "all"]:
        app_state["neural"] = NeuralNode(config)
        await app_state["neural"].start()
    
    if config.mode in ["wired", "all"]:
        app_state["wired"] = WiredCore(config)
        await app_state["wired"].start()
    
    if config.mode in ["bridge", "all"]:
        app_state["bridge"] = BridgeService(config)
        await app_state["bridge"].start()

async def shutdown_components():
    """Shutdown all components gracefully"""
    for component_name, component in app_state.items():
        if component and hasattr(component, 'stop'):
            try:
                await component.stop()
            except Exception as e:
                logging.error(f"Error stopping {component_name}: {e}")

def load_config() -> GhostLinkConfig:
    """Load configuration from environment and files"""
    config = GhostLinkConfig()
    
    # Override from environment variables
    config.mode = os.getenv("GHOSTLINK_MODE", config.mode)
    config.host = os.getenv("GHOSTLINK_CONTROLLER_HOST", config.host)
    config.port = int(os.getenv("GHOSTLINK_CONTROLLER_PORT", config.port))
    config.data_path = os.getenv("GHOSTLINK_DATA", config.data_path)
    config.neural_mode = os.getenv("NEURAL_MODE", config.neural_mode)
    config.sovereignty_gate = os.getenv("SOVEREIGNTY_GATE", config.sovereignty_gate)
    config.log_level = os.getenv("LOG_LEVEL", config.log_level)
    
    return config

def get_sovereignty_gate():
    """Dependency to get sovereignty gate"""
    if not app_state["sovereignty_gate"]:
        raise HTTPException(status_code=503, detail="Sovereignty gate not initialized")
    return app_state["sovereignty_gate"]

# API Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = asyncio.get_event_loop().time() - app_state["start_time"] if app_state["start_time"] else 0
    
    components = {}
    for name, component in app_state.items():
        if component and name != "start_time":
            if hasattr(component, "health_check"):
                components[name] = await component.health_check()
            else:
                components[name] = "running"
        elif name != "start_time":
            components[name] = "disabled"
    
    return HealthResponse(
        status="healthy",
        mode=os.getenv("GHOSTLINK_MODE", "controller"),
        version="7.0.0",
        uptime=uptime,
        components=components
    )

@app.get("/status", response_model=SystemStatus)
async def system_status():
    """Get detailed system status"""
    return SystemStatus(
        controller="running" if app_state["controller"] else "disabled",
        neural="running" if app_state["neural"] else "disabled",
        wired="running" if app_state["wired"] else "disabled",
        bridge="running" if app_state["bridge"] else "disabled",
        sovereignty_gate="active" if app_state["sovereignty_gate"] else "disabled"
    )

@app.post("/sovereignty/check")
async def sovereignty_check(
    action: str,
    context: Dict[str, Any],
    gate: SovereigntyGate = Depends(get_sovereignty_gate)
):
    """Check action against sovereignty gate"""
    result = await gate.check_action(action, context)
    return {"allowed": result.allowed, "reason": result.reason}

@app.post("/neural/process")
async def neural_process(
    input_data: Dict[str, Any],
    gate: SovereigntyGate = Depends(get_sovereignty_gate)
):
    """Process data through neural node"""
    if not app_state["neural"]:
        raise HTTPException(status_code=404, detail="Neural node not available")
    
    # Check sovereignty
    check_result = await gate.check_action("neural_process", input_data)
    if not check_result.allowed:
        raise HTTPException(status_code=403, detail=check_result.reason)
    
    result = await app_state["neural"].process(input_data)
    return result

@app.post("/wired/command")
async def wired_command(
    command: str,
    params: Dict[str, Any],
    gate: SovereigntyGate = Depends(get_sovereignty_gate)
):
    """Execute command through wired core"""
    if not app_state["wired"]:
        raise HTTPException(status_code=404, detail="Wired core not available")
    
    # Check sovereignty
    context = {"command": command, "params": params}
    check_result = await gate.check_action("wired_command", context)
    if not check_result.allowed:
        raise HTTPException(status_code=403, detail=check_result.reason)
    
    result = await app_state["wired"].execute_command(command, params)
    return result

@app.get("/bridge/status")
async def bridge_status():
    """Get bridge service status"""
    if not app_state["bridge"]:
        raise HTTPException(status_code=404, detail="Bridge service not available")
    
    return await app_state["bridge"].get_status()

# Signal handlers
def handle_signal(signum, frame):
    """Handle shutdown signals"""
    logging.info(f"Received signal {signum}, initiating shutdown...")
    sys.exit(0)

def main():
    """Main entry point"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger("ghostlink.main")
    
    # Load configuration
    config = load_config()
    
    # Setup signal handlers
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    
    logger.info(f"Starting GhostLink in {config.mode} mode")
    logger.info(f"Sovereignty gate: {config.sovereignty_gate}")
    logger.info(f"Neural mode: {config.neural_mode}")
    
    # Run the application
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level=config.log_level.lower(),
        access_log=True
    )

if __name__ == "__main__":
    main()
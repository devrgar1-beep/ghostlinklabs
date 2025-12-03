#!/usr/bin/env python3
"""
GhostLink Backend API Server
FastAPI-based REST API for GhostLink services
"""
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="GhostLink Backend API",
    description="Backend services for GhostLink platform",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models


class HealthResponse(BaseModel):
    status: str
    version: str


class AgentRequest(BaseModel):
    agent_id: str
    command: str
    parameters: Optional[dict] = None


class AgentResponse(BaseModel):
    agent_id: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None


# Routes


@app.get("/")
async def root():
    return {"message": "GhostLink Backend API", "status": "running"}


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", version="0.1.0")


@app.get("/agents")
async def list_agents():
    """List all available agents"""
    return {
        "agents": [
            {"id": "controller", "type": "metrics", "status": "active"},
            {"id": "peer", "type": "sensor", "status": "standby"},
            {"id": "bridge", "type": "ai", "status": "inactive"}
        ]
    }


@app.post("/agents/execute", response_model=AgentResponse)
async def execute_agent(request: AgentRequest):
    """Execute command on specified agent"""
    # Placeholder implementation
    if not request.agent_id:
        raise HTTPException(status_code=400, detail="agent_id required")
    
    return AgentResponse(
        agent_id=request.agent_id,
        status="completed",
        result={
            "message": (
                f"Command '{request.command}' "
                f"executed on {request.agent_id}"
            )
        }
    )


@app.get("/metrics")
async def get_metrics():
    """Get system metrics (proxies to controller on 9108)"""
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://127.0.0.1:9108/metrics",
                timeout=2.0
            )
            return {"metrics": response.text, "status": "ok"}
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        return {"metrics": None, "status": "unavailable", "error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port, log_level="info")

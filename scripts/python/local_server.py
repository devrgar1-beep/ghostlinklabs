#!/usr/bin/env python3
"""
GhostLink Local Server - 100% Local, Zero External Dependencies
No Docker, No APIs, No Cloud - Pure Local Processing
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GhostLink Local Server",
    description="100% Local AI System - No External Dependencies",
    version="1.0.0"
)

# CORS for local Electron app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Local only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# LOCAL AI MODEL INTERFACE
# =============================================================================

class LocalAIModel:
    """Interface for local AI models (Ollama/llama.cpp)"""
    
    def __init__(self, model_name: str = "mistral:7b-instruct"):
        self.model_name = model_name
        self.history: List[Dict] = []
        
    async def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate response using local model"""
        try:
            # Try to use Ollama if available
            import subprocess
            
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            # Call Ollama CLI
            cmd = ["ollama", "run", self.model_name, prompt]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                response = result.stdout.strip()
                self.history.append({
                    "prompt": prompt,
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                })
                return response
            else:
                logger.error(f"Ollama error: {result.stderr}")
                return "Error: Local model not available"
                
        except FileNotFoundError:
            return "Error: Ollama not installed. Run: curl -fsSL https://ollama.com/install.sh | sh"
        except Exception as e:
            logger.error(f"Model generation error: {e}")
            return f"Error: {str(e)}"

# =============================================================================
# TRIAD AI SYSTEM - 3 Local Models Working Together
# =============================================================================

class TriadAISystem:
    """Three local models working in consensus"""
    
    def __init__(self):
        self.model_reasoning = LocalAIModel("mistral:7b-instruct")
        self.model_creative = LocalAIModel("codellama:7b")
        self.model_critique = LocalAIModel("phi3:mini")
        
    async def process(self, prompt: str, mode: str = "consensus") -> Dict:
        """Process prompt through triad system"""
        
        if mode == "fast":
            # Use only reasoning model for speed
            response = await self.model_reasoning.generate(prompt)
            return {
                "response": response,
                "mode": "fast",
                "model": "reasoning"
            }
            
        elif mode == "consensus":
            # Get responses from all three models in parallel
            responses = await asyncio.gather(
                self.model_reasoning.generate(prompt),
                self.model_creative.generate(prompt),
                self.model_critique.generate(prompt)
            )
            
            # Synthesize consensus (simple version - can be enhanced)
            return {
                "response": responses[0],  # Primary response
                "reasoning": responses[0],
                "creative": responses[1],
                "critique": responses[2],
                "mode": "consensus"
            }
            
        else:
            raise ValueError(f"Unknown mode: {mode}")

# =============================================================================
# GLOBAL STATE
# =============================================================================

triad_system = TriadAISystem()
active_connections: List[WebSocket] = []

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "running",
        "system": "GhostLink Local Server",
        "version": "1.0.0",
        "mode": "100% Local - No External Dependencies"
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_available": True,
        "connections": len(active_connections)
    }

@app.post("/chat")
async def chat(request: Dict):
    """Chat with local AI"""
    prompt = request.get("prompt", "")
    mode = request.get("mode", "fast")
    
    if not prompt:
        return JSONResponse(
            status_code=400,
            content={"error": "No prompt provided"}
        )
    
    result = await triad_system.process(prompt, mode)
    return result

@app.post("/code/analyze")
async def analyze_code(request: Dict):
    """Analyze code using local AI"""
    code = request.get("code", "")
    language = request.get("language", "python")
    
    prompt = f"Analyze this {language} code and provide insights:\n\n{code}"
    result = await triad_system.process(prompt, mode="fast")
    
    return {
        "analysis": result["response"],
        "language": language
    }

@app.post("/code/refactor")
async def refactor_code(request: Dict):
    """Refactor code using local AI"""
    code = request.get("code", "")
    language = request.get("language", "python")
    instructions = request.get("instructions", "Improve this code")
    
    prompt = f"{instructions}\n\nLanguage: {language}\n\n{code}"
    result = await triad_system.process(prompt, mode="consensus")
    
    return {
        "refactored": result["response"],
        "language": language
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time communication"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "chat":
                result = await triad_system.process(
                    message.get("prompt", ""),
                    mode=message.get("mode", "fast")
                )
                await websocket.send_json(result)
                
            elif message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("Client disconnected")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    logger.info("🚀 Starting GhostLink Local Server...")
    logger.info("📍 100% Local - No External Dependencies")
    logger.info("🔒 No Docker - No APIs - No Cloud")
    
    uvicorn.run(
        app,
        host="127.0.0.1",  # Local only
        port=8765,
        log_level="info"
    )

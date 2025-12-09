#!/usr/bin/env python3
"""
GhostLink Chromium Integration Service
Provides headless browser automation via Puppeteer/Playwright
"""

import base64
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="GhostLink Chromium Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BrowserState:
    def __init__(self):
        self.browser = None
        self.page = None
        self.is_running = False

browser_state = BrowserState()

class NavigationRequest(BaseModel):
    url: str

class ScriptExecutionRequest(BaseModel):
    script: str

@app.on_event("startup")
async def startup_event():
    """Initialize the browser service"""
    logger.info("GhostLink Chromium Service starting up")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up browser resources"""
    await cleanup_browser()
    logger.info("GhostLink Chromium Service shutting down")

async def init_browser():
    """Initialize Puppeteer browser"""
    try:
        from pyppeteer import launch

        browser_state.browser = await launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--single-process',
                '--disable-gpu'
            ]
        )
        browser_state.page = await browser_state.browser.newPage()
        browser_state.is_running = True
        logger.info("Browser initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize browser: {e}")
        return False

async def cleanup_browser():
    """Clean up browser resources"""
    try:
        if browser_state.page:
            await browser_state.page.close()
            browser_state.page = None

        if browser_state.browser:
            await browser_state.browser.close()
            browser_state.browser = None

        browser_state.is_running = False
        logger.info("Browser cleanup completed")
    except Exception as e:
        logger.error(f"Error during browser cleanup: {e}")

@app.post("/api/chromium/start")
async def start_browser():
    """Start the headless browser"""
    if browser_state.is_running:
        return {"status": "already_running", "message": "Browser is already running"}

    success = await init_browser()
    if success:
        return {"status": "started", "message": "Browser started successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to start browser")

@app.post("/api/chromium/stop")
async def stop_browser():
    """Stop the headless browser"""
    if not browser_state.is_running:
        return {"status": "not_running", "message": "Browser is not running"}

    await cleanup_browser()
    return {"status": "stopped", "message": "Browser stopped successfully"}

@app.post("/api/chromium/navigate")
async def navigate_to_url(request: NavigationRequest):
    """Navigate to a URL"""
    if not browser_state.is_running or not browser_state.page:
        raise HTTPException(status_code=400, detail="Browser is not running")

    try:
        await browser_state.page.goto(request.url, {'waitUntil': 'networkidle0', 'timeout': 30000})

        # Get page title
        title = await browser_state.page.title()

        # Take a screenshot
        screenshot_data = await browser_state.page.screenshot({'type': 'png', 'fullPage': False})
        screenshot_b64 = base64.b64encode(screenshot_data).decode('utf-8')

        return {
            "status": "navigated",
            "url": request.url,
            "title": title,
            "screenshot": screenshot_b64
        }
    except Exception as e:
        logger.error(f"Navigation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to navigate: {str(e)}")

@app.post("/api/chromium/screenshot")
async def take_screenshot():
    """Take a screenshot of the current page"""
    if not browser_state.is_running or not browser_state.page:
        raise HTTPException(status_code=400, detail="Browser is not running")

    try:
        screenshot_data = await browser_state.page.screenshot({'type': 'png', 'fullPage': True})
        screenshot_b64 = base64.b64encode(screenshot_data).decode('utf-8')

        return {
            "status": "screenshot_taken",
            "screenshot": screenshot_b64
        }
    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to take screenshot: {str(e)}")

@app.post("/api/chromium/execute")
async def execute_script(request: ScriptExecutionRequest):
    """Execute JavaScript in the browser context"""
    if not browser_state.is_running or not browser_state.page:
        raise HTTPException(status_code=400, detail="Browser is not running")

    try:
        # Execute the script and capture the result
        result = await browser_state.page.evaluate(request.script)

        return {
            "status": "executed",
            "result": str(result)
        }
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Script execution failed: {str(e)}")

@app.get("/api/chromium/status")
async def get_browser_status():
    """Get the current browser status"""
    return {
        "is_running": browser_state.is_running,
        "current_url": await browser_state.page.url() if browser_state.page else None,
        "title": await browser_state.page.title() if browser_state.page else None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chromium-integration"}

if __name__ == "__main__":
    uvicorn.run(
        "chromium_service:app",
        host="0.0.0.0",
        port=8081,
        reload=True,
        log_level="info"
    )
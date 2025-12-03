#!/usr/bin/env python3
"""Simple test script for GhostLink API"""

import uvicorn

from ghostlink.main import app

if __name__ == "__main__":
    print("Starting GhostLink API server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

#!/usr/bin/env python3
"""Minimal test for SovereignApp"""

import os
import sys

# Add the ghostlink module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ghostlink.sovereign_deps import SovereignApp

app = SovereignApp(title="Test")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/test")
def test():
    return {"status": "ok"}

#!/usr/bin/env python3
"""Minimal test for FastAPI"""

from fastapi import FastAPI

app = FastAPI(title="Test")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/test")
def test():
    return {"status": "ok"}

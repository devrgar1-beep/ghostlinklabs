#!/usr/bin/env python3
"""Debug test for GhostLink API"""

from fastapi import FastAPI

app = FastAPI(title="Debug")


@app.get("/")
def root():
    return {"message": "Debug server running"}


@app.get("/test")
def test():
    return {"status": "ok", "data": []}


# Try importing GhostLink components
try:
    from ghostlink.reasoning import process_metaphors
    from ghostlink.storage import MockIPFS

    ipfs = MockIPFS()

    @app.get("/debug")
    def debug():
        # Test basic functionality
        data = "test"
        hash_val = ipfs.store(data)
        retrieved = ipfs.retrieve(hash_val)
        processed = process_metaphors("life is a journey")

        return {
            "ipfs_store": hash_val,
            "ipfs_retrieve": retrieved,
            "reasoning": processed,
            "status": "components working",
        }

except ImportError:

    @app.get("/debug")
    def debug():
        return {"error": str(e), "status": "import failed"}

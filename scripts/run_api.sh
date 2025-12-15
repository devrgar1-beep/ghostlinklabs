#!/bin/bash
set -e

# Run the API with uvicorn
python3 -m uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload

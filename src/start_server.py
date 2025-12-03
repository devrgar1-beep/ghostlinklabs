import sys
sys.path.insert(0, '/home/ghost/Projects/ghostlinklabs')

from ghostlink.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
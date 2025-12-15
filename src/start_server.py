import os
import sys

# Add the ghostlink module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ghostlink.main import app
from ghostlink.sovereign_deps import SovereignASGIServer

if __name__ == "__main__":
    server = SovereignASGIServer(app, host="0.0.0.0", port=8000)
    server.run()

#!/usr/bin/env python3
"""
Test script for GhostLink API Server
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main function
from ghostlink_api_server_enhanced import main

if __name__ == "__main__":
    # Run with default arguments
    sys.argv = ['ghostlink_api_server_enhanced.py', '--port', '3000']
    main()
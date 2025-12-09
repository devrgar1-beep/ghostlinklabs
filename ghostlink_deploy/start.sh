#!/bin/bash

echo "Initializing GhostLink Production Environment..."
echo "----------------------------------------------"

# Check for Python 3
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
else
    echo "❌ Python 3 not found. Aborting."
    exit 1
fi

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Execute Main Kernel
echo "🚀 Launching Kernel..."
$PYTHON_CMD "$DIR/main.py"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "----------------------------------------------"
    echo "✅ GhostLink Session Ended Successfully."
else
    echo "----------------------------------------------"
    echo "❌ GhostLink Session Failed (Code: $EXIT_CODE)."
fi

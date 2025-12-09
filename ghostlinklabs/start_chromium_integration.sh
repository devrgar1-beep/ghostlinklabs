#!/bin/bash
# GhostLink Chromium Integration Startup Script

echo "🚀 Starting GhostLink Chromium Integration..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Start the Chromium backend service in the background
echo "🔧 Starting Chromium backend service on port 8081..."
cd /Users/ghost-link-labs/ghostlinklabs
python3 chromium_service.py &
BACKEND_PID=$!

# Wait a moment for the backend to start
sleep 3

# Start the React frontend
echo "⚛️  Starting React frontend on port 3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Services started successfully!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8081"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $FRONTEND_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set up signal handler
trap cleanup SIGINT SIGTERM

# Wait for processes
wait
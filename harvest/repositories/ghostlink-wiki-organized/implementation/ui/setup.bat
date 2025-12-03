@echo off
echo Setting up GhostLink Lattice UI...

cd /d "%~dp0"

if not exist node_modules (
    echo Installing dependencies...
    npm install
) else (
    echo Dependencies already installed.
)

echo Starting development server...
npm run dev
@echo off
REM GhostLink Local AI Setup Script for Windows
REM This script helps you install and run Ollama for local AI models

echo 🤖 GhostLink Local AI Setup
echo ===========================
echo.

REM Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing Ollama...
    echo.

    REM Download and install Ollama for Windows
    echo Downloading Ollama installer...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://ollama.ai/download/OllamaSetup.exe' -OutFile 'OllamaSetup.exe'}"

    if exist OllamaSetup.exe (
        echo Running Ollama installer...
        echo Please complete the installation, then press any key to continue...
        pause >nul
        del OllamaSetup.exe
    ) else (
        echo ❌ Failed to download Ollama. Please install manually from: https://ollama.ai
        exit /b 1
    )
) else (
    echo ✅ Ollama is already installed
)

echo.
echo 🚀 Starting Ollama service...

REM Start Ollama service
start /B ollama serve > ollama.log 2>&1
timeout /t 3 /nobreak >nul

REM Check if Ollama is running
powershell -Command "& {try { $response = Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -TimeoutSec 5; exit 0 } catch { exit 1 }}" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama is running!
) else (
    echo ❌ Ollama failed to start. Check ollama.log for details.
    exit /b 1
)

echo.
echo 📥 Pulling default model (llama2)...
ollama pull llama2

echo.
echo 🎉 Setup complete! You can now use GhostLink with local AI models.
echo.
echo Try it out:
echo   python main.py ask "Hello local AI!"
echo.
echo Other available commands:
echo   python main.py --terminal-90s    (Launch cyberpunk interface)
echo   python main.py status           (Check system status)
echo   python main.py providers        (List AI providers)
echo.
echo To install more models:
echo   ollama pull mistral             (Fast and capable)
echo   ollama pull codellama          (Code-focused model)
echo   ollama pull llama2:13b         (Larger, more capable model)
echo.
pause
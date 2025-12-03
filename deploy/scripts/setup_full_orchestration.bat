@echo off
REM GhostLink Full Agent Orchestration Setup Script (Windows)
REM Automates installation of all dependencies, monitoring, and services

setlocal enabledelayedexpansion

REM Check for help first
if "%1"=="--help" goto :show_help

REM Configuration
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "LOG_FILE=%PROJECT_ROOT%\setup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log"
set "LOG_FILE=%LOG_FILE: =0%"

REM Colors (using color codes)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Logging functions
:log
echo %GREEN%[%date% %time%] %~1%NC%
echo [%date% %time%] %~1 >> "%LOG_FILE%"
goto :eof

:error
echo %RED%[ERROR] %~1%NC%
echo [ERROR] %~1 >> "%LOG_FILE%"
goto :eof

:warn
echo %YELLOW%[WARN] %~1%NC%
echo [WARN] %~1 >> "%LOG_FILE%"
goto :eof

:info
echo %BLUE%[INFO] %~1%NC%
echo [INFO] %~1 >> "%LOG_FILE%"
goto :eof

REM Check if winget is available (preferred on Windows)
:check_winget
where winget >nul 2>nul
if %errorlevel% equ 0 (
    call :info "Using winget for package management"
    set "PACKAGE_MANAGER=winget"
    goto :eof
)

REM Fallback to Chocolatey
where choco >nul 2>nul
if %errorlevel% neq 0 (
    call :warn "Neither winget nor Chocolatey found. Installing Chocolatey..."
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    call refreshenv
)
set "PACKAGE_MANAGER=choco"
call :info "Using Chocolatey for package management"
goto :eof

REM Install system dependencies
:install_system_deps
call :log "Installing system dependencies..."

REM Install packages based on available package manager
if "%PACKAGE_MANAGER%"=="winget" (
    call :info "Installing packages with winget..."
    winget install --id Git.Git --accept-source-agreements --accept-package-agreements
    winget install --id Python.Python.3 --accept-source-agreements --accept-package-agreements
    winget install --id Docker.DockerDesktop --accept-source-agreements --accept-package-agreements
    winget install --id PostgreSQL.PostgreSQL --accept-source-agreements --accept-package-agreements
    winget install --id Redis.Redis --accept-source-agreements --accept-package-agreements
    winget install --id Microsoft.VisualStudioCode --accept-source-agreements --accept-package-agreements
    winget install --id LMStudio.LMStudio --accept-source-agreements --accept-package-agreements
) else (
    call :info "Installing packages with Chocolatey..."
    choco install -y git python3 docker-desktop postgresql redis-64 vscode lmstudio
)

REM Install Python packages that might need compilation
pip install --upgrade pip setuptools wheel

REM Install Docker Compose if not present
docker-compose version >nul 2>nul
if %errorlevel% neq 0 (
    if "%PACKAGE_MANAGER%"=="winget" (
        winget install --id Docker.DockerCompose --accept-source-agreements --accept-package-agreements
    ) else (
        choco install -y docker-compose
    )
)

call :log "System dependencies installed successfully"
goto :eof

REM Setup Python virtual environment
:setup_python_env
call :log "Setting up Python virtual environment..."

cd "%PROJECT_ROOT%"

REM Create virtual environment
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip setuptools wheel

REM Install Python dependencies
if exist pyproject.toml (
    pip install -e .
) else if exist requirements.txt (
    pip install -r requirements.txt
) else (
    pip install fastapi uvicorn redis sqlalchemy psycopg2-binary
)

REM Install development dependencies
pip install -e .[dev,test,docs] 2>nul || call :warn "Development dependencies not available"

call :log "Python environment setup complete"
goto :eof

REM Setup Docker services
:setup_docker_services
call :log "Setting up Docker services..."

cd "%PROJECT_ROOT%"

REM Create necessary directories
if not exist data mkdir data
if not exist logs mkdir logs
if not exist models mkdir models
if not exist monitoring\grafana\provisioning\datasources mkdir monitoring\grafana\provisioning\datasources
if not exist monitoring\grafana\provisioning\dashboards mkdir monitoring\grafana\provisioning\dashboards

REM Generate environment file if it doesn't exist
if not exist .env (
    echo # GhostLink Environment Configuration > .env
    echo # Copy this file to .env and customize as needed >> .env
    echo. >> .env
    echo # Application Settings >> .env
    echo HOST=0.0.0.0 >> .env
    echo PORT=8000 >> .env
    echo LOG_LEVEL=INFO >> .env
    echo DEBUG=false >> .env
    echo. >> .env
    echo # Database Settings >> .env
    echo DATABASE_URL=sqlite:///./data/ghostlink.db >> .env
    echo POSTGRES_PASSWORD=changeme789 >> .env
    echo. >> .env
    echo # AI Provider API Keys ^(set these to enable providers^) >> .env
    echo OPENAI_API_KEY= >> .env
    echo ANTHROPIC_API_KEY= >> .env
    echo GROK_API_KEY= >> .env
    echo GOOGLE_API_KEY= >> .env
    echo LMSTUDIO_BASE_URL=http://lmstudio:1234 >> .env
    echo. >> .env
    echo # Security Settings >> .env
    echo SECRET_KEY=%random%%random%%random%%random% >> .env
    echo JWT_SECRET_KEY=%random%%random%%random%%random% >> .env
    echo. >> .env
    echo # Monitoring >> .env
    echo GRAFANA_PASSWORD=admin >> .env
    echo PROMETHEUS_RETENTION=200h >> .env
    echo. >> .env
    echo # Redis >> .env
    echo REDIS_URL=redis://redis:6379 >> .env
    call :info "Created .env file. Please edit it with your API keys and settings."
)

REM Pull Docker images
docker-compose pull

call :log "Docker services setup complete"
goto :eof

REM Setup monitoring stack
:setup_monitoring
call :log "Setting up monitoring stack..."

cd "%PROJECT_ROOT%"

REM Create monitoring configuration if not exists
if not exist monitoring\prometheus.yml (
    echo global: > monitoring\prometheus.yml
    echo   scrape_interval: 15s >> monitoring\prometheus.yml
    echo   evaluation_interval: 15s >> monitoring\prometheus.yml
    echo. >> monitoring\prometheus.yml
    echo rule_files: >> monitoring\prometheus.yml
    echo   # - "first_rules.yml" >> monitoring\prometheus.yml
    echo   # - "second_rules.yml" >> monitoring\prometheus.yml
    echo. >> monitoring\prometheus.yml
    echo scrape_configs: >> monitoring\prometheus.yml
    echo   - job_name: 'prometheus' >> monitoring\prometheus.yml
    echo     static_configs: >> monitoring\prometheus.yml
    echo       - targets: ['localhost:9090'] >> monitoring\prometheus.yml
    echo. >> monitoring\prometheus.yml
    echo   - job_name: 'ghostlink' >> monitoring\prometheus.yml
    echo     static_configs: >> monitoring\prometheus.yml
    echo       - targets: ['ghostlink:9108'] >> monitoring\prometheus.yml
    echo     scrape_interval: 5s >> monitoring\prometheus.yml
    echo     metrics_path: '/metrics' >> monitoring\prometheus.yml
    echo. >> monitoring\prometheus.yml
    echo   - job_name: 'redis' >> monitoring\prometheus.yml
    echo     static_configs: >> monitoring\prometheus.yml
    echo       - targets: ['redis:6379'] >> monitoring\prometheus.yml
    echo. >> monitoring\prometheus.yml
    echo   - job_name: 'postgres' >> monitoring\prometheus.yml
    echo     static_configs: >> monitoring\prometheus.yml
    echo       - targets: ['postgres:9187'] >> monitoring\prometheus.yml
    echo. >> monitoring\prometheus.yml
    echo   - job_name: 'ollama' >> monitoring\prometheus.yml
    echo     static_configs: >> monitoring\prometheus.yml
    echo       - targets: ['ollama:11434'] >> monitoring\prometheus.yml
    echo     scrape_interval: 30s >> monitoring\prometheus.yml
    echo. >> monitoring\prometheus.yml
    echo   - job_name: 'node-exporter' >> monitoring\prometheus.yml
    echo     static_configs: >> monitoring\prometheus.yml
    echo       - targets: ['node-exporter:9100'] >> monitoring\prometheus.yml
    echo. >> monitoring\prometheus.yml
    echo   - job_name: 'cadvisor' >> monitoring\prometheus.yml
    echo     static_configs: >> monitoring\prometheus.yml
    echo       - targets: ['cadvisor:8080'] >> monitoring\prometheus.yml
    echo. >> monitoring\prometheus.yml
    echo   - job_name: 'grafana' >> monitoring\prometheus.yml
    echo     static_configs: >> monitoring\prometheus.yml
    echo       - targets: ['grafana:3000'] >> monitoring\prometheus.yml
)

REM Setup Grafana provisioning
if not exist monitoring\grafana\provisioning\datasources\prometheus.yml (
    echo apiVersion: 1 > monitoring\grafana\provisioning\datasources\prometheus.yml
    echo. >> monitoring\grafana\provisioning\datasources\prometheus.yml
    echo datasources: >> monitoring\grafana\provisioning\datasources\prometheus.yml
    echo   - name: Prometheus >> monitoring\grafana\provisioning\datasources\prometheus.yml
    echo     type: prometheus >> monitoring\grafana\provisioning\datasources\prometheus.yml
    echo     access: proxy >> monitoring\grafana\provisioning\datasources\prometheus.yml
    echo     url: http://prometheus:9090 >> monitoring\grafana\provisioning\datasources\prometheus.yml
    echo     isDefault: true >> monitoring\grafana\provisioning\datasources\prometheus.yml
    echo     editable: true >> monitoring\grafana\provisioning\datasources\prometheus.yml
)

if not exist monitoring\grafana\provisioning\dashboards\dashboards.yml (
    echo apiVersion: 1 > monitoring\grafana\provisioning\dashboards\dashboards.yml
    echo. >> monitoring\grafana\provisioning\dashboards\dashboards.yml
    echo providers: >> monitoring\grafana\provisioning\dashboards\dashboards.yml
    echo   - name: 'GhostLink' >> monitoring\grafana\provisioning\dashboards\dashboards.yml
    echo     type: file >> monitoring\grafana\provisioning\dashboards\dashboards.yml
    echo     disableDeletion: false >> monitoring\grafana\provisioning\dashboards\dashboards.yml
    echo     updateIntervalSeconds: 10 >> monitoring\grafana\provisioning\dashboards\dashboards.yml
    echo     allowUiUpdates: true >> monitoring\grafana\provisioning\dashboards\dashboards.yml
    echo     options: >> monitoring\grafana\provisioning\dashboards\dashboards.yml
    echo       path: /etc/grafana/provisioning/dashboards >> monitoring\grafana\provisioning\dashboards\dashboards.yml
)

call :log "Monitoring stack setup complete"
goto :eof

REM Setup LM Studio integration
:setup_lm_studio
call :log "Setting up LM Studio integration..."

call :info "LM Studio is already installed via package manager."
call :info "Setup Instructions:"
echo 1. Launch LM Studio from Start Menu or desktop shortcut
echo 2. Download a model ^(recommended: llama-2-7b-chat or mistral-7b^)
echo 3. Load the model in LM Studio
echo 4. Go to 'Local Server' tab and click 'Start Server'
echo 5. Ensure server is running on port 1234
echo 6. Test with: python test_lmstudio.py

REM Create LM Studio test script if it doesn't exist
if not exist test_lmstudio.py (
    echo #!/usr/bin/env python3 > test_lmstudio.py
    echo """ >> test_lmstudio.py
    echo LM Studio Integration Test Script >> test_lmstudio.py
    echo """ >> test_lmstudio.py
    echo import asyncio >> test_lmstudio.py
    echo import requests >> test_lmstudio.py
    echo from ghostlink.core.ai_providers import LMStudioProvider >> test_lmstudio.py
    echo. >> test_lmstudio.py
    echo async def test_lmstudio^(^): >> test_lmstudio.py
    echo     print^("🔗 Testing LM Studio Connection..."^) >> test_lmstudio.py
    echo     try: >> test_lmstudio.py
    echo         response = requests.get^("http://localhost:1234/v1/models", timeout=5^) >> test_lmstudio.py
    echo         if response.status_code == 200: >> test_lmstudio.py
    echo             print^("✅ LM Studio is running!"^) >> test_lmstudio.py
    echo             provider = LMStudioProvider^(^) >> test_lmstudio.py
    echo             models = provider.get_models^(^) >> test_lmstudio.py
    echo             if models: >> test_lmstudio.py
    echo                 response = await provider.ask^("Hello, test message"^) >> test_lmstudio.py
    echo                 print^("✅ Response: {response[:100]}..."^) >> test_lmstudio.py
    echo         else: >> test_lmstudio.py
    echo             print^("❌ LM Studio not responding"^) >> test_lmstudio.py
    echo     except Exception as e: >> test_lmstudio.py
    echo         print^("❌ Error: {e}"^) >> test_lmstudio.py
    echo. >> test_lmstudio.py
    echo if __name__ == "__main__": >> test_lmstudio.py
    echo     asyncio.run^(test_lmstudio^(^)^) >> test_lmstudio.py
)

call :log "LM Studio integration setup complete"
goto :eof

REM Setup development tools
:setup_dev_tools
call :log "Setting up development tools..."

cd "%PROJECT_ROOT%"

REM Install pre-commit hooks
if exist .pre-commit-config.yaml (
    pip install pre-commit
    pre-commit install
    call :info "Pre-commit hooks installed. Run 'pre-commit run --all-files' to test."
)

REM Setup commitizen for conventional commits
pip install commitizen
call :info "Commitizen installed. Use 'cz commit' for conventional commits."

call :log "Development tools setup complete"
goto :eof

REM Main installation function
:main
call :log "🚀 Starting GhostLink Full Agent Orchestration Setup (Windows)"
call :log "Log file: %LOG_FILE%"

REM Check package managers
call :check_winget

REM Parse command line arguments
set "MONITORING=false"
set "LM_STUDIO=false"
set "DEV_TOOLS=false"

if "%1"=="--monitoring" set "MONITORING=true"
if "%1"=="--lm-studio" set "LM_STUDIO=true"
if "%1"=="--dev-tools" set "DEV_TOOLS=true"
if "%1"=="--all" (
    set "MONITORING=true"
    set "LM_STUDIO=true"
    set "DEV_TOOLS=true"
)

REM Install system dependencies
call :install_system_deps

REM Setup Python environment
call :setup_python_env

REM Setup Docker services
call :setup_docker_services

REM Conditional setups
if "%MONITORING%"=="true" call :setup_monitoring
if "%LM_STUDIO%"=="true" call :setup_lm_studio
if "%DEV_TOOLS%"=="true" call :setup_dev_tools

call :log "🎉 GhostLink setup complete!"
echo.
call :info "Next steps:"
echo 1. Edit .env file with your API keys
echo 2. Start services: docker-compose up -d
if "%MONITORING%"=="true" (
    echo 3. Access monitoring:
    echo    - Prometheus: http://localhost:9090
    echo    - Grafana: http://localhost:3000 ^(admin/admin^)
)
if "%LM_STUDIO%"=="true" (
    echo 4. Setup LM Studio as described above
)
echo 5. Access GhostLink: http://localhost:8000
echo.
call :info "For help, run: docker-compose logs -f"
goto :eof

:show_help
echo Usage: %0 [OPTIONS]
echo.
echo Options:
echo   --monitoring    Setup Prometheus and Grafana monitoring
echo   --lm-studio     Setup LM Studio integration
echo   --dev-tools     Setup development tools ^(pre-commit, etc.^)
echo   --all          Setup everything
echo   --help         Show this help
exit /b 0

REM Run main function with all arguments
call :main %*
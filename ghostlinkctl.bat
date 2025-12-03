@echo off
REM GhostLink Control Script (Windows)
REM Provides quick overview and control of all services

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

REM Colors (using mode con for Windows)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "PURPLE=[95m"
set "CYAN=[96m"
set "NC=[0m"

goto :main

:check_service
setlocal
set "service=%~1"
set "port=%~2"
set "description=%~3"

powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:%port%' -TimeoutSec 2 -UseBasicParsing; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo %GREEN%✅ %description% (localhost:%port%)%NC%
    endlocal & set "result=1"
) else (
    echo %RED%❌ %description% (localhost:%port%)%NC%
    endlocal & set "result=0"
)
goto :eof

:check_docker_service
setlocal
set "service_name=%~1"

docker ps --format "table {{.Names}}" | findstr /C:"%service_name%" >nul 2>&1
if %errorlevel% equ 0 (
    echo %GREEN%✅ %service_name%%NC%
    endlocal & set "result=1"
) else (
    echo %RED%❌ %service_name%%NC%
    endlocal & set "result=0"
)
goto :eof

:show_status
echo %CYAN%🚀 GhostLink Full Agent Orchestration Status%NC%
echo ==============================================
echo.
echo %BLUE%📊 Web Services:%NC%

set "web_up=0"
set "total_web=0"

call :check_service ghostlink 8000 "GhostLink API"
set /a "total_web+=1"
if !result! equ 1 set /a "web_up+=1"

call :check_service prometheus 9090 "Prometheus Monitoring"
set /a "total_web+=1"
if !result! equ 1 set /a "web_up+=1"

call :check_service grafana 3000 "Grafana Dashboards"
set /a "total_web+=1"
if !result! equ 1 set /a "web_up+=1"

call :check_service redis 6379 "Redis Cache"
set /a "total_web+=1"
if !result! equ 1 set /a "web_up+=1"

call :check_service postgres 5432 "PostgreSQL Database"
set /a "total_web+=1"
if !result! equ 1 set /a "web_up+=1"

call :check_service ollama 11434 "Ollama AI Models"
set /a "total_web+=1"
if !result! equ 1 set /a "web_up+=1"

echo.
echo %BLUE%🐳 Docker Services:%NC%

set "docker_up=0"
set "total_docker=0"

call :check_docker_service ghostlink-ghostlink
set /a "total_docker+=1"
if !result! equ 1 set /a "docker_up+=1"

call :check_docker_service ghostlink-prometheus
set /a "total_docker+=1"
if !result! equ 1 set /a "docker_up+=1"

call :check_docker_service ghostlink-grafana
set /a "total_docker+=1"
if !result! equ 1 set /a "docker_up+=1"

call :check_docker_service ghostlink-redis
set /a "total_docker+=1"
if !result! equ 1 set /a "docker_up+=1"

call :check_docker_service ghostlink-postgres
set /a "total_docker+=1"
if !result! equ 1 set /a "docker_up+=1"

echo.
echo %PURPLE%📈 Summary:%NC%
echo Web Services: %web_up%/%total_web% running
echo Docker Services: %docker_up%/%total_docker% running

echo.
echo %BLUE%🤖 Local AI:%NC%
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:1234/v1/models' -TimeoutSec 2 -UseBasicParsing; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo %GREEN%✅ LM Studio (localhost:1234)%NC%
) else (
    echo %YELLOW%⚠️  LM Studio not detected (start LM Studio app if needed)%NC%
)
goto :eof

:start_services
echo %CYAN%🚀 Starting GhostLink Services...%NC%

cd "%PROJECT_ROOT%"

REM Start basic services
echo Starting core services...
docker-compose up -d

REM Wait a bit for services to start
timeout /t 5 /nobreak >nul

REM Check if monitoring should be started
if "%~1"=="--monitoring" (
    echo Starting monitoring services...
    docker-compose --profile monitoring up -d
)
if "%~1"=="--all" (
    echo Starting monitoring services...
    docker-compose --profile monitoring up -d
    echo Starting LLM services...
    docker-compose --profile llm up -d
)

echo %GREEN%✅ Services started!%NC%
call :show_status
goto :eof

:stop_services
echo %CYAN%🛑 Stopping GhostLink Services...%NC%

cd "%PROJECT_ROOT%"
docker-compose down

echo %GREEN%✅ Services stopped!%NC%
goto :eof

:restart_services
echo %CYAN%🔄 Restarting GhostLink Services...%NC%

cd "%PROJECT_ROOT%"
docker-compose restart

echo %GREEN%✅ Services restarted!%NC%
call :show_status
goto :eof

:show_logs
cd "%PROJECT_ROOT%"

if "%~1"=="ghostlink" (
    docker-compose logs -f ghostlink
) else if "%~1"=="monitoring" (
    docker-compose logs -f prometheus grafana
) else if "%~1"=="database" (
    docker-compose logs -f postgres redis
) else (
    docker-compose logs -f
)
goto :eof

:show_help
echo GhostLink Control Script (Windows)
echo Usage: %0 [COMMAND] [OPTIONS]
echo.
echo Commands:
echo   status              Show status of all services
echo   start [--monitoring|--all]  Start services
echo   stop                Stop all services
echo   restart             Restart all services
echo   logs [service]      Show logs (ghostlink^|monitoring^|database^|all)
echo   test                Run integration tests
echo   help                Show this help
echo.
echo Examples:
echo   %0 status
echo   %0 start --all
echo   %0 logs ghostlink
goto :eof

:run_tests
echo %CYAN%🧪 Running GhostLink Tests...%NC%

cd "%PROJECT_ROOT%"

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM Run LM Studio test
if exist "test_lmstudio.py" (
    echo Testing LM Studio integration...
    python test_lmstudio.py || echo LM Studio test failed (expected if LM Studio not running)
)

REM Run pytest if available
python -c "import pytest" >nul 2>&1
if %errorlevel% equ 0 (
    echo Running pytest...
    python -m pytest tests/ -v || echo Some tests failed
) else (
    echo pytest not found, skipping unit tests
)

echo %GREEN%✅ Testing complete!%NC%
goto :eof

:main
if "%1"=="status" goto :show_status
if "%1"=="start" (
    call :start_services %2
    goto :eof
)
if "%1"=="stop" goto :stop_services
if "%1"=="restart" goto :restart_services
if "%1"=="logs" (
    call :show_logs %2
    goto :eof
)
if "%1"=="test" goto :run_tests
if "%1"=="help" goto :show_help
if "%1"=="-h" goto :show_help
if "%1"=="--help" goto :show_help

REM Default to status if no command given
call :show_status
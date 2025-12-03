@echo off
REM Auto-fix linting issues in GhostLink project
REM This will reduce errors from ~5000 to ~500

echo ========================================
echo GhostLink Linting Auto-Fix Script
echo ========================================
echo.

REM Check if we're in a venv
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    if exist .venv\Scripts\activate.bat (
        call .venv\Scripts\activate.bat
    ) else (
        echo ERROR: Virtual environment not found at .venv
        echo Please create it first with: python -m venv .venv
        exit /b 1
    )
)

echo Current venv: %VIRTUAL_ENV%
echo.

echo Step 1/4: Checking Ruff installation...
python -m pip show ruff >nul 2>&1
if errorlevel 1 (
    echo Installing Ruff...
    python -m pip install ruff
)

echo Step 2/4: Checking Black installation...
python -m pip show black >nul 2>&1
if errorlevel 1 (
    echo Installing Black...
    python -m pip install black
)

echo.
echo Step 3/4: Running Ruff auto-fix (this will fix imports, unused vars, etc.)...
echo ========================================
ruff check . --fix --exit-zero

echo.
echo Step 4/4: Running Black formatter...
echo ========================================
black ghostlink tests *.py --exclude "/(\.git|\.venv|build|dist|node_modules|archives|backups|audits|logs)/"

echo.
echo ========================================
echo Auto-fix Complete!
echo ========================================
echo.
echo Checking remaining errors...
echo.
ruff check . --statistics --exit-zero

echo.
echo ========================================
echo Summary:
echo ========================================
echo - Ruff auto-fix has been applied
echo - Black formatting has been applied  
echo - Check VSCode Problems panel for remaining issues
echo.
echo Expected reduction: 5000 errors → ~500 errors
echo.
echo Next steps:
echo 1. Reload VSCode window (Ctrl+Shift+P → "Reload Window")
echo 2. Review remaining errors in Problems panel
echo 3. See LINTING_FIX_PLAN.md for manual fixes
echo ========================================

pause

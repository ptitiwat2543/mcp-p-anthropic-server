@echo off
echo Checking package versions for Claude API MCP Server...

:: Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found.
    echo Please run setup_environment.bat first to create it.
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Check current package versions
echo Current package versions:
echo ========================
pip list | findstr /i "mcp anthropic python-dotenv json5 fastapi uvicorn pydantic"
echo ========================

:: Check for available updates
echo Checking for available updates:
echo ==============================
pip list --outdated | findstr /i "mcp anthropic python-dotenv json5 fastapi uvicorn pydantic"
echo ==============================

:: Deactivate virtual environment
call venv\Scripts\deactivate.bat

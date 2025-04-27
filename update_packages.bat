@echo off
echo Updating packages for Claude API MCP Server...

:: Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found.
    echo Running setup_environment.bat to create it...
    call setup_environment.bat
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to set up environment.
        exit /b 1
    )
) else (
    :: Activate virtual environment
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

:: Update dependencies to latest versions
echo Updating dependencies to latest versions...
pip install --upgrade -r requirements.txt

echo Package update completed.
echo To start the server, run: start_server.bat
echo To start the API server, run: start_api_server.bat

:: Deactivate virtual environment
call venv\Scripts\deactivate.bat

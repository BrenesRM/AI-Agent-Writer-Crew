@echo off
echo ==========================================================
echo   AI Writer Crew - Modern Web Interface Launcher
echo ==========================================================
echo.

REM Change to the project directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "novel_env" (
    echo Activating virtual environment...
    call novel_env\Scripts\activate.bat
) else (
    echo Virtual environment not found. Using system Python...
)

REM Install/update required packages
echo Installing/updating required packages...
pip install fastapi uvicorn pydantic pydantic-settings --quiet

REM Launch the web interface
echo.
echo Starting AI Writer Crew Web Interface...
echo.
python launch_web_interface.py

pause

@echo off
chcp 65001 >nul
cls

echo 🚀 AI Agent Writer Crew - Connection Fix
echo =========================================

REM Try to run the Python fix script
python connection_fix.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Python script failed or Python not found
    echo 🔄 Falling back to manual fix...
    echo.
    
    REM Manual Docker commands
    echo 📍 Stopping containers...
    docker-compose down
    
    echo 🔧 Building containers...
    docker-compose build
    
    echo 🚀 Starting containers...
    docker-compose up -d
    
    echo ⏳ Waiting 15 seconds for startup...
    timeout /t 15 /nobreak >nul
    
    echo 📋 Container status:
    docker-compose ps
    
    echo.
    echo 🌐 Try accessing: http://localhost:8501
)

echo.
pause

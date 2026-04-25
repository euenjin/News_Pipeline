@echo off
REM Public Health News Pipeline Launcher for Windows

echo.
echo ============================================================
echo Public Health News Pipeline - Launcher
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Error: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo Error: .env file not found!
    echo Please create .env from .env.example with your API key
    pause
    exit /b 1
)

REM Run the news scheduler
echo Starting Public Health News Pipeline...
echo Logs will be saved to public_health_news_agent.log
echo Press Ctrl+C to stop the agent
echo.

python news_scheduler.py

pause

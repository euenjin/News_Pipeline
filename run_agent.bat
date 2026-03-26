@echo off
REM Financial News Agent Launcher for Windows

echo.
echo ============================================================
echo Financial News Agent - Launcher
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
echo Starting Financial News Agent...
echo Logs will be saved to news_agent.log
echo Press Ctrl+C to stop the agent
echo.

python news_scheduler.py

pause

@echo off
REM News Agent Daily Runner - Runs from 7:59 AM to ~8:02 AM
REM Use Windows Task Scheduler to run this at 7:59 AM daily

echo Starting News Agent for daily news extraction...
cd /d "%~dp0"
python news_scheduler.py
echo News Agent completed for today.
pause
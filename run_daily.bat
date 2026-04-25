@echo off
REM Public Health News Pipeline Daily Runner - Runs from 7:59 AM to ~8:02 AM
REM Use Windows Task Scheduler to run this at 7:59 AM daily

echo Starting Public Health News Pipeline for daily extraction...
cd /d "%~dp0"
python news_scheduler.py
echo Public Health News Pipeline completed for today.
pause

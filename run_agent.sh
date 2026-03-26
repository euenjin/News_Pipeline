#!/bin/bash

# Financial News Agent Launcher for Linux/Mac

echo ""
echo "============================================================"
echo "Financial News Agent - Launcher"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found!"
    echo "Please create .env from .env.example with your API key"
    exit 1
fi

# Run the news scheduler
echo "Starting Financial News Agent..."
echo "Logs will be saved to news_agent.log"
echo "Press Ctrl+C to stop the agent"
echo ""

python news_scheduler.py

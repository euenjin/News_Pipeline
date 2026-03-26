# Quick Start Guide

## 🚀 Get Up and Running in 5 Minutes

### Step 1: Get an API Key (2 minutes)

1. Go to https://newsapi.org/
2. Sign up for a free account
3. Copy your API key

### Step 2: Configure the Project (1 minute)

1. Create `.env` file:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```

2. Edit `.env` and paste your API key:
   ```
   NEWS_API_KEY=your_api_key_here
   ```

### Step 3: Install Dependencies (1 minute)

```bash
python -m venv venv
venv\Scripts\activate  # Windows: venv\Scripts\activate.bat

pip install -r requirements.txt
```

### Step 4: Test the Setup (30 seconds)

```bash
python test_setup.py
```

### Step 5: Start the Agent (1 minute)

**Windows:**
```bash
run_agent.bat
```

**Linux/Mac:**
```bash
bash run_agent.sh
```

## ✅ What happens next?

- The agent will run and wait for 8 AM (Monday-Friday)
- At 8 AM, it will automatically fetch the latest financial news
- News will be saved to `news_archive/` folder
- All activities logged to `news_agent.log`

## 🧪 Want to test immediately?

```bash
python manual_fetch.py
```

This will fetch news right now and save it to the archive.

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `news_scheduler.py` | Main scheduler that runs the agent |
| `news_fetcher.py` | Fetches news from the API |
| `news_agent.log` | Log file (auto-created) |
| `news_archive/` | Folder where news is saved (auto-created) |

## 🆘 Troubleshooting

**Issue: "NEWS_API_KEY not configured"**
- Make sure `.env` exists and has your API key

**Issue: "No module named 'apscheduler'"**
- Run: `pip install -r requirements.txt`

**Issue: Empty news results**
- Check if your API key is valid on newsapi.org
- Check your API request quota (free tier: 100/day)

## 📚 More Information

See [README.md](README.md) for detailed documentation and advanced configuration options.

# Quick Start Guide

## Get Up and Running in 5 Minutes

### Step 1: Get an API Key

1. Go to https://newsapi.org/
2. Sign up for an account
3. Copy your API key

### Step 2: Configure the Project

Create or update `.env`:

```bash
copy .env.example .env
```

Then set:

```text
NEWS_API_KEY=your_api_key_here
```

### Step 3: Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4: Test the Setup

```bash
python test_setup.py
```

### Step 5: Start the Pipeline

```bash
run_agent.bat
```

## What Happens Next?

- The pipeline waits for the configured weekday schedule.
- At the scheduled time, it fetches current public health and clinical research news.
- The digest is saved to `news_archive/`.
- Activities are logged to `public_health_news_agent.log`.

Note: The digest supports public health monitoring and research awareness only. It is not for medical decision-making.

## Test Immediately

```bash
python manual_fetch.py
```

This fetches a public health news digest immediately and saves it to the archive.

## Files Overview

| File | Purpose |
|------|---------|
| `news_scheduler.py` | Scheduler that runs the pipeline |
| `news_fetcher.py` | Fetches, formats, saves, and emails news |
| `public_health_news_agent.log` | Log file, auto-created |
| `news_archive/` | Saved public health news digests |

## Troubleshooting

**Issue: `NEWS_API_KEY` not configured**

Make sure `.env` exists and has your API key.

**Issue: `No module named 'apscheduler'`**

Run:

```bash
pip install -r requirements.txt
```

**Issue: Empty news results**

Check that your API key is valid and that your NewsAPI quota has requests remaining.

See [README.md](README.md) for detailed documentation.

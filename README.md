# Public Health News Pipeline

An automated pipeline that extracts **10 focused public health, medical, and clinical research news articles** Monday to Friday at 8 AM. It is designed for public health monitoring, clinical research updates, and a concise health news digest.

Note: This project is for research awareness and public health monitoring only. It is **not for medical decision-making**.

## Features

- Automated scheduling Monday-Friday at 8 AM
- Public health and clinical research topics such as Alzheimer's, diabetes, CDC updates, clinical AI, digital health, epidemiology, and health policy
- Fresh daily articles from NewsAPI
- Ranking focus based on health topic relevance, recency, and source relevance
- Timestamped archive files
- Optional email delivery
- Logging to file and console
- Efficient short-window operation instead of running all day

## Prerequisites

- Python 3.8 or higher
- pip package manager
- A NewsAPI.org API key

## Setup

```bash
cd News_Pipeline
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create or update `.env`:

```text
NEWS_API_KEY=your_actual_api_key_here
SCHEDULE_HOUR=8
SCHEDULE_MINUTE=0
SAVE_TO_FILE=true
LOG_LEVEL=INFO
```

Optional email settings:

```text
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
RECIPIENT_EMAIL=recipient@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SEND_EMAIL=true
```

## Usage

Run the scheduler:

```bash
python news_scheduler.py
```

Run an immediate fetch:

```bash
python manual_fetch.py
```

Or from Python:

```python
from news_fetcher import extract_daily_news

news = extract_daily_news()
print(news)
```

## Project Structure

```text
News_Pipeline/
├── news_scheduler.py              # Scheduler entry point
├── news_fetcher.py                # News fetching, formatting, saving, email
├── manual_fetch.py                # Immediate fetch helper
├── test_setup.py                  # Setup validation
├── test_email.py                  # Email validation
├── requirements.txt               # Python dependencies
├── public_health_news_agent.log   # Log file, auto-created
└── news_archive/                  # Saved public health news digests
```

## Archive Files

Extracted news is saved as:

```text
news_archive/
├── public_health_news_20260306_080000.txt
├── public_health_news_20260307_080000.txt
└── ...
```

## Logs

Activities are logged to `public_health_news_agent.log`:

```text
2026-03-06 08:00:01 - INFO - Starting public health news extraction...
2026-03-06 08:00:03 - INFO - News saved to news_archive/public_health_news_20260306_080000.txt
2026-03-06 08:00:03 - INFO - Public health news extraction completed successfully
```

## Windows Task Scheduler

Create a task that runs `run_daily.bat` Monday-Friday just before the configured schedule time. The pipeline starts, waits for the scheduled run, saves the digest, optionally sends email, and stops shortly after completion.

## Troubleshooting

- If `NEWS_API_KEY` is missing, confirm `.env` exists and contains a valid key.
- If no articles are returned, check the NewsAPI key and quota.
- If email fails, verify `SENDER_EMAIL`, `SENDER_PASSWORD`, `RECIPIENT_EMAIL`, `SMTP_SERVER`, and `SMTP_PORT`.

## Future Enhancements

- Topic-specific digest sections
- Source allowlist or priority scoring
- Database storage
- Duplicate article detection
- REST API for digest access

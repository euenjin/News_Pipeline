# Financial News Agent 📰

An automated agent that extracts **10 focused financial news articles daily** from Monday to Friday at 8 AM, specifically curated for stock investing and market analysis with the **freshest available content**.

## Features

✅ **Automated Scheduling**: Extracts news Monday-Friday at 8 AM  
✅ **Stock-Focused Content**: 10 curated articles on stock investing, market analysis, and investment opportunities  
✅ **Fresh Daily News**: Latest financial results and market updates (1-2 days old)  
✅ **Integration with NewsAPI**: Fetches latest market-relevant news from multiple sources  
✅ **Automatic File Saving**: Archives all extracted news with timestamps  
✅ **Email Delivery**: Sends daily digest to configured email address  
✅ **Logging**: Comprehensive logging to file and console  
✅ **Efficient Operation**: Runs only 3 minutes per day instead of 24/7  

## Prerequisites

- Python 3.8 or higher
- pip package manager
- A free API key from [NewsAPI.org](https://newsapi.org/)

## Setup Instructions

### 1. Clone/Create Project

```bash
cd News_Agent
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

1. Get a free API key from [NewsAPI.org](https://newsapi.org/)
2. Create a `.env` file from the template:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

3. Edit `.env` and add your NewsAPI key:

```
NEWS_API_KEY=your_actual_api_key_here
```

### 5. Configure Email (Optional)

To receive news via email:

1. **For Gmail users:**
   - Enable 2-factor authentication on your Google account
   - Generate an App Password: Go to [Google Account Settings](https://myaccount.google.com/) → Security → 2-Step Verification → App passwords
   - Create a new app password for "Mail"
   - Use your Gmail address as `SENDER_EMAIL` and the app password as `SENDER_PASSWORD`

2. **Edit `.env` and add email settings:**

```
# Email Settings
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
RECIPIENT_EMAIL=ea3222@nyu.edu
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SEND_EMAIL=true
```

**Note:** For other email providers, adjust `SMTP_SERVER` and `SMTP_PORT` accordingly.

## Usage

### Efficient Daily Scheduling (Recommended)

For better performance, run the agent only during a short time window instead of 24/7:

**Option 1: Windows Task Scheduler (Automated)**
1. Open Windows Task Scheduler
2. Create new task:
   - **Name:** News Agent Daily
   - **Trigger:** Daily at 7:59 AM, Monday-Friday
   - **Action:** Start program → `run_daily.bat`
   - **Start in:** `C:\Users\eunji\OneDrive\바탕 화면\News_Agent`
3. The agent runs only ~3 minutes per day!

**Option 2: Manual Daily Run**
```bash
# Run at 7:59 AM daily (Monday-Friday)
run_daily.bat
```

**Benefits:**
- ✅ Runs only 3 minutes per day vs 24 hours
- ✅ Lower CPU/memory usage
- ✅ Same functionality
- ✅ Auto-stops after job completion

### Manual News Extraction

To manually extract news without scheduling:

```bash
python
>>> from news_fetcher import extract_daily_news
>>> news = extract_daily_news()
>>> print(news)
```

## Project Structure

```
News_Agent/
├── news_scheduler.py      # Main scheduler script
├── news_fetcher.py        # News fetching logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── .env                  # Your configuration (create from .env.example)
├── news_agent.log        # Log file (auto-created)
└── news_archive/         # Folder for saved news (auto-created)
```

## Configuration

Edit `.env` to customize:

```
SCHEDULE_HOUR=8          # Hour for execution (0-23)
SCHEDULE_MINUTE=0        # Minute for execution (0-59)
SAVE_TO_FILE=true        # Save extracted news to file
LOG_LEVEL=INFO           # Logging level
```

## Running as Background Service

### Windows (Using Task Scheduler)

1. Create a batch file `run_news_agent.bat`:

```batch
@echo off
cd /d "C:\Users\eunji\OneDrive\바탕 화면\News_Agent"
call venv\Scripts\activate.bat
python news_scheduler.py
pause
```

2. Open Task Scheduler and create a new task:
   - Action: Run the batch file
   - Trigger: At system startup
   - Run with highest privileges

### Linux/Mac (Using Cron)

Add to crontab:

```bash
@reboot cd /path/to/News_Agent && source venv/bin/activate && nohup python news_scheduler.py > news_agent.log 2>&1 &
```

## File Structure

### news_archive/

Extracted news is saved as:
```
news_archive/
├── financial_news_20260306_080000.txt
├── financial_news_20260305_080000.txt
└── ...
```

### Logs

All activities are logged to `news_agent.log`:
```
2026-03-06 08:00:01 - INFO - Starting financial news extraction...
2026-03-06 08:00:03 - INFO - News saved to news_archive/financial_news_20260306_080000.txt
2026-03-06 08:00:03 - INFO - Financial news extraction completed successfully
```

## Troubleshooting

### "NEWS_API_KEY environment variable not set!"

- Make sure `.env` file exists in the project root
- Verify the file contains: `NEWS_API_KEY=your_key_here`
- Ensure there are no extra spaces or quotes

### No news extracted

- Check your API key validity on [NewsAPI.org](https://newsapi.org/)
- Verify you have API requests remaining
- Check logs in `news_agent.log`

### Agent not running at scheduled time

- Ensure the system time is correct
- Verify the scheduler is running (no errors in log)
- Check system clock synchronization

## API Keys

- **NewsAPI.org**: Free tier allows 100 requests/day
  - Sign up at: https://newsapi.org/
  - Great for development and small-scale usage
  - Commercial plans available for higher limits

## License

MIT License

## Support

For issues or questions:
1. Check the logs in `news_agent.log`
2. Verify API key configuration
3. Ensure all dependencies are installed

## Future Enhancements

- [ ] Email notifications with daily news
- [ ] Database storage for news
- [ ] Multiple news sources integration
- [ ] Sentiment analysis
- [ ] News filtering by sector
- [ ] REST API for news access

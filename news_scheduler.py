import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from news_fetcher import extract_daily_news, FinancialNewsFetcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FinancialNewsScheduler:
    """Schedules financial news extraction"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False
    
    def schedule_daily_extraction(self, hour: int = 8, minute: int = 0):
        """
        Schedule news extraction for weekdays at specified time
        
        Args:
            hour: Hour (0-23)
            minute: Minute (0-59)
        """
        # CronTrigger: day_of_week=0-4 means Monday-Friday
        trigger = CronTrigger(
            day_of_week='mon-fri',
            hour=hour,
            minute=minute
        )
        
        job = self.scheduler.add_job(
            func=self._execute_extraction,
            trigger=trigger,
            id='daily_financial_news',
            name='Extract Daily Financial News',
            replace_existing=True
        )
        
        logger.info(f"Job scheduled: {job.name}")
        logger.info(f"Schedule: Monday-Friday at {hour:02d}:{minute:02d}")
        return job
    
    def _execute_extraction(self):
        """Execute the news extraction"""
        try:
            logger.info("Starting financial news extraction...")
            send_email = os.getenv('SEND_EMAIL', 'false').lower() == 'true'
            news_content = extract_daily_news(save_to_file=True, send_email=send_email)
            logger.info("Financial news extraction completed successfully")
            if send_email:
                logger.info("News email sent to configured recipient")
            logger.info(f"\n{news_content}")
        except Exception as e:
            logger.error(f"Error during news extraction: {e}")
    
    def start(self):
        """Start the scheduler"""
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.info("News scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("News scheduler stopped")
    
    def get_jobs(self):
        """Get all scheduled jobs"""
        return self.scheduler.get_jobs()


def main():
    """Main entry point - runs efficiently for short time window"""
    import os
    import time
    from datetime import datetime, timedelta
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Verify API key is available
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        logger.error("NEWS_API_KEY environment variable not set!")
        logger.info("Please set NEWS_API_KEY in .env file or as environment variable")
        return
    
    # Create scheduler
    scheduler = FinancialNewsScheduler()
    
    # Get schedule time from environment or default to 8:00 AM
    schedule_hour = int(os.getenv('SCHEDULE_HOUR', '8'))
    schedule_minute = int(os.getenv('SCHEDULE_MINUTE', '0'))
    
    # Schedule the job
    scheduler.schedule_daily_extraction(hour=schedule_hour, minute=schedule_minute)
    scheduler.start()
    
    try:
        logger.info(f"News Agent started. Will run until {schedule_hour:02d}:{schedule_minute + 2:02d} AM then stop.")
        
        # Calculate when to stop (2 minutes after scheduled time)
        now = datetime.now()
        stop_time = now.replace(hour=schedule_hour, minute=schedule_minute + 2, second=0, microsecond=0)
        
        # If stop time has already passed today, set it for tomorrow
        if stop_time <= now:
            stop_time = stop_time + timedelta(days=1)
        
        logger.info(f"Scheduler will auto-stop at: {stop_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run until stop time
        while datetime.now() < stop_time:
            time.sleep(10)  # Check every 10 seconds
        
        logger.info("Auto-stopping scheduler (time window completed)")
        
    except KeyboardInterrupt:
        logger.info("Shutting down News Agent...")
    finally:
        scheduler.stop()
        logger.info("News Agent stopped")


if __name__ == '__main__':
    main()

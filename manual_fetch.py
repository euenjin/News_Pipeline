#!/usr/bin/env python
"""
Manual news extraction script - useful for testing
Run this to fetch and display financial news immediately
"""

import os
import sys
from dotenv import load_dotenv
from news_fetcher import extract_daily_news, FinancialNewsFetcher

def main():
    """Manually extract and display financial news"""
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("ERROR: NEWS_API_KEY not configured!")
        print("Please update your .env file with a valid API key from https://newsapi.org/")
        sys.exit(1)
    
    print("Fetching financial news...")
    print("-" * 80)
    
    try:
        # Extract news
        news = extract_daily_news(save_to_file=True)
        print(news)
        print("-" * 80)
        print("✓ News extracted and saved to news_archive/")
    except Exception as e:
        print(f"ERROR: Failed to extract news: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

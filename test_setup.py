#!/usr/bin/env python
"""
Test script to verify News Agent setup
"""

import os
import sys
from dotenv import load_dotenv

def test_setup():
    """Test if all components are properly configured"""
    print("=" * 60)
    print("Financial News Agent - Setup Test")
    print("=" * 60)
    
    # Test 1: Check if .env file exists
    print("\n1. Checking .env file...")
    if os.path.exists('.env'):
        print("   ✓ .env file found")
    else:
        print("   ✗ .env file not found")
        print("   → Create .env from .env.example: copy .env.example .env")
        return False
    
    # Test 2: Load environment variables
    print("\n2. Loading environment variables...")
    load_dotenv()
    api_key = os.getenv('NEWS_API_KEY')
    if api_key and api_key != 'your_api_key_here':
        print(f"   ✓ NEWS_API_KEY configured: {api_key[:10]}...")
    else:
        print("   ✗ NEWS_API_KEY not configured or using placeholder")
        print("   → Get a free key from https://newsapi.org/")
        return False
    
    # Test 3: Check if required packages are installed
    print("\n3. Checking required packages...")
    required_packages = {
        'requests': 'requests',
        'apscheduler': 'apscheduler',
        'dotenv': 'dotenv'
    }
    
    all_installed = True
    for name, package in required_packages.items():
        try:
            __import__(package)
            print(f"   ✓ {name} installed")
        except ImportError:
            print(f"   ✗ {name} not installed")
            all_installed = False
    
    if not all_installed:
        print("   → Run: pip install -r requirements.txt")
        return False
    
    # Test 4: Test API connection
    print("\n4. Testing API connection...")
    try:
        from news_fetcher import FinancialNewsFetcher
        fetcher = FinancialNewsFetcher(api_key=api_key)
        articles = fetcher.fetch_news()
        if articles:
            print(f"   ✓ Successfully fetched {len(articles)} articles")
            print(f"   → First article: {articles[0].get('title', 'N/A')[:50]}...")
        else:
            print("   ✗ No articles returned (API key may be invalid)")
            return False
    except Exception as e:
        print(f"   ✗ API connection failed: {e}")
        return False
    
    # Test 5: Test scheduler
    print("\n5. Testing scheduler configuration...")
    try:
        from news_scheduler import FinancialNewsScheduler
        scheduler = FinancialNewsScheduler()
        scheduler.schedule_daily_extraction(hour=8, minute=0)
        jobs = scheduler.get_jobs()
        if jobs:
            print(f"   ✓ Scheduler configured successfully")
            print(f"   → Scheduled job: {jobs[0].name}")
            print(f"   → Trigger: {jobs[0].trigger}")
        else:
            print("   ✗ Failed to configure scheduler")
            return False
    except Exception as e:
        print(f"   ✗ Scheduler test failed: {e}")
        return False
    
    # Test 6: Check news_archive folder
    print("\n6. Checking news archive folder...")
    if not os.path.exists('news_archive'):
        try:
            os.makedirs('news_archive')
            print("   ✓ Created news_archive folder")
        except Exception as e:
            print(f"   ✗ Failed to create folder: {e}")
            return False
    else:
        print("   ✓ news_archive folder exists")
    
    return True


def main():
    """Main test function"""
    success = test_setup()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ All tests passed! Your setup is ready.")
        print("\nTo start the news agent, run:")
        print("  python news_scheduler.py")
    else:
        print("✗ Setup test failed. Please fix the issues above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == '__main__':
    main()

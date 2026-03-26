import os
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class FinancialNewsFetcher:
    """Fetches financial news from various sources"""
    
    def __init__(self, api_key: str = None, source: str = "newsapi"):
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.source = source
        self.base_url = {
            'newsapi': 'https://newsapi.org/v2/everything',
            'finnhub': 'https://finnhub.io/api/v1/news'
        }.get(source, 'https://newsapi.org/v2/everything')
    
    def fetch_newsapi(self) -> List[Dict]:
        """Fetch news from NewsAPI.org"""
        if not self.api_key:
            logger.error("NewsAPI key not configured")
            raise ValueError("NEWS_API_KEY environment variable is required")
        
        params = {
            'q': 'stock market analysis OR stock investment strategy OR stock trading analysis OR market forecast OR investment portfolio OR stock picks OR market outlook OR equity analysis OR stock performance OR market trends analysis',
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': self.api_key,
            'pageSize': 10
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'ok':
                return data.get('articles', [])
            else:
                logger.error(f"API error: {data.get('message', 'Unknown error')}")
                return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch news: {e}")
            return []
    
    def fetch_news(self) -> List[Dict]:
        """Fetch financial news based on configured source"""
        if self.source == 'newsapi':
            return self.fetch_newsapi()
        else:
            return self.fetch_newsapi()  # Default to NewsAPI
    
    def format_news(self, articles: List[Dict]) -> str:
        """Format articles into readable text"""
        if not articles:
            return "No financial news found for today."
        
        formatted = f"\n{'='*80}\n"
        formatted += f"FINANCIAL NEWS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        formatted += f"{'='*80}\n\n"
        
        for i, article in enumerate(articles, 1):
            title = article.get('title') or 'No title'
            source_name = article.get('source', {}).get('name') or 'Unknown'
            published_at = article.get('publishedAt') or 'Unknown'
            description = article.get('description') or 'No description'
            url = article.get('url') or 'No URL'
            
            formatted += f"{i}. {title}\n"
            formatted += f"   Source: {source_name}\n"
            formatted += f"   Published: {published_at}\n"
            formatted += f"   Description: {description[:200] if description else 'No description'}...\n"
            formatted += f"   URL: {url}\n\n"
        
        return formatted


def extract_daily_news(save_to_file: bool = True, send_email: bool = False, recipient_email: str = None) -> str:
    """Main function to extract daily financial news"""
    fetcher = FinancialNewsFetcher()
    articles = fetcher.fetch_news()
    formatted_news = fetcher.format_news(articles)
    
    if save_to_file:
        save_news_to_file(formatted_news)
    
    if send_email:
        send_news_email(formatted_news, recipient_email)
    
    return formatted_news


def save_news_to_file(news_content: str, folder: str = 'news_archive'):
    """Save news to file"""
    os.makedirs(folder, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(folder, f'financial_news_{timestamp}.txt')
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(news_content)
        logger.info(f"News saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to save news: {e}")


def send_news_email(news_content: str, recipient_email: str = None):
    """Send news via email"""
    if not recipient_email:
        recipient_email = os.getenv('RECIPIENT_EMAIL')
    
    if not recipient_email:
        logger.warning("No recipient email configured, skipping email send")
        return False
    
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not all([sender_email, sender_password]):
        logger.error("SMTP credentials not configured (SENDER_EMAIL, SENDER_PASSWORD)")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Financial News - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Add body
        body = f"Automated Financial News Update\n\n{news_content}"
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        logger.info(f"News email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send news email: {e}")
        return False

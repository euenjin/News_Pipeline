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

HEALTH_TOPIC_KEYWORDS = [
    "public health",
    "cdc",
    "clinical research",
    "clinical trial",
    "diabetes",
    "alzheimer",
    "clinical ai",
    "digital health",
    "medical research",
    "epidemiology",
    "health policy",
]

SOURCE_PRIORITY_KEYWORDS = [
    "cdc",
    "nih",
    "who",
    "jama",
    "nejm",
    "bmj",
    "lancet",
    "nature",
    "stat",
    "medpage",
]

EXCLUDED_NEWS_KEYWORDS = [
    "stock",
    "stocks",
    "share price",
    "shares",
    "market weakness",
    "market rally",
    "investor",
    "investors",
    "investment",
    "trading",
    "portfolio",
    "equity",
    "earnings",
    "nasdaq",
    "dow jones",
]


class PublicHealthNewsFetcher:
    """Fetches public health and clinical research news from various sources"""
    
    def __init__(self, api_key: str = None, source: str = "newsapi"):
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.source = source
        self.base_url = {
            'newsapi': 'https://newsapi.org/v2/everything'
        }.get(source, 'https://newsapi.org/v2/everything')
    
    def fetch_newsapi(self) -> List[Dict]:
        """Fetch news from NewsAPI.org"""
        if not self.api_key:
            logger.error("NewsAPI key not configured")
            raise ValueError("NEWS_API_KEY environment variable is required")
        
        params = {
            'q': '("public health" OR CDC OR "clinical research" OR diabetes OR Alzheimer\'s OR "clinical AI" OR "digital health" OR "medical research" OR epidemiology OR "health policy")',
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': self.api_key,
            'pageSize': 25
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'ok':
                return self.rank_articles(self.filter_articles(data.get('articles', [])))[:10]
            else:
                logger.error(f"API error: {data.get('message', 'Unknown error')}")
                return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch news: {e}")
            return []

    def filter_articles(self, articles: List[Dict]) -> List[Dict]:
        """Remove off-topic business coverage before ranking."""
        return [article for article in articles if not self._is_excluded_article(article)]

    def rank_articles(self, articles: List[Dict]) -> List[Dict]:
        """Rank by health topic relevance, recency, and source relevance."""
        return sorted(articles, key=self._score_article, reverse=True)

    def _is_excluded_article(self, article: Dict) -> bool:
        title = article.get('title') or ''
        description = article.get('description') or ''
        text = f"{title} {description}".lower()

        return any(keyword in text for keyword in EXCLUDED_NEWS_KEYWORDS)

    def _score_article(self, article: Dict) -> float:
        title = article.get('title') or ''
        description = article.get('description') or ''
        source_name = article.get('source', {}).get('name') or ''
        text = f"{title} {description}".lower()
        source = source_name.lower()

        topic_score = sum(2 for keyword in HEALTH_TOPIC_KEYWORDS if keyword in text)
        source_score = sum(1 for keyword in SOURCE_PRIORITY_KEYWORDS if keyword in source)
        recency_score = self._recency_score(article.get('publishedAt'))

        return topic_score + source_score + recency_score

    def _recency_score(self, published_at: str) -> float:
        if not published_at:
            return 0

        try:
            published = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            age_hours = max((datetime.now(published.tzinfo) - published).total_seconds() / 3600, 0)
            return max(0, 3 - (age_hours / 24))
        except ValueError:
            return 0
    
    def fetch_news(self) -> List[Dict]:
        """Fetch public health news based on configured source"""
        if self.source == 'newsapi':
            return self.fetch_newsapi()
        else:
            return self.fetch_newsapi()  # Default to NewsAPI
    
    def format_news(self, articles: List[Dict]) -> str:
        """Format articles into readable text"""
        if not articles:
            return "No public health news found for today."
        
        formatted = f"\n{'='*80}\n"
        formatted += f"PUBLIC HEALTH NEWS DIGEST - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        formatted += f"{'='*80}\n\n"
        formatted += "Note: This digest is for public health monitoring and research awareness only; it is not for medical decision-making.\n"
        formatted += "Ranking focus: health topic relevance, recency, and source relevance.\n\n"
        
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
    """Main function to extract daily public health news"""
    fetcher = PublicHealthNewsFetcher()
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
    filename = os.path.join(folder, f'public_health_news_{timestamp}.txt')
    
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
        msg['Subject'] = f"Public Health News Digest - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Add body
        body = f"Automated Public Health News Digest\n\n{news_content}"
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

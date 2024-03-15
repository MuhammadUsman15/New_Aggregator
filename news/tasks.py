from celery import shared_task

from news_aggregator.news.views import fetch_news
from .models import Article
from django.core.cache import cache

@shared_task
def update_feed_cache():
    # Replace with your list of RSS feed URLs
    feed_urls = [
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'https://www.cbsnews.com/latest/rss/us',
        'https://feeds.nbcnews.com/nbcnews/public/news',
    ]

    articles = []
    for url in feed_urls:
        articles.extend(fetch_news(url))  # Assuming you have a fetch_news function
        cache.delete(f"articles_{url}")  # Clear existing cache for the feed

    # Sort and cache all articles
    articles.sort(key=lambda a: a.pub_date, reverse=True)
    for url in feed_urls:
        cache.set(f"articles_{url}", articles, timeout=3600)  # Cache for 1 hour


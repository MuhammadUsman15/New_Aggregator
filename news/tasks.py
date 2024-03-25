# tasks.py

from celery import shared_task
from .utils import fetch_news  # Import the fetch_news function
from django.core.cache import cache



@shared_task
def update_feed_cache():
    feed_urls = [
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'https://feeds.nbcnews.com/nbcnews/public/news',
        'https://slate.com/feeds/all.rss'
    ]

    
    articles = []
    for url in feed_urls:
        articles.extend(fetch_news(url))  # Assuming you have a fetch_news function
        cache_key = f"articles_{url}"  # Ensure cache key matches the one used in the view
        cache.delete(cache_key)  # Clear existing cache for the feed
        cache.set(cache_key, articles, timeout=3600)  # Cache articles with appropriate key




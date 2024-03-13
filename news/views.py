from django.shortcuts import render
import feedparser
from .models import Article
# Create your views here.

def fetch_news(feed_url):
  feed = feedparser.parse(feed_url)
  articles = []
  for entry in feed.entries:
    article = Article(
      title=entry.title,
      url=entry.link,
      pub_date=entry.published,
      source=entry.source.name,
      summary=entry.summary if hasattr(entry, 'summary') else '',
    )
    articles.append(article)
  return articles

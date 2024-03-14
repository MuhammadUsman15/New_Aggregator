from django.shortcuts import render
import feedparser
from .models import Article


def fetch_news(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        article = Article(
            title=entry.title,
            url=entry.link,
            pub_date=entry.published,
            # Include description if it exists
            summary=entry.summary if hasattr(entry, 'summary') else '',
        )
        articles.append(article)
    return articles


def news_list(request):
    # Replace with your list of RSS feed URLs
    feed_urls = ['https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml','https://www.cbsnews.com/latest/rss/main','https://feeds.nbcnews.com/nbcnews/public/news']
    articles = []
    for url in feed_urls:
        articles.extend(fetch_news(url))
    articles.sort(key=lambda a: a.pub_date, reverse=True)
    context = {'articles': articles}
    return render(request, 'news/templates/news_list.html', context)

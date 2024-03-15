import datetime
from django.http import HttpResponse
from django.shortcuts import render
from .models import Article
from django.core.paginator import Paginator
from django.core.cache import cache
import feedparser
def fetch_news(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        try:
            pub_date = datetime.datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')  # Adjust format if needed
        except (ValueError, AttributeError):
            pub_date = None  # Set to None or a default value if parsing fails
        article = Article(
            title=entry.title,
            url=entry.link,
            pub_date=pub_date,
            summary=entry.summary if hasattr(entry, 'summary') else '',
        )
        articles.append(article)
    return articles


def news_list(request):
    # Replace with your list of RSS feed URLs (consider removing from view)
    feed_urls = [
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'https://www.cbsnews.com/latest/rss/us',
        'https://feeds.nbcnews.com/nbcnews/public/news',
    ]

    # Use cached articles (assuming Celery updates the cache)
    cache_key = 'all_articles'
    articles = cache.get(cache_key)

    if articles is None:
        return HttpResponse('Articles not available yet. Please try again later.')


    # Pagination logic (unchanged)
    paginator = Paginator(articles, 10)  # 10 articles per page (customize this)
    page_number = request.GET.get('page')  # Get page number from URL parameter
    page_obj = paginator.get_page(page_number)

    context = {'articles': page_obj, 'paginator': paginator}
    return render(request, 'news/templates/news_list.html', context)



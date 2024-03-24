import datetime
from django.http import HttpResponse
from django.shortcuts import render
from .models import Article
from django.core.paginator import Paginator
from django.core.cache import cache
from .utils import fetch_news  # Import the fetch_news function
from .tasks import update_feed_cache

def news_list(request):
    # Call the task to update the feed cache
    update_feed_cache.delay()

    # Use cached articles (assuming Celery updates the cache)
    cache_key = 'all_articles'
    articles = cache.get(cache_key)

    if articles is None:
        # Fetch articles using the fetch_news function if cache is empty
        feed_urls = [
            'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
            # 'https://www.cbsnews.com/latest/rss/us',
            'https://feeds.nbcnews.com/nbcnews/public/news',
            'https://slate.com/feeds/all.rss'
        ]
        articles = []
        for url in feed_urls:
            fetched_articles = fetch_news(url)
            if fetched_articles:  # Check if any articles were fetched
                articles.extend(fetched_articles)

        # Cache the fetched articles
        cache.set(cache_key, articles, timeout=3600)

    # Pagination logic (unchanged)
    paginator = Paginator(articles, 10)  # 10 articles per page (customize this)
    page_number = request.GET.get('page')  # Get page number from URL parameter
    page_obj = paginator.get_page(page_number)

    context = {'articles': page_obj, 'paginator': paginator}
    return render(request, 'news_list.html', context)

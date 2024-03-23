import feedparser
import datetime
from .models import Article

def fetch_news(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        try:
            pub_date = datetime.datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
        except (ValueError, AttributeError):
            pub_date = None
        
        # Exclude articles with None publication date
        if pub_date is not None:
            article = Article(
                title=entry.title,
                url=entry.link,
                pub_date=pub_date,
                summary=entry.summary if hasattr(entry, 'summary') else '',
            )
            articles.append(article)
    
    # Sort articles by publication date in descending order
    articles.sort(key=lambda x: x.pub_date, reverse=True)
    
    return articles

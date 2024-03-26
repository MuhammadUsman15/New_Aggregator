from urllib.parse import urlparse
import feedparser
import datetime
from dateutil import parser as date_parser
from .models import Article

def fetch_news(feed_urls):
    all_articles = []

    for feed_url in feed_urls:
        feed = feedparser.parse(feed_url)
        website_name = urlparse(feed_url).hostname
        source_name = website_name.split('.')[-2]  # Extracting the source name
        articles = []

        for entry in feed.entries:
            try:
                # Try to parse the publication date using dateutil.parser
                if 'published' in entry:
                    pub_date_str = entry['published']
                elif 'pubDate' in entry:
                    pub_date_str = entry['pubDate']
                elif 'dateTimeWritten' in entry:
                    pub_date_str = entry['dateTimeWritten']
                elif 'pubdate' in entry:
                    pub_date_str = entry['pubdate']

                pub_date = date_parser.parse(pub_date_str)
            except Exception as e:
                print("Error:", e)
                pub_date = None

            # Fetch the image URL if available
            image_url = None
            if 'media_content' in entry:
                for media in entry.media_content:
                    if 'url' in media:
                        image_url = media['url']
                        break
            elif 'media:content' in entry:
                media_content = entry['media:content']
                if media_content:
                    # If media content is a list
                    if isinstance(media_content, list):
                        for media in media_content:
                            if media.get('type') == 'image/jpeg' and media.get('medium') == 'image':
                                image_url = media.get('url')
                                break
                    # If media content is a dictionary
                    elif isinstance(media_content, dict):
                        if media_content.get('type') == 'image/jpeg' and media_content.get('medium') == 'image':
                            image_url = media_content.get('url')

            article = Article(
                title=entry.get('title', ''),
                url=entry.get('link', ''),
                pub_date=pub_date,
                summary=entry.get('summary', ''),
                image_url=image_url,
                website_name=source_name,  # Assigning source name instead of full hostname
            )

            articles.append(article)

        all_articles.extend(articles)

    # Sort all articles by publication date in descending order
    all_articles.sort(key=lambda x: x.pub_date if x.pub_date else datetime.datetime.min, reverse=True)

    return all_articles

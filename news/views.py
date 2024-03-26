from audioop import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
from .utils import fetch_news  # Import the fetch_news function
from .tasks import update_feed_cache
from django.contrib import auth
from django.contrib.auth.models import User


@login_required
def news_list(request):
    # Call the task to update the feed cache
    update_feed_cache.delay()

    # Use cached articles (assuming Celery updates the cache)
    cache_key = 'all_articles'
    articles = cache.get(cache_key)

    if articles is None:
        # List of feed URLs
        feed_urls = [
            'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
            'https://feeds.nbcnews.com/nbcnews/public/news',
            'https://slate.com/feeds/all.rss',
        ]
        
        # Fetch articles using the fetch_news function if cache is empty
        articles = fetch_news(feed_urls)

        # Cache the fetched articles
        cache.set(cache_key, articles, timeout=3600)

    # Pagination logic (unchanged)
    paginator = Paginator(articles, 10)  # 10 articles per page (customize this)
    page_number = request.GET.get('page')  # Get page number from URL parameter

    # If user is not authenticated and trying to access a page other than the first one
    if not request.user.is_authenticated and page_number and int(page_number) != 1:
        return redirect('login')  # Redirect to login page if user is not authenticated

    page_obj = paginator.get_page(page_number)

    context = {'articles': page_obj, 'paginator': paginator}
    return render(request, 'news_list.html', context)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.core.cache import cache
from django.contrib import auth
from .utils import fetch_news
from .tasks import update_feed_cache

def news_list(request):
    # Call the task to update the feed cache
    update_feed_cache.delay()

    # Use cached articles (assuming Celery updates the cache)
    cache_key = 'all_articles'
    articles = cache.get(cache_key)

    if articles is None:
        # List of feed URLs
        feed_urls = [
            'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
            'https://feeds.nbcnews.com/nbcnews/public/news',
            'https://slate.com/feeds/all.rss',
        ]
        
        # Fetch articles using the fetch_news function if cache is empty
        articles = fetch_news(feed_urls)

        # Cache the fetched articles
        cache.set(cache_key, articles, timeout=3600)

    # Pagination logic (unchanged)
    paginator = Paginator(articles, 10)  # 10 articles per page (customize this)
    page_number = request.GET.get('page')  # Get page number from URL parameter

    # If user is not authenticated and trying to access a page other than the first one
    if not request.user.is_authenticated and page_number and int(page_number) != 1:
        return redirect('login')  # Redirect to login page if user is not authenticated

    page_obj = paginator.get_page(page_number)

    context = {'articles': page_obj, 'paginator': paginator}
    return render(request, 'news_list.html', context)

def login(request):
    if request.method ==  "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request,  username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('news_list')  # Redirect to news list after login
        else:
            error_message = 'Invalid username or password'
            return render(request,'login.html', {'error_message': error_message })
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                # Authenticate the user after registration
                auth.login(request, user)
                # Redirect to the news_list page after successful registration
                return redirect('news_list')
            except:
                error_message = 'Error creating account'
                return  render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password does not match.'
            return render(request, 'register.html',{'error_message':error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('news_list')

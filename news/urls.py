from django.urls import path
from . import views
urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('login', views.login, name='login'),
    path('register',views.register, name='register'),
    path('logout',views.logout, name='logout'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_tweets_from_timeline, name='main'),
]

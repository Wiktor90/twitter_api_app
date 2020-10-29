from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('tweets/<int:pk>/', views.get_tweets_from_timeline, name='tweets'),
]

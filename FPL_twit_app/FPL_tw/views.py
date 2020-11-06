from django.shortcuts import render, get_object_or_404
from .models import Club
import tweepy, datetime, time
from .credentials import consumer_key, consumer_secret, access_token, access_token_secret
from django.core.paginator import Paginator


def main_view (request):
    clubs = Club.objects.all()

    context = {'clubs':clubs}
    return render(request, 'FPL_tw/main.html', context)


# my authorization to twitter api
def get_api_auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


# grab all tweets from last 24h from user timeline
def grab_last_24h_tweets(api, username):
    tweets = []
    page = 1
    end = False
    while True:
        timeline = api.user_timeline(screen_name=username, page=page, tweet_mode="extended")
        for status in timeline:
            if (datetime.datetime.now() - status.created_at).days < 1:
                tweets.append(status)
            else:
                end = True
                return tweets
        if not end:
            page += 1


def get_tweets_from_timeline(request, pk):
    api = get_api_auth()

    #create obj-Club instance
    club = get_object_or_404(Club, pk=pk)

    #get list of status objects
    #timeline = api.user_timeline(screen_name=club.screen_name, count=10, tweet_mode="extended")
    timeline = grab_last_24h_tweets(api, club.screen_name)
    
    #get list of status(tweet) full text
    tweet_full_text = [status.retweeted_status.full_text if 'retweeted_status' in status._json else status.full_text for status in timeline]
    tweet_full_text = [text.split("|")[0] if "|" in text else text for text in tweet_full_text]
    
    #get list of status(tweet) creation date
    tweet_created_at = [status.created_at for status in timeline]

    # get list of links to each status(tweet) included status id + screen_name. They are a status link constructors.
    tweet_link = [(status.author.screen_name, status.id) for status in timeline]

    tweets = zip(tweet_created_at, tweet_full_text, tweet_link)

    # Pagination
    p = Paginator([item for item in tweets], 5)
    page = request.GET.get('page')
    tweets = p.get_page(page)
    
    context = {
        'tweets':tweets,
        'club':club,
        }
    return render(request, 'FPL_tw/tweets.html', context)


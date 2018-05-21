# exploring twitter's API reference https://chatbotslife.com/twitter-data-mining-a-guide-to-big-data-analytics-using-python-4efc8ccfa219
# https://gist.github.com/yanofsky/5436496

import csv
import time
from datetime import datetime

import tweepy       #http://docs.tweepy.org/en/v3.5.0/api.html

from modules.tweet import AkTweet
from modules.user import AkUser

def get_access_tokens():
    """Loading App secrets and keys."""
    keys = {}
    with open('Access_Data_NO_GIT.csv', 'r') as infile:
        reader = csv.DictReader(infile)
        for r in reader:
            for k,v in r.items():
                keys[k] = v
                #print('adding {} to keys[{}]'.format(v,k))
    return keys


def get_twitter_api_obj(keys = None):
    if not keys:
        keys = get_access_tokens()
    # Creating the authentication object
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    # Setting your access token and secret
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    # Creating the API object while passing in auth information
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def print_tweets(public_tweets):
    # Print out each tweet in a list of tweets.
    for tweet in public_tweets:
        print_tweet(tweet)


def print_tweet(tweet):
    # Printing a summary of a tweet object
    print('At: {} : {}'.format(tweet.created_at, tweet.text))
    print('   tweeted by : {} from {}'.format(tweet.user.screen_name, tweet.user.location))


def my_home_timeline(api):
    # Get tweets from my timeline.
    public_tweets = api.home_timeline()
    print_tweets(public_tweets)


def get_users_timeline(api, id):
    ### Get tweets from a users timeline. ###

    tweets = []
    # get first 200 tweets (200 is max number allowed in one get)
    tweets.extend(api.user_timeline(screen_name=id, count=200, tweet_mode='extended'))
    # set max_id to id of last retreved tweet
    max_id = tweets[-1].id - 1

    MAX_TIMELINE_PAGES = 16 # apparantly sometime 17
    cursor = tweepy.Cursor(api.user_timeline, id=id, count=200, max_id=max_id, tweet_mode='extended').pages(MAX_TIMELINE_PAGES)
    i=1
    for page in cursor:
        print('Obtained ' + str(i) + ' tweet pages for user ' + str(id) + '.')
        i += 1
        for tweet in page:
            tweets.append(tweet)
        max_id = page[-1].id - 1

    #writing data to csv
    akt = AkTweet()
    out = akt.get_tweet_csv_writer('Timeline'+ id)
    for t in tweets:
        if t.lang != 'en':  # skipping tweets not in english
            continue
        akt.write_tweet(t, out)
        #print_tweet(t)


def search_tweets(api, query, language="en"):
    # Calling the search function
    akt = AkTweet()
    out, fields = akt.get_tweet_csv_writer('search' + query)
    results = api.search(q=query, lang=language)
    for t in results:
        if t.lang != 'en':  # skipping tweets not in english
            continue
        akt.write_tweet(t, out)
        print_tweet(t)

def get_followers(api, id):
    ### get followers from the API.###

    users = []
    MAX_FOLLOWER_PAGES = 5 # got 14 pages before limit
    cursor = tweepy.Cursor(api.followers, id=id).pages(MAX_FOLLOWER_PAGES)
    i = 1
    for page in cursor:
        print('Obtained ' + str(i) + ' follower pages for user ' + str(id) + '.')
        i += 1
        for user in page:
            users.append(user)
        max_id = page[-1].id - 1

    # writing data to csv
    akt = AkUser()
    out = akt.get_user_csv_writer('followers' + id)
    for u in users:
        akt.write_user(u, out)
        print('SName: {}, has {} followers and {} friends'.format(u.screen_name, u.friends_count, u.following))
        print('    Created in: {}, from {}'.format(str(u.created_at), u.location))







api = get_twitter_api_obj()
# my_home_timeline(api)
# get_users_timeline(api, "alsnkline")
# search_tweets(api, "GOP")
get_followers(api, 'GOP')
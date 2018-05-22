"""Exploring twitter's API and collecting data for further analysis
reference https://chatbotslife.com/twitter-data-mining-a-guide-to-big-data-analytics-using-python-4efc8ccfa219
"""

import csv
import time
from datetime import datetime

import tweepy       #http://docs.tweepy.org/en/v3.5.0/api.html

from modules.tweet import AkTweet
from modules.user import AkUser

def get_access_tokens():
    """Loading Twitter API secrets and keys from file."""
    try:
        with open('Access_Data_NO_GIT.csv', 'r') as infile:
            reader = csv.DictReader(infile)
            for r in reader:
                return r
    except Exception as e:
        print('Failed to load App Keys and Secrets: {}'.format(e))
        exit()

def get_twitter_api_obj(keys = None):
    """Creating Tweepy API object using default or provided keys."""
    if not keys:
        keys = get_access_tokens()
    # Creating the authentication object
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    # Setting your access token and secret
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    # Creating the API object while passing in auth information
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) # notification gives wait in secs
    return api

def print_tweets(public_tweets):
    """Print out each tweet in a list of tweets."""
    for tweet in public_tweets:
        print_tweet(tweet)

def print_tweet(tweet):
    """Printing a summary of a tweet object."""
    print('At: {} : {}'.format(tweet.created_at, tweet.text))
    print('   tweeted by : {} from {}'.format(tweet.user.screen_name, tweet.user.location))

def my_home_timeline(api):
    """Get tweets from my timeline."""
    public_tweets = api.home_timeline()
    print_tweets(public_tweets)

def get_users_timeline(api, user_id):
    """Get tweets from provided user_id's timeline and save to .csv."""
    tweets = []
    # get first 200 tweets (200 is max number allowed in one get)
    tweets.extend(api.user_timeline(screen_name=user_id, count=200, tweet_mode='extended'))
    # set max_id to id of last retreved tweet
    max_id = tweets[-1].id - 1

    MAX_TIMELINE_PAGES = 16 # apparantly sometime 17
    cursor = tweepy.Cursor(api.user_timeline, id=user_id, count=200, max_id=max_id, tweet_mode='extended').pages(MAX_TIMELINE_PAGES)
    for i, page in enumerate(cursor):
        print('Obtained ' + str(i+1) + ' tweet pages for user ' + str(user_id) + '.')
        for tweet in page:
            tweets.append(tweet)
        max_id = page[-1].id - 1

    #writing data to csv
    print('Writing {} tweets for {} to file.'.format(len(tweets), user_id))
    akt = AkTweet()
    out = akt.get_tweet_csv_writer(user_id)
    for t in tweets:
        if t.lang != 'en':  # skipping tweets not in english
            continue
        akt.write_tweet(t, out)
        #print_tweet(t)

def get_tweets_from_search(api, query, language="en"):
    """Searching for tweets with provided query and with optional language selection. Saving results to .csv"""
    tweets = []
    # get 500 tweets from 5 pages as we get max 100 tweets per page
    MAX_SEARCH_PAGES = 2
    cursor = tweepy.Cursor(api.search, q=query, lang=language, count=100).pages(MAX_SEARCH_PAGES)
    for i, page in enumerate(cursor):
        print('Obtained ' + str(i+1) + ' tweet pages for search ' + str(query) + '.')
        for tweet in page:
            tweets.append(tweet)

    # writing data to csv
    print('Writing {} tweets for {} to file.'.format(len(tweets), query))
    akt = AkTweet()
    out = akt.get_search_results_tweet_csv_writer(query)
    for t in tweets:
        akt.write_tweet(t, out)

def get_followers(api, user_id):
    """Get followers from the provided user_id and save to .csv."""
    # ~15 pages per rate limit trigger
    MAX_FOLLOWER_PAGES = 30     # returns 6000 followers with one 15 min wait assuming a full allocation is available
    akt = AkUser('Followers', api, user_id)
    get_users_inner(akt, user_id, MAX_FOLLOWER_PAGES, False)

def get_friends(api, user_id):
    """get friends (followed accounts) from provided user_id and save to .csv."""
    # ~14 pages per rate limit trigger
    MAX_FRIEND_PAGES = 14       # returns up to 2800 friends, usually this is everyone
    akuser = AkUser('Friends', api, user_id)
    get_users_inner(akuser, user_id, MAX_FRIEND_PAGES, True)


def get_users_inner(akuser, user_id, max_pages, verbose=False):
    """Inner method, get users from appropiate api then writing them out to .csv"""
    users = []
    cursor = tweepy.Cursor(akuser.api_call, id=user_id, count=200,).pages(max_pages)
    for i, page in enumerate(cursor):
        print('Obtained {} {} pages for user {}.'.format(str(i+1), akuser.desc, user_id))
        for user in page:
            akuser.write_user(user, akuser.out)
            users.append(user)
            if verbose:
                print('SName: {}, is following {} accounts and has {} accounts following them'.format(user.screen_name,
                                                                                                  user.friends_count,
                                                                                                  user.followers_count))
    print('Written {} {} for {} to file {}.'.format(len(users), akuser.desc, user_id, akuser.filename))


api = get_twitter_api_obj()
# my_home_timeline(api)
# get_users_timeline(api, "GOP")
# get_tweets_from_search(api, "pencil")
# get_followers(api, 'NRCC')
get_friends(api, 'L_Faulkner_')
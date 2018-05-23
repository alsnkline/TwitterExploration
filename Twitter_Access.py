"""Exploring twitter's API and collecting data for further analysis
reference https://chatbotslife.com/twitter-data-mining-a-guide-to-big-data-analytics-using-python-4efc8ccfa219
"""

import csv
from datetime import datetime

import tweepy   # http://docs.tweepy.org/en/v3.5.0/api.html

from modules.tweet import AkTweet
from modules.user import AkUser


def get_access_tokens():
    """Loading Twitter API secrets and keys from file.
    :rtype: dictionary
    """
    try:
        with open('Access_Data_NO_GIT.csv', 'r') as infile:
            reader = csv.DictReader(infile)
            for r in reader:
                return r
    except Exception as e:
        print('Failed to load App Keys and Secrets: {}'.format(e))
        exit()


def get_twitter_api_obj(keys=None):
    """Creating Tweepy API object using default or provided keys."""
    if not keys:
        keys = get_access_tokens()
    # Creating the authentication object
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    # Setting your access token and secret
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    # Creating the API object while passing in auth information
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)  # notification gives wait in secs
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
    max_pages = 5       # 16 or sometime 17 return max number of tweets
    cursor = tweepy.Cursor(api.user_timeline, id=user_id, count=200, tweet_mode='extended').pages(max_pages)
    aktweet = AkTweet('Timeline', user_id)
    get_tweets_inner(aktweet, cursor)


def get_tweets_from_search(api, query, language="en"):
    """Searching for tweets with provided query and with optional language selection. Saving results to .csv"""
    # get 500 tweets from 5 pages as we get max 100 tweets per page
    max_pages = 2
    cursor = tweepy.Cursor(api.search, q=query, lang=language, count=100).pages(max_pages)
    aktweet = AkTweet('Search', query)
    get_tweets_inner(aktweet, cursor)


def get_tweets_inner(aktweet, cursor):
    tweets = []
    for i, page in enumerate(cursor):
        now = datetime.now().strftime('%H:%M:%S')
        print('At {}: Obtained {} tweet pages for {}.'.format(now, str(i+1), aktweet.desc))
        for tweet in page:
            tweets.append(tweet)
            aktweet.write_tweet(tweet, aktweet.out)
    print('Written {} tweets for {} to file {}.'.format(len(tweets), aktweet.desc, aktweet.filename))


def get_followers(api, user_id):
    """Get followers from the provided user_id and save to .csv."""
    # ~15 pages per rate limit trigger
    max_pages = 30     # 30 returns 6000 followers with one 15 min wait assuming a full allocation is available
    akuser = AkUser('Followers', api, user_id)
    get_users_inner(akuser, user_id, max_pages, False)


def get_friends(api, user_id):
    """get friends (followed accounts) from provided user_id and save to .csv."""
    # ~14 pages per rate limit trigger
    max_pages = 14       # returns up to 2800 friends, usually this is everyone
    akuser = AkUser('Friends', api, user_id)
    get_users_inner(akuser, user_id, max_pages, True)


def get_users_inner(akuser, user_id, max_pages, verbose=False):
    """Inner method, get users from appropiate api then writing them out to .csv"""
    users = []
    cursor = tweepy.Cursor(akuser.api_call, id=user_id, count=200,).pages(max_pages)
    for i, page in enumerate(cursor):
        now = datetime.now().strftime('%H:%M:%S')
        print('At {}: Obtained {} {} pages for user {}.'.format(now, str(i+1), akuser.desc, user_id))
        for user in page:
            akuser.write_user(user, akuser.out)
            users.append(user)
            if verbose:
                print('SName: {}, is following {} accounts and has {} accounts ' +
                      'following them'.format(user.screen_name, user.friends_count, user.followers_count))
    print('Written {} {} for {} to file {}.'.format(len(users), akuser.desc, user_id, akuser.filename))


# current_api = get_twitter_api_obj()
# my_home_timeline(api)
# get_users_timeline(api, "GOP")
# get_tweets_from_search(current_api, "pencil")
# get_followers(api, 'HouseDemocrats')
# get_friends(api, 'L_Faulkner_')

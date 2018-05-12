# exploring twitter's API reference https://chatbotslife.com/twitter-data-mining-a-guide-to-big-data-analytics-using-python-4efc8ccfa219
import tweepy       #http://docs.tweepy.org/en/v3.5.0/api.html
import csv
import time
from datetime import datetime

def get_access_tokens():
    """Loading App secrets and keys."""
    keys = {}
    with open("Access_Data_NO_GIT.csv", 'r') as infile:
        reader = csv.DictReader(infile)
        for r in reader:
            for k,v in r.items():
                keys[k] = v
                #print('adding {} to keys[{}]'.format(v,k))
    return keys


def get_twitter_api_obj(keys):
    # Creating the authentication object
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    # Setting your access token and secret
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    # Creating the API object while passing in auth information
    api = tweepy.API(auth)
    return api

def print_tweets(public_tweets):
    # foreach through all tweets pulled
    for tweet in public_tweets:
        # printing the text stored inside the tweet object
        print('At: {} : {}'.format(tweet.created_at, tweet.text))
        print('   tweeted by : {} from {}'.format(tweet.user.screen_name, tweet.user.location))


def my_home_timeline(api):
    # Using the API object to get tweets from your timeline, and storing it in a variable called public_tweets
    public_tweets = api.home_timeline()
    print_tweets(public_tweets)


def users_timeline(api, id, tweets_to_pull=5):
    # Calling the user_timeline function with our parameters
    results = api.user_timeline(id=id, count=tweets_to_pull)
    print_tweets(results)

def search_tweets(api, query, language="en"):
    # Calling the search function with our parameters
    results = api.search(q=query, lang=language)
    print_tweets(results)

def getcsvwriter(filename, fields):
    w = csv.DictWriter(open(filename, "w"), fields)
    w.writeheader()
    return w

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print('RateLimetError at : {}, waiting 15 mins...'.format(datetime.now()))
            time.sleep(15 * 60)  #wait 15mins for the limit to refresh

def get_followers(api, id):
    fields=['screen_name','followers_count', 'following', 'created_at', 'location', 'default_profile', 'default_profile_image',\
            'description', 'favourites_count', 'friends_count', 'geo_enabled', 'has_extended_profile', 'lang', 'name',\
            'profile_use_backgroud_image', 'statuses_count']
    out = getcsvwriter('data/followersOf'+id+'.csv', fields)
    rows= {}
    # Calling the paginated followers function with provided parameters
    for followers in limit_handled(tweepy.Cursor(api.followers, id=id).pages()):
        # Calling the followers function with provided parameters
        for fol in followers:
            if fol.lang != 'en':            # skipping followers who don't have english as their set language
                continue
            row = {
                fields[0]: fol.screen_name,
                fields[1]: fol.followers_count,
                fields[2]: fol.following,
                fields[3]: str(fol.created_at),
                fields[4]: fol.location,
                fields[5]: fol.default_profile,
                fields[6]: fol.default_profile_image,
                fields[7]: fol.description,
                fields[8]: fol.favourites_count,
                fields[9]: fol.friends_count,
                fields[10]: fol.geo_enabled,
                fields[11]: fol.has_extended_profile,
                fields[12]: fol.lang,
                fields[13]: fol.name,
                fields[14]: fol.profile_use_background_image,
                fields[15]: fol.statuses_count,
            }
            out.writerow(row)
            print('SName: {}, has {} followers and {} friends'.format(fol.screen_name, fol.friends_count, fol.following))
            print('    Created in: {}, from {}'.format(str(fol.created_at), fol.location))

api = get_twitter_api_obj(get_access_tokens())
# my_home_timeline(api)
# users_timeline(api, "nytimes", 2)
# search_tweets(api, "Toptal")
get_followers(api, 'GOP')
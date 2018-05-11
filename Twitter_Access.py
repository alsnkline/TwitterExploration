# exploring twitter's API reference https://chatbotslife.com/twitter-data-mining-a-guide-to-big-data-analytics-using-python-4efc8ccfa219
import tweepy       #http://docs.tweepy.org/en/v3.5.0/api.html
import csv

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
    # Calling the user_timeline function with our parameters
    results = api.search(q=query, lang=language)
    print_tweets(results)

api = get_twitter_api_obj(get_access_tokens())
# my_home_timeline(api)
# users_timeline(api, "nytimes", 2)
search_tweets(api, "Toptal")
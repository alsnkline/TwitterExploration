# exploring twitter's API reference https://chatbotslife.com/twitter-data-mining-a-guide-to-big-data-analytics-using-python-4efc8ccfa219
# https://gist.github.com/yanofsky/5436496
import tweepy       #http://docs.tweepy.org/en/v3.5.0/api.html
import csv
import time
from datetime import datetime

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
    # Get tweets from a users timeline.

    tweets = []
    # get first 200 tweets (200 is max number allowed in one get)
    tweets.extend(api.user_timeline(screen_name=id, count=200))
    # set max_id to id of last retreved tweet
    max_id = tweets[-1].id - 1

    MAX_TIMELINE_PAGES = 16
    cursor = tweepy.Cursor(api.user_timeline, id=id, count=200, max_id=max_id).pages(MAX_TIMELINE_PAGES)
    i=1
    for page in cursor:
        print('Obtained ' + str(i) + ' tweet pages for user ' + str(id) + '.')
        i += 1
        for tweet in page:
            if not hasattr(tweet, 'retweeted_status'):      # I believe this attr is now the retweeted bool
                tweets.append(tweet)
        max_id = page[-1].id - 1

    #writing data to csv
    out, fields = get_tweet_csv_writer('Timeline'+ id)
    for t in tweets:
        if t.lang != 'en':  # skipping tweets not in english
            continue
        write_tweet(t, out, fields)
        #print_tweet(t)


def search_tweets(api, query, language="en"):
    # Calling the search function
    out, fields = get_tweet_csv_writer('search' + query)
    results = api.search(q=query, lang=language)
    for t in results:
        if t.lang != 'en':  # skipping tweets not in english
            continue
        write_tweet(t, out, fields)
        print_tweet(t)

def write_tweet(t, out, fields):
    row = {
        fields[0]: t.id,
        fields[1]: t.user.screen_name,
        fields[2]: t.in_reply_to_screen_name,
        fields[3]: str(t.created_at),
        fields[4]: t.favorite_count,
        fields[5]: t.favorited,
        fields[6]: t.retweet_count,
        fields[7]: t.retweeted,
        fields[8]: t.truncated,
        fields[9]: t.lang,
        fields[10]: t.text
    }
    out.writerow(row)


def get_tweet_csv_writer(id):
    fields = ['id', 'user.screen_name', 'in_reply_to_screen_name', 'created_at', 'favorite_count', 'favorited',\
              'retweet_count', 'retweeted', 'truncated', 'lang', 'text']
    return (get_csv_writer('init_data/tweets' + id + '.csv', fields), fields)

def get_csv_writer(filename, fields):
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
    out = get_csv_writer('init_data/followersOf' + id + '.csv', fields)
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




#api = get_twitter_api_obj()
# my_home_timeline(api)
#get_users_timeline(api, "GOP")
# search_tweets(api, "GOP")
#get_followers(api, 'GOP')
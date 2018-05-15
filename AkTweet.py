import csv

FIELDS = ['id_str', 'user.screen_name', 'in_reply_to_screen_name', 'created_at', 'favorite_count',\
              'quote_count', 'reply_count', 'retweet_count', 'truncated', 'lang', 'text', 'from']
FILENAME_ROOT = 'init_data/tweets'
# 'favorited' - bool indicating if this tweet been liked by the authenticating user (ie me) so not useful
# 'retweeted' - bool indicating if this tweet been retweeted by the authenticating user (ie me) so not useful
# 'reply_count' and 'quote_count' are not support by the tweepy libarary at this time

class AkTweet(object):
    """A Tweet object, to allow easy and consistent tracking and expansion of fields and writing to file
       https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object"""

    def get_tweet_csv_writer(self, id):
        """create and return a csv writer for tweet data"""
        w = csv.DictWriter(open(FILENAME_ROOT + id + '.csv', "w"), FIELDS)
        w.writeheader()
        return w

    def write_tweet(self, t, out):
        """write a tweet to one row of csv out file"""
        self.__write_row(t, out, ttype='regular')
        if hasattr(t, 'retweeted_status'):
            self.__write_row(t.retweeted_status, out, ttype='from_retweeted_status')
        if hasattr(t, 'quoted_status'):
            self.__write_row(t.quoted_status, out, ttype='from_quoted_status')

    def __write_row(self, t, out, **kwargs):
        text = t.text if hasattr(t, 'text') else t.full_text
        row = {
            FIELDS[0]: t.id_str,                # unique ID (signed 64 bit integer, id_str is safer)
            FIELDS[1]: t.user.screen_name,      # user who posted this Tweet, screen name
            FIELDS[2]: t.in_reply_to_screen_name,# Screen name of orginal tweet's author if its a reply
            FIELDS[3]: str(t.created_at),       # UTC time when tweet was created
            FIELDS[4]: t.favorite_count,        # approx how many times tweet has been liked
            FIELDS[5]: t.quote_count if hasattr(t,'quote_count') else '0',   # approx how many times tweet has been quoted
            FIELDS[6]: t.reply_count if hasattr(t,'reply_count') else '0',   # number of times tweet has been replied too
            FIELDS[7]: t.retweet_count,         # number of times tweet has been retweeted
            FIELDS[8]: t.truncated,             # Has tweet been shortened - if full text available in retweeted_status then set to false
            FIELDS[9]: t.lang,                  # indicates a BCP 47 language identifier eg 'en' or 'und' if none detected
            FIELDS[10]: text,                 # the actual UTF-8 text of the status update
            FIELDS[11]: kwargs['ttype']         # indicator of type of tweet
        }
        out.writerow(row)
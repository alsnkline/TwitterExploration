"""
Provides an AkTweet Class that process a tweepy tweet object into a csv data file
"""

import modules.utils as ut

FIELDS = [
    'id_str',                   # unique ID (signed 64 bit integer, id_str is safer)
    'user.screen_name',         # user who posted this Tweet, screen name
    'in_reply_to_screen_name',  # Screen name of original tweet's author if its a reply
    'created_at',               # UTC time when tweet was created
    'favorite_count',           # approx how many times tweet has been liked
    'quote_count',              # approx how many times tweet has been quoted
    'reply_count',              # number of times tweet has been replied too
    'retweet_count',            # number of times tweet has been retweeted
    'truncated',                # Has tweet been shortened - if full text available in retweeted_status then its false
    'lang',                     # indicates a BCP 47 language identifier eg 'en' or 'und' if none detected
    'text',                     # the actual UTF-8 text of the status update
    'from',                     # indicator of type of tweet
    'tweeted_with'              # id_str of our users tweet for a re-tweet or quoted tweet, None otherwise
]
# Other fields available in raw tweet json not processed and stored in output csv:
# 'favorited' - bool indicating if this tweet been liked by the authenticating user (ie me) so not useful.
# 'retweeted' - bool indicating if this tweet been retweeted by the authenticating user (ie me) so not useful.
# 'reply_count' and 'quote_count' seem not support by the tweepy libarary at this time - possibly issue #946 on github.
TIMELINE_FILENAME_ROOT = 'init_data/tweetsTimeline'
SEARCH_RESULTS_FILENAME_ROOT = 'init_data/searchFor'


class AkTweet(object):
    """Provides the AkTweet Class that process' a Tweepy tweet object into a csv data file.
    Attributes are:
        filename: the .csv filename that output will be saved to.
        desc: a descriptive string used in print statements
        out: the csv_writer used to output user records to file.
    """
    # The Twitter API tweet data dictionary for reference:
    # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
    def __init__(self, call_type, string):
        if call_type is 'Timeline':
            self.filename = TIMELINE_FILENAME_ROOT + string + '.csv'
            self.desc = 'user: ' + string
        elif call_type is 'Search':
            self.filename = SEARCH_RESULTS_FILENAME_ROOT + string + '.csv'
            self.desc = 'query: ' + string
        self.out = ut.get_csv_writer(self.filename, FIELDS)

    def write_tweet(self, t, out):
        """Write a tweet to the csv out file,
        original tweets are in one row, retweeted or quoted tweet are put in a second row."""
        self.__write_row(t, out, ttype='regular', twtd_with='None')
        if hasattr(t, 'retweeted_status'):
            self.__write_row(t.retweeted_status, out, ttype='from_retweeted_status', twtd_with=t.id_str)
        if hasattr(t, 'quoted_status'):
            self.__write_row(t.quoted_status, out, ttype='from_quoted_status', twtd_with=t.id_str)

    def __write_row(self, t, out, **kwargs):
        """Write one row of tweet data to .csv"""
        text = t.text if hasattr(t, 'text') else t.full_text
        row = {
            FIELDS[0]: t.id_str,
            FIELDS[1]: t.user.screen_name,
            FIELDS[2]: t.in_reply_to_screen_name,
            FIELDS[3]: str(t.created_at),
            FIELDS[4]: t.favorite_count,
            FIELDS[5]: t.quote_count if hasattr(t, 'quote_count') else '0',
            FIELDS[6]: t.reply_count if hasattr(t, 'reply_count') else '0',
            FIELDS[7]: t.retweet_count,
            FIELDS[8]: t.truncated,
            FIELDS[9]: t.lang,
            FIELDS[10]: text,
            FIELDS[11]: kwargs['ttype'],
            FIELDS[12]: kwargs['twtd_with'],
        }
        out.writerow(row)

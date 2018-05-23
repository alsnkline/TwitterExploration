"""
Provides an AkUser Class that process a tweepy user object into a csv data file
"""

import modules.utils as ut

FIELDS = [
    'id_str',               # unique ID (signed 64 bit integer, id_str is safer)
    'name',                 # name as user defined it max 20 char
    'screen_name',          # user who posted this Tweet, screen name
    'location',             # user-defined location - may not be a loc or machine parseable
    'description',          # user defined UTF-8 string description of their account
    # 'derived',            # derived consistent geo-data
    'protected',            # when true indicates user has chosen to protect their tweets
    'verified',             # when true indicates user has a verified account
    'followers_count',      # the number of current followers (may be 0 under duress)
    'friends_count',        # the number of users this account is following (may be 0 under duress)
    'listed_count',         # number of public lists this user is a member of.
    'favourites_count',     # number of Tweets this user has liked in the account's lifetime
    'statuses_count',       # number of Tweets (inc retweets) issued by the user
    'created_at',           # UTC datetime that the user account was created on twitter
    'utc_offset',           # The offset from GMT/UTC in seconds
    'geo_enabled',          # when true user has enabled geotagging,
    'lang',                 # The BCP 47 code for user's self declared language
    'profile_use_backgroud_image',  # when true user wants their uploaded background image to be used
    'default_profile',      # When true indicates user has not alterd the theme or background of their profile
    'default_profile_image',  # When true indicates user has not uploaded their own profile image
]
FOLLOWER_FILENAME_ROOT = 'init_data/followersOf'
FRIEND_FILENAME_ROOT = 'init_data/friendsOf'


class AkUser(object):
    """Provides the AkUser Class that process' a tweepy user object into a csv data file.
    Attributes are:
        filename: the .csv filename that output will be saved to.
        desc: a descriptive string used in print statements
        api_call: the tweepy api call used for retreving user data
        out: the csv_writer used to output user records to file.
    """
    # The Twitter API tweet data dictionary for reference:
    # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
    def __init__(self, call_type, api, user_id):
        if call_type is 'Friends':
            self.filename = FRIEND_FILENAME_ROOT + user_id + '.csv'
            self.desc = 'Friends'
            self.api_call = api.friends
        elif call_type is 'Followers':
            self.filename = FOLLOWER_FILENAME_ROOT + user_id + '.csv'
            self.desc = 'Followers'
            self.api_call = api.followers
        self.out = ut.get_csv_writer(self.filename, FIELDS)

    def write_user(self, u, out):
        """write a user to one row of csv out file"""
        self.__write_row(u, out)

    def __write_row(self, u, out):
        """write a user to one row of csv out file"""
        row = {
            FIELDS[0]: u.id_str,
            FIELDS[1]: u.name,
            FIELDS[2]: u.screen_name,
            FIELDS[3]: u.location,
            FIELDS[4]: u.description,
            FIELDS[5]: u.protected,
            FIELDS[6]: u.verified,
            FIELDS[7]: u.followers_count,
            FIELDS[8]: u.friends_count,
            FIELDS[9]: u.listed_count,
            FIELDS[10]: u.favourites_count,
            FIELDS[11]: u.statuses_count,
            FIELDS[12]: str(u.created_at),
            FIELDS[13]: u.utc_offset,
            FIELDS[14]: u.geo_enabled,
            FIELDS[15]: u.lang,
            FIELDS[16]: u.profile_use_background_image,
            FIELDS[17]: u.default_profile,
            FIELDS[18]: u.default_profile_image,
        }
        out.writerow(row)
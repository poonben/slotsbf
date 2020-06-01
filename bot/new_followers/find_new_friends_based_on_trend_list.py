from os import getenv
from random import shuffle, choice
from .waits.med_wait import  med_wait
from .waits.short_wait import short_wait
from .mailer.send_error_email import send_error_email
from tweepy import Cursor, TweepError, API, OAuthHandler


# ---------------------------------------------------------------------------- #
# API key:
api_key = getenv("CONSUMER_KEY")
# API secret key:
api_secret = getenv("CONSUMER_SECRET")
# Access token: 
access_token = getenv("API_KEY")
# Access token secret: 
access_token_secret = getenv("API_SECRET")
# ---------------------------------- Tweepy ---------------------------------- #
# Tweepy 0Auth 1a authentication:
auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
# API Variable:
api = API(auth, wait_on_rate_limit=True)


# ---------------------------------------------------------------------------- #
def pick_random_hashtags(hashtag_list):
    search_list = []
    shuffle(hashtag_list)
    for ht in range(1, 4):
        search_list.append(choice(hashtag_list))
    return search_list

def find_new_friends_based_on_trend_list(trend_list):
    tweet_number = 1
    shuffle(trend_list)
    htlist = pick_random_hashtags(trend_list)
    for trend in htlist:
        try:
            tweets = Cursor(api.search, trend).items(tweet_number)
            for tweet in tweets:
                try:
                    api.create_friendship(tweet.user.id)
                    print(f'-> Followed @{tweet.user.screen_name}!')
                    med_wait()
                except TweepError as error:
                    send_error_email(error)
                    print(f"-> ERROR: {error.reason}")
                    pass
        except TweepError as error:
            print(f"-> Error: {error.reason}")
            send_error_email(error)
            pass 
        med_wait()


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    find_new_friends_based_on_trend_list()
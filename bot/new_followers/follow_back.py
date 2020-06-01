from os import getenv
from random import shuffle
from .waits import short_wait, med_wait
from .mailer import send_error_email
from tweepy import Cursor, TweepError, OAuthHandler, API


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
def follow_back(followers, people_i_follow):
    count = 5
    for person in followers:
        if person not in people_i_follow:
            try:
                api.create_friendship(person)
                user = api.get_user(person)
                print(f"-> Just followed @{user.screen_name}!")
                count -= 1
                if count == 0:
                    "Done following for now."
                    return
                med_wait.med_wait()
            except TweepError as error:
                print(f"-> Error: {error.reason}")
                send_error_email.send_error_email(error)
                pass
        short_wait.short_wait()


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    follow_back()
from os import getenv
from .mailer import send_error_email
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
def find_trending_topics_in_usa():
    #Use this when trying to find trends worldwide
    #try:
        #trends_available = api.trends_available()
    #except TweepError as error:
        #print(f"-> Error: {error.reason}")
        #send_error_email(error)
        #pass
    trending_topic_list = []
    try:
        usa = api.trends_place(23424977)  #USA = 23424977
        for trend_list in usa:
            for (k,v) in trend_list.items():
                for event in v:
                    if isinstance(event, dict):
                        for (a, b) in event.items():
                            if a == 'name':
                                trending_topic_list.append(b)
        return trending_topic_list
    except TweepError as error:
        print(f"-> Error: {error.reason}")
        send_error_email.send_error_email(error)
        pass


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    find_trending_topics_in_usa()

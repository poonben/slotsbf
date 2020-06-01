from os import getenv
from time import sleep
from flask import Flask
from requests import get
from random import choice
from string import digits
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from tweepy import Cursor, TweepError, API, OAuthHandler
# ---------------------------------------------------------------------------- #
from bot.status.pick_status import pick_status
from bot.dms.refresh_dm_db import refresh_dm_db
from bot.mentions.rff import retweet_favorite_follow
from bot.waits import short_wait, med_wait, long_wait
from bot.mailer.send_error_email import send_error_email
from bot.remove import delete_old_tweets, unfollow_nonfollowers
from bot.mentions.refresh_mentions_db import refresh_mentions_db
from bot.hashtags import retweet_hashtags, find_trending_topics_in_usa
from bot.new_followers import find_new_friends_based_on_trend_list, follow_back
from bot.get_friends_and_followers import get_my_followers, get_people_i_follow


# ----------------------------------- Flask ---------------------------------- #
app = Flask(__name__)


# --------------------------------- DB Config -------------------------------- #
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
db = SQLAlchemy(app)
host = getenv('HOST')
port = getenv('PORT')


# -------------------------------- Twitter API ------------------------------- #
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
class TwitterBot:
    def id_generator(size=6, chars=digits):
        return ''.join(choice(chars) for x in range(size))

    #Delete old tweets:
    def remove_old_tweets_from_timeline():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("–=–=– Deleting Old Tweets From Timeline... –=–=–")
        try:
            delete_old_tweets.delete_old_tweets()
        except Exception as error:
            emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
            print(f"-> ERROR @ 'remove_old_tweets_from_timeline': {emsg}")
            try:
                send_error_email(emsg)
            except Exception as error:
                emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
                print(f"-> ERROR @ 'remove_old_tweets_from_timeline'.'send_error_email': {emsg}")
                pass
            pass
        print(f"** Done deleting tweets... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    #Update status from list:
    def post_status():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Picking a status from the list...")
        try:
            status = pick_status()
            api.update_status(status)
            print("-> Status posted!!!")
        except Exception as error:
            emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
            print(f"-> ERROR @ 'post_status': {emsg}")
            try:
                send_error_email(emsg)
            except Exception as error:
                emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
                print(f"-> ERROR @ 'post_status'.'send_error_email': {emsg}")
                pass
            pass
        print("** Done with Status... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    
    #Retweet hashtags from list:
    #Follow users from on search based on same list:
    def retweet_my_hashtags():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Now, I'm searching for hashtag posts to retweet...")
        hashtags = [
            '#dc',
            '#sanfrancisco',
            '#la',
            '#ny',
            '#webdevelopment', 
            '#skateboarding',
            '#WashingtonDC',
            '#sanfrancisco',
            '#losangeles',
            '#dmvmusic', 
            '#coding', 
            '#100daysofcode',
            '#dcrestaurant',
            '#sfrestaurant',
            '#larestaurant',
            '#nyrestaurant',
            '#gamedev',
            '#dcevents',
            '#sfevents',
            '#laevents',
            '#nyevents',
            '#dcnightlife',
            '#lanightlife',
            '#sfnightlife',
            '#nynightlife',
            '#ufc',
            '#gamingnews',
            '#newmusic',
            '#ustreetdc',
            '#techjobs',
        ]
        try:
            retweet_hashtags.retweet_hashtags(hashtags)
            print('•••• Finding people to follow based on your hasthtags: ••••')
            find_new_friends_based_on_trend_list.find_new_friends_based_on_trend_list(hashtags)
        except Exception as error:
            emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
            print(f"-> ERROR @ 'retweet_my_hashtags': {emsg}")
            try:
                send_error_email(emsg)
            except Exception as error:
                emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
                print(f"-> ERROR @ 'retweet_my_hashtags'.'send_error_email': {emsg}")
                pass
            pass
        print("** Done Retweeting... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    #Reply to mentions, favorite those, and follow user:
    def reply_to_mentions_and_follow():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Replying to user's that have mentioned me and following them!")
        # Set all tweets that mention my user to list:
        try:
            retweet_favorite_follow()
        except Exception as error:
            emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
            print(f"-> ERROR @ 'reply_to_mentions_and_follow' : {emsg}")
            try:
                send_error_email(emsg)
            except Exception as error:
                emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
                print(f"-> ERROR @ 'reply_to_mentions_and_follow'.'send_error_email': {emsg}")
                pass
            pass
        print("** Done with mentions... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    #Follow users back:
    def follow_back():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Giving my followers the ol' follow back...")
        try:
            me = api.me().screen_name
            followers = get_my_followers.get_my_followers()
            following = get_people_i_follow.get_people_i_follow()
            follow_back.follow_back(followers, following)
        except Exception as error:
            emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
            print(f"-> ERROR @ 'follow_back': {emsg}")
            try:
                send_error_email(emsg)
            except Exception as error:
                emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
                print(f"-> ERROR @ 'follow_back'.'send_error_email': {emsg}")
                pass
            pass
        print("** Done with 'Follow Back' **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        
    #Unfollow people that don't follow bot:
    def unfollow_nonfollowers():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Unfollowing those that don't me...")
        try:
            me = api.me().screen_name
            followers = get_my_followers.get_my_followers()
            following = get_people_i_follow.get_people_i_follow()
            unfollow_nonfollowers.unfollow_nonfollowers(followers, following)
        except Exception as error:
            emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
            print(f"-> ERROR @ 'unfollow_nonfollowers': {emsg}")
            try:
                send_error_email(emsg)
            except Exception as error:
                emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
                print(f"-> ERROR @ 'unfollow_nonfollowers'.'send_error_email': {emsg}")
                pass
            pass
        print("** Done unfollowing... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    #Find and retweet trending hashtags:
    def retweet_trending_topics():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Now, I'm searching for trending topics in the USA for posts to retweet...")
        try:
            usa_trends = find_trending_topics_in_usa.find_trending_topics_in_usa()
            retweet_hashtags.retweet_hashtags(usa_trends)
        except Exception as error:
            emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
            print(f"-> ERROR @ 'retweet_trending_topics: {emsg}")
            try:
                send_error_email(emsg)
            except Exception as error:
                print(f"-> ERROR @ 'retweet_trending_topics'.'send_error_email': {emsg}")
                pass
            pass
        print("** Done Retweeting... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    #Find users to follow based on hashtag list:
    def follow_trendy_users():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("** Following trendy users: **")
        try:
            trends = find_trending_topics_in_usa.find_trending_topics_in_usa()
            find_new_friends_based_on_trend_list.find_new_friends_based_on_trend_list(trends)
        except Exception as error:
            emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
            print(f"-> ERROR @ 'follow_trendy_users:#{emsg}")
            try:
                send_error_email(emsg)
            except Exception as error:
                print(f"-> ERROR @ 'follow_trendy_users'.'send_error_email': {emsg}")
                pass
            pass
        print("** Done Following trendy users... **")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    
    #Use twitter-to-sqlite to refresh dbs:
    def refresh_db():
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print('Updating DBs... This may take a few mins...')
        try:
            refresh_mentions_db()
            refresh_dm_db()
        except Exception as error:
            emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
            print(f"-> ERROR @ 'refresh_db: {emsg}")
            try:
                send_error_email(emsg)
            except Exception as error:
                emsg = (f"#{TwitterBot.id_generator()} @ {datetime.now()} => {error}")
                print(f"-> ERROR @ 'refresh_db'.'send_error_email': {emsg}")
                pass
            pass
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")


# ---------------------------------- Run Bot --------------------------------- #
if __name__ == "__main__":
    url = 'http://joshbot9000.herokuapp.com/'
    while True:
        print("ººººº Twitter Bot Started! ººººº")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        sleep(2)
        print('┬─┬ノ( º _ ºノ)')
        sleep(2)
        TwitterBot.remove_old_tweets_from_timeline()
        print('(╯°□°)╯︵ ┻━┻')
        TwitterBot.refresh_db()
        TwitterBot.post_status()
        print('┬─┬ノ( ಠ ل͜ಠノ)')
        print("////-------Med Rest Period-------////")
        get(url)
        med_wait.med_wait()
        TwitterBot.retweet_my_hashtags()
        print('(┛ಠ_ಠ)┛彡┻━┻')
        print("////-------Medium Rest Period-------////")
        get(url)
        med_wait.med_wait()
        TwitterBot.follow_back()
        TwitterBot.post_status()
        print('┳━┳ ヽ(ಠل͜ಠ)ﾉ')
        print("////-------Medium Rest Period-------////")
        get(url)
        med_wait.med_wait()
        TwitterBot.retweet_trending_topics()
        print('(╯°Д°)╯︵/(.□ . \)')
        print("////-------Medium Rest Period-------////")
        get(url)
        med_wait.med_wait() 
        TwitterBot.follow_trendy_users()
        TwitterBot.post_status()
        print('(˚Õ˚)ر ~~~~╚╩╩╝')
        print("////-------Medium Rest Period-------////")
        get(url)
        short_wait.short_wait()
        TwitterBot.unfollow_nonfollowers()
        print('┏━┓┏━┓┏━┓ ︵ /(^.^/)')
        print("////-------Medium Rest Period-------////")
        get(url)
        short_wait.short_wait()
        TwitterBot.reply_to_mentions_and_follow()
        print('┻━┻︵ \(°□°)/ ︵ ┻━┻')
        print("////-------Medium Rest Period-------////")
        get(url)
        med_wait.med_wait()
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Getting ready to start again!")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print('┏━┓┏━┓┏━┓ ︵ /(^.^/)')
        print("////-------Long Rest Period-------////")
        get(url)
        long_wait.long_wait()
        
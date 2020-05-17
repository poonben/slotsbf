import tweepy
from time import sleep
from random import choice, shuffle
from os import getenv, system
import sqlite3
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from models import Tweets, MentionsTweets, Users
from requests import get
from datetime import datetime, timedelta
# ----------------------------------- Flask ---------------------------------- #
app = Flask(__name__)

# --------------------------------- DB Config -------------------------------- #
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
db = SQLAlchemy(app)

# ------------------------------------- - ------------------------------------ #
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
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
# API Variable:
api = tweepy.API(auth, wait_on_rate_limit=True)

# ------------------------------------- - ------------------------------------ #
class Logic:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def short_wait(): #0.5 mins - 1 min
        #Set list of nums for random sleep time:
        sleep_nums = [num for num in range(30, 61)]
        #Return a random sleep time:
        return sleep(choice(sleep_nums))

    def med_wait(): #5 mins - 10 mins
        #Set list of nums for random sleep time:
        sleep_nums = [num for num in range(300, 601)]
        #Return a random sleep time:
        return sleep(choice(sleep_nums))

    def long_wait(): #30 min - 60 mins
        #Set list of nums for random sleep time:
        sleep_nums = [num for num in range(1800, 3600)]
        #Return a random sleep time:
        return sleep(choice(sleep_nums))

    def delete_old_tweets():
        days_to_keep = 5
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        tweets_to_save = []
        print("¨…¨…¨Retrieving timeline tweets¨…¨…¨")
        timeline = tweepy.Cursor(api.user_timeline).items()
        deletion_count = 0
        ignored_count = 0
        print(f"Cutoff date is: {cutoff_date}. The following tweets are being deleted:")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        for t in timeline:
            try:
                if t.id not in tweets_to_save and t.created_at < cutoff_date:
                    print(f"-> Deleted {t.id} created {t.created_at}")
                    api.destroy_status(t.id)
                    deletion_count += 1
                else:
                    ignored_count += 1
            except tweepy.TweepError as error:
                print("-> Couldn't update your status this time around.")
                print(f"-> Error: {error.reason}")
        print(f"¨…¨…¨Deleted {deletion_count} tweets from user-timeline¨…¨…¨")
        print(f"¨…¨…¨Ignored {ignored_count} tweets¨…¨…¨")
        print(f"≤≤≤ Done deleting tweets ≥≥≥")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    def pick_status():
        status_options = [
            "(┛ಠ_ಠ)┛彡┻━┻",
            "Check out my creator's portfolio here: https://jharriswebdev.herokuapp.com/ #freelance #webdeveloper #coding #100DaysOfCode",
            "My creator is kind of funny, too. Check him out: @jheeeeezy #bot",
            "@jheeeeezy is the one that created me! Check him out!",
            "Beep boop boop bmmmmmmmmm *~*laser sounds*~* beep",
            "Best bot in the biz, baby! #bot #webdev #coding #python",
            "*- Does robot dance to future music -*",
            "Share a meme with me!",
            "@jheeeeezy .... --- .--     -- .- -. -.--     .--. . --- .--. .-.. .     .- .-. .     --. --- .. -. --.     - ---     - .-. .- -. ... .-.. .- - .     - .... .. ...     .--- ..- ... -     - ---     ..-. .. -. -..     .. - ...     .--- ..- ... -     - .... .. ...     --.- ..- . ... - .. --- -. ··--··",
            "これは英語ではありません！",
            "@jheeeeezy can create a bot for you, too! #bot #freelance #hitmeup #work",
            "https://jharriswebdev.herokuapp.com/ #freelance #webdev",
        ]
        return choice(status_options)

    def retweet_hashtags(hashtag_list):
        shuffle(hashtag_list)
        for hashtag in hashtag_list:
            tweetNumber = 3
            tweets = tweepy.Cursor(api.search, hashtag).items(tweetNumber)
            for tweet in tweets:
                try:
                    tweet.retweet()
                    print("-> Retweet Done!")
                    Logic.short_wait()
                except tweepy.TweepError as error:
                    print(error.reason)
                    pass
                Logic.med_wait()

    def retweet_favorite_follow(mention_list, following):
        id_list = []
        #Get my screen name:
        me = api.me().screen_name
        #Get mentions from DB:
        mentions_in_db = MentionsTweets.query.all()
        #Loop thorugh mentions in db:
        for ment in mentions_in_db:
            id_list.append(ment.tweet)
        #print(id_list)
        #Loop thorugh mention_list from args:
        for mention in reversed(mention_list):
            #print(mention.id)
            if mention.user.screen_name != me and mention.id not in id_list:
                #print(mention.id)
                try:
                    #Reply to mention:
                    api.update_status("Thanks for then mention, @" + mention.user.screen_name + ". I'll forward this to my creator, @jheeeeezy for you! Follow me in the meantime!", mention.id)
                    #print(f"This is a bot, @{mention.user.screen_name}. I'll forward this to my creator, @jheeeeezy for you! Follow me back!")
                    #Favorite mention:
                    api.create_favorite(mention.id)
                    #print(f"Favorited {mention.id}")
                    #Retweet mention:
                    api.retweet(mention.id)
                    #print(f"Retweeted {mention.id}")
                    #Rest
                    Logic.short_wait()
                except tweepy.TweepError as error:
                    print(f"-> Error: {error.reason}")
                    pass
                except AttributeError:
                    pass
            if mention.user not in following:
                try:
                    api.create_friendship(mention.user.screen_name)
                    print(f"-> Just followed @{mention.user.screen_name}!")
                    Logic.short_wait()
                except tweepy.TweepError as error:
                    print(f"-> Error: {error.reason}")
                    pass
        #Update mentions in database:
        system('twitter-to-sqlite mentions-timeline twitter.db')
        print("Updated mentions db...")
    
    def follow_back(followers, people_i_follow):
        for person in followers:
            if person not in people_i_follow:
                try:
                    api.create_friendship(person)
                    user = api.get_user(person)
                    print(f"-> Just followed @{user.screen_name}!")
                except tweepy.TweepError as error:
                    print(f"-> Error: {error.reason}")
                    pass
            elif person in people_i_follow:
                user = api.get_user(person)
                print(f"-> You already follow @{user.screen_name}.")
    
    def unfollow_nonfollowers(followers, people_i_follow):
        for person in people_i_follow:
            if person not in followers:
                try:
                    user = api.get_user(person)
                    print(f"-> {user.screen_name} not in followers")
                    api.destroy_friendship(person)
                    print(f"-> Unfollowed @{user.screen_name}...")
                except tweepy.TweepError as error:
                    print(f"-> Error: {error.reason}")
                    pass

    def refresh_usertimeline_db():
        system('twitter-to-sqlite user-timeline twitter.db')

    def get_people_i_follow():
        following = api.friends()
        following_id_list = []
        for page in tweepy.Cursor(api.friends_ids).pages():
            following_id_list.extend(page)
        return following_id_list 

    def get_my_followers():
        followers = api.followers()
        follower_id_list = []
        for page in tweepy.Cursor(api.followers_ids).pages():
            follower_id_list.extend(page)
            sleep(10)
        return follower_id_list
        
   
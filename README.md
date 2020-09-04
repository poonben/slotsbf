# Josh Bot 2.0 Under Development: https://github.com/jharris711/josh-bot-2.0

# josh_bot_9000
An automated Twitter bot, created with Python 3 and Tweepy. Hosted on Heroku, running 24/7. Auto reply, like and favorite when mentioned. Auto-retweet specified hashtags. Posts status updates. Follows the users that follow the bot. Unfollows those not found in followers list. Deletes old tweets. Finds trends in USA and follows trendy users. Errors sent to gmail through smtp. Messages coming soon.

To host your own on Heroku:

-> Edit the hashtags, statuses, and anything else you want to customize.

-> Get your Keys and Tokens from https://developer.twitter.com/apps

-> Create an app on Heroku

-> Set the keys and tokens from Twitter as follows in your .env and in the Environment settings on Heroku:
```
CONSUMER_KEY=<Consumer API Key goes here>
CONSUMER_SECRET=<Consumer API Secret goes Here>
API_KEY=<Access token goes here>
API_SECRET=<Access token secret goes here>
SQLALCHEMY_DATABASE_URI=sqlite:///twitter.db
SQLALCHEMY_TRACK_MODIFICATIONS=False
SENDER_EMAIL=<Your Gmail goes here> **Must be gmail unless you change the smtp type**
SENDER_PW=<Your Gmail PW>
REC_EMAIL=<Where you want to send emails about errors>
```

-> For the error mailer to work, make sure you allow 'Less secure app' access in your gmail setting!

-> Create the Github Repo where you plan on keeping the code for this bot.

-> Connect Heroku to your Github Repo in the deployment section on Heroku's dashboard and setup auto builds.

-> Watch the logs to see your bots progress and watch it flip tables!

In order to keep the bot running and avoid the free dynos provided by heroku from idling, register you app at http://kaffeine.herokuapp.com/

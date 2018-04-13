from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
from config import *

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

selected_user = 'WSJ'

print('Getting data for user: '+selected_user)

item = auth_api.get_user(selected_user)

print("name: " + item.name)
print("screen_name: " + item.screen_name)
print("description: " + item.description)
print("statuses_count: " + str(item.statuses_count))
print("friends_count: " + str(item.friends_count))
print("followers_count: " + str(item.followers_count))


#stuff = auth_api.user_timeline(screen_name = item.screen_name, count = 100, include_rts = True)
#print('More info:')
# print(stuff)

# Calculate the average number of tweets per day

tweets = item.statuses_count
account_created_date = item.created_at
delta = datetime.utcnow() - account_created_date
account_age_days = delta.days
print("Account age (in days): " + str(account_age_days))

print("Account age (in years): " + str(account_age_days/365))

if account_age_days > 0:
    print("Average tweets per day: " + "%.2f" %
          (float(tweets)/float(account_age_days)))

# Url from a single tweet by WSJ
# https://twitter.com/i/web/status/984269901333450753 <-- TWEET ID


# Not working
hashtags = []
mentions = []
tweet_count = 0
end_date = datetime.utcnow() - timedelta(days=30)
for status in Cursor(auth_api.user_timeline, id=selected_user).items():
    tweet_count += 1
    if hasattr(status, "entities"):
        entities = status.entities
        if "hashtags" in entities:
            for ent in entities["hashtags"]:
                if ent is not None:
                    if "text" in ent:
                        hashtag = ent["text"]
                        if hashtag is not None:
                            hashtags.append(hashtag)
        if "user_mentions" in entities:
            for ent in entities["user_mentions"]:
                if ent is not None:
                    if "screen_name" in ent:
                        name = ent["screen_name"]
                        if name is not None:
                            mentions.append(name)
    if status.created_at < end_date:
        break

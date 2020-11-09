import datetime as datetime
import time

import pandas as pd
import tweepy as twitter
import GetOldTweets3 as got

from config import keys

# Twitter Authentication
auth = twitter.OAuthHandler(keys['ApiKey'], keys['ApiSecretKey'])
auth.set_access_token(keys['AccessToken'], keys['ApiSecretToken'])
api = twitter.API(auth, wait_on_rate_limit=True)

# Time variable to calculate how long it takes for program to run
startTime = time.time()

# Date 6 days ago
# Wanted to use data further than 6 days ago, However the library im using doesnt allow that unfortunately
# 12 hours later -- Found a library that gets old Tweets.
today = datetime.datetime.now()
startDate = "2020-04-{}"


# Function takes in start date, the amount of tweets we want to return and the file we want to write to.
# the reason we use files is because twitter has a limit to the amount of requests we can make per minute, so in order
# to bypass wait times for a large set of tweets we can just write a bunch of data to a file and read it back when we want to perform sentiment analysis
def loadData(start, items, filename):
    results = [status for status in
               twitter.Cursor(api.search, q="#Coronavirus OR #COVID-19 -filter:retweets", encoding='utf-8', until=start,
                              show_user=True, tweet_mode='extended', lang='en').items(items)]
    pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'display.max_colwidth',
                  None)
    df = pd.DataFrame(columns=['Date', 'Username', 'Name', 'Location', 'Followers', 'Text'])

    # Holds count of the amount of tweets we have, used as an index for our Pandas Data frame.
    result_count = 0

    # Each status object in reults is a different tweet
    # We iterate through them with the loop below
    for tweet in results:
        user = tweet.user

        # Date and time tweet was created
        date = tweet.created_at

        # Twitter Handle
        username = '@{}'.format(user.screen_name)

        # Name of user
        name = user.name

        # Amount of followers
        followers = user.followers_count

        # Tweet text content
        text = tweet.full_text.replace("\n", " ")

        # location of twitter user, determined by the location set in the users settings
        location = user.location

        # inputs a row of data per tweet into the data frame
        df.loc[result_count] = pd.Series(
            {'Date': date, 'Username': username, 'Name': name, 'Location': location, 'Followers': followers,
             'Text': text})

        result_count += 1

    df.to_csv(filename, index=False)

def loadOldTweets(start, endTime, items):
    # Querys old tweets
    tweetCriteria = got.manager.TweetCriteria().setSince(start).setUntil(endTime).setQuerySearch(
        "Coronavirs OR COVID-19 -filter:retweets").setMaxTweets(items).setLang("en")

    pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None,'display.max_colwidth',None)
    df = pd.DataFrame(columns=['Date', 'Text'])

    result_count = 0
    for i in range(items):
        try:
            tweet = got.manager.TweetManager.getTweets(tweetCriteria)[i]
            print(i)
        except:
            break
        date = tweet.date
        text = tweet.text
        df.loc[result_count] = pd.Series({'Date': date,'Text': text})
        result_count +=1

    df.to_csv("{}.csv".format(endTime),index=False)


# Loads Our CSV files. UNCOMMENT NEXT TWO LINES to use data from current day and 7 days ago. may take many many hours depending on the amount of tweets were fetching
# loadDataFromDates(startDate.format(today.day-6), 30000, "NAME OF FILE") --> loads csv file with 30000 tweets from 6-7 days ago
# loadDataFromDates(startDate.format(today.day), 30000, "NAME OF FILE") --> loads csv file with 30000 tweets from today

# Loads the weeks with 50 tweets each, can be changed however twitter limits the amount of tweets received
# loadOldTweets("2020-01-30","2020-01-31",50)
# loadOldTweets("2020-02-06","2020-02-07",50)
# loadOldTweets("2020-02-13","2020-02-14",50)
# loadOldTweets("2020-02-20","2020-02-21",50)
# loadOldTweets("2020-02-27","2020-02-28",50)
# loadOldTweets("2020-03-02","2020-03-03",50)
# loadOldTweets("2020-03-09","2020-03-10",50)
# loadOldTweets("2020-03-16","2020-03-17",50)
# loadOldTweets("2020-03-23","2020-03-24",50)
# loadOldTweets("2020-03-31","2020-04-01",50)
# loadOldTweets("2020-04-07","2020-04-08",50)
# loadOldTweets("2020-04-14","2020-04-15",50)
# loadOldTweets("2020-04-21","2020-04-22",50)

# Time elapsed
print(time.time() - startTime)

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from textblob import TextBlob <-- dont like this library as much as Vader, doesnt seem as consistent
# Attempted to use NLTK, found it was more difficult to use than I had intended and decided to stick with Vader

pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'display.max_colwidth',
              None)


def getSentimentValues(text):

    analyzer = SentimentIntensityAnalyzer()
    compoundSum = 0
    negTweets = 0
    posTweets = 0
    neuTweets = 0

    for text in text['Text']:
        vs = analyzer.polarity_scores(text)
        compoundSum += vs['compound']
        if vs['compound'] < 0:
            negTweets += 1
        elif vs['compound'] > 0:
            posTweets += 1
        else:
            neuTweets += 1

    try:
        newComp = compoundSum / (posTweets + negTweets)
    except Exception as e:
        print(e)

    return [negTweets, neuTweets, posTweets, newComp]


# Pandas dataframes of tweets
text4_18 = pd.read_csv("Data_4-18.csv")[['Location','Text']]
text4_25 = pd.read_csv("Data_4-25.csv")[['Location','Text']]

weeks = [pd.read_csv("2020-01-31.csv")[['Date', 'Text']],
         pd.read_csv("2020-02-07.csv")[['Date', 'Text']],
         pd.read_csv("2020-02-14.csv")[['Date', 'Text']],
         pd.read_csv("2020-02-21.csv")[['Date', 'Text']],
         pd.read_csv("2020-02-28.csv")[['Date', 'Text']],
         pd.read_csv("2020-03-03.csv")[['Date', 'Text']],
         pd.read_csv("2020-03-10.csv")[['Date', 'Text']],
         pd.read_csv("2020-03-17.csv")[['Date', 'Text']],
         pd.read_csv("2020-03-24.csv")[['Date', 'Text']],
         pd.read_csv("2020-04-01.csv")[['Date', 'Text']],
         pd.read_csv("2020-04-08.csv")[['Date', 'Text']],
         pd.read_csv("2020-04-15.csv")[['Date', 'Text']],
         pd.read_csv("2020-04-22.csv")[['Date', 'Text']],
         ]


sentimentText4_18 = getSentimentValues(text4_18)
sentimentText4_25 = getSentimentValues(text4_25)

sentimentScores = []
for texts in weeks:
    sentimentScores.append(getSentimentValues(texts))

# 4 SENTIMENT VALUES
# VALUE 1 : NUMBER OF NEGATIVE TWEETS
# VALUE 2 : NUMBER OF NEUTRAL TWEETS
# VALUE 3 : NUMBER OF POSITIVE TWEETS
# VALUE 4 : TOTAL COMPOUND SCORE OF DATA SET

print("Sentiment for 30,000 tweets april 18", sentimentText4_18)
print("Sentiment for 30,000 tweets april 25", sentimentText4_25)
print("Sentiment for 50 tweets 2020-01-31: Week 0", sentimentScores[0])
print("Sentiment for 50 tweets 2020-02-07: Week 1", sentimentScores[1])
print("Sentiment for 50 tweets 2020-02-14: Week 2", sentimentScores[2])
print("Sentiment for 50 tweets 2020-02-21: Week 3", sentimentScores[3])
print("Sentiment for 50 tweets 2020-02-28: Week 4", sentimentScores[4])
print("Sentiment for 50 tweets 2020-03-03: Week 5", sentimentScores[5])
print("Sentiment for 50 tweets 2020-03-10: Week 6", sentimentScores[6])
print("Sentiment for 50 tweets 2020-03-17: Week 7", sentimentScores[7])
print("Sentiment for 50 tweets 2020-03-24: Week 8", sentimentScores[8])
print("Sentiment for 50 tweets 2020-04-01: Week 9", sentimentScores[9])
print("Sentiment for 50 tweets 2020-04-08: Week 10", sentimentScores[10])
print("Sentiment for 50 tweets 2020-04-15: Week 11", sentimentScores[11])
print("Sentiment for 50 tweets 2020-04-22: Week 12", sentimentScores[12])

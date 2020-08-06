from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt
import re
import config

def percent(part, whole):
    return 100 * (float(part) / float(whole))

def clean_tweet(tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())     

def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet.text))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'       


auth = tweepy.OAuthHandler(config.API_Key, config.API_Secret)
auth.set_access_token(config.accessToken, config.accessTokenSecret)
api = tweepy.API(auth)

searchTerm = input("Enter keywords/hashtag for searching: ")
count = int(input("Enter how many tweets to analyse: "))

fetched_tweets = api.search(q=searchTerm, count=count)

tweets = []

for tweet in fetched_tweets:
    parsed_tweets = {}
    parsed_tweets['text'] = tweet.text
    parsed_tweets['sentiment'] = get_tweet_sentiment(tweet)
    tweets.append(parsed_tweets)

pos_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
neg_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
neu_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']

pos_percent = percent(len(pos_tweets), len(tweets))
neg_percent = percent(len(neg_tweets), len(tweets))
neu_percent = percent(len(neu_tweets), len(tweets))

names = ['Positive', 'Negative', 'Neutral']
data = [pos_percent, neg_percent, neu_percent]

print(data)

plt.pie(data, labels=names, autopct='%1.2f')
plt.legend(names, title="Tweets")
plt.show()
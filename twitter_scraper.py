import tweepy
import json
import datetime
import time

time.sleep(3)

#Sentiment Analyzer

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()


# Importing Keys

with open('keys.json') as keysfile:
	keys = json.load(keysfile)


#adding support for sentiment analysis of multiple stoinks

Total = {
	"total_sentiment": 0.0,
	"Stocks_analized": 0
}

Stocks = {
	"$GME": {
		"total_sentiment": 0.0,
		"Stocks_analized": 0
	},
	"$TSLA": {
		"total_sentiment": 0.0,
		"Stocks_analized": 0
	},
}

# Setting up Tweepy (Twitter API Wrapper for python)

auth = tweepy.OAuthHandler(keys['API_Key'], keys['API_Secret_Key'])
auth.set_access_token(keys['Access_Token'], keys['Access_Token_Secret'])

api = tweepy.API(auth)


# Getting the text of a status, including retweets.

def get_status_full_text(status):
	if 'extended_tweet' in status.__dict__.keys():
		return status.extended_tweet['full_text'] # extended text
	elif 'retweeted_status' in status.__dict__.keys():
		if "full_text" in status.retweeted_status.__dict__.keys():
			return status.retweeted_status.full_text #retweet full text
		else:
			if status.retweeted_status.truncated:
				return status.retweeted_status.extended_tweet['full_text'] # Retweet extended text full text
			else:
				return status.text #retweet normal text
	else:
		return status.text

import tweepy 
import sys
import pymongo

consumer_key="7UA87U6yIVRoatFWn6ybNdK6i"
consumer_secret="gEUeeh4KLifPjY5FkrGjLAxKmvedxhIDVPlZreB0FnKOXjWHOt"

access_token="15932807-PbbpeqO6vzwr8yrFa9wZhwWgWGe6mcRrRjv0NngnH"
access_token_secret="pfwcDn56cE0RQnhIRaTHZ2DX2RFooCuwBPfwf1yMVqtY1"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
	def __init__(self, api):
		self.api = api
		super(tweepy.StreamListener, self).__init__()

		self.db = pymongo.MongoClient().Ebolag

	def on_status(self, status):
		print status.text ,"\n"

		data = {}
		data['text'] = status.text
		data['created_at'] = status.created_at
		data['geo'] = status.geo
		data['source'] = status.source

		self.db.Tweets.insert(data)

	def on_error(self, status_code):
		print >> sys.stderr, "error with status code:", status_code
		return True 

	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(track=['canucks'])
import tweepy 
import sys
import pymongo


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
import twitter_pb2
from sets import Set
from collections import Counter

tweets = twitter_pb2.Tweets()

f = open('twitter.pb', "rb")
tweets.ParseFromString(f.read())

# Find the number of deleted messages in the dataset.
count = 0
for tweet in tweets.tweets:
	if tweet.is_delete:
		count += 1

print count
# answer is 1554!

# Find the number of tweets that are replies to another tweet in this dataset.
tweet_id_set = Set()
for tweet in tweets.tweets:
	if not tweet.is_delete:
		tweet_id_set.add(tweet.insert.id)

count = 0
for tweet in tweets.tweets:
	if not tweet.is_delete and tweet.insert.reply_to in tweet_id_set:
		count += 1

print count
#answer is 17!


# Find the five uids that have tweeted the most.
uid_tweet_counter = Counter()

for tweet in tweets.tweets:
	if not tweet.is_delete:
		uid_tweet_counter[tweet.insert.uid] += 1

print uid_tweet_counter.most_common(5)
#answer is [(1269521828L, 5), (392695315L, 4), (424808364L, 3), (1706901902L, 3), (1471774728L, 2)]



# Find the names of the top five places by number of tweets. (Tweets may have a "place" attribute that describes where the tweet is from).
place_tweet_counter = Counter()

for tweet in tweets.tweets:
	if not tweet.is_delete and tweet.insert.place.name != "":
		place_tweet_counter[tweet.insert.place.name] += 1

print place_tweet_counter.most_common(5)
#answer is [(u'T\xfcrkiye', 4), (u'Gambir', 3), (u'Mississippi', 2), (u'Malalayang', 2), (u'Nongsa', 2)]

f.close()
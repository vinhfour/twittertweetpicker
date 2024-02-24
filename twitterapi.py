import tweepy
import os
from random import sample

client = tweepy.Client(os.environ["API_KEY"])


def get_retweeters(id):
	"""
	Takes in tweet id and returns a dictionary of the # of eligible retweets and the list of users.
	"""
	#Request two pages from Twitter API each up to 100 retweets and add up the count and data from each page
	#Requesting first page
	page = client.get_retweeters(id)
	list_of_users = []
	count = 0
	if(page.data is not None):
		list_of_users = page.data
		count = page.meta["result_count"]
		if("next_token" in page.meta):
			next_token = page.meta["next_token"]
			#Requesting second page using the next_token
			page = client.get_retweeters(id, pagination_token=next_token)
			if(page.data is not None):
				list_of_users += page.data
				count += page.meta["result_count"]
			
	return {"count": count , "list_of_users" : list_of_users}



def pick_retweeters(list_of_users,n):
	"""
	Takes in a list of users and picks n random users from the list.
	"""
	picked_users = sample(list_of_users, n)
	return picked_users	
	


def filter_quote_retweets(list_of_qrt, keyword):
	"""
	Takes in a list of tweets and filter those tweets by a keyword 
	and return a new list of tweets containing only those keywords
	"""
	new_list = []
	for qrt in list_of_qrt:
		if keyword.lower() in qrt.text.lower():#case insensitive
			new_list.append(qrt)
	return new_list


def get_quote_retweeters(id, keyword):			
	"""
	Takes in a tweet id and a keyword to filter only quote retweets containing that keyword.
	Returns count of eligible tweets and a list of users where each user is a dictionary object of their username and text.
	"""
	#This function requests the API twice, each time returns up to 100 results
	page = client.get_quote_tweets(id, expansions="author_id", tweet_fields=["author_id"], max_results=100)#Ask twitter API to include the author_id of the quote tweets and include additional user information about a user that will be stored in includes["users"]
	q_tweets = []
	userObjs = []#will store the additional user information here
	if(page.data is not None):
		q_tweets = page.data
		userObjs = page.includes["users"]
		if("next_token" in page.meta):
			next_token = page.meta["next_token"]
			page = client.get_quote_tweets(id, expansions="author_id", tweet_fields=["author_id"], max_results=100, pagination_token=next_token)
			if(page.data is not None):
				q_tweets += page.data
				userObjs += page.includes["users"]	
	#check to see if the user wants to filter by any keyword
	if(keyword != ""):
		q_tweets = filter_quote_retweets(q_tweets, keyword)
	users = []
	#For each tweet, loop through the user objects to check the tweet author_id against the user object id to find the author's username
	for t in q_tweets:
		for u in userObjs:
			if t.author_id == u.id:
				users.append({"username" : u.username, "text": t.text})
				break

	return {"count": len(users) , "list_of_users" : users}



def get_hashtag_tweets(hashtag):
	"""
	Takes in a hashtag and builds a query that excludes retweets and sends it to the Twitter API.
	Returns the count of eligible users and a list of dictionary objects that hjolds the username and the text of tweet
	"""
	query = hashtag + " -is:retweet"
	#Requests two pages of information from the twitter api
	page = client.search_recent_tweets(query,expansions="author_id", tweet_fields=["author_id"], max_results=100)
	tweets = []
	userObjs = []
	if(page.data is not None):
		tweets = page.data
		userObjs = page.includes["users"]
		if("next_token" in page.meta):
			next_token = page.meta["next_token"]
			page = client.search_recent_tweets(query,expansions="author_id", user_fields="username", tweet_fields=["author_id"], max_results=100, next_token=next_token)
			if(page.data is not None):
				tweets += page.data
				userObjs += page.includes["users"]	
	users = []
	#Maps userid from tweet to username
	for t in tweets:
		for u in userObjs:
			if t.author_id == u.id:
				users.append({"username" : u.username, "text": t.text})
				break

	return {"count": len(users) , "list_of_users" : users}



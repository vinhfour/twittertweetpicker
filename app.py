from flask import Flask, render_template, request, url_for
from twitterapi import get_retweeters, pick_retweeters, get_quote_retweeters, get_hashtag_tweets
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
	"""
	Renders the index page when user submits form for get retweeters	
	"""
	winners = []
	if(request.method == "POST"):
		url = request.form["url"].strip()#strip leading and trailing whitespaces from input
		num_of_winner = int(request.form["num"])
		#split the url to get the last element (tweet id)
		split_url = url.split("/")
		size = len(split_url)
		results = get_retweeters(split_url[size-1])#pass in the tweet id
		if(results["count"] == 0):
			winners = ["No winners. There are no retweets."]
		else:
			if(num_of_winner > results["count"]):
				winners = ["ERROR! Number of winners exceed # of qualified retweets"]
			else:
				winners = pick_retweeters(results["list_of_users"], num_of_winner)

		return render_template("index.html", count=results["count"], winners=winners)	
	else:
		return render_template("index.html")

@app.route("/quote_retweets", methods=["POST"])
def quote_retweets():
	"""
	Renders the index page when user submits form for get quote retweets
	"""
	winners = []
	#remove all leading and trailing whitespace from input
	url = request.form["url2"].strip()
	keyword = request.form["keyword"].strip()
	num_of_winner = int(request.form["num2"])
	split_url = url.split("/")
	size = len(split_url)
	results = get_quote_retweeters(split_url[size-1], keyword)#pass in the tweet id and the keyword to filter
	if(results["count"] == 0):
		winners = ["No winners. There are no retweets."]
	else:
		if(num_of_winner > results["count"]):
			winners = ["ERROR! Number of winners exceed # of qualified retweets"]
		else:
			winners = pick_retweeters(results["list_of_users"], num_of_winner)
	return render_template("index.html", count=results["count"], q_winners=winners)


@app.route("/hashtag_tweets", methods=["POST"])
def hashtag_tweets():
	"""
	Renders the index page when user submits form for get tweets by hashtag
	"""
	winners = []
	hashtag = request.form["hashtag"].strip()
	#Ensures user has the hashtag in their input
	if(hashtag[0] != "#"):
		winners = ["Invalid Hashtag. See example hashtag."]
		return render_template("index.html", count=0, q_winners=winners)
	else:
		num_of_winner = int(request.form["num3"])
		results = get_hashtag_tweets(hashtag)
		if(results["count"] == 0):
			winners = ["No winners. There are no tweets with that hashtag."]
		else:
			if(num_of_winner > results["count"]):
				winners = ["ERROR! Number of winners exceed # of qualified retweets"]
			else:
				winners = pick_retweeters(results["list_of_users"], num_of_winner)
		return render_template("index.html", count=results["count"], q_winners=winners)


if __name__ == "__main__":
	app.run(host='0.0.0.0')




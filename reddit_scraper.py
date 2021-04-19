import praw
import requests
import json
import time
import re

reddit = praw.Reddit("stonks")

#   Use this to get the most recent Reddit posts
#   Will only return up to 250 posts and does NOT support pagination
def search_reddit_titles(ticker):
    relevantData = []

    for submission in reddit.subreddit("all").search("title:"+ticker, "new", limit=250):
        relevantData.append([submission.title, submission.selftext, submission.created_utc])
    
    return relevantData

#   Use this method to get historical Reddit posts in batches by the hundred
#   timePage should be in Unix epoch format (round to int if needed)
def search_pushshift_titles(ticker, size, timePage):
    relevantData = []

    if timePage == 0:
        timePage = round(time.time())

    search_url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(ticker)+'&size=100&author=![deleted]&is_self=true&before='
    i = 0

    while i < size:
        r = requests.get(search_url + str(timePage))

        data = json.loads(r.text)

        for submission in data["data"]:
            if hasContent(submission) and i < size:
                selftext = re.sub(r"\[(.*?)\)|http\S+", "", str(submission["selftext"]))
                relevantData.append([str(submission["title"]), selftext, submission["created_utc"]])
                i += 1

        if len(data["data"]) % 100 > 0: #   If API returns < 100 posts, we reached the end so stop searching
            print("Out of posts!")
            break

        timePage = round(data["data"][-1]["created_utc"])

    print(str(len(relevantData)))

    return relevantData

def hasContent(submission):
    if "selftext" in submission:    #   Some posts don't even have a selftext field, so check first
        selftext = submission["selftext"]
        selftext = selftext.replace("[removed]", "")
        selftext = selftext.replace("[deleted]", "")
        selftext = re.sub(r"\[(.*?)\)|http\S+", "", selftext)
        return len(selftext) > 0

    return False
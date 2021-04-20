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
        if hasContent(submission, "reddit"):
            selftext = re.sub(r"\[(.*?)\)|http\S+", "", submission.selftext)
            relevantData.append([submission.title, selftext, submission.created_utc])
    
    return relevantData

#   Use this method to get historical Reddit posts in batches by the hundred
#   timePage should be in Unix epoch format (round to int if needed)
def search_pushshift_titles(ticker, size, timePage):
    relevantData = []

    startTime = time.time()

    if timePage == 0:
        timePage = round(time.time())

    search_url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(ticker)+'&size=100&score=>100&author=![deleted]&is_self=true&before='
    i = 0

    reqs = 0

    while i < size:
        for attempt in range(5):
            limitRate(startTime, reqs)
            try:
                r = requests.get(search_url + str(timePage))
                data = json.loads(r.text)
                reqs += 1
            except ValueError:
                print("Pushshift API Error: Status Code " + str(r.status_code))
                time.sleep(1)
            else:
                break
        else:
            print("Pushshift did not provide data after 5 attempts!")
            if len(relevantData == 0):
                return None #   Return None on complete failure
            else:
                break   #   Return partial data on partial failure

        for submission in data["data"]:
            if hasContent(submission, "pushshift") and i < size:
                selftext = re.sub(r"\[(.*?)\)|http\S+", "", str(submission["selftext"]))
                relevantData.append([str(submission["title"]), selftext, submission["created_utc"]])
                i += 1

        if len(data["data"]) % 100 > 0: #   If API returns < 100 posts, we reached the end so stop searching
            print("Out of posts!")
            break

        timePage = round(data["data"][-1]["created_utc"])

    print("Got data of size: " + str(len(relevantData)))

    return relevantData

def search_pushshift_titles_timeframe(ticker, newTime, oldTime):
    relevantData = []
    
    startTime = time.time()
    
    if newTime == 0:
        newTime = round(startTime)

    search_url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(ticker)+'&size=100&score=>5&author=![deleted]&is_self=true&before='+str(newTime)+'&after='
    i = 0

    reqs = 0

    while True:
        for attempt in range(5):
            limitRate(startTime, reqs)
            try:
                r = requests.get(search_url + str(oldTime))
                data = json.loads(r.text)
                reqs += 1
            except ValueError:
                print("Pushshift API Error: Status Code " + str(r.status_code))
                time.sleep(1)
            else:
                break
        else:
            print("Pushshift did not provide data after 5 attempts!")
            if len(relevantData) == 0:
                return None #   Return None on complete failure
            else:
                break   #   Return partial data on partial failure

        for submission in data["data"]:
            if hasContent(submission, "pushshift"):
                selftext = re.sub(r"\[(.*?)\)|http\S+", "", str(submission["selftext"]))
                relevantData.append([str(submission["title"]), selftext, submission["created_utc"]])
                i += 1

        if len(data["data"]) % 100 > 0: #   If API returns < 100 posts, we reached the end so stop searching
            print("Out of posts!")
            break

        oldTime = round(data["data"][-1]["created_utc"])
        print("Current posts: "+str(i))
        
    print("Got data of size: " + str(len(relevantData)))

    return relevantData

def hasContent(submission, api):
    if api == "pushshift":
        if "selftext" not in submission:
            return False
        else:
            selftext = submission["selftext"]
    elif api == "reddit":
        if not submission.is_self:
            return False
        else:
            selftext = submission.selftext
    
    selftext = selftext.replace("[removed]", "").replace("[deleted]", "").replace(" ", "").replace("\r\n", "").replace("\n", "")
    selftext = re.sub(r"\[(.*?)\)|http\S+", "", selftext)
    return len(selftext) > 0

def limitRate(startTime, requests):
    maxRPM = 120

    rpm = 0
    if time.time() - startTime > 0:
        rpm = requests / ((time.time() - startTime) / 60)

    print("RPM: ", str(rpm))
    while rpm > maxRPM:
        print("RPM: ", str(rpm))
        time.sleep(1)
        rpm = requests / ((time.time() - startTime) / 60)

    return

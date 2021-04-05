import praw

reddit = praw.Reddit("stonks")

def search_reddit_titles(ticker):
    titles = []
    for submission in reddit.subreddit("all").search("title:"+ticker, "new", limit=250):
        titles.append(submission.title)
    
    return titles

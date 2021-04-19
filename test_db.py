import dbconn
import reddit_scraper
import pandas as pd

# f = open('gme_titles.txt', 'r', encoding='utf8')
# for line in f:
#     dbconn.insert_reddit_post('GME', line.strip())
# print("DONE")

# print(dbconn.get_reddit_posts('TSLA'))
# print(reddit_scraper.search_pushshift_titles_content_only('GME',1,0))

df = pd.DataFrame(reddit_scraper.search_pushshift_titles_content_only('GME',1,0),columns = ['Title','Context','Timestamp'])
print(df.head())
# df2 = pd.DataFrame(reddit_scraper.search_pushshift_titles('GME',1,0),columns = ['Title','Context','Timestamp'])
# print(df2.head())

# reddit_scraper.search_pushshift_titles_content_only('GME',1,0)
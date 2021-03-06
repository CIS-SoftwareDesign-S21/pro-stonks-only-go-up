import dbconn
import reddit_scraper
import pandas as pd
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import time

s = 1609459200
t = 1618941644

# df = pd.DataFrame(reddit_scraper.search_pushshift_titles('GME',100,0),columns = ['Title','Context','Timestamp'])
# df2 = pd.DataFrame(reddit_scraper.search_pushshift_titles('TSLA',100,0),columns = ['Title','Context','Timestamp'])
# df3 = pd.DataFrame(reddit_scraper.search_pushshift_titles('AMC',100,0),columns = ['Title','Context','Timestamp'])
# df4 = pd.DataFrame(reddit_scraper.search_pushshift_titles('CLOV',100,0),columns = ['Title','Context','Timestamp'])
# df5 = pd.DataFrame(reddit_scraper.search_pushshift_titles('PLTR',100,0),columns = ['Title','Context','Timestamp'])
# df6 = pd.DataFrame(reddit_scraper.search_pushshift_titles('AAPL',100,0),columns = ['Title','Context','Timestamp'])
# df7 = pd.DataFrame(reddit_scraper.search_pushshift_titles('NVDA',100,0),columns = ['Title','Context','Timestamp'])
# df8 = pd.DataFrame(reddit_scraper.search_pushshift_titles('NIO',100,0),columns = ['Title','Context','Timestamp'])
# df9 = pd.DataFrame(reddit_scraper.search_pushshift_titles('SNDL',100,0),columns = ['Title','Context','Timestamp'])
# df10 = pd.DataFrame(reddit_scraper.search_pushshift_titles('PTON',100,0),columns = ['Title','Context','Timestamp'])

df = pd.DataFrame(reddit_scraper.search_pushshift_titles_timeframe('GME',t,s,100),columns = ['Title','Context','Timestamp'])
df2 = pd.DataFrame(reddit_scraper.search_pushshift_titles_timeframe('TSLA',t,s,0),columns = ['Title','Context','Timestamp'])
df3 = pd.DataFrame(reddit_scraper.search_pushshift_titles_timeframe('AMC',t,s,50),columns = ['Title','Context','Timestamp'])
df4 = pd.DataFrame(reddit_scraper.search_pushshift_titles_timeframe('CLOV',t,s,0),columns = ['Title','Context','Timestamp'])
df5 = pd.DataFrame(reddit_scraper.search_pushshift_titles_timeframe('PLTR',t,s,0),columns = ['Title','Context','Timestamp'])
df6 = pd.DataFrame(reddit_scraper.search_pushshift_titles_timeframe('AAPL',t,s,0),columns = ['Title','Context','Timestamp'])
df7 = pd.DataFrame(reddit_scraper.search_pushshift_titles_timeframe('NVDA',t,s,0),columns = ['Title','Context','Timestamp'])
df8 = pd.DataFrame(reddit_scraper.search_pushshift_titles_timeframe('NIO',t,s,0),columns = ['Title','Context','Timestamp'])
df9 = pd.DataFrame(reddit_scraper.search_pushshift_titles_timeframe('SNDL',t,s,0),columns = ['Title','Context','Timestamp'])
df10 = pd.DataFrame(reddit_scraper.search_pushshift_titles_timeframe('PTON',t,s,0),columns = ['Title','Context','Timestamp'])

df.insert(0,'Ticker','GME')
df2.insert(0,'Ticker','TSLA')
df3.insert(0,'Ticker','AMC')
df4.insert(0,'Ticker','CLOV')
df5.insert(0,'Ticker','PLTR')
df6.insert(0,'Ticker','AAPL')
df7.insert(0,'Ticker','NVDA')
df8.insert(0,'Ticker','NIO')
df9.insert(0,'Ticker','SNDL')
df10.insert(0,'Ticker','PTON')

df_total = pd.concat([df,df2,df3,df4,df5,df6,df7,df8,df9,df10],ignore_index=True)

df_total = df_total.replace('[^a-zA-Z ]', ' ', regex=True)

sia = SIA()

df_total['Compound'] = [sia.polarity_scores(x)['compound'] for x in df_total['Context']]
# print(df.info())
for post in df_total.index:
    dbconn.insert_reddit_post(df_total['Ticker'][post],df_total['Title'][post],df_total['Context'][post],time.strftime("%Y-%m-%d", time.gmtime(df_total['Timestamp'][post].item())),df_total['Compound'][post].item())

# df_total.to_csv('Sentiment.CSV',index=False)


#Functions below were for lemmatizing then rejoining the data into sentences. The performance was not as good.

# nlp = spacy.load("en_core_web_sm")
# df_total2['Clean Context'] = df_total2['Context'].apply(lemmatize)

# internal function
# def lemmatize(text):
#     context = nlp(text)
#     lemma_list = [str(tok.lemma_).lower() for tok in context
#                   if tok.is_alpha]
#     lemma_context = " ".join(lemma_list)
#     return lemma_context

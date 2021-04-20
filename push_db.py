import dbconn
import pandas as pd
import time
import plotly.graph_objects as go
import numpy as np

# df = pd.read_csv('Sentiment.CSV')

# print(df.head())



# print(df['Ticker'][0],df['Title'][0],df['Context'][0],time.strftime("%Y-%m-%d", time.gmtime(df['Timestamp'][0].item())),df['Compound'][0].item())
# i=0
# for post in df.index:
#     dbconn.insert_reddit_post(df['Ticker'][post],df['Title'][post],df['Context'][post],time.strftime("%Y-%m-%d", time.gmtime(df['Timestamp'][post].item())),df['Compound'][post].item())
        # print(df['Ticker'][post],df['Title'][post],df['Context'][post],time.strftime("%Y-%m-%d", time.gmtime(df['Timestamp'][post].item())),df['Compound'][post].item())

df_gme = pd.DataFrame(dbconn.get_reddit_posts('GME','2021-02-20'),columns=['Title','Context','Data','Score'])
df_tsla = pd.DataFrame(dbconn.get_reddit_posts('TSLA','2021-02-20'),columns=['Title','Context','Data','Score'])
df_amc = pd.DataFrame(dbconn.get_reddit_posts('AMC','2021-02-20'),columns=['Title','Context','Data','Score'])
df_clov = pd.DataFrame(dbconn.get_reddit_posts('CLOV','2021-02-20'),columns=['Title','Context','Data','Score'])
df_pltr = pd.DataFrame(dbconn.get_reddit_posts('PLTR','2021-02-20'),columns=['Title','Context','Data','Score'])
df_aapl = pd.DataFrame(dbconn.get_reddit_posts('AAPL','2021-02-20'),columns=['Title','Context','Data','Score'])
df_nio = pd.DataFrame(dbconn.get_reddit_posts('NIO','2021-02-20'),columns=['Title','Context','Data','Score'])
df_sndl = pd.DataFrame(dbconn.get_reddit_posts('SNDL','2021-02-20'),columns=['Title','Context','Data','Score'])
df_pton = pd.DataFrame(dbconn.get_reddit_posts('PTON','2021-02-20'),columns=['Title','Context','Data','Score'])
df_gme.insert(0,'Ticker','GME')
df_tsla.insert(0,'Ticker','TSLA')
df_amc.insert(0,'Ticker','AMC')
df_clov.insert(0,'Ticker','CLOV')
df_pltr.insert(0,'Ticker','PLTR')
df_aapl.insert(0,'Ticker','AAPL')
df_nio.insert(0,'Ticker','NIO')
df_sndl.insert(0,'Ticker','SNDL')
df_pton.insert(0,'Ticker','PTON')

df_total = pd.concat([df_gme,df_tsla,df_amc,df_clov,df_pltr,df_aapl,df_nvda,df_nio,df_sndl,df_pton])

print(df_total.shape)

# df_list = [df_gme,df_tsla,df_amc,df_clov,df_pltr,df_aapl,df_nvda,df_nio,df_sndl,df_pton]
df_tickers = ['GME','TSLA','AMC','CLOV','PLTR','AAPL','NVDA','NIO','SNDL','PTON']
# df_combo = zip(df_list,df_tickers)

df_total['label'] = 0
df_total.loc[df_total['Score'] > 0.2, 'label'] = 1
df_total.loc[df_total['Score'] < -0.2, 'label'] = -1

# for k,v in df_combo:


# # print(df_gme.shape)

#     fig = go.Figure()

# for data,ticker in df_combo:

#     data['label'] = 0
#     data.loc[data['Score'] > 0.2, 'label'] = 1
#     data.loc[data['Score'] < -0.2, 'label'] = -1

#     stonks = [ticker]

#     fig = go.Figure(data=[
#         go.Bar(name='Positive', x=stonks, y=[np.in1d(data['label'],1).sum()]),
#         go.Bar(name='Negative', x=stonks, y=[np.in1d(data['label'],-1).sum()])
#     ])

# fig.update_layout(barmode='stack')

# fig.show()
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from dash.dependencies import Input, Output
import reddit_scraper
import dbconn
import time

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [
    {
        'href':"https://kit.fontawesome.com/d313d59031.js",
        'rel': 'stylsheet',
        'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__, title = 'Stonks Only Go Up 📈', update_title = 'Collecting Data...', external_stylesheets=external_stylesheets)
app.server.assets_folder = 'assets'

server = app.server

##################TEMPORARY###############################
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

Tickers = ['GME','GME','TSLA','TSLA','AMC','AMC','CLOV','CLOV','PLTR','PLTR','AAPL','AAPL','NIO','NIO','SNDL','SNDL','PTON','PTON']
totals = []
Sentiment = ['Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative']

df_total = pd.concat([df_gme,df_tsla,df_amc,df_clov,df_pltr,df_aapl,df_nio,df_sndl,df_pton])

df_total['label'] = 0
df_total.loc[df_total['Score'] > 0.2, 'label'] = 1
df_total.loc[df_total['Score'] < -0.2, 'label'] = -1

for tickers in df_total.Ticker.unique():
    totals.append(df_total[(df_total['Ticker']==tickers) & (df_total['label']==1)].label.count())
    totals.append(df_total[(df_total['Ticker']==tickers) & (df_total['label']==-1)].label.count())

fig = px.bar(x=Tickers, y=totals, color=Sentiment)

fig.update_layout(
    title="Sentiment and frequency over past month.",
    xaxis_title="Tickers",
    yaxis_title="Total Comments",
    legend_title="Sentiment",
)

#############################################################################################


app.layout = html.Div(style={"margin": "0px"}, children=[
    
    html.Div([
        #html.H1("Stonks Only Go Up"),
        # html.Img(src="/assets/stonksgif.gif")
    ], className="banner"),
    
    #html.Img(src=app.get_asset_url('stonks.jpg'), style = {'padding-left': '90%', 'height': '10%', 'width': '10%', 'display': 'inline-block'}),
    html.H1('Stonks Only Go Up'),
    html.H3(children='Social Media Sentiment and Historical Prices of Stonks'),

    dcc.RadioItems(
        id='Stonks',
        options=[
            {'label': 'Gamestop', 'value': 'GME'},
            {'label': 'Tesla', 'value': 'TSLA'},
        ],
        value='GME',
        labelStyle={'display': 'inline-block', 'color': 'white'}
    ),
    dcc.Graph(id='Historical', style={"border": "5px solid #4d8eff"}),

    html.H3("Sentiment since 2021-02-20"),
    dcc.Graph(figure=fig),
    
    # searching interface
    html.H2('Most Recent Relevant Posts (100+ upvotes)'),
    dcc.Dropdown(
        id='scraper-platform',
        options=[
            {'label': 'Reddit', 'value': 'reddit'},
            {'label': 'Twitter', 'value': 'twitter'}
        ],
        value='reddit',
        style={"display": "inline-block", "width": "200px", "color": "black"}
    ),
    dcc.Dropdown(
        id='scraper-ticker',
        options=[
            {'label': 'Gamestop', 'value': 'gme'},
            {'label': 'Tesla', 'value': 'tsla'},
            {'label': 'AMC', 'value': 'amc'},
            {'label': 'Clover', 'value': 'clov'},
            {'label': 'Palantir', 'value': 'pltr'},
            {'label': 'Apple', 'value': 'aapl'},
            {'label': 'Nio', 'value': 'nio'},
            {'label': 'Sundial', 'value': 'sndl'},
            {'label': 'Peloton', 'value': 'pton'}
        ],
        value='gme',
        style={"display": "inline-block", "width": "200px", "color": "black"}
    ),
    dcc.Dropdown(
        id='scraper-quantity',
        options=[
            {'label': '50 posts', 'value': '50'},
            {'label': '100 posts', 'value': '100'},
            {'label': '500 posts', 'value': '500'}
        ],
        value='50',
        style={"display": "inline-block", "width": "200px", "color": "black"}
    ),
    html.Span('   Start searching from '),
    dcc.Input(
        id='scraper-time',
        type='number',
        placeholder=0,
        min=0,
        max=730,
        style={"display": "inline-block", "width": "50px"}
    ),
    html.Span(' days back   '),
    html.Button('Query Social Media', id='scraper-go'),
    html.Div("Fetching posts...", id='scraper-listbox', style={"maxHeight": "400px", "overflow": "scroll"}),
    
    # save scraped data
    html.Button('Save To Database', id='save-button'),
    html.Span(id='save-result'),

    # graph scraped sentiment
    html.H3("Sentiment: ", id="scraper-sentiment"),
    dcc.Graph(id='scraper-graph'),
    
    # database interface
    html.H2('Posts stored in Database'),
    dcc.Dropdown(
        id='db-platform',
        options=[
            {'label': 'Reddit', 'value': 'reddit'},
            {'label': 'Twitter', 'value': 'twitter'}
        ],
        value='reddit',
        style={"display": "inline-block", "width": "200px", "color": "black"}
    ),
    dcc.Dropdown(
        id='db-ticker',
        options=[
            {'label': 'Gamestop', 'value': 'gme'},
            {'label': 'Tesla', 'value': 'tsla'},
            {'label': 'AMC', 'value': 'amc'},
            {'label': 'Clover', 'value': 'clov'},
            {'label': 'Palantir', 'value': 'pltr'},
            {'label': 'Apple', 'value': 'aapl'},
            {'label': 'Nio', 'value': 'nio'},
            {'label': 'Sundial', 'value': 'sndl'},
            {'label': 'Peloton', 'value': 'pton'}
        ],
        value='gme',
        style={"display": "inline-block", "width": "200px", "color": "black"}
    ),
    dcc.Dropdown(
        id='db-time',
        options=[
            {'label': 'Today', 'value': '0'},
            {'label': '1 week', 'value': '7'},
            {'label': '2 weeks', 'value': '14'},
            {'label': '1 month', 'value': '31'},
            {'label': '3 months', 'value': '93'},
            {'label': '6 months', 'value': '186'},
            {'label': 'Forever', 'value': '-1'},    
        ],
        value='7',
        style={"display": "inline-block", "width": "200px", "color": "black"}
    ),
    html.Button('Query Database', id='db-go'),
    html.Div('Fetching posts...', id='db-listbox', style={"maxHeight": "400px", "overflow": "scroll"}),
    
    # graph stored sentiment
    html.H3("Sentiment: ", id="db-sentiment"),
    dcc.Graph(id='db-graph'),

    # footer
    html.Div(children=[
        html.Footer([
            html.Img(src="/assets/stonksgif.gif"),
            html.H5("Created By: Ayman El-sayed 🌑 Steven Zhou 🌑 Aidan Buehler 🌑 Karl Schaller 🌑 Ji Park"),
            html.H5("Stonks Only Go Up ©️ 2021"),
        ])
    ], className="footer"),
])


# callback for graph radio buttons
@app.callback(Output('Historical', 'figure'),
              [Input('Stonks', 'value')])
def render_charts(stonk):

    df = pd.read_csv(r'GME.csv')
    df2 = pd.read_csv(r'TSLA.csv')

    fig = go.Figure()
    fig2 = go.Figure()

    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'],
                             mode='lines',
                             name='GME'))
    fig.add_trace(go.Scatter(x=df2['Date'], y=np.random.rand(len(df['Date']))*df['Close'].max(),
                             mode='lines',
                             name='Sentiment',
                             opacity=0.3))

    fig2.add_trace(go.Scatter(x=df2['Date'], y=df2['Close'],
                              mode='lines',
                              name='TSLA'))
    fig2.add_trace(go.Scatter(x=df2['Date'], y=np.random.rand(len(df['Date']))*df2['Close'].max(),
                              mode='lines',
                              name='Sentiment',
                              opacity=0.3))

    if stonk == 'GME':
        return fig
    elif stonk == 'TSLA':
        return fig2


# callback for scraper dropdown
@app.callback(
    dash.dependencies.Output('scraper-sentiment', 'children'),
    dash.dependencies.Output('scraper-graph', 'figure'),
    dash.dependencies.Output('scraper-listbox', 'children'),
    [dash.dependencies.Input('scraper-go', 'n_clicks')],
    [dash.dependencies.State('scraper-platform', 'value')],
    [dash.dependencies.State('scraper-ticker', 'value')],
    [dash.dependencies.State('scraper-time', 'value')],
    [dash.dependencies.State('scraper-quantity', 'value')]
)
def update_scraper_box(n_clicks, platform, ticker, n_days, n_posts):
    print("Searching for " + ticker + " from " + platform + " in scraper...")
    if not n_days:
        n_days = 0
    newPosts = reddit_scraper.search_pushshift_titles(ticker, int(n_posts), round(time.time() - int(n_days) * 86400))
    #newPosts = reddit_scraper.search_pushshift_titles_timeframe(ticker, 0, 1603080000)  #   Oct 19, 2020
    # newPosts = reddit_scraper.search_reddit_titles(ticker)

    # TODO: IMPLEMENT TWITTER
    # if platform == 'reddit':
    #     newPosts = reddit_scraper.search_pushshift_titles(ticker, 100, 0)
    # elif platform == 'twitter':
    #     newPosts = twitter_scraper.get_posts(ticker)

    df = sentiment_analysis(newPosts)
    compound_scores = np.array(df['compound'])
    newPosts = np.hstack((newPosts, np.reshape(compound_scores, (-1, 1))))

    overall, fig = sentiment_bar_graph(compound_scores)

    for i in range(len(newPosts)):
        newPosts[i][2] = time.strftime("%Y-%m-%d", time.gmtime(int(newPosts[i][2])))
    print('Updating table for scraper box')
    table = make_table(newPosts, platform)

    return overall, fig, table
    # return overall, table


# callback for save button
@app.callback(
    dash.dependencies.Output('save-result', 'children'),
    [dash.dependencies.Input('save-button', 'n_clicks')],
    [dash.dependencies.Input('scraper-listbox', 'children')],
    [dash.dependencies.State('scraper-ticker', 'value')],
    [dash.dependencies.State('scraper-platform', 'value')]
)
def save_posts(n_clicks, table, ticker, platform):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'].split('.')[0] == 'save-button':
        print("Saving Posts")
        tableBody = table['props']['children'][1]
        for tableRow in tableBody['props']['children']:
            tds = tableRow['props']['children']
            dbconn.insert_reddit_post(ticker, tds[1]['props']['children'], tds[2]['props']['children'], tds[0]['props']['children'], tds[3]['props']['children'])
            # TODO: IMPLEMENT TWITTER
            # if platform == 'reddit':
            #     dbconn.insert_reddit_post(ticker, tds[0]['props']['children'], tds[1]['props']['children'])
            # elif platform == 'twitter':
            #     dbconn.insert_twitter_post(ticker, tds[0]['props']['children'])
        print("Saving Done")
        return "Saved " + str(len(tableBody['props']['children'])) + " posts"
    return ''


# callback for database dropdown
@app.callback(
    dash.dependencies.Output('db-sentiment', 'children'),
    dash.dependencies.Output('db-graph', 'figure'),
    dash.dependencies.Output('db-listbox', 'children'),
    [dash.dependencies.Input('db-go', 'n_clicks')],
    [dash.dependencies.State('db-platform', 'value')],
    [dash.dependencies.State('db-ticker', 'value')],
    [dash.dependencies.State('db-time', 'value')]
)
def update_db_box(n_clicks, platform, ticker, n_days):
    print("Searching for " + ticker + " from " + platform + " in db...")
    if n_days == '-1':
        newPosts = dbconn.get_reddit_posts(ticker)
    else:
        newPosts = dbconn.get_reddit_posts(ticker, time.strftime("%Y-%m-%d", time.gmtime(time.time() - int(n_days) * 86400)))   
    # TODO: IMPLEMENT TWITTER
    # if platform == 'reddit':
    #     newPosts = dbconn.get_reddit_posts(ticker)
    # elif platform == 'twitter':
    #     newPosts = dbconn.get_twitter_posts(ticker)

    compound_scores = np.array(newPosts).reshape(-1, 4)[:, 3].astype(float)
    overall, fig = sentiment_bar_graph(compound_scores)

    print("Updating table for db box")
    table = make_table(newPosts, platform)

    return overall, fig, table


# helper function to create html table
def make_table(posts, platform):
    if platform == 'reddit':
        tableHead = html.Thead(html.Tr([html.Th("DATE"), html.Th("TITLE"), html.Th("CONTENT"), html.Th("SENTIMENT")]))
        tableBody = html.Tbody([html.Tr([html.Td(post[2]), html.Td(post[0]), html.Td(post[1]), html.Td(post[3])]) for post in posts])
    elif platform == 'twitter':
        tableHead = html.Thead(html.Tr([html.Th("DATE"), html.Th("CONTENT"), html.Th("SENTIMENT")]))
        tableBody = html.Tbody([html.Tr([html.Td(post[2]), html.Td(post[0]), html.Td(post[3])]) for post in posts])
    
    return html.Table([tableHead, tableBody])


# helper function to perform sentiment analysis
def sentiment_analysis(posts):
    sia = SIA()
    results = []
    for post in posts:
        title = post[0].strip('\n')
        pol_score = sia.polarity_scores(title)
        pol_score['headline'] = title
        results.append(pol_score)

    return pd.DataFrame.from_records(results)


# helper function to create sentiment bar chart
def sentiment_bar_graph(compound_scores):
    df = pd.DataFrame(compound_scores, columns=['compound'])
    df['label'] = 0
    df.loc[df['compound'] > 0.2, 'label'] = 1
    df.loc[df['compound'] < -0.2, 'label'] = -1

    if df.label.sum() > 0:
        sentiment = "Sentiment: Positive"
    elif df.label.sum() < 0:
        sentiment = "Sentiment: Negative"
    else: 
        sentiment = "Sentiment: Neutral"

    fig = go.Figure()

    stonks = ['GME']

    fig = go.Figure(data=[
        go.Bar(name='Positive', x=stonks, y=[np.in1d(df['label'],1).sum()]),
        go.Bar(name='Negative', x=stonks, y=[np.in1d(df['label'],-1).sum()])
    ])

    fig.update_layout(barmode='stack',
                    width=400,
                    height=600)

    return sentiment, fig


def generate_graph():
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

    Tickers = ['GME','GME','TSLA','TSLA','AMC','AMC','CLOV','CLOV','PLTR','PLTR','AAPL','AAPL','NIO','NIO','SNDL','SNDL','PTON','PTON']
    totals = []
    Sentiment = ['Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative','Postive','Negative']

    df_total = pd.concat([df_gme,df_tsla,df_amc,df_clov,df_pltr,df_aapl,df_nio,df_sndl,df_pton])

    df_total['label'] = 0
    df_total.loc[df_total['Score'] > 0.2, 'label'] = 1
    df_total.loc[df_total['Score'] < -0.2, 'label'] = -1

    for tickers in df_total.Ticker.unique():
      totals.append(df_total[(df_total['Ticker']==tickers) & (df_total['label']==1)].label.count())
      totals.append(df_total[(df_total['Ticker']==tickers) & (df_total['label']==-1)].label.count())

    fig = px.bar(x=Tickers, y=totals, color=Sentiment,
                labels={
                    Tickers:"Tickers",
                    totals:"Total posts",
                    Sentiment:"Sentiment"
                },
                title='Sentiment score and frequency over past month.')

    return fig

# def create_footer():
#     footer_style= {"background-color": "green", "padding": "0.5rem"}
#     p0 = html.P(
#         children = [
#             html.Span("Built with "),
#             html.A(
#                 "Plotly Dash", href="https://github.com/plotly/dash", target="_blank"
#             ),
#         ]
#     )
#     p1 = html.P(
#         children = [
#             html.Span("Data From "),
#             html.A("Reddit & Twitter"),
#         ]
#     )
#     a_fa = html.A(
#         children=[
#             html.I([], classname = "fa fa-font-awesome fa-2x"), html.Span("Font Awesome")
#         ],
#         style = {"text-decoration": "none"},
#         href="http://fontawesome.io/",
#         target="_blank",
#     )
    
#     div = html.Div([p0, p1, a_fa])
#     footer = html.Footer(children = div, style=footer_style)
#     return footer

if __name__ == '__main__':
    app.run_server(debug=True)
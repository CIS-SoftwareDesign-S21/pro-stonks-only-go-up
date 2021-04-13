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

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
app.server.assets_folder = 'assets'

app.layout = html.Div(style={"margin": "15px"}, children=[

    html.H1(children='Stonks only go Up', className="app-header--title"),

    # graphs
    html.H3(children='Social Media Sentiment and Historical Prices of Stonks'),

   html.H3(children='Social Media Sentiment and Historical Prices of Stonks'),
    
    # dcc.Input(
    #     id="input_text",
    #     type="text",
    #     placeholder="input type text",
    # ),
    dcc.RadioItems(
        id='Stonks',
        options=[
            {'label': 'Gamestop', 'value': 'GME'},
            {'label': 'Tesla', 'value': 'TSLA'},
        ],
        value='GME',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='Historical', style={"border": "5px solid #4d8eff"}),
    
    # searching interface
    html.H2('Recent Relevant Posts (100)'),
    html.H3("Sentiment: ", id="scraper-sentiment"),
    dcc.Dropdown(
        id='scraper-platform',
        options=[
            {'label': 'Reddit', 'value': 'reddit'},
            {'label': 'Twitter', 'value': 'twitter'}
        ],
        value='reddit',
        style={"display": "inline-block", "width": "200px"}
    ),
    html.Div("Sentiment: ", id="Sentiment"),
    dcc.Graph(
        id='Sentiment_Graph',
    ),
    html.H2(children='Recent Relevant Reddit Posts (500)'),
    html.Button('Query Reddit for Selected Stock Posts',
                id='update_titles', n_clicks=0),
    dcc.Dropdown(
        id='scraper-ticker',
        options=[
            {'label': 'Gamestop', 'value': 'gme'},
            {'label': 'Tesla', 'value': 'tsla'}
        ],
        value='gme',
        style={"display": "inline-block", "width": "200px"}
    ),
    html.Button('Refresh', id='scraper-refresh'),
    html.Div("init", id='scraper-listbox', style={"maxHeight": "400px", "overflow": "scroll"}),
    html.Button('Save', id='save-button'),
    html.Span(id='save-result'),
    
    # database interface
    html.H2('Posts stored in Database'),
    html.H3("Sentiment: ", id="db-sentiment"),
    dcc.Dropdown(
        id='db-platform',
        options=[
            {'label': 'Reddit', 'value': 'reddit'},
            {'label': 'Twitter', 'value': 'twitter'}
        ],
        value='reddit',
        style={"display": "inline-block", "width": "200px"}
    ),
    dcc.Dropdown(
        id='db-ticker',
        options=[
            {'label': 'Gamestop', 'value': 'gme'},
            {'label': 'Tesla', 'value': 'tsla'}
        ],
        value='gme',
        style={"display": "inline-block", "width": "200px"}
    ),
    html.Button('Refresh', id='db-refresh'),
    html.Div('init', id='db-listbox', style={"maxHeight": "400px", "overflow": "scroll"})
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
    dash.dependencies.Output('Sentiment_Graph', 'figure'),
    dash.dependencies.Output('scraper-listbox', 'children'),
    [dash.dependencies.Input('scraper-refresh', 'n_clicks')],
    [dash.dependencies.Input('scraper-ticker', 'value')],
    [dash.dependencies.Input('scraper-platform', 'value')]
)
def update_scraper_box(n_clicks, ticker, platform):
    print("Searching for " + ticker + " from " + platform + " in scraper")
    newPosts = reddit_scraper.search_pushshift_titles(ticker, 100, 0)
    # newPosts = reddit_scraper.search_reddit_titles(ticker)

    # TODO: IMPLEMENT TWITTER
    # if platform == 'reddit':
    #     newPosts = reddit_scraper.search_pushshift_titles(ticker, 100, 0)
    # elif platform == 'twitter':
    #     newPosts = twitter_scraper.get_posts(ticker)

    sentiment, fig = sentiment_analysis_graph(newPosts)

    print('Updating table for scraper box')
    table = make_table(newPosts, platform)

    return sentiment, fig, table


# callback for save button
@app.callback(
    dash.dependencies.Output('save-result', 'children'),
    [dash.dependencies.Input('save-button', 'n_clicks')],
    [dash.dependencies.Input('scraper-listbox', 'children')],
    [dash.dependencies.Input('scraper-ticker', 'value')],
    [dash.dependencies.Input('scraper-platform', 'value')]
)
def save_posts(n_clicks, table, ticker, platform):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'].split('.')[0] == 'save-button':
        print("Saving Posts")
        tableBody = table['props']['children'][1]
        for tableRow in tableBody['props']['children']:
            tds = tableRow['props']['children']
            dbconn.insert_reddit_post(ticker, tds[0]['props']['children'], tds[1]['props']['children'])
            # TODO: IMPLEMENT TWITTER
            # if platform == 'reddit':
            #     dbconn.insert_reddit_post(ticker, tds[0]['props']['children'], tds[1]['props']['children'])
            # elif platform == 'twitter':
            #     dbconn.insert_twitter_post(ticker, tds[0]['props']['children'])
        print("Saving Done")
        return "Saved " + str(len(tableBody['props']['children'])) + " posts"


# callback for database dropdown
@app.callback(
    dash.dependencies.Output('db-sentiment', 'children'),
    dash.dependencies.Output('db-listbox', 'children'),
    [dash.dependencies.Input('db-refresh', 'n_clicks')],
    [dash.dependencies.Input('db-ticker', 'value')],
    [dash.dependencies.Input('db-platform', 'value')]
)
def update_db_box(n_clicks, ticker, platform):
    print("Searching for " + ticker + " from " + platform + " in db")
    newPosts = dbconn.get_reddit_posts(ticker)

    # TODO: IMPLEMENT TWITTER
    # if platform == 'reddit':
    #     newPosts = dbconn.get_reddit_posts(ticker)
    # elif platform == 'twitter':
    #     newPosts = dbconn.get_twitter_posts(ticker)

    sentiment = sentiment_analysis(newPosts)

    print("Updating table for db box")
    table = make_table(newPosts, platform)

    return sentiment, table


# helper function to create html table
def make_table(posts, platform):
    if platform == 'reddit':
        tableHead = html.Thead(html.Tr([html.Th("TITLE"), html.Th("CONTENT")]))
        tableBody = html.Tbody([html.Tr([html.Td(post[0]), html.Td(post[1])]) for post in posts])
    elif platform == 'twitter':
        tableHead = html.Thead(html.Tr([html.Th("CONTENT")]))
        tableBody = html.Tbody([html.Tr([html.Td(post[0])]) for post in posts])
    
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
    
    df = pd.DataFrame.from_records(results)
    df['label'] = 0
    df.loc[df['compound'] > 0.2, 'label'] = 1
    df.loc[df['compound'] < -0.2, 'label'] = -1

    sentiment = ""

    if df.label.sum() > 0:
        sentiment = "Sentiment: Positive"
    elif df.label.sum() < 0:
        sentiment = "Sentiment: Negative"
    else: 
        sentiment = "Sentiment: Neutral"

    return sentiment

def sentiment_analysis_graph(posts):
    sia = SIA()
    results = []
    for post in posts:
        title = post[0].strip('\n')
        pol_score = sia.polarity_scores(title)
        pol_score['headline'] = title
        results.append(pol_score)
    
    df = pd.DataFrame.from_records(results)
    df['label'] = 0
    df.loc[df['compound'] > 0.2, 'label'] = 1
    df.loc[df['compound'] < -0.2, 'label'] = -1

    sentiment = ""

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

    fig.update_layout(barmode='stack')

    return sentiment, fig

if __name__ == '__main__':
    app.run_server(debug=True)
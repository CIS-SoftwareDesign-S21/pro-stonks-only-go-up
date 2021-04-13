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

# df = pd.read_csv(
#     r'GME.csv')

# fig = go.Figure()

# fig.add_trace(go.Scatter(x=df['Date'],y=df['Close'],
#                         mode = 'lines',
#                         name = 'GME'))

app.layout = html.Div(style={"margin": "15px"},
    children=[

    html.H1(children='Stonks only go Up', className="app-header--title"),

    # graphs
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
    dcc.Graph(
        id='Historical',
    ),
    
    # searching interface
    html.H2(children='Recent Relevant Reddit Posts (500)'),
    html.Button('Refresh',
                id='scraper-refresh', n_clicks=0),
    dcc.Dropdown(
        id='scraper-dropdown',
        options=[
            {'label': 'Gamestop', 'value': 'gme'},
            {'label': 'Tesla', 'value': 'tsla'}
        ],
        value='gme'
    ),
    html.Div("Sentiment: ", id="scraper-sentiment"),
    html.Div(children="init",
        style={"maxHeight": "400px", "overflow": "scroll"},
        id='scraper-listbox'
    ),
    
    # database interface
    html.H2(children='Reddit Posts stored in Database matching GME'),
    dcc.Dropdown(
        id='db-dropdown',
        options=[
            {'label': 'Gamestop', 'value': 'gme'},
            {'label': 'Tesla', 'value': 'tsla'}
        ],
        value='gme'
    ),
    html.Div("Sentiment: ", id="db-sentiment"),
    html.Div(children='init',
        style={"maxHeight": "400px", "overflow": "scroll"},
        id='db-listbox'
    )
])


# callback for graph radio buttons
@app.callback(Output('Historical', 'figure'),
              [Input('Stonks', 'value')])
def render_charts(stonk):

    df = pd.read_csv(r'GME.csv')
    df2 = pd.read_csv(r'TSLA.csv')

    # charts = [
    #     go.Scatter(labels=df['Date'], values=df2['Close'],
    #                mode='lines', name='GME'),
    #     go.Scatter(labels=df2['Date'], values=df2['Close'],
    #                mode='lines', name='TSLA'),
    # ]

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


# callback for search dropdown
@app.callback(
    dash.dependencies.Output('scraper-sentiment', 'children'),
    dash.dependencies.Output('scraper-listbox', 'children'),
    [dash.dependencies.Input('scraper-refresh', 'n_clicks')],
    [dash.dependencies.Input('scraper-dropdown', 'value')]
)
def update_gme_titles(n_clicks, ticker):
    print("Searching for " + ticker + " in scraper")
    newPosts = reddit_scraper.search_pushshift_titles(ticker, 50, 0)
    # newPosts = reddit_scraper.search_reddit_titles(ticker)

    sia = SIA()
    results = []
    for post in newPosts:
        title = post[0].strip('\n')
        pol_score = sia.polarity_scores(title)
        pol_score['headline'] = title
        results.append(pol_score)
    
    df = pd.DataFrame.from_records(results)
    df['label'] = 0
    df.loc[df['compound'] > 0.2, 'label'] = 1
    df.loc[df['compound'] < -0.2, 'label'] = -1

    if df.label.sum() > 0:
        sentiment = "Sentiment: Positive"
    elif df.label.sum() < 0:
        sentiment = "Sentiment: Negative"
    else: 
        sentiment = "Sentiment: Neutral"

    print('Updating titles for scraper box')
    table = html.Table([
        html.Thead(
            html.Tr([html.Th("TITLE"), html.Th("CONTENT")])
        ),
        html.Tbody([
            html.Tr([html.Td(post[0]), html.Td(post[1])]) for post in newPosts
        ])
    ])

    return sentiment, table


# callback for database dropdown
@app.callback(
    dash.dependencies.Output('db-sentiment', 'children'),
    dash.dependencies.Output('db-listbox', 'children'),
    [dash.dependencies.Input('db-dropdown', 'value')]
)
def update_db_box(ticker):
    print("Searching for " + ticker + " in db")
    newPosts = dbconn.get_reddit_posts('GME')

    sia = SIA()
    results = []
    for post in newPosts:
        title = post[0].strip('\n')
        pol_score = sia.polarity_scores(title)
        pol_score['headline'] = title
        results.append(pol_score)
    
    df = pd.DataFrame.from_records(results)
    df['label'] = 0
    df.loc[df['compound'] > 0.2, 'label'] = 1
    df.loc[df['compound'] < -0.2, 'label'] = -1

    if df.label.sum() > 0:
        sentiment = "Sentiment: Positive"
    elif df.label.sum() < 0:
        sentiment = "Sentiment: Negative"
    else: 
        sentiment = "Sentiment: Neutral"

    print("Updating titles for db box")
    table = html.Table([
        html.Thead(
            html.Tr([html.Th("TITLE"), html.Th("CONTENT")])
        ),
        html.Tbody([
            html.Tr([html.Td(post[0]), html.Td(post[1])]) for post in newPosts
        ])
    ])

    return sentiment, table


if __name__ == '__main__':
    app.run_server(debug=True)

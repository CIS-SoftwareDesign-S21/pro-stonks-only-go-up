import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import reddit_scraper

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
app.server.assets_folder = 'assets'

# df = pd.read_csv(
#     r'GME.csv')

# fig = go.Figure()

# fig.add_trace(go.Scatter(x=df['Date'],y=df['Close'],
#                         mode = 'lines',
#                         name = 'GME'))

app.layout = html.Div(children=[
    html.H1(children='Stonks only go Up',className = "app-header--title"),

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
    html.H2(children='Recent Relevant Post Titles (250)'),
    html.Button('Query Reddit for Selected Stock Posts', id='update_titles', n_clicks=0),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[
            {'label': 'Gamestop', 'value': 'gme'},
            {'label': 'Tesla', 'value': 'tsla'}
        ],
        value='gme'
    ),
    html.Div(children="init",
        style={"maxHeight": "400px", "overflow": "scroll"},
        id='gme_titles_listbox'
    )
])

@app.callback(Output('Historical', 'figure'),
              [Input('Stonks', 'value')])
def render_charts(stonk):

    df = pd.read_csv(
        r'GME.csv')

    df2 = pd.read_csv(
        r'TSLA.csv')

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

@app.callback(
    dash.dependencies.Output('gme_titles_listbox', 'children'),
    [dash.dependencies.Input('update_titles', 'n_clicks')],
    [dash.dependencies.Input('ticker-dropdown', 'value')]
)
def update_gme_titles(n_clicks, ticker):
    print("Searching for " + ticker)
    newTitles = reddit_scraper.search_reddit_titles(ticker)
    
    newList = html.Ul([html.Li(x) for x in newTitles])
    print("Updating titles for ticker")

    return newList

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Stonks only go Up'),

    html.Div(children='''
        Social media sentiment and historical prices of stonks.
    '''),

    # dcc.Input(
    #     id="input_text",
    #     type="text",
    #     placeholder="input type text",
    # ),
    dcc.RadioItems(
        options=[
            {'label': 'Gamestop', 'value': 'GME'},
            {'label': 'Tesla', 'value': 'TSLA'},
        ],
        value='MTL',
        labelStyle={'display': 'inline-block'}
    )

]
)

if __name__ == '__main__':
    app.run_server(debug=True)

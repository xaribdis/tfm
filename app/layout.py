import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from constants import districts

TEMPLATE = 'plotly_dark'
config = {"displayModeBar": False}

BUTTON_LAYOUT = [
    dcc.Link(
        html.Button('HOME', id='home-button', className='mr-1'),
        href='/'),
    dcc.Link(
        html.Button('DISTRICTS', id='districts-button', className='mr-1'),
        href='/districts'),
]


def set_district_layout():
    layout = html.Div([
        html.Div(id=f'details'),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col(html.H1('Districts'), width=9),
            dbc.Col(width=2),
        ], justify='center'),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='district-dropdown',
                    options=[{'label': district, 'value': district} for district in districts.keys()],
                    value='Arganzuela'
                ), width=6
            ),
            dbc.Col(width=5),
        ], justify='center'),
        dcc.Graph(id='temp-series',
                  config=config),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='district-map',
                              config=config)
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='subzones-bar',
                              config=config)
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='some-plot',config=config)
                ]), width=4),
        ]),
    ])
    return layout

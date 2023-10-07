import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from constants import districts

TEMPLATE = 'plotly_dark'

BUTTON_LAYOUT = [
    dcc.Link(
        html.Button('HOME', id='home-button', className='mr-1'),
        href='/'),
    dcc.Link(
        html.Button('DISTRICTS', id='districts-button', className='mr-1'),
        href='/districts'),
]


def set_district_layout(district: str, date: str):
    layout = html.Div([
        html.Div(id=f'{district}-details'),
        html.Br(),
        dbc.Row([
            dbc.Col(
                html.Div(BUTTON_LAYOUT), width=4),
            dbc.Col(width=7),
        ], justify='center'),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col(html.H1(district), width=9),
            dbc.Col(width=2),
        ], justify='center'),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='district-dropdown',
                    options=[{'label': district, 'value': district} for district in districts],
                ), width=6
            ),
            dbc.Col(width=5),
        ], justify='center'),
        dcc.Graph(id=f'{district}-temp-series'),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(figure="""TODO display_map()""")
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(figure="""TODO plot_histogram()""")
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(figure="""TODO plot_()""")
                ]), width=4),
        ]),
    ])
    return layout

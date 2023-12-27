import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from config import settings

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
            dbc.Col(html.H1('Información de distrito'), width=9),
            dbc.Col(width=2),
        ], justify='center'),
        html.Br(),
        html.Br(),
        dbc.Row([
            dcc.Store('memory-intervals', storage_type='session'),
            dbc.Col(
                dcc.Dropdown(
                    id='district-dropdown',
                    options=[{'label': district, 'value': district} for district in settings.DISTRICTS.keys()],
                    value='Arganzuela',
                    persistence=True,
                    persistence_type='session'
                ), width=6
            ),
            dbc.Col(width=5),
        ], justify='center'),
        dcc.Graph(id='temp-series',
                  config=config),
        html.Br(),
        dcc.Graph(id='subarea-boxplots',
                  config=config),
        html.Br(),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='subarea-plots',
                              config=config)
                ]), width=8),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='highest-occupation',
                              config=config)
                ]), width=4),
        ]),
    ])
    return layout

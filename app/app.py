from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
# from pyspark.sql.types import StringType
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
# import plotly.io as pio
import structlog

from main_spark import df_pipeline, get_spark_session
import spark_process as sp
from crud import mongo
import layout as lo
from schemas import historic_data_schema
from constants import GEOJSON_FILE, districts, subarea_colors

structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.getLogger()

spark_session = get_spark_session()
app = Dash(external_stylesheets=[dbc.themes.YETI], suppress_callback_exceptions=True)

df = df_pipeline(spark_session)  # Dataframe for the incoming data
temp_series_df = sp.get_historic_data_df(spark_session, historic_data_schema)  # Dataframe for the historic data

# TODO save dropdown value between timeperiods

# subarea_colors = px.colors.qualitative.Dark24

geojsonfile = GEOJSON_FILE
with open(geojsonfile) as file:
    geojson = json.load(file)

server = app.server

"""App layout"""
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(
            html.Div(lo.BUTTON_LAYOUT), width=4),
        dbc.Col(width=7),
    ], justify='center'),
    html.Br(),
    html.Br(),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # Time interval in ms
        n_intervals=0
    ),
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.Div(id='page-content'),
])

index_page = html.Div([
    html.H1(children='Homepage', style={'textAlign': 'center'}),
    dcc.Store(id='map-data', storage_type='session'),
    dcc.Graph(id="map"),
])

"""District layout"""
district_layout = lo.set_district_layout()


# Function to update the dataframe in the background at 5 min intervals
@app.callback(Output("hidden-div", "children"), Input('interval-component', 'n_intervals'))
def update_df(n_intervals):
    global df
    global temp_series_df
    df = df_pipeline(spark_session)
    temp_series_df = sp.get_historic_data_df(spark_session, historic_data_schema)  # Dataframe for the historic data
    return {}


# Load the graph from a json in a Store to avoid load time
# @callback(Output("map", "figure"), Input("interval-component", "n_intervals"),
#           State("map-data", 'data'))
# def display_map(n_intervals, data):
#     return dcc.Graph(figure=str(json.loads(data)))


# Filter the dataframe and display the map of the homepage
@app.callback(Output("map", "figure"), Input('interval-component', 'n_intervals'))
def get_index_map_data(n_intervals):
    filtered_df = sp.field_larger_than(df, 'nivelServicio', 1)
    filtered_df = sp.cast_to_datetime(filtered_df)

    lat_foc = 40.42532
    lon_foc = -3.686722

    fig_go = go.Figure(go.Scattermapbox(
        mode="markers",
        lat=filtered_df['latitud'], lon=filtered_df['longitud'], hovertext=filtered_df[['intensidad', 'descripcion']],
        marker=dict(color=filtered_df.intensidad, colorscale='bluered', showscale=False, cmin=0, cmax=2500)
    ))

    district_agg = sp.agg_districts(df).toPandas()

    fig = px.choropleth_mapbox(district_agg, geojson=geojson, mapbox_style="open-street-map", color='avg(intensidad)',
                               locations='distrito', featureidkey='properties.name', color_continuous_scale='viridis',
                               opacity=0.6, center={'lat': lat_foc, 'lon': lon_foc}, zoom=10)

    fig.add_trace(fig_go.data[0])
    fig.update_layout(margin=dict(l=10, r=1, t=10, b=10))
    return fig


# Show map with every sensor of the dropdown selected district
# @app.callback(Output("district-map", "figure"),
#               Input('district-dropdown', 'value'),
#               Input('interval-component', 'n_intervals'))
def get_district_map_data(value, n_intervals):
    district = value
    log.info(f"{district}")
    filtered_df = sp.filter_district(df, district)
    filtered_df = sp.cast_to_datetime(filtered_df)

    district_center = districts[district]
    lon_foc = district_center[0]
    lat_foc = district_center[1]
    log.info(str(lon_foc) + ", " + str(lat_foc))

    # TODO adjust colorscale
    fig = px.scatter_mapbox(filtered_df, lat=filtered_df['latitud'], lon=filtered_df['longitud'], opacity=1,
                            mapbox_style="open-street-map", hover_data=filtered_df[['intensidad', 'descripcion']],
                            center={'lat': lat_foc,  'lon': lon_foc}, zoom=13,
                            color='carga', color_continuous_scale='bluered')

    fig.update_layout(margin=dict(l=10, r=5, t=10, b=10), )
    return fig


# @app.callback(Output('subzones-bar', 'figure'),
#               Input('district-dropdown', 'value'),
#               Input('interval-component', 'n_intervals'))
def plot_subzones_bar(value, n_intervals):
    district = value
    log.info(f"barplot: {district}")
    filtered_df = sp.agg_subzones_of_district(df, district).toPandas()

    fig = px.bar(filtered_df, x='subarea', y='avg(carga)', color_discrete_sequence=subarea_colors, color='subarea')
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    return fig


@app.callback(Output("subarea-plots", "figure"),
              Input('district-dropdown', 'value'),
              Input('interval-component', 'n_intervals'))
def subarea_plots(value, n_intervals):
    filtered_df = sp.agg_subzones_of_district(df, value).sort('subarea').toPandas()
    # filtered_df['subarea_colors'] = subarea_colors[value]
    filtered_df['subarea_colors'] = filtered_df['subarea'].map(subarea_colors[value])
    map_df = sp.filter_district(df, value).sort('subarea')
    map_df = sp.cast_to_datetime(map_df)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'mapbox'}, {'type': 'xy'}]],
        horizontal_spacing=0.06
    )

    fig.append_trace(go.Bar(x=filtered_df['subarea'], y=filtered_df['avg(carga)'],
                            legendgroup='subareas',
                            marker=dict(color=filtered_df['subarea_colors']),
                            opacity=0.7,
                            hoverinfo='skip',
                            showlegend=False), 1, 2)

    # TODO fix minsize. sizemin property of marker is not valid in scattermapbox because potato
    trace = go.Scattermapbox(lat=map_df['latitud'], lon=map_df['longitud'],
                             legendgroup='subareas',
                             mode='markers',
                             marker=dict(sizemode='area',
                                         color=map_df['subarea_color']),
                             hovertext=map_df['subarea'],
                             marker_size=map_df.carga,
                             showlegend=False)

    district_center = districts[value]
    lon_foc = district_center[0]
    lat_foc = district_center[1]

    fig.update_layout(mapbox=dict(style='open-street-map', center=dict(lat=lat_foc, lon=lon_foc), zoom=12),
                      margin=dict(l=5, r=5, t=5, b=5))

    fig.append_trace(trace, 1, 1)
    fig['layout']['yaxis']['title'] = 'Nivel de Carga'

    return fig


@app.callback(Output('temp-series', 'figure'),
              Input('district-dropdown', 'value'),
              Input('interval-component', 'n_intervals'))
def plot_temp_series(value, n_intervals):
    district = value
    filtered_df = sp.agg_subzones_of_district_by_time(temp_series_df, district)
    filtered_df = sp.cast_to_datetime(filtered_df)
    filtered_df.pivot(index='fecha_hora', columns='subarea', values='avg(carga)')
    fig = px.line(filtered_df, x='fecha_hora', y='avg(carga)', color='subarea')
    fig.update_xaxes(rangeselector=dict(buttons=list([
        dict(count=1, label='1H', step='hour', stepmode='backward'),
        dict(count=6, label='6H', step='hour', stepmode='backward'),
        dict(count=1, label='1d', step='day', stepmode='backward'),
        dict(count=1, label='1m', step='month', stepmode='backward')
    ])))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    return fig


@app.callback(Output('highest-occupation', 'figure'),
              Input('district-dropdown', 'value'),
              Input('interval-component', 'n_intervals'))
def plot_most_traffic_sensors(value, n_intervals):
    filtered_df = sp.filter_district(df, value)
    filtered_df = sp.get_n_first_elements_by_field(filtered_df, 10, 'intensidad')
    fig = px.bar(filtered_df, y='idelem', x='intensidad',
                 orientation='h', color='subarea_color',
                 hover_data={'subarea_color': False, 'idelem': False, 'intensidad': False,
                             'descripcion': True, 'intensidadSat': True})
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    return fig


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/districts":
        return district_layout
    else:
        return index_page


if __name__ == "__main__":
    try:
        app.run_server(debug=True)
    except KeyboardInterrupt:
        mongo.close_connection()
        print('Interrupted')

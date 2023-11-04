from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from pyspark.sql.types import StringType
import json
import plotly.graph_objects as go
import plotly.express as px
# import plotly.io as pio
import structlog

from main_spark import df_pipeline, get_spark_session
from spark_process import field_larger_than, agg_districts, agg_subzones_of_district, get_historic_data_df
from spark_process import filter_district, agg_subzones_of_district_by_time, cast_to_datetime
from crud import mongo
import layout as lo
from schemas import historic_data_schema
from constants import GEOJSON_FILE, districts

structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.getLogger()

spark_session = get_spark_session()
app = Dash(external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)

df = df_pipeline(spark_session)  # Dataframe for the incoming data
temp_series_df = get_historic_data_df(spark_session, historic_data_schema)  # Dataframe for the historic data


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
    temp_series_df = get_historic_data_df(spark_session, historic_data_schema)  # Dataframe for the historic data
    return {}


# Load the graph from a json in a Store to avoid load time
# @callback(Output("map", "figure"), Input("interval-component", "n_intervals"),
#           State("map-data", 'data'))
# def display_map(n_intervals, data):
#     return dcc.Graph(figure=str(json.loads(data)))


# Filter the dataframe and display the map of the homepage
@app.callback(Output("map", "figure"), Input('interval-component', 'n_intervals'))
def get_index_map_data(n_intervals):
    filtered_df = field_larger_than(df, 'nivelServicio', 1)
    filtered_df = cast_to_datetime(filtered_df)

    lat_foc = 40.42532
    lon_foc = -3.686722

    fig_go = go.Figure(go.Scattermapbox(
        mode="markers",
        lat=filtered_df['latitud'], lon=filtered_df['longitud'], hovertext=filtered_df[['intensidad', 'descripcion']],
        marker=dict(color=filtered_df.intensidad, colorscale='bluered', showscale=False, cmin=0, cmax=2500)
    ))

    district_agg = agg_districts(df).toPandas()

    fig = px.choropleth_mapbox(district_agg, geojson=geojson, mapbox_style="open-street-map", color='avg(intensidad)',
                               locations='distrito', featureidkey='properties.name', color_continuous_scale='viridis',
                               opacity=0.6, center={'lat': lat_foc, 'lon': lon_foc}, zoom=10)

    fig.add_trace(fig_go.data[0])
    fig.update_layout(margin=dict(l=10, r=1, t=10, b=10))
    return fig


# Show map with every sensor of the dropdown selected district
@app.callback(Output("district-map", "figure"),
              Input('district-dropdown', 'value'),
              Input('interval-component', 'n_intervals'))
def get_district_map_data(value, n_intervals):
    district = value
    log.info(f"{district}")
    filtered_df = filter_district(df, district)
    filtered_df = cast_to_datetime(filtered_df)

    district_center = districts[district]
    lon_foc = district_center[0]
    lat_foc = district_center[1]
    log.info(str(lon_foc) + ", " + str(lat_foc))

    fig = px.scatter_mapbox(filtered_df, lat=filtered_df['latitud'], lon=filtered_df['longitud'],
                            mapbox_style="open-street-map", hover_data=filtered_df[['intensidad', 'descripcion']],
                            color_continuous_scale='bluered', center={'lat': lat_foc,  'lon': lon_foc}, zoom=13,
                            color='intensidad', color_continuous_midpoint=1000)

    fig.update_layout(margin=dict(l=10, r=5, t=10, b=10))
    return fig


@app.callback(Output('subzones-bar', 'figure'),
              Input('district-dropdown', 'value'),
              Input('interval-component', 'n_intervals'))
def plot_subzones_bar(value, n_intervals):
    district = value
    log.info(f"barplot: {district}")
    filtered_df = agg_subzones_of_district(df, district).toPandas()
    filtered_df = filtered_df.sort_index()

    fig = px.bar(filtered_df, x='subarea', y='avg(carga)')
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    return fig


@app.callback(Output('temp-series', 'figure'), [Input('district-dropdown', 'value')])
def plot_temp_series(value):
    district = value
    filtered_df = agg_subzones_of_district_by_time(df, district)
    filtered_df = cast_to_datetime(filtered_df)
    filtered_df.pivot(index='fecha_hora', columns='subarea', values='avg(carga)')
    fig = px.line(filtered_df, x='fecha_hora', y='avg(carga)',)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
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

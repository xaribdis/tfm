from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import json
import plotly.graph_objects as go
import plotly.express as px

from main_spark import df_pipeline, get_spark_session
import spark_process as sp
from crud import mongo
import layout as lo
from schemas import historic_data_schema
from constants import GEOJSON_FILE
import graphs as gr


spark_session = get_spark_session()
app = Dash(external_stylesheets=[dbc.themes.YETI], suppress_callback_exceptions=True)

# Store in serverside
df = df_pipeline(spark_session)  # Dataframe for the incoming data
time_series_df = sp.get_historic_data_df(spark_session, historic_data_schema)  # Dataframe for the historic data


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
    global time_series_df
    df = df_pipeline(spark_session)
    time_series_df = sp.get_historic_data_df(spark_session, historic_data_schema)  # Dataframe for the historic data
    return {}


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


# Attempt to refactorice, so filter_district is not called unnecessarily, but does not work
# and the error does not give any information. Possibly a bug of Dash.
# @app.callback(Output("subarea-plots", "figure"), Output('highest-occupation', 'figure'),
#               Input('district-dropdown', 'value'), Input('interval-component', 'n_intervals'))
# def update_district_graphs(value, n_intervals):
#     district_df = sp.filter_district(df, value)
#
#     subarea_plots = gr.subarea_plots(district_df, value)
#     highest_occupation_graph = gr.plot_highest_traffic_sensors(district_df)
#
#     return subarea_plots, highest_occupation_graph
#
#
# @app.callback(Output('temp-series', 'figure'), Output('subarea-boxplots', 'figure'),
#               Input('district-dropdown', 'value'), Input('interval-component', 'n_intervals'))
# def update_district_graphs(value, n_intervals):
#     district_timeseries = sp.filter_district(time_series_df, value)
#
#     time_series_graph = gr.plot_time_series(time_series_df)
#     boxplots = gr.plot_subarea_box(time_series_df, value)
#
#     return time_series_graph, boxplots


# District map with every sensor colored by subarea, and size dependant on charge percentage.
@app.callback(Output("subarea-plots", "figure"),
              Input('district-dropdown', 'value'),
              Input('interval-component', 'n_intervals'))
def subarea_plots(value, n_intervals):
    return gr.subarea_plots(df, value)


# Time series with the average charge of a district. Time selector for last hour, 6 h, 1 day and 1 month.
@app.callback(Output('temp-series', 'figure'),
              Input('district-dropdown', 'value'),
              Input('interval-component', 'n_intervals'))
def plot_time_series(value, n_intervals):
    return gr.plot_time_series(time_series_df, value)


# Recover the 10 sensors that detect highest traffic
@app.callback(Output('highest-occupation', 'figure'),
              Input('district-dropdown', 'value'),
              Input('interval-component', 'n_intervals'))
def plot_highest_traffic_sensors(value, n_intervals):
    return gr.plot_highest_traffic_sensors(df, value)


# # Boxplot for time series of district subareas
@app.callback(Output('subarea-boxplots', 'figure'),
              Input('district-dropdown', 'value'),
              Input('interval-component', 'n_intervals'))
def plot_subarea_box(value, n_intervals):
    return gr.plot_subarea_box(time_series_df, value)


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/districts":
        return district_layout
    else:
        return index_page


if __name__ == "__main__":
    try:
        app.run_server(host='0.0.0.0', debug=True)
    except KeyboardInterrupt:
        mongo.close_connection()
        print('Interrupted')

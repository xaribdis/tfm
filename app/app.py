from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import json
import plotly.graph_objects as go
import plotly.express as px
from main_spark import df_pipeline
from spark_process import field_larger_than, agg_districts, agg_subzones_of_district
from crud import mongo
import layout as lo
import constants as c


app = Dash(external_stylesheets=[dbc.themes.DARKLY])

df = df_pipeline() # Dataframe for the incoming data
# temp_series_df = temp_series() # Dataframe for the historic data

geojsonfile = c.GEOJSON_FILE
with open(geojsonfile) as file:
    geojson = json.load(file)

server = app.server

"""Homepage"""
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(
            html.Div(lo.BUTTON_LAYOUT), width=4),
        dbc.Col(width=7),
    ], justify='center'),
    html.Br(),
    html.Br(),
    html.Div(id='page-content'),
])

index_page = html.Div([
    html.H1(children='Homepage', style={'textAlign': 'center'}),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # Time interval in ms
        n_intervals=0
    ),
    dcc.Graph(id="map"),
])

"""District layout"""
district_layout = lo.set_district_layout()


@app.callback(Output("map", "figure"), Input('interval-component', 'n_intervals'))
def display_map(n_intervals):
    global df
    df = df_pipeline()
    filtered_df = field_larger_than(df, 'nivelServicio', 1).toPandas()

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
    return fig


@app.callback(Output('subzones-bar', 'figure'), [Input('district-dropdown', 'value')])
def plot_subzones_bar(district):
    filtered_df = agg_subzones_of_district(df, district).toPandas()
    filtered_df.sort_index()
    fig = px.bar(filtered_df, x='subarea', y='carga')
    return fig


@app.callback(Output('subzones-bar', 'figure'), [Input('district-dropdown', 'value')])
def plot_temp_series(district):
    filtered_df = df.filter(district).toPandas()
    filtered_df.sort_index()
    fig = px.bar(filtered_df, x='subarea', y='carga')
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

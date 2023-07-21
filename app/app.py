from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import json
import plotly.graph_objects as go
import plotly.express as px
from main_spark import df_pipeline
from spark_process import field_larger_than, agg_districts
from crud import mongo


app = Dash(external_stylesheets=[dbc.themes.DARKLY])

geojsonfile = "data/madrid-districts.geojson"
with open(geojsonfile) as file:
    geojson = json.load(file)

lat_foc = 40.42532
lon_foc = -3.686722

server = app.server

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    dcc.Graph(id="graph"),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # Time interval in ms
        n_intervals=0
    )
])


@app.callback(
    Output("graph", "figure"), Input('interval-component', 'n_intervals'))
def display_map(n):
    df = df_pipeline()
    filtered_df = field_larger_than(df, 'nivelServicio', 1).toPandas()

    fig_go = go.Figure(go.Scattermapbox(
        mode="markers",
        lat=filtered_df['latitud'], lon=filtered_df['longitud'], hovertext=filtered_df[['intensidad', 'descripcion']],
        marker=dict(color=filtered_df.intensidad, colorscale='bluered', showscale=False, cmin=0, cmax=2500)
    ))

    district_agg = agg_districts(df).toPandas()

    # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
    #                   mapbox={
    #                       'style': "open-street-map",
    #                       'center': {'lat': lat_foc, 'lon': lon_foc},
    #                       'zoom': 10, 'layers': [{
    #                           'source': geojson,
    #                           'type': 'line', 'below': 'traces', 'color': 'blue', 'opacity': 1}]},
    #                   geo=dict(projection_scale=1000,
    #                            center=dict(lat=lat_foc, lon=lon_foc)))

    fig = px.choropleth_mapbox(district_agg, geojson=geojson, mapbox_style="open-street-map",
                                  color='avg(intensidad)', locations='distrito', featureidkey='properties.name',
                                  color_continuous_scale='viridis', opacity=0.4, center={'lat': lat_foc, 'lon': lon_foc}, zoom=10)

    fig.add_trace(fig_go.data[0])
    # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__ == "__main__":
    try:
        app.run_server(debug=True)
    except KeyboardInterrupt:
        mongo.close_connection()
        print('Interrupted')


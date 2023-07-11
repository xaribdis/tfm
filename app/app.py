from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
# import plotly.graph_objects as go
from main import df_pipeline


app = Dash(external_stylesheets=[dbc.themes.DARKLY])

lat_foc = 40.42532
lon_foc = -3.686722

server = app.server

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    dcc.Graph(id="graph"),
    dcc.Interval(
        id='interval-component',
        interval=30*1000,
        n_intervals=0
    )
])


@app.callback(
    Output("graph", "figure"), Input('interval-component', 'n_intervals'))
def display_map(n):
    geojson = "data/madrid-districts.geojson"
    df = df_pipeline()

    fig = px.scatter_geo(df, "latitud", "longitud", color="intensidad",
                         color_continuous_scale=px.colors.cyclical.IceFire, hover_data="descripcion",
                         geojson=geojson)
    fig.update_geos(visible=False, showcountries=True, showsubunits=True)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      geo=dict(projection_scale=1000,
                               center=dict(lat=lat_foc, lon=lon_foc)))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
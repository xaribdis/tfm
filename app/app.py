from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px


app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    dcc.Graph(id="graph")
])


@app.callback(
    Output("graph", "figure"))
def display_map(df):
    geojson = ""

    fig = px.scatter_mapbox(df, "st_x", "st_y", color="intensidad", color_continuous_scale=px.colors.cyclical.IceFire)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

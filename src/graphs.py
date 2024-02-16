import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

import spark_process as sp
from config import settings


def subarea_plots(df, value):
    district_df = sp.filter_district(df, value)
    filtered_df = sp.agg_subzones_of_district(district_df, value).sort('subarea').toPandas()
    filtered_df['subarea_colors'] = filtered_df['subarea'].map(settings.SUBAREA_COLORS[value])
    map_df = sp.cast_to_datetime(district_df)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'mapbox'}, {'type': 'xy'}]],
        horizontal_spacing=0.06
    )

    fig.append_trace(go.Bar(x=filtered_df['subarea'], y=filtered_df['avg(carga)'],
                            legendgroup='subareas',
                            marker=dict(color=filtered_df['subarea_colors']),
                            opacity=0.8,
                            hoverinfo='skip',
                            showlegend=False), 1, 2)

    # TODO sizemin property of marker is not valid in scattermapbox because potato
    trace = go.Scattermapbox(lat=map_df['latitud'], lon=map_df['longitud'],
                             legendgroup='subareas',
                             mode='markers',
                             marker=dict(sizemode='area', 
                                         color=map_df['subarea_color']),
                             hovertext=map_df['subarea'],
                             marker_size=map_df.carga,
                             showlegend=False)

    district_center = settings.DISTRICTS[value]
    lon_foc = district_center[0]
    lat_foc = district_center[1]

    fig.update_layout(mapbox=dict(style='open-street-map', center=dict(lat=lat_foc, lon=lon_foc), zoom=12),
                      margin=dict(l=5, r=5, t=5, b=5))

    fig.append_trace(trace, 1, 1)
    fig['layout']['yaxis']['title'] = 'nivel de carga'

    return fig


def plot_time_series(df, value):
    district_df = sp.filter_district(df, value)
    filtered_df = sp.agg_district_by_time(district_df)
    filtered_df = sp.cast_to_datetime(filtered_df)

    fig = px.line(filtered_df, x='fecha_hora', y='avg(carga)')
    fig.update_xaxes(rangeselector=dict(buttons=list([
        dict(count=1, label='1H', step='hour', stepmode='backward'),
        dict(count=6, label='6H', step='hour', stepmode='backward'),
        dict(count=1, label='1d', step='day', stepmode='backward'),
        dict(count=1, label='1m', step='month', stepmode='backward')
    ])))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    return fig


def plot_highest_traffic_sensors(df, value):
    district_df = sp.filter_district(df, value)
    filtered_df = sp.get_n_first_elements_by_field(district_df, 10, 'intensidad')

    fig = px.bar(filtered_df, y='idelem', x='intensidad', opacity=0.8,
                 orientation='h', color='subarea_color',
                 hover_data={'subarea_color': False, 'idelem': False, 'intensidad': False,
                             'descripcion': True, 'intensidadSat': True})
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    return fig


def plot_subarea_box(df, value):
    district_df = sp.filter_district(df, value)
    filtered_df = sp.agg_subzones_of_district_by_time(district_df)
    filtered_df = sp.cast_to_datetime(filtered_df)
    filtered_df = filtered_df.pivot(index='fecha_hora', columns='subarea', values='avg(carga)').drop(columns=np.nan, errors='ignore')

    fig = go.Figure(data=[go.Box(
        y=filtered_df[col].values, name=col, marker_color=settings.SUBAREA_COLORS[value].get(col, "hsl(70, 8%, 15%)"), opacity=0.8) for col in filtered_df])
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    fig.update_yaxes(title="avg(carga)", range=[0, 100])

    return fig


def plot_count_service_levels(df, value):
    district_df = sp.filter_district(df, value)
    district_df = district_df.select('idelem', 'nivelServicio').toPandas()

    agg_df = district_df.groupby('nivelServicio').count().reset_index()

    fig = px.pie(agg_df, values='idelem', names='nivelServicio', width=450, height=450)
    fig.update_layout(margin=dict(l=15, r=15, t=15, b=15), showlegend=True)
    return fig

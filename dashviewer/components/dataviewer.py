# notes
'''
This file is for creating the sidebar element for the dash app.
This component will sit at the bottom side of the application.
'''

# package imports
from dash import Dash, html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
from ecoviewer.display import get_state_colors
from utils.images import logo_encoded

CONTENT_STYLE = {
    "position": "fixed",
    "left": 0,
    "right": 0,
    "top": 0,
    "bottom": 0,
    "margin-left": "21rem",
    "padding": "2rem 1rem",
    "overflow": "scroll"
}
#################################

# Create the graphs to display the data
graphs = html.Div(id='graph-container')
summary = html.Div(id='summary-container')
hourly_shapes = html.Div(id='hourly-shapes-container')

data_viewer_component = html.Div(
    [
        html.H1(children='Data Dashboard', style={'textAlign':'center'}),
        dcc.Tabs(id='tabs', value='tab-4', children=[
            dcc.Tab(label='Summary Data', value='tab-4', children=[
                summary,
            ]),
            dcc.Tab(label='Raw Data', value='tab-1', children=[
                graphs,
            ]),
            dcc.Tab(label='Hourly Shapes', value='tab-3', children=[
                hourly_shapes,
            ]),
            dcc.Tab(label='Dictionary', value='tab-2', children=[
                html.Div(id='data-dictionary'),
            ]),
        ])
    ], style=CONTENT_STYLE,
)

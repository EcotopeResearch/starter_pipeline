# notes
'''
This file is for creating the sidebar element for the dash app.
This component will sit at the bottom side of the application.
'''

# package imports
from dash import html, dcc
import dash_bootstrap_components as dbc
from ecoviewer.display import get_state_colors
from utils.images import logo_encoded

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "19rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}

color_key = html.Div(
    className='color-key',
    children=[
        html.Div(
            className='legend-title',
            children='Shading Legend:'
        ),
        *[ 
            html.Div(
                children=[
                    html.Span(children=f"{state}: ",), 
                    html.Span(
                        style={
                            'background-color': get_state_colors()[state],
                            'display': 'inline-block',
                            'width': '15px',
                            'height': '15px',
                            'opacity': '0.2',
                            'margin-right': '5px'
                        }
                    )
                ]
            )
            for state in get_state_colors()
        ]
    ],
)

sidebar = html.Div(
    [
        dcc.Link(
            html.Img(
                style={'width':'65%', 'margin-left': '10px'},
                src=logo_encoded#app.get_asset_url("logo_Ecotope_clear_bkgnd.png")
            ),
            href='https://www.ecotope.com/',
            target='_blank' # this line make the link open in a new tab
        ),
        html.Hr(),
        html.H3("Filter Options"),
        html.Label("Date Range:"),
        dcc.DatePickerRange(
            id="date-range-picker",
            start_date_placeholder_text="start date",
            end_date_placeholder_text="end date",
        ),
        html.P(id='date-note', style={'color': 'blue'}),
        html.Br(),
        html.Label("Select Site:"),
        dcc.Dropdown(
            id='site-selection'
        ),
        html.Br(),
        dcc.Checklist(
            id='checkbox-selection',
            options=[
                {'label': 'Retrieve Raw Data', 'value': 'get_raw_data'},
                {'label': 'State Shading', 'value': 'state_shading'},
            ],
            value = ['get_raw_data']
        ),
        html.Br(),
        color_key,
        html.P(style={'color': 'blue'}, children=
            'If using state shading, it is recommended to use smaller time frames as this may slow run time.'
        ),
        html.Br(),
        html.Button(id='go-button', n_clicks=0, children='Go', style={'marginRight': '20px'}),
        html.Button("Download csv", id="csv-download-button", n_clicks=0), 
        dcc.Download(id="download"),
    ],
    style=SIDEBAR_STYLE,
)
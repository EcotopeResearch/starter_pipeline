from flask import request
import requests
from dash import Dash, html, dcc, Output, Input, State, dash_table
import pandas as pd
import mysql.connector
from ecoviewer.config import *
from ecoviewer.display import *
import os
from datetime import datetime
from components import sidebar, data_viewer_component
from utils.dataviewer_utils import get_application_content

app = Dash(__name__)
#################################

app.layout = html.Div([
    sidebar,
    data_viewer_component
])

################################################
### FUNCTIONS ###
################################################

@app.callback(
    Output('site-selection', 'options'),
    Output('site-selection', 'value'),
    Output('graph-container', 'children'),
    Output('summary-container', 'children'),
    Output('hourly-shapes-container', 'children'),
    Output('data-dictionary', 'children'),
    Output('date-note', 'children'),
    Output('date-range-picker', 'start_date'),
    Output('date-range-picker', 'end_date'),
    Input('go-button', 'n_clicks'),
    State('site-selection', 'value'),
    State('date-range-picker', 'start_date'),
    State('date-range-picker', 'end_date'),
    State('checkbox-selection', 'value'),
)
def update_application(n_clicks, selected_table, start_date, end_date, checkbox_selections):
    user_email = "nolan@ecotope.com"
    return get_application_content(user_email, n_clicks, selected_table, start_date, end_date, checkbox_selections, app)

@app.callback(
        Output("download", "data"), 
        State('site-selection', 'value'),
        State('date-range-picker', 'start_date'),
        State('date-range-picker', 'end_date'),
        [Input("csv-download-button", "n_clicks")])
def generate_csv(selected_table, start_date, end_date, n_clicks):
    if n_clicks > 0:
    
        site_df, table_names = get_site_df_from_ini(os.path.abspath("../code/Pipeline/src/Config.ini"))
        field_df = get_field_df_from_csv(os.path.abspath("../input/Variable_Names.csv"), site_df.index.to_list()[0])
        min_table = site_df.loc[selected_table, 'minute_table']
        hour_table = site_df.loc[selected_table, 'hour_table']
        day_table = site_df.loc[selected_table, 'daily_table']
        db_name = site_df.loc[selected_table, 'db_name']
        # Create a connection object
        cnx = mysql.connector.connect(
                host=site_df.loc[selected_table, 'db_host'],
                user=site_df.loc[selected_table, 'db_user'],
                password=site_df.loc[selected_table, 'db_pw'],
                database=db_name
            )
        cursor = cnx.cursor()

        query = generate_raw_data_query(min_table, hour_table, day_table, field_df, selected_table, state_tracking = False,
                                        start_date = start_date, end_date = end_date)

        df = get_df_from_query(query, cursor)

        # close db connections
        cursor.close()
        cnx.close()
        
        df = df.set_index('time_pt')
        field_df = field_df[field_df['site_name'] == selected_table]
        fields_to_keep = field_df['field_name'].values
        fields_to_keep = [x for x in fields_to_keep if x in df.columns]
        df = df[fields_to_keep]
        rename_mapping = field_df.set_index('field_name').loc[fields_to_keep]['pretty_name'].to_dict()
        df.rename(columns=rename_mapping, inplace=True)

        if not df.empty:
            return dcc.send_data_frame(df.to_csv, filename=f"{selected_table}_{df.index[0]}_through_{df.index[-1]}.csv")
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
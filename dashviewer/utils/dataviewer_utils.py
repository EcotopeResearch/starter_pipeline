from dash import Dash, html
import pandas as pd
import mysql.connector
from ecoviewer.config import *
from ecoviewer.display import *
import os

def return_error_values(display_message):
    return [
        [],
        None,
        display_message, #Output('graph-container', 'children'),
        display_message, #Output('summary-container', 'children'),, #Output('summary-container', 'children'),
        display_message, #Output('hourly-shapes-container', 'children'),
        display_message, #Output('data-dictionary', 'children'),
        "If no date range is filled, The last three days of raw data and last 30 days of summary data will be returned.", #Output('date-note', 'children'),
        None, #Output('date-range-picker', 'start_date'),
        None, #Output('date-range-picker', 'end_date')
    ]

def get_application_content(n_clicks, selected_table, start_date, end_date, checkbox_selections, app : Dash):
    try:

        site_df, table_names = get_site_df_from_ini(os.path.abspath("../code/Pipeline/src/Config.ini"))
        graph_df = get_graph_df_from_csv(os.path.abspath("../input/Graph_Config.csv"))
        field_df = get_field_df_from_csv(os.path.abspath("../input/Variable_Names.csv"), site_df.index.to_list()[0])
        if len(table_names) == 0:
            return return_error_values("Error: No data available. Application is not configured correctly")

        if selected_table is None:
            selected_table = table_names[0]['value']
        raw_data_pull = False
        if is_within_raw_data_limit(start_date, end_date) and 'get_raw_data' in checkbox_selections:
            raw_data_pull = True

        raw_graphs, hourly_shapes, start_date, end_date, organized_mapping = get_graph_container_content(selected_table, site_df, graph_df, field_df, table_names, checkbox_selections, start_date, end_date, raw_data_pull, n_clicks)
        
        summary_output, start_date, end_date = get_summary_content(selected_table, site_df, field_df, raw_data_pull, start_date, end_date, app)
        db_name = site_df.loc[selected_table, 'db_name']
        site_pretty_name = site_df.loc[selected_table, "pretty_name"]


        date_string = "If no date range is filled, The last three days of raw data and last 30 days of summary data will be returned."
        if n_clicks != 0:
            # Create a connection object
            cnx = mysql.connector.connect(
                    host=site_df.loc[selected_table, 'db_host'],
                    user=site_df.loc[selected_table, 'db_user'],
                    password=site_df.loc[selected_table, 'db_pw'],
                    database=db_name
                )
            cursor = cnx.cursor()
            date_string = create_date_note(selected_table, cursor, site_pretty_name)
            cursor.close()
            cnx.close()
        return [
            table_names,
            selected_table,
            raw_graphs, #Output('graph-container', 'children'),
            summary_output, #Output('summary-container', 'children'),, #Output('summary-container', 'children'),

            hourly_shapes, #Output('hourly-shapes-container', 'children'),
            create_data_dictionary(organized_mapping), #Output('data-dictionary', 'children'),
            date_string, #Output('date-note', 'children'),
            start_date, #Output('date-range-picker', 'start_date'),
            end_date, #Output('date-range-picker', 'end_date')
        ]
    
    except Exception as e:
        return return_error_values(html.P(style={'color': 'red', 'textAlign': 'center'}, children=[
                                        html.Br(),
                                        f"An error occurred: {str(e)}"
                                    ])
        )

def get_summary_content(selected_table, site_df, field_df, raw_data_pull, start_date, end_date, app : Dash):

    hour_table = site_df.loc[selected_table, 'hour_table']
    day_table = site_df.loc[selected_table, 'daily_table']
    db_name = site_df.loc[selected_table, 'db_name']
    load_shift_tracking = site_df.loc[selected_table, 'load_shift_tracking']

    summary_query = generate_summary_query(day_table, numDays = 30, start_date = start_date, end_date = end_date)
    hourly_summary_query = generate_hourly_summary_query(hour_table, day_table, numHours = 740, load_shift_tracking = load_shift_tracking,
                                                        start_date = start_date, end_date = end_date)

    # Create a connection object
    cnx = mysql.connector.connect(
            host=site_df.loc[selected_table, 'db_host'],
            user=site_df.loc[selected_table, 'db_user'],
            password=site_df.loc[selected_table, 'db_pw'],
            database=db_name
        )
    cursor = cnx.cursor()

    summary_df = get_df_from_query(summary_query, cursor)
    hourly_summary_df = get_df_from_query(hourly_summary_query, cursor)

    # Filter hourly_summary_df to include only the desired range
    start = summary_df['time_pt'].min()
    end = summary_df['time_pt'].max() + pd.DateOffset(days=1)  # Extend to the end of the last day
    hourly_summary_df = hourly_summary_df[
        (hourly_summary_df['time_pt'] >= start) & (hourly_summary_df['time_pt'] < end)
    ]

    if 'load_shift_day' in hourly_summary_df.columns:
        hourly_summary_df["load_shift_day"] = hourly_summary_df["load_shift_day"].fillna(method='ffill') #ffill loadshift day
    else:
        hourly_summary_df["load_shift_day"] = 'normal'

    summary_df = summary_df.set_index('time_pt')
    hourly_summary_df = hourly_summary_df.set_index('time_pt')

    if not raw_data_pull:
        # we know this is intentional so we should update the dates
        if start_date is None:
            start_date = summary_df.index[0].date()
        if end_date is None:
            end_date = summary_df.index[-1].date()

    if selected_table == 'bayview':
        hourly_summary_df = bayview_prune_additional_power(hourly_summary_df)
        hourly_summary_df = bayview_power_processing(hourly_summary_df)
        summary_df = bayview_prune_additional_power(summary_df)
        summary_df = bayview_power_processing(summary_df)

    summary_output = [
            *create_summary_graphs(summary_df, hourly_summary_df, field_df[field_df['site_name'] == selected_table], site_df.loc[selected_table], cursor),
            create_meta_data_table(site_df, selected_table, app)
        ]
    # close db connections
    cursor.close()
    cnx.close()

    return [
        summary_output, #Output('summary-container', 'children'),, #Output('summary-container', 'children'),
        start_date, #Output('date-range-picker', 'start_date'),
        end_date, #Output('date-range-picker', 'end_date')
    ]

def get_graph_container_content(selected_table, site_df, graph_df, field_df, table_names, checkbox_selections, start_date, end_date,
                                raw_data_pull, n_clicks):
    
    if not raw_data_pull or n_clicks == 0:
        display_message = html.P(style={'color': 'black', 'textAlign': 'center'}, children=[
            html.Br(),
            f"Hello! Please enter parameters then press 'Go' to view data."
        ])
        if not raw_data_pull:
            display_message = get_no_raw_retrieve_msg()

        return [
            display_message, #Output('summary-container', 'children'),
            display_message, #Output('hourly-shapes-container', 'children'),
            start_date,
            end_date,
            {}
        ]

    if selected_table is None:
        selected_table = table_names[0]['value']
    
    min_table = site_df.loc[selected_table, 'minute_table']
    hour_table = site_df.loc[selected_table, 'hour_table']
    day_table = site_df.loc[selected_table, 'daily_table']
    db_name = site_df.loc[selected_table, 'db_name']
    state_tracking = site_df.loc[selected_table, 'state_tracking']

    # Create a connection object
    cnx = mysql.connector.connect(
            host=site_df.loc[selected_table, 'db_host'],
            user=site_df.loc[selected_table, 'db_user'],
            password=site_df.loc[selected_table, 'db_pw'],
            database=db_name
        )
    cursor = cnx.cursor()
    
    query = generate_raw_data_query(min_table, hour_table, day_table, field_df, selected_table, state_tracking = state_tracking,
                                    start_date = start_date, end_date = end_date)
    df = get_df_from_query(query, cursor)
    
    cursor.close()
    cnx.close()

    # Forward fill values in columns with "COP" in their names
    cop_columns = [col for col in df.columns if 'COP' in col]
    df[cop_columns] = df[cop_columns].fillna(method='ffill')
    if 'OAT_NOAA' in df.columns:
        df["OAT_NOAA"] = df["OAT_NOAA"].fillna(method='ffill')
    if 'system_state' in df.columns:
        df["system_state"] = df["system_state"].fillna(method='ffill')

    if df.empty:
        display_message = html.P(style={'color': 'red', 'textAlign': 'center'}, children=[
            html.Br(),
            "No data available for parameters specified."
        ])
        # close db connections
        return [
            display_message, #Output('summary-container', 'children'),
            display_message, #Output('hourly-shapes-container', 'children'),
            start_date,
            end_date,
            {}
        ]

    df = df.set_index('time_pt')
    
    # Remove columns with no data
    df = df.dropna(axis=1, how='all')
    # Deal with date
    if start_date is None:
        start_date = df.index[0].date()
    if end_date is None:
        end_date = df.index[-1].date()

    organized_mapping = get_organized_mapping(df.columns, graph_df, field_df, selected_table)
    shading = False
    if 'state_shading' in checkbox_selections:
        shading = True

    return [
        create_conjoined_graphs(df, organized_mapping, shading), #Output('graph-container', 'children')
        create_hourly_shapes(df, graph_df, field_df, selected_table), #Output('hourly-shapes-container', 'children')
        start_date,
        end_date,
        organized_mapping
    ]
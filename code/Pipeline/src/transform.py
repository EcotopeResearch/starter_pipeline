from ecopipeline import rename_sensors, rename_sensors_by_system, avg_duplicate_times, aggregate_df
from config import _config_directory, _data_directory, _output_directory, _input_directory
import pandas as pd


def transform(df): 
    
    df = rename_sensors(df)
    
    df = avg_duplicate_times(df, None)
    
    hourly_df, daily_df = aggregate_df(df)
    
    return df, hourly_df, daily_df





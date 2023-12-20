from ecopipeline import rename_sensors, avg_duplicate_times, aggregate_df
import pandas as pd


def transform(df): 
    
    df = rename_sensors(df)
    
    df = avg_duplicate_times(df, None)
    
    hourly_df, daily_df = aggregate_df(df)
    
    return df, hourly_df, daily_df





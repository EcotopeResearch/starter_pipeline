from ecopipeline.transform import rename_sensors, avg_duplicate_times, aggregate_df
import pandas as pd
from ecopipeline import ConfigManager


def transform(df, config : ConfigManager): 
    
    df = rename_sensors(df, config)
    
    df = avg_duplicate_times(df, None)
    
    hourly_df, daily_df = aggregate_df(df)
    
    return df, hourly_df, daily_df





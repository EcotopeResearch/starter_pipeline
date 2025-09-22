"""
Alarm

"""
from ecopipeline import ConfigManager
from ecopipeline.event_tracking import central_alarm_df_creator
from ecopipeline.load import load_event_table
import pandas as pd

def alarm(df : pd.DataFrame, daily_data : pd.DataFrame, config : ConfigManager):
    alarm_df = central_alarm_df_creator(df,daily_data, config)
    if len(alarm_df) > 0:
        load_event_table(config, alarm_df)
    
    
    
"""
Alarm

"""
from ecopipeline import ConfigManager
from ecopipeline.event_tracking import flag_boundary_alarms
from ecopipeline.load import load_event_table
import pandas as pd

def alarm(df : pd.DataFrame, config : ConfigManager):
    print('Checking for alarms...')
    alarm_df = flag_boundary_alarms(df, config)

    if len(alarm_df) > 0:
        print("Alarms detected. Adding them to site_events table...")
        load_event_table(config, alarm_df)
    else:
        print("No alarms detected.")
    
    
    
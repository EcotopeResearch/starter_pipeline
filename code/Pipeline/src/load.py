from ecopipeline.load import load_overwrite_database
from ecopipeline import ConfigManager
import pandas as pd
import traceback

def load(load_dfs: dict, config : ConfigManager):
    
    config_dict = config.get_db_table_info(load_dfs.keys()) 
    db_connection, db_cursor = config.connect_db()
    
    try:
    
        for df in load_dfs:
            
            load_overwrite_database(cursor = db_cursor, dataframe = load_dfs[df], config_info = config_dict, data_type = df)
            db_connection.commit()
    except Exception as e: traceback.print_exc()
        
        
    db_connection.close()
    db_cursor.close()
    

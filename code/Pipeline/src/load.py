from ecopipeline import get_login_info, connect_db, load_overwrite_database
import pandas as pd
import traceback

def load(load_dfs: dict):
    config_dict = get_login_info(load_dfs.keys())
    
    db_connection, db_cursor = connect_db(config_dict['database'])
    
    try:
    
        for df in load_dfs:
            
            load_overwrite_database(cursor = db_cursor, dataframe = load_dfs[df], config_info = config_dict, data_type = df)
            db_connection.commit()
    except Exception as e: traceback.print_exc()
        
        
    db_connection.close()
    db_cursor.close()
    
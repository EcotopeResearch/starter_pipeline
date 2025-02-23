from ecopipeline.load import load_overwrite_database
from ecopipeline import ConfigManager


def load(load_dfs: dict, config : ConfigManager):
    
    config_dict = config.get_db_table_info(load_dfs.keys())
    
    for df in load_dfs:   
        load_overwrite_database(config, dataframe = load_dfs[df], config_info = config_dict, data_type = df)

    

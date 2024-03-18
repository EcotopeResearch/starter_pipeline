import pandas as pd
from ecopipeline.extract import extract_files, csv_to_df, get_last_full_day_from_db, extract_new, json_to_df
from ecopipeline import ConfigManager

def extract(config : ConfigManager):
    ###############################################################
    ##### IF DATA IS MODBUS FORMAT, USE THIS SECTION ##############
    ########### OTHERWISE, DELETE THIS SECTION ####################
    ###############################################################
    filenames = extract_files('.csv', config)
    last_full_day = get_last_full_day_from_db(config).replace(tzinfo=None)
    filenames = extract_new(last_full_day, filenames, True)
    df = csv_to_df(filenames, True)
    # add any more custom extraction code you need using functions from ecopipeline

    ###############################################################
    ##### IF DATA IS RCC FORMAT, USE THIS SECTION #################
    ########### OTHERWISE, DELETE THIS SECTION ####################
    ###############################################################
    filenames = extract_files('.gz', config)
    last_full_day = get_last_full_day_from_db(config)
    filenames = extract_new(last_full_day, filenames)
    df = json_to_df(filenames)
    # add any more custom extraction code you need using functions from ecopipeline

    return df, last_full_day


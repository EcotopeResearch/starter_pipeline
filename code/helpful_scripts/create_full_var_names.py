import os
import csv
from pathlib import Path
from datetime import datetime, timedelta
import re
import pandas as pd
import gzip
import json

# ATTENTION: edit the data_directory varriable to be the path to the folder which contains modbus data files
data_directory = "../../data/path/to/modbus/folder"
file_suffix = ".csv" # ".gz" or ".csv"
data_after_year = 2023
data_after_month = 12
data_after_day = 1

#####################################################
######## LEAVE BELOW CODE ALONE #####################
#####################################################

def get_most_recent_files(directory_name : str, file_name_suffix : str):
    """
    Function to return a list of the most recent modbus files in a directory for every available modbus
    """
    filenames = []
    if file_name_suffix == ".gz":
        for file in os.listdir(directory_name):
            if file.endswith(file_name_suffix):
                filenames.append(file)
        data_after_date = datetime(data_after_year, data_after_month, data_after_day)
        startTime_int = int(data_after_date.strftime("%Y%m%d%H%M%S"))
        filenames = list(filter(lambda filename: int(filename[-17:-3]) >= startTime_int, filenames))
        return filenames

    elif file_name_suffix == ".csv":
        filenames = [filename for filename in os.listdir(directory_name) if filename.endswith(file_name_suffix) and filename.startswith('mb-')]
        most_recent_seen = {}
        most_recent_filename = {}
        base_date = datetime(1970, 1, 1)

        # Iterate through the files in the directory
        for filename in filenames:
            # Extract the prefix (e.g., 'mb-###') from the filename
            prefix = filename.split('.')[0]
            file_date = pd.Timestamp(base_date + timedelta(seconds = int(re.search(r'\.(.*?)_', filename).group(1), 16)))
            # Check if we've already seen this prefix or if it's the most recent file for the prefix
            if not (prefix in most_recent_seen) or most_recent_seen[prefix] < file_date:
                most_recent_seen[prefix] = file_date
                most_recent_filename[prefix] = filename

        return sorted([value for value in most_recent_filename.values()])
    
    else:
        raise Exception(f"unrecognized file suffix {file_name_suffix}")

output_file = '../../input/variable_names_full.csv'
column_names = []

# Iterate through the most recent files for each modbus
filenames = get_most_recent_files(data_directory, file_suffix)
if file_suffix == ".csv":
    for filename in filenames:
        prefix = filename.split('.')[0]

        # Open and read the CSV file
        with open(os.path.join(data_directory, filename), 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Read the header row

            # Add the prefix to each column name and store in the list
            for column in header:
                if column != '-':
                    column = column.replace(" ","_")
                    column_names.extend([f"{prefix}_{column}"])

elif file_suffix == ".gz":
    sensor_ids = set() 
    for file in filenames:
        try:
            with gzip.open(os.path.join(data_directory, file), 'rt', encoding='utf-8') as f:
                data = json.load(f)
                
                # Assuming data is a list of dictionaries
                if isinstance(data, list):
                    for entry in data:
                        if 'sensors' in entry and isinstance(entry['sensors'], list):
                            for sensor in entry['sensors']:
                                if 'id' in sensor and isinstance(sensor['id'], str):
                                    sensor_ids.add(sensor['id'])
                                else:
                                    raise Exception(f'Invalid sensor entry in {file}')
                else:
                    raise Exception(f'Invalid JSON structure in {file}')
        
        except FileNotFoundError:
            raise Exception(f"File Not Found: {file}")
        except json.decoder.JSONDecodeError:
            raise Exception(f'Empty or invalid JSON File in {file}')
    
    column_names = list(sensor_ids)
        

# Write the list to a new CSV file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the "variable_alias" row
    fieldnames = ["variable_alias","variable_name","pretty_name","descr","data_type","graph_id","secondary_axis","color","low_alarm","high_alarm","timeframe","alarm_priority","changepoint","ffill_length","lower_bound","upper_bound","system","summary_group"]  # Get the header from the input CSV
    writer.writerow(fieldnames)
    
    # Write the column names with prefixes
    for column_name in column_names:
        writer.writerow([column_name])

print(f'Full varriable names csv written to {output_file}.')
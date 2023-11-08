import os
import csv
from pathlib import Path
from datetime import datetime, timedelta
import re
import pandas as pd

# ATTENTION: edit the data_directory varriable to be the path to the folder which contains modbus data files
data_directory = "../../data/path/to/modbus/folder"

#####################################################
######## LEAVE BELOW CODE ALONE #####################
#####################################################

def get_most_recent_files(directory_name : str):
    """
    Function to return a list of the most recent modbus files in a directory for every available modbus
    """
    filenames = [filename for filename in os.listdir(directory_name) if filename.endswith('.csv') and filename.startswith('mb-')]
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

    return [value for value in most_recent_filename.values()]

output_file = '../../input/variable_names_full.csv'
column_names_with_prefix = []

# Iterate through the most recent files for each modbus
filenames = get_most_recent_files(data_directory)
for filename in filenames:
    prefix = filename.split('.')[0]

    # Open and read the CSV file
    with open(os.path.join(data_directory, filename), 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read the header row

        # Add the prefix to each column name and store in the list
        for column in header:
            if column != '-':
                column_names_with_prefix.extend([f"{prefix}_{column}"])

# Write the list to a new CSV file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the "variable_alias" row
    fieldnames = ["variable_alias","variable_name","pretty_name","descr","data_type","color","low_alarm","high_alarm","timeframe","alarm_priority","changepoint","ffill_length","lower_bound","upper_bound","system"]  # Get the header from the input CSV
    writer.writerow(fieldnames)
    
    # Write the column names with prefixes
    for column_name in column_names_with_prefix:
        writer.writerow([column_name])

print(f'Full varriable names csv written to {output_file}.')
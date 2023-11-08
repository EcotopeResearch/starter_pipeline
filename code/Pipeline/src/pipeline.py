from extract import extract
from transform import transform
from load import load


merged_data, last_full_day = extract()
print("last full day in database found", last_full_day)

transformed_data, hourly_data, daily_data = transform(merged_data.copy())

dfs_to_load = {"minute": transformed_data,
               "hour": hourly_data,
               "day": daily_data}

load(dfs_to_load)






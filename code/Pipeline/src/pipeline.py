from extract import extract
from transform import transform
from load import load
import traceback
from ecopipeline import ConfigManager

config = ConfigManager()
try:
    merged_data, last_full_day = extract(config)
    print("last full day in database found", last_full_day)

    transformed_data, hourly_data, daily_data = transform(merged_data.copy(), config)

    dfs_to_load = {"minute": transformed_data,
                "hour": hourly_data,
                "day": daily_data}

    load(dfs_to_load, config)
except Exception as e: 
        traceback.print_exc()
        # uncomment below to report data loss
        # report_data_loss(config)






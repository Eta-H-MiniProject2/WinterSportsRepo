import pandas as pd
import glob
import os

data_path = 'UV Helsinki/'

# Paths for data files
helsinki_path = 'Helsinki*' 
# Get all path for all the locations
all_helsinki_paths = glob.glob(helsinki_path)

# Combine all files
helsinki_df = pd.concat(map(pd.read_csv, all_helsinki_paths), ignore_index=True)

# Write to csv-files
helsinki_df.to_csv('helsinki_uv_all.csv', index=False)



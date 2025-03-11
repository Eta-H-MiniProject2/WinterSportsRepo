import pandas as pd
import glob
import os

data_path = 'Sotkamo_uv_index_raw_data/'

# Paths for data files
sotkamo_path = data_path + 'Sotkamo*' 
# Get all path for all the locations
all_sotkamo_paths = glob.glob(sotkamo_path)

# Combine all files
sotkamo_df = pd.concat(map(pd.read_csv, all_sotkamo_paths), ignore_index=True)

# Write to csv-files
sotkamo_df.to_csv('sotkamo_uv_all.csv', index=False)
import pandas as pd
import glob
import os

data_path = 'UV/UV Jyväskylä/'

# Paths for data files
jk_path = data_path + 'Jyväskylä*' 
# Get all path for all the locations
all_jk_paths = glob.glob(jk_path)
print(all_jk_paths)

# Combine all files
jk_df = pd.concat(map(pd.read_csv, all_jk_paths), ignore_index=True)

# Write to csv-files
jk_df.to_csv('jyväskylä_uv_all.csv', index=False)
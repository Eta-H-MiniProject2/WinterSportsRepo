import pandas as pd
import glob
import os


data_path = r'C:\Users\vuojo\Desktop\MINIPROJECT 2\Sodankylä_Tähtelä_uv_index_raw_data'

# Paths for data files
sk_path = os.path.join(data_path, 'Sodankylä*')

# Get all path for all the locations
all_sk_paths = glob.glob(sk_path)
print("Löydetyt tiedostot:", all_sk_paths)  # Debug

if not all_sk_paths:
    raise FileNotFoundError("Ei löydetty yhtään tiedostoa polusta: " + sk_path)

# Combine all files
sk_df = pd.concat(map(pd.read_csv, all_sk_paths), ignore_index=True)

# Write to csv-files
sk_df.to_csv('sodankylä_uv_all.csv', index=False)

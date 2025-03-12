import pandas as pd
import numpy as np
import glob
import os


def clean_data(df):
    df = df.drop_duplicates(subset=['date'], keep='last')
    df = df.replace('-', np.nan)
    df.snow_depth_cm = df.snow_depth_cm.replace(to_replace='-1', value='0')
    return df


def combine_data_by_location(location):

    folders = ['cloud_coverage_by_location',
               'snow_depth_avg_temp_by_location',
               'uv_index_by_location']
    
    dataframes = []

    # Loop through each folder and read matching CSV files
    for folder in folders:
        file_pattern = os.path.join(folder, f"{location}*.csv")  # Match files containing given location
        
        for file in glob.glob(file_pattern):
            df = pd.read_csv(file)
            df["date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
            
            df.drop(['Year','Month','Day'], inplace=True, axis=1)

            if 'Time [Local time]' in df.columns.to_list():
                df.drop(['Time [Local time]'], inplace=True, axis=1)

            if 'Observation station' in df.columns.to_list():
                df.drop(['Observation station'], inplace=True, axis=1)

            if 'Direct solar radiation mean [W/m2]' in df.columns.to_list():
                df.drop(['Direct solar radiation mean [W/m2]'], inplace=True, axis=1)

            dataframes.append(df)
    
    merged_df = dataframes[0]
    
    for df in dataframes[1:]:
        merged_df = pd.merge(merged_df, df, on="date", how="outer")  # Use outer join to keep all dates

    merged_df['cloud_cover_rate'] = merged_df['Cloud cover [1/8]'].str.split('(').str[1].str[0]
    merged_df['cloud_cover'] = merged_df['Cloud cover [1/8]'].str.split('(').str[0].str.strip()

    merged_df.drop(['Cloud cover [1/8]'], inplace=True, axis=1) 

    merged_df.rename(columns={'Snow depth [cm]': 'snow_depth_cm', 
                              'Average temperature [°C]': 'avg_temp_c', 
                              'UV index mean': 'uv_index'}, inplace=True) # Rename the columns
    merged_df = clean_data(merged_df)

    merged_df["location"] = location



    # Define the path where to write the files
    subfolder = "data_by_location"
    os.makedirs(subfolder, exist_ok=True)  # Create subfolder if it doesn't exist

    output_file = os.path.join(subfolder, f'{location}_data.csv')

    merged_df.to_csv(output_file, index=False)

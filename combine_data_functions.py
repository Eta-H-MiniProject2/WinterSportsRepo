import pandas as pd
import numpy as np
import glob
import os


def clean_data(df):
    df = df.drop_duplicates(subset=['date'], keep='last')
    df = df.replace('-', np.nan)
    df.snow_depth_cm = df.snow_depth_cm.replace(to_replace='-1', value='0')
    return df

# Combinig raw data from multiple files to one file per location.
# Function writes combined data to csv-files.
def combine_data_by_location(location):

    folders = ['cloud_coverage_by_location',
               'snow_depth_avg_temp_by_location',
               'uv_index_by_location']
    
    dataframes = []

    # Loop through each folder and read matching CSV files
    for folder in folders:
        file_pattern = os.path.join(folder, f"*{location}*.csv")  # Match files containing given location
        
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
    print(f'Raw data for {location} combined.')


# Function for preprocessing the data for the model.
# Function takes file path as a parameter
# and returns dataframe
def preprocess_with_time_features(file_path):
    df = pd.read_csv(file_path)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['date'], keep='last')
    
    # Replace values
    df.replace(to_replace='-', value=np.nan, inplace=True)
    df.snow_depth_cm = df.snow_depth_cm.replace(to_replace='-1', value='0')

    # Delete rows where snow_depth is null
    df = df.dropna(subset=['snow_depth_cm'])

    # Convert to numeric
    df['avg_temp_c'] = pd.to_numeric(df['avg_temp_c'], errors='coerce')
    df['snow_depth_cm'] = pd.to_numeric(df['snow_depth_cm'], errors='coerce')
    df['uv_index'] = pd.to_numeric(df['uv_index'], errors='coerce')
    
    # Create lag features
    df['snow_depth_1d_ago'] = df['snow_depth_cm'].shift(1)
    df['snow_depth_7d_ago'] = df['snow_depth_cm'].shift(7)
    df['snow_depth_365d_ago'] = df['snow_depth_cm'].shift(365)

    # Convert date string to datetime object
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract time-based features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_year'] = df['date'].dt.dayofyear
    
    # Drop rows with missing target values
    df = df.dropna(subset=['snow_depth_cm'])
    
    return df

import pandas as pd
import glob
import os

def combine_cloud_coverage():
    data_path = 'cloud_coverage_raw_data/'

    # Paths for data files
    pello_path = data_path + 'Pello*' 
    kuusamo_path = data_path + 'Kuusamo*' 
    sodankyla_path = data_path + 'Sodankyl*' 
    salla_path = data_path + 'Salla*' 
    kittila_path = data_path + 'Kittil*'
    savonlinna_path = data_path + 'Ruuna*' + '/' + 'Savonlinn*' 
    kuopio_path = data_path + 'Kasurila*' + '/' + 'Kuopio*' 
    lahti_path = data_path + 'Messil*' + '/*'
    ilomantsi_path = data_path + 'Mustavaara*' + '/*'
    purnu_path = data_path + 'Purnu*' + '/*'

    # Get all path for all the locations
    all_pello_paths = glob.glob(pello_path)
    all_kuusamo_paths = glob.glob(kuusamo_path)
    all_sodankyla_paths = glob.glob(sodankyla_path)
    all_salla_paths = glob.glob(salla_path)
    all_kittila_paths = glob.glob(kittila_path)
    all_savonlinna_paths = glob.glob(savonlinna_path)
    all_kuopio_paths = glob.glob(kuopio_path)
    all_lahti_paths = glob.glob(lahti_path)
    all_ilomantsi_paths = glob.glob(ilomantsi_path)
    all_purnu_paths = glob.glob(purnu_path)

    # Combine all files
    pello_df = pd.concat(map(pd.read_csv, all_pello_paths), ignore_index=True)
    kuusamo_df = pd.concat(map(pd.read_csv, all_kuusamo_paths), ignore_index=True)
    sodankyla_df = pd.concat(map(pd.read_csv, all_sodankyla_paths), ignore_index=True)
    salla_df = pd.concat(map(pd.read_csv, all_salla_paths), ignore_index=True)
    kittila_df = pd.concat(map(pd.read_csv, all_kittila_paths), ignore_index=True)
    savonlinna_df = pd.concat(map(pd.read_csv, all_savonlinna_paths), ignore_index=True)
    kuopio_df = pd.concat(map(pd.read_csv, all_kuopio_paths), ignore_index=True)
    lahti_df = pd.concat(map(pd.read_csv, all_lahti_paths), ignore_index=True)
    ilomantsi_df = pd.concat(map(pd.read_csv, all_ilomantsi_paths), ignore_index=True)
    purnu_df = pd.concat(map(pd.read_csv, all_purnu_paths), ignore_index=True)

    # Define the path where to write the files
    subfolder = "cloud_coverage_by_location"
    os.makedirs(subfolder, exist_ok=True)  # Create subfolder if it doesn't exist

    # Define the paths to new csv-files
    pello_output_file = os.path.join(subfolder, 'Ounasvaara_cloud_coverage.csv')
    kuusamo_output_file = os.path.join(subfolder, 'Ruka_cloud_coverage.csv')
    sodankyla_output_file = os.path.join(subfolder, 'Luosto_cloud_coverage.csv')
    salla_output_file = os.path.join(subfolder, 'Salla_cloud_coverage.csv')
    kittila_output_file = os.path.join(subfolder, 'Levi_cloud_coverage.csv')
    savonlinna_output_file = os.path.join(subfolder, 'Ruunarinteet_cloud_coverage.csv')
    kuopio_output_file = os.path.join(subfolder, 'Kasurila_cloud_coverage.csv')
    lahti_output_file = os.path.join(subfolder, 'Messila_cloud_coverage.csv')
    ilomantsi_output_file = os.path.join(subfolder, 'Mustavaara_cloud_coverage.csv')
    purnu_output_file = os.path.join(subfolder, 'Purnu_cloud_coverage.csv')

    # Write to csv-files
    pello_df.to_csv(pello_output_file, index=False)
    kuusamo_df.to_csv(kuusamo_output_file, index=False)
    sodankyla_df.to_csv(sodankyla_output_file, index=False)
    salla_df.to_csv(salla_output_file, index=False)
    kittila_df.to_csv(kittila_output_file, index=False)
    savonlinna_df.to_csv(savonlinna_output_file, index=False)
    kuopio_df.to_csv(kuopio_output_file, index=False)
    lahti_df.to_csv(lahti_output_file, index=False)
    ilomantsi_df.to_csv(ilomantsi_output_file, index=False)
    purnu_df.to_csv(purnu_output_file, index=False)

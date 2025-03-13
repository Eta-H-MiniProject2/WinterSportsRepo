import combine_data
from ipynb.fs.full.xgboost_model import create_prediction_files

#data_combining_functions.combine_cloud_coverage()
#data_combining_functions.combine_snow_depth_and_temperature_files()

locations = ['Kasurila','Levi','Luosto','Messila','Mustavaara','Ounasvaara','Purnu','Ruka','Ruunarinteet','Salla']

for location in locations:
    combine_data.combine_data_by_location(location)

create_prediction_files(locations)


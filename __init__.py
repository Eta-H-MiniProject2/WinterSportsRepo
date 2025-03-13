from combine_data_functions import combine_data_by_location
from xgboost_model_create import train_xgboost_model
from xgboost_model_create import evaluate_model
from xgboost_model_create import get_model
from create_predictions import create_prediction_files
from create_predictions import preprocess_with_time_features

#data_combining_functions.combine_cloud_coverage()
#data_combining_functions.combine_snow_depth_and_temperature_files()

locations = ['Kasurila','Levi','Luosto','Messila','Mustavaara','Ounasvaara','Purnu','Ruka','Ruunarinteet','Salla']
train_locations = ['Messila','Purnu','Ruunarinteet','Kasurila']
test_location = 'Ruka'

# Combine raw data and write it to one csv per file
for location in locations:
    combine_data_by_location(location)

# Train the model and save it to joblib-file
# Test the model with 20 % of train data
train_xgboost_model(train_locations) 

# Testing model with another location (not included in training data)
print(f'\nTesting created model with {test_location}')

test_df = preprocess_with_time_features(f'data_by_location/{test_location.lower()}_data.csv')

X = test_df[['avg_temp_c', 
                 'cloud_cover_rate',
                 'uv_index', 
                 'snow_depth_1d_ago', 
                 'snow_depth_7d_ago', 
                 'snow_depth_365d_ago', 
                 'year', 
                 'month', 
                 'day', 
                 'day_of_year']]  # Features 
y = test_df['snow_depth_cm']  # Target variable (snow depth)

evaluate_model(get_model(), X, y)

# Create prediction files for all locations
# and save the predictions to csv-file.
create_prediction_files(locations)

import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import xgboost as xgb
import matplotlib.pyplot as plt
from combine_data_functions import preprocess_with_time_features


# Function to predict future years from given model
def predict_future_snow_depth(model, start_date, days=365, location_data=None):
    """
    Predict snow depth for future dates
    
    Parameters:
    - model: Trained model
    - start_date: Start date for predictions (string YYYY-MM-DD or datetime)
    - days: Number of days to predict forward
    - location_data: Sample data from a location to use as base values
    
    Returns:
    - DataFrame with dates and predicted snow depths
    """
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    
    # Create date range
    future_dates = [start_date + timedelta(days=i) for i in range(days)]
    future_df = pd.DataFrame({'date': future_dates})

    if location_data is not None:
        past_snow_data = location_data[['date', 'snow_depth_cm']].copy()
    
        past_snow_data['snow_depth_1d_ago'] = past_snow_data['snow_depth_cm'].shift(1)
        past_snow_data['snow_depth_7d_ago'] = past_snow_data['snow_depth_cm'].shift(7)
        past_snow_data['snow_depth_365d_ago'] = past_snow_data['snow_depth_cm'].shift(365)
    
        future_df = future_df.merge(past_snow_data[['date', 'snow_depth_1d_ago', 'snow_depth_7d_ago', 'snow_depth_365d_ago']], 
                                on='date', how='left')
    
    # Extract time features
    future_df['year'] = future_df['date'].dt.year
    future_df['month'] = future_df['date'].dt.month
    future_df['day'] = future_df['date'].dt.day
    future_df['day_of_year'] = future_df['date'].dt.dayofyear
    
    # Generate weather features based on historical averages by day of year
    if location_data is not None:
        # Group location data by day of year and get averages
        daily_averages = location_data.groupby('day_of_year').agg({
            'avg_temp_c': 'mean',
            'uv_index': 'mean',
            'cloud_cover_rate': 'mean'
        }).reset_index()
        
        # Merge with future dates
        future_df = future_df.merge(daily_averages, on='day_of_year', how='left')

        # For days not in historical data, use nearest day
        future_df = future_df.ffill().bfill()
    else:
        # If no location data is provided, use seasonal patterns
        # This is simplified - would be better with actual historical weather data
        future_df['month_rad'] = future_df['month'] * 2 * np.pi / 12
        
        # Temperature follows seasonal cycle (simplified model)
        # Northern hemisphere: coldest in Jan/Feb, warmest in Jul/Aug
        future_df['avg_temp_c'] = -10 * np.cos(future_df['month_rad']) + 5
        
        # UV follows similar seasonal pattern
        future_df['uv_index'] = 3 * np.cos((future_df['month_rad'] + np.pi)) + 3
        
        # Cloud cover (simplified)
        future_df['cloud_cover_rate'] = 0.5 + 0.2 * np.sin(future_df['month_rad'])
    
    # Prepare features for prediction in the same format as training data
    X_future = future_df[['avg_temp_c', 
                          'cloud_cover_rate',
                          'uv_index', 
                          'snow_depth_1d_ago', 
                          'snow_depth_7d_ago', 
                          'snow_depth_365d_ago', 
                          'year', 
                          'month', 
                          'day', 
                          'day_of_year']]
    
    # Make predictions
    future_df['predicted_snow_depth'] = model.predict(X_future)
    
    # Ensure non-negative snow depths
    future_df['predicted_snow_depth'] = future_df['predicted_snow_depth'].clip(lower=0)
    
    return future_df[['date', 
                      'predicted_snow_depth', 
                      'avg_temp_c', 
                      'uv_index', 
                      'cloud_cover_rate']]


# Create prediction files for locations
def create_prediction_files(locations):
    # Load the trained model
    trained_model = joblib.load('snow_depth_time_model.joblib')

    for location in locations:
        location_df = preprocess_with_time_features(f'data_by_location/{location.lower()}_data.csv')

        start_prediction_date = '2005-01-01'
        future_predictions = predict_future_snow_depth(
            model=trained_model,
            start_date=start_prediction_date,
            days=365*40,
            location_data=location_df
        )
        future_predictions['location'] = location

        future_predictions.to_csv(f'snow_depth_predictions_{location.lower()}_2025.csv', index=False)
        print(f'Future predictions for {location} saved csv-file')

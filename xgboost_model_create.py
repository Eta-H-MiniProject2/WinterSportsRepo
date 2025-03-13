import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import xgboost as xgb
import matplotlib.pyplot as plt
from combine_data_functions import preprocess_with_time_features

# If there is model created in the file, returns it
def get_model():
    try:
        trained_model = joblib.load('snow_depth_time_model.joblib')
    except:
        return
    return trained_model

# Function trains new xgboost model with given locations
def train_xgboost_model(locations):
    datasets = []

    for location in locations:
        datasets.append(f'data_by_location/{location.lower()}_data.csv')

    all_data = []

    for dataset in datasets:
        try:
            df = preprocess_with_time_features(dataset)
            all_data.append(df)
        except Exception as e:
            print(f"Error processing {dataset}: {e}")

    combined_df = pd.concat(all_data)


    # Remove duplicates (if same location and date)
    combined_df = combined_df.drop_duplicates(subset=['date', 'location'], keep='last')

    # Create an XGBoost regressor model
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

    X = combined_df[['avg_temp_c', 
                     'cloud_cover_rate',
                     'uv_index', 
                     'snow_depth_1d_ago', 
                     'snow_depth_7d_ago', 
                     'snow_depth_365d_ago', 
                     'year', 
                     'month', 
                     'day', 
                     'day_of_year']]  # Features 

    y = combined_df['snow_depth_cm']  # Target variable (snow depth)

    # Split into training (80%) and test (20%) data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model on the training data
    model.fit(X_train, y_train)

    print('\nInit testing for the model: ')
    evaluate_model(model, X_test, y_test)

    # Save the model
    joblib.dump(model, 'snow_depth_time_model.joblib')

    # Plot feature importance
    xgb.plot_importance(model)
    plt.show()

    print('Model created and saved.')


def evaluate_model(model, X_test, y_test):
    # Calculate predictions for testing the model
    predictions = model.predict(X_test)

    # Calculate Mean Absolute Error (MAE)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Mean Absolute Error: {mae}")

    # Calculate Mean Squared Error (MSE)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")

    # Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)
    print(f"Root Mean Squared Error: {rmse}\n")

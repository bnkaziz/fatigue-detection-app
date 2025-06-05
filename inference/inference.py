import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import time
import os
from front.components.session_manager import SessionManager

# Configuration
MODEL_PATH = 'inference/resources/lstm_model.h5'  # Path to the saved LSTM model
CSV_PATH = 'data/features/features_recording.csv'  # Path to the CSV file from BioRadio
OUTPUT_TXT = 'inference/results/inference_results.txt'  # Path to save inference results
TIMESTEPS = 5  # Number of timesteps for LSTM input (same as during training)

# Initialize SessionManager to access temperament
session_manager = SessionManager()  # Initialized by the frontend

# Load the LSTM model
lstm_model = load_model(MODEL_PATH)
print("Model loaded successfully.")

# Function to reshape data for LSTM: (samples, timesteps, features)
def reshape_for_lstm(X, timesteps):
    num_samples = len(X) - timesteps + 1
    if num_samples < 1:
        return None  # Not enough data yet
    X_reshaped = np.zeros((num_samples, timesteps, X.shape[1]))
    for i in range(num_samples):
        X_reshaped[i] = X[i:i + timesteps]
    return X_reshaped

# Feature columns expected by the model (excluding Timestamp)
feature_columns = [
    'Fp2_delta', 'Fp2_theta', 'Fp2_alpha', 'Fp2_beta', 'Fp2_gamma',
    'Fp1_delta', 'Fp1_theta', 'Fp1_alpha', 'Fp1_beta', 'Fp1_gamma',
    'O1_delta', 'O1_theta', 'O1_alpha', 'O1_beta', 'O1_gamma',
    'O2_delta', 'O2_theta', 'O2_alpha', 'O2_beta', 'O2_gamma',
    'HR', 'SDNN', 'CV', 'RMSSD', 'pNN50'
]

# Initialize variables
last_processed_index = -1  # Track the last processed row
buffer_data = []  # Buffer to store rows for LSTM reshaping

# Main loop to monitor the CSV file and perform inference
while True:
    try:
        # Read the CSV file
        if not os.path.exists(CSV_PATH):
            print(f"CSV file {CSV_PATH} not found. Waiting...")
            time.sleep(5)
            continue

        df = pd.read_csv(CSV_PATH)

        # Check if new rows are added
        new_rows = df.iloc[last_processed_index + 1:]
        if len(new_rows) == 0:
            time.sleep(1)  # Wait before checking again
            continue

        # Get temperament from SessionManager
        temperament = session_manager.user_info.get('temperament')

        # Process each new row
        for index, row in new_rows.iterrows():
            # Update temperament in the row (replace the placeholder)
            row_data = row.copy()
            row_data['Temperament'] = temperament

            # Extract features (excluding Timestamp)
            features = row_data[feature_columns].values
            features = np.append(features, temperament)  # Append temperament as a feature

            # Add to buffer
            buffer_data.append(features)

            # Reshape for LSTM if enough data is available
            if len(buffer_data) >= TIMESTEPS:
                # Convert buffer to numpy array
                X_input = np.array(buffer_data)
                X_reshaped = reshape_for_lstm(X_input, TIMESTEPS)

                if X_reshaped is not None:
                    # Perform inference
                    predictions = lstm_model.predict(X_reshaped, verbose=0)
                    predicted_class = np.argmax(predictions[-1], axis=0)  # Take the last prediction

                    # Save the predicted class to the text file
                    with open(OUTPUT_TXT, 'a') as f:
                        f.write(f"{predicted_class}\n")

            # Update the last processed index
            last_processed_index = index

        # Keep buffer at a manageable size (remove oldest data if needed)
        if len(buffer_data) > TIMESTEPS * 2:
            buffer_data = buffer_data[-TIMESTEPS * 2:]

    except KeyboardInterrupt:
        print("Inference stopped.")
        break
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(5)  # Wait before retrying

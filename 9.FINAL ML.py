import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional

# Load data
file_path = r"D:\GNSS PROJECT\2020 BLR NASA WORK\2020 final 18 dec 2024\MASTER PWV.xlsx"
df = pd.read_excel(file_path, usecols=["GPS_Time", "PWV(final)"])

# Convert GPS_Time to datetime
df["GPS_Time"] = pd.to_datetime(df["GPS_Time"])
df.set_index("GPS_Time", inplace=True)

# Normalize data
scaler = MinMaxScaler()
df["PWV(final)"] = scaler.fit_transform(df[["PWV(final)"]])

# Prepare data for training
X, y = [], []
look_back = 24  # Use past 24 hours for prediction
for i in range(len(df) - look_back - 3):  # Predict next 3 days (72 hours)
    X.append(df["PWV(final)"].iloc[i:i+look_back].values)
    y.append(df["PWV(final)"].iloc[i+look_back:i+look_back+3].values)

X, y = np.array(X), np.array(y)

# Reshape input for LSTM: (samples, timesteps, features)
X = X.reshape((X.shape[0], X.shape[1], 1))

# Split data: 60% train, 20% validation, 20% test
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, shuffle=False)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, shuffle=False)

# Define Half-LSTM model
def create_half_lstm():
    model = Sequential([
        Bidirectional(LSTM(50, return_sequences=False, input_shape=(look_back, 1))),  # Half of the model is LSTM
        Dense(50, activation='relu'),  # Half of the model is feedforward
        Dropout(0.2),
        Dense(3)  # Predicting next 3 values
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Train model
model = create_half_lstm()
history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_val, y_val), verbose=1)

# Predict
y_pred = model.predict(X_test)

# Inverse transform predictions
y_test_rescaled = scaler.inverse_transform(y_test)
y_pred_rescaled = scaler.inverse_transform(y_pred)

# Plot results
def plot_results(y_test_rescaled, y_pred_rescaled):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index[-len(y_test):], y_test_rescaled[:, 0], label="Actual PWV", color="blue")
    plt.plot(df.index[-len(y_pred):], y_pred_rescaled[:, 0], label="Predicted PWV", linestyle="dashed", color="red")
    plt.xlabel("Date")
    plt.ylabel("PWV")
    plt.legend()
    plt.title("PWV Prediction vs Actual")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

plot_results(y_test_rescaled, y_pred_rescaled)


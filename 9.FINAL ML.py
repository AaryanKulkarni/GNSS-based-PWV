# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.neural_network import MLPRegressor
# import tkinter as tk
# from tkinter import ttk
#
# # Load data
# file_path = r"D:\GNSS PROJECT\2020 BLR NASA WORK\2020 final 18 dec 2024\MASTER PWV.xlsx"
# df = pd.read_excel(file_path, usecols=["GPS_Time", "PWV(final)"])
#
# # Convert GPS_Time to datetime
# df["GPS_Time"] = pd.to_datetime(df["GPS_Time"])
# df.set_index("GPS_Time", inplace=True)
#
# # Normalize data
# scaler = MinMaxScaler()
# df["PWV(final)"] = scaler.fit_transform(df[["PWV(final)"]])
#
# # Prepare data for training
# X, y = [], []
# look_back = 24  # Use past 24 hours for prediction
# for i in range(len(df) - look_back - 3):  # Predict next 3 days (72 hours)
#     X.append(df["PWV(final)"].iloc[i:i+look_back].values)
#     y.append(df["PWV(final)"].iloc[i+look_back:i+look_back+3].values)
#
# X, y = np.array(X), np.array(y)
#
# # Split data: 60% train, 20% validation, 20% test
# X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, shuffle=False)
# X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, shuffle=False)
#
# # Define model
# def create_model(hidden_layer_size, learning_rate):
#     return MLPRegressor(hidden_layer_sizes=(hidden_layer_size,), max_iter=500, learning_rate_init=learning_rate, random_state=42)
#
# # Train model
# mlp = create_model(50, 0.01)
# mlp.fit(X_train, y_train)
#
# # Predict
# y_pred = mlp.predict(X_test)
#
# # Inverse transform predictions
# y_test_rescaled = scaler.inverse_transform(y_test)
# y_pred_rescaled = scaler.inverse_transform(y_pred)
#
# # Plot results
# def plot_results(y_test_rescaled, y_pred_rescaled):
#     plt.figure(figsize=(10, 5))
#     plt.plot(df.index[-len(y_test):], y_test_rescaled[:, 0], label="Actual PWV", color="blue")
#     plt.plot(df.index[-len(y_pred):], y_pred_rescaled[:, 0], label="Predicted PWV", linestyle="dashed", color="red")
#     plt.xlabel("Date")
#     plt.ylabel("PWV")
#     plt.legend()
#     plt.title("PWV Prediction vs Actual")
#     plt.xticks(rotation=45)
#     plt.grid()
#     plt.show()
#
# plot_results(y_test_rescaled, y_pred_rescaled)
#
# # GUI for parameter tuning
# def update_model():
#     hidden_layer = int(hidden_layer_slider.get())
#     learning_rate = float(learning_rate_slider.get())
#     max_iter = int(max_iter_slider.get())
#
#     mlp = create_model(hidden_layer, learning_rate)
#     mlp.max_iter = max_iter
#     mlp.fit(X_train, y_train)
#     new_pred = mlp.predict(X_test)
#     new_pred_rescaled = scaler.inverse_transform(new_pred)
#
#     plot_results(y_test_rescaled, new_pred_rescaled)
#
# # Create GUI
# root = tk.Tk()
# root.title("PWV Model Tuning")
#
# ttk.Label(root, text="Hidden Layer Size").grid(row=0, column=0)
# hidden_layer_slider = tk.Scale(root, from_=10, to=200, orient="horizontal")
# hidden_layer_slider.set(50)
# hidden_layer_slider.grid(row=0, column=1)
#
# ttk.Label(root, text="Learning Rate").grid(row=1, column=0)
# learning_rate_slider = tk.Scale(root, from_=0.001, to=0.1, resolution=0.001, orient="horizontal")
# learning_rate_slider.set(0.01)
# learning_rate_slider.grid(row=1, column=1)
#
# ttk.Label(root, text="Max Iterations").grid(row=2, column=0)
# max_iter_slider = tk.Scale(root, from_=100, to=1000, orient="horizontal")
# max_iter_slider.set(500)
# max_iter_slider.grid(row=2, column=1)
#
# ttk.Button(root, text="Update Model", command=update_model).grid(row=3, columnspan=2)
#
# root.mainloop()
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

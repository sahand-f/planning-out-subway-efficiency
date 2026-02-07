# -*- coding: utf-8 -*-
"""
Sahand  Farahmand - sahandfarahmand3@gmail.com

Simulation of Passenger Wait Times and Service Frequency
Toronto Subway System

This script generates synthetic passenger arrival data,
simulates subway waiting and travel times under varying
train service frequencies, and visualizes key trade-offs
between passenger experience and operational demand.
"""

# -----------------------------
# Import required libraries
# -----------------------------
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# -----------------------------
# Load real station-to-station travel time data
# -----------------------------
# Attempt to load the subway travel time dataset.
# If the file is not found, exit the program.
try:
    Torontodata = pd.read_csv('Subway Travel Time.csv')
except:
    print("File not found")
    sys.exit()

# Store station names separately
Name = Torontodata["Unnamed: 0"]

# Remove the unnamed column from the dataset
Torontodata = Torontodata.drop(columns={"Unnamed: 0"})

# Replace missing values represented by '-' with NaN
Torontodata = Torontodata.replace("-", "nan")

# Convert all travel time values to floats
Torontodata = Torontodata.astype(float)

# Reattach station names as a separate column
Torontodata["Name"] = Name

# -----------------------------
# Initialize simulation parameters
# -----------------------------
train_freq = 10        # Baseline train frequency (minutes)
deviation = 150        # Standard deviation of passenger arrival times
average = 150          # Mean passenger arrival time
n_stations = len(Torontodata)  # Number of subway stations
time_total = 400       # Total operating time (minutes)
n_people = 5000        # Number of simulated passengers
miss_cost = 100        # Penalty waiting time for missed service

# Set random seed for reproducibility
random.seed(42)

# -----------------------------
# Maintenance / service cost function
# -----------------------------
def maintanence(interval):
    """
    Models maintenance and service demand as an exponential
    decay function of the train arrival interval.
    """
    return np.exp(-0.2 * interval) * 20

# -----------------------------
# Initialize synthetic passenger dataset
# -----------------------------
data = {
    'station entered': [],
    'station exited': [],
    'time entered': []
}

# -----------------------------
# Generate synthetic passenger data
# -----------------------------
for _ in range(n_people):
    # Randomly choose an entry station
    en = random.choice(list(range(0, n_stations - 1)))
    data['station entered'].append(en)

    # Ensure exit station is after entry station
    data['station exited'].append(random.randint(en + 1, n_stations - 1))

    # Generate passenger arrival time from Gaussian distribution
    x = random.gauss(average, deviation)

    # Ensure arrival time falls within operating window
    while x < 0 or x > time_total:
        x = random.gauss(average, deviation)

    data['time entered'].append(x)

# Convert to DataFrame
data = pd.DataFrame(data)

# Save synthetic data to CSV
data.to_csv('Travel Times-Destination and arrival.csv')

# -----------------------------
# Plot passenger arrival time distribution
# -----------------------------
plt.figure(figsize=(10, 6))
plt.hist(data['time entered'] / 60 + 6, bins=40, alpha=0.7)
plt.title('Histogram of Gaussian Distribution')
plt.xlabel('Time in Hours')
plt.ylabel('Travel Frequency')
plt.show()

# -----------------------------
# Identify most crowded stations
# -----------------------------
# Find most common entry and exit stations
crowded_entrance = data["station entered"].mode().iloc[0]
crowded_exit = data["station exited"].mode().iloc[0]

# Find nearest stations based on minimum travel time
smallest_value_columns = (
    Torontodata
    .select_dtypes(include='number')
    .idxmin(axis=1)
)

nearest_to_crowded_entrance = smallest_value_columns.iloc[crowded_entrance]
nearest_to_crowded_exit = smallest_value_columns.iloc[crowded_exit]

# -----------------------------
# Travel time lookup function
# -----------------------------
def distance(entered_station, exited_station):
    """
    Returns the travel time between two stations
    using the real travel time dataset.
    """
    name = Torontodata["Name"][entered_station]
    time = int(Torontodata[name][exited_station])
    return time

# -----------------------------
# Subway simulation function
# -----------------------------
def metro(interval):
    """
    Simulates passenger waiting and travel times
    for a given train arrival interval.
    """
    metro_travel_time = []
    wait_list = []

    for i in range(len(data)):
        # Time since last train arrival
        temp = data['time entered'][i] % interval

        # If a train arrives within the operating window
        if data['time entered'][i] < (time_total - interval):
            wait = interval - temp
        else:
            # Apply penalty if passenger misses final train
            wait = miss_cost

        metro_travel_time.append(
            distance(data['station entered'][i], data['station exited'][i])
        )
        wait_list.append(wait)

    return {"wait": wait_list, "travel": metro_travel_time}

# -----------------------------
# Evaluate average wait time over different intervals
# -----------------------------
interval = np.arange(1, 20)  # Train arrival intervals (minutes)
time = []

# Compute average wait time for each interval
for x in interval:
    time.append(sum(metro(x)["wait"]) / len(data))

# Compute maintenance cost curve
y_gray = maintanence(interval)

# -----------------------------
# Plot wait time vs maintenance cost
# -----------------------------
plt.figure(figsize=(10, 6))
plt.plot(interval, time, linewidth=2, label='Customer wait time')
plt.plot(interval, y_gray, linewidth=2, label='Maintenance and service time')
plt.xlabel("Interval Between Arrivals (minutes)")
plt.ylabel("Time (minutes)")
plt.title("Average Wait Time and Maintenance Cost vs Interval")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# -----------------------------
# Compare individual travel vs wait times
# -----------------------------
x = np.arange(len(data))
y1 = metro(train_freq)["travel"]
y2 = metro(train_freq)["wait"]
w = 0.35

plt.figure(figsize=(10, 6))
plt.bar(x - w/2, y1, w, label="Travel time")
plt.bar(x + w/2, y2, w, label="Wait time")
plt.xticks(np.arange(0, len(data), 500))
plt.xlabel("Passenger")
plt.ylabel("Time (minutes)")
plt.legend()
plt.title("Comparison of Travel Time and Wait Time")
plt.show()

# -----------------------------
# Print crowded station results
# -----------------------------
print("The nearest crowded entrance is:", nearest_to_crowded_entrance)
print("The nearest crowded exit is:", nearest_to_crowded_exit)

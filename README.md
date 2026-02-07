# WIP 
# Subway Service Frequency and Passenger Wait Time Simulation

This repository contains a Python-based simulation model that examines the relationship between train service frequency, passenger waiting times, and operational demand in the Toronto subway system. The project uses synthetic passenger arrival data and real station-to-station travel time data to explore trade-offs relevant to transit planning and service optimization.

The code was developed in support of an undergraduate conference paper and is intended as an exploratory, simulation-based analysis rather than a fully calibrated operational model.

---

## Project Overview

Urban subway systems must balance passenger experience with operational constraints. Increasing train frequency can reduce passenger waiting times but leads to higher maintenance and service demands. This project investigates this trade-off by:

- Simulating passenger arrivals using a Gaussian distribution  
- Estimating passenger waiting times under varying train arrival intervals  
- Modeling maintenance and service demand as a function of service frequency  
- Visualizing the relationship between service frequency, waiting time, and operational effort  

---

## Data

The project uses two types of data:

### 1. Real Travel Time Data
- **`Subway Travel Time.csv`**
- Contains station-to-station travel times used to calculate in-vehicle travel durations
- Preprocessed within the script to handle missing values and formatting

### 2. Synthetic Passenger Data
- Generated within the script using a Gaussian distribution
- Includes:
  - Entry station
  - Exit station
  - Arrival time
- Saved as **`Travel Times-Destination and arrival.csv`** for reference

---

## Methodology Summary

- Passenger arrivals are modeled using a normal distribution with fixed mean and standard deviation
- Train arrivals are assumed to occur at regular intervals
- Passenger waiting time is calculated based on arrival time modulo train interval
- A penalty waiting time is assigned to passengers who miss the final train
- Maintenance and service demand is represented using an exponential decay function
- A fixed random seed is used to ensure reproducibility

---

## Key Parameters

| Parameter        | Description                                   | Value |
|------------------|-----------------------------------------------|-------|
| `train_freq`     | Baseline train frequency (minutes)            | 10    |
| `average`        | Mean passenger arrival time (minutes)         | 150   |
| `deviation`      | Std. deviation of arrival times (minutes)     | 150   |
| `time_total`     | Total operating time (minutes)                | 400   |
| `n_people`       | Number of simulated passengers                | 5000  |
| `miss_cost`      | Penalty waiting time for missed service       | 100   |
| `random.seed()`  | Random seed for reproducibility               | 42    |

---

## Outputs and Visualizations

The script generates several plots:

- Histogram of simulated passenger arrival times  
- Average passenger waiting time vs. train arrival interval  
- Maintenance/service demand vs. train arrival interval  
- Comparison of individual passenger travel times and waiting times  

These figures correspond directly to those presented in the accompanying paper.

---

## Requirements

- Python 3.x
- NumPy
- Pandas
- Matplotlib

You can install the required packages using:

```bash
pip install numpy pandas matplotlib

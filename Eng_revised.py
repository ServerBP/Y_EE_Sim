import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Constants
AU = 1.496e+11  # Astronomical unit in meters
year_in_seconds = 365.25 * 24 * 3600  # One year in seconds
seconds_in_day = 24 * 3600  # One day in seconds

# Parameters for Earth's orbit
a = AU  # Semi-major axis (average distance to the Sun)
e = 0.0167  # Earth's actual eccentricity

# Time array in seconds and days
t_seconds = np.linspace(0, year_in_seconds, 1000)
t_days = t_seconds / seconds_in_day

# Mean anomaly (M)
M = 2 * np.pi * t_seconds / year_in_seconds

# Eccentric anomaly (E) using Newton's method
E = M
for _ in range(10):  # Iterate to solve for E
    E = M + e * np.sin(E)

# True anomaly (ν)
nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))

# Distance from the Sun at each point in the orbit
r = a * (1 - e**2) / (1 + e * np.cos(nu))
distance_km = r / 1e3  # Convert to kilometers

# Convert positions to astronomical units for plotting
x_au = r * np.cos(nu) / AU
y_au = r * np.sin(nu) / AU

# Plot 2D orbit in astronomical units
plt.figure(figsize=(8, 8))
plt.plot(x_au, y_au, label="Earth's Orbit")
plt.plot(0, 0, 'yo', label="Sun")  # Sun at the origin
plt.xlabel('X position (AU)')
plt.ylabel('Y position (AU)')
plt.title('2D Orbit of Earth around the Sun (Realistic)')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()

# Plot distance over time in days
plt.figure(figsize=(10, 6))
plt.plot(t_days, distance_km / 1e6, label="Distance (Actual)")  # in Gm
plt.xlabel('Time (days)')
plt.ylabel('Distance (Gm)')
plt.title('Distance between Earth and Sun over Time')
plt.grid(True)
plt.show()

# Sinusoidal regression function
def sinusoidal(t, A, B, C, D):
    return A * np.sin(B * t + C) + D

# Fit the sinusoidal model to the distance data using time in days
initial_guess = [1e8, 2 * np.pi / 365.25, 0, AU / 1e3]  # Initial guess for A, B, C, D in km
params, params_covariance = curve_fit(sinusoidal, t_days, distance_km, p0=initial_guess)

# Generate fitted distance data
fitted_distance_km = sinusoidal(t_days, *params)

# Plot the original and fitted data for comparison
plt.figure(figsize=(10, 6))
plt.plot(t_days, distance_km / 1e6, label="Distance (Actual)")  # in Gm
plt.plot(t_days, fitted_distance_km / 1e6, label="Distance (Fitted)", linestyle='--')  # in Gm
plt.xlabel('Time (days)')
plt.ylabel('Distance (Gm)')
plt.title('Distance between Earth and Sun with Sinusoidal Fit')
plt.legend()
plt.grid(True)
plt.show()

# Print the fitted parameters
A, B, C, D = params
print(f"Fitted parameters: A = {A} km, B = {B} rad/day, C = {C} rad, D = {D} km")
print(f"Sinusoidal equation: distance(t) = {A:.2e} * sin({B:.2e} * t + {C:.2e}) + {D:.2e} km")

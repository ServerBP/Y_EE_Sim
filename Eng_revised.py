import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Constants
AU = 1.496e+11  # Astronomical unit in meters
year_in_seconds = 365.25 * 24 * 3600  # One year in seconds

# Parameters for Earth's orbit
a = AU  # Semi-major axis (average distance to the Sun)
e = 0.5  # Increased eccentricity for a more elliptical orbit
b = a * np.sqrt(1 - e**2)  # Semi-minor axis

# Time array
t = np.linspace(0, year_in_seconds, 1000)

# Orbit calculations (parametric equations for ellipse)
theta = 2 * np.pi * t / year_in_seconds
x = a * np.cos(theta)
y = b * np.sin(theta)

# Convert positions to astronomical units
x_au = x / AU
y_au = y / AU

# Calculate distance from Earth to Sun
distance = np.sqrt(x**2 + y**2)  # in meters
distance_km = distance / 1e3  # convert to kilometers

# Plot 2D orbit in astronomical units
plt.figure(figsize=(8, 8))
plt.plot(x_au, y_au, label="Earth's Orbit")
plt.plot(0, 0, 'yo', label="Sun")  # Sun at the origin
plt.xlabel('X position (AU)')
plt.ylabel('Y position (AU)')
plt.title('2D Orbit of Earth around the Sun (More Elliptical)')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()

# Plot distance over time
plt.figure(figsize=(10, 6))
plt.plot(t / (24 * 3600), distance / 1e9, label="Distance (Actual)")  # in Gm
plt.xlabel('Time (days)')
plt.ylabel('Distance (Gm)')
plt.title('Distance between Earth and Sun over Time')
plt.grid(True)
plt.show()

# Sinusoidal regression function
def sinusoidal(t, A, B, C, D):
    return A * np.sin(B * t + C) + D

# Fit the sinusoidal model to the distance data
initial_guess = [1e8, 2 * np.pi / year_in_seconds, 0, AU / 1e3]  # Initial guess for A, B, C, D in km
params, params_covariance = curve_fit(sinusoidal, t, distance_km, p0=initial_guess)

# Generate fitted distance data
fitted_distance_km = sinusoidal(t, *params)

# Plot the original and fitted data for comparison
plt.figure(figsize=(10, 6))
plt.plot(t / (24 * 3600), distance / 1e9, label="Distance (Actual)")  # in Gm
plt.plot(t / (24 * 3600), fitted_distance_km / 1e6, label="Distance (Fitted)", linestyle='--')  # in Gm
plt.xlabel('Time (days)')
plt.ylabel('Distance (Gm)')
plt.title('Distance between Earth and Sun with Sinusoidal Fit')
plt.legend()
plt.grid(True)
plt.show()

# Print the fitted parameters
A, B, C, D = params
print(f"Fitted parameters: A = {A} km, B = {B} rad/s, C = {C} rad, D = {D} km")
print(f"Sinusoidal equation: distance(t) = {A:.2e} * sin({B:.2e} * t + {C:.2e}) + {D:.2e} km")

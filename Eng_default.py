import numpy as np
import matplotlib.pyplot as plt

# Parameter settings, default variables
a = 1.496e8  # km, semi-major axis
e = 0.0167  # eccentricity value

# Half-shortened calculation
def calculate_b(a, e):
    return a * np.sqrt(1 - e**2)

b = calculate_b(a, e)

# generate an array of angles(between 0 and 2pi)
theta = np.linspace(0, 2 * np.pi, 1000)

# Ellipse coordinate calculation
x = a * np.cos(theta)
y = b * np.sin(theta)

# Define the position of the sun
focus_x = a * e
focus_y = 0

# Calculate the distance from each point to the sun
r = np.sqrt((x - focus_x)**2 + (y - focus_y)**2)

# Draw the graphs using matplotlib
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Orbit of earth')
plt.plot(focus_x, focus_y, 'ro', label='Sun')
for i in range(0, 1000, 100):
    plt.plot([focus_x, x[i]], [focus_y, y[i]], 'g--', lw=0.5)  # Iterate through 1000 angles(equal ∆) and calculate the distance

plt.xlabel('x (km)')
plt.ylabel('y (km)')
plt.legend()
plt.title("Earth's elliptical orbit and the distance of each point form the sun")
plt.grid(True)
plt.axis('equal')
plt.show()

# Graph the changes in distance over time
plt.figure(figsize=(10, 6))
plt.plot(theta, r)
plt.xlabel('Angle (rad)')
plt.ylabel('Distance between sun and Earth (km)')
plt.title('The distance between the sun and the Earth with respect to the angle between them')
plt.grid(True)
plt.show()

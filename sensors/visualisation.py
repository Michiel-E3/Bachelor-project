import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

import ADC

# Initialize ADC reader
read_ADC = ADC.READ()

# Static positions for Left, Front, Right
positions = np.array([
    [0.0, 0.0],       # Left
    [0.5, 0.866],     # Front
    [1.0, 0.0],       # Right
])

# Compute static centroid of the triangle (geometric center)
triangle_center = np.mean(positions, axis=0)

# Set up figure and scatter plot
fig, ax = plt.subplots()
plt.gca().set_aspect('equal', adjustable='box')

# Initial scatter (just the 3 colored dots)
sc = ax.scatter(positions[:, 0], positions[:, 1], s=[0, 0, 0], c=['r', 'g', 'b'])

# Create initial arrow (dummy small)
arrow = ax.arrow(triangle_center[0], triangle_center[1], 0, 0, head_width=0.03, head_length=0.05, fc='black', ec='black')

# Configure axes
ax.set_xlim(-0.5, 1.5)
ax.set_ylim(-0.5, 1.5)
ax.set_xticks([0, 0.5, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Left', 'Front', 'Right'])
ax.set_yticklabels(['Back', 'Front'])

# Update function
def update(frame):
    global arrow
    values = np.array(read_ADC.values(), dtype=float)[0:3]

    # Update dot sizes
    sizes = values / 100
    sc.set_sizes(sizes)

    # Calculate weighted center (center of mass)
    weighted_pos = np.average(positions, axis=0, weights=values)

    # Remove old arrow
    arrow.remove()

    # Calculate vector from triangle center to center of mass
    vec = weighted_pos - triangle_center

    # Draw new arrow
    arrow = ax.arrow(triangle_center[0], triangle_center[1], vec[0], vec[1],
                     head_width=0.03, head_length=0.05, fc='black', ec='black')

    return sc, arrow

# Animate
ani = FuncAnimation(fig, update, interval=1000)

plt.title("Live ADC Readings with Directional Arrow (dot size = ADC value)")
plt.xlabel("Sensor Position")
plt.ylabel("Sensor Position")
plt.show()

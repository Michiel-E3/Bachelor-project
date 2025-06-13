import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

# Original data setup
threshold = np.linspace(1000, 3000, 3)
distance = np.linspace(0, 4, 5)
data = np.ndarray((3,5))

for i, value in enumerate(threshold):
    for j, x in enumerate(distance):
        data[i,j] = np.random.random() * x  # is a time

# Invert the mapping: from (threshold, distance) -> time
# to (distance, time) -> threshold

# Flatten the data to points for interpolation
T_vals = []
D_vals = []
Time_vals = []

for i, t in enumerate(threshold):
    for j, d in enumerate(distance):
        T_vals.append(t)
        D_vals.append(d)
        Time_vals.append(data[i, j])

# Create grid for distance and time
d_grid = np.linspace(min(distance), max(distance), 100)
time_grid = np.linspace(min(Time_vals), max(Time_vals), 100)
D_mesh, Time_mesh = np.meshgrid(d_grid, time_grid)

# Interpolate threshold values over this new grid
points = np.column_stack((D_vals, Time_vals))
threshold_grid = griddata(points, T_vals, (D_mesh, Time_mesh), method='linear')

# Plotting
fig, ax = plt.subplots()
ax.set_title('Required Threshold')
c = ax.pcolormesh(D_mesh, Time_mesh, threshold_grid, cmap='viridis', shading='auto')
ax.set_xlabel("Distance")
ax.set_ylabel("Desired Time")
fig.colorbar(c, ax=ax, label="Required Threshold")
plt.show()

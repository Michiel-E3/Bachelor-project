import matplotlib.pyplot as plt
import numpy as np

######################################################
# This cannot be changed:
threshold = np.linspace(1000, 3000, 3)
distance = np.linspace(0, 4, 5)
data = np.ndarray((3,5))

for i, value in enumerate(threshold):
    for j, x in enumerate(distance):
        data[i,j] = np.random.random()*x # is a time

print(data)
#######################################################
# Change this:

data = np.array(data).T  # Transpose to shape (5, 3)

X, Y = np.meshgrid(threshold, distance)

fig, ax = plt.subplots()
ax.set_title('Heatmap')
c = ax.pcolormesh(X, Y, data, cmap='inferno', shading='auto')  # shading='auto' avoids warnings

fig.colorbar(c, ax=ax, label="Time")
plt.show()

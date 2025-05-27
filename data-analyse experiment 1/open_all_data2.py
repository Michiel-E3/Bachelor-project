import matplotlib.pyplot as plt
import numpy as np

number_of_files = 40

data = []
data_T = [[], [], [], [], [], [], []]

for i in range(6, number_of_files+1):
    data.append([])
    t = []
    A0 = []
    A1 = []
    A2 = []
    A3 = []
    open_file = open(f"data/data-{i}.csv", 'r')
    for line in open_file:
        data_opgeknipt = line.split(',')
        try:
            data_opgeknipt = line.split(',')
            t.append(float(data_opgeknipt[0]))
            A0.append(float(data_opgeknipt[1]))
            A1.append(float(data_opgeknipt[2])) 
            A2.append(float(data_opgeknipt[3]))
            A3.append(float(data_opgeknipt[4]))
        except:
            if data_opgeknipt[0] == "height of setup:":
                height = round(float(data_opgeknipt[1]) - 60.05, 2)
    open_file.close()

    A_avg = np.mean(np.array([A0, A1, A2, A3]), axis=0)

    data[i-6].append([height] * len(t))
    data[i-6].append(t)
    data[i-6].append(A0)
    data[i-6].append(A1)
    data[i-6].append(A2)
    data[i-6].append(A3)
    data[i-6].append(A_avg)

    data_T[0].append([height] * len(t))
    data_T[1].append(t)
    data_T[2].append(A0)
    data_T[3].append(A1)
    data_T[4].append(A2)
    data_T[5].append(A3)
    data_T[6].append(A_avg)


data_all = [[], [], [], [], [], [], []]
for i in range(len(data_all)):
    for row in data_T[i]:
        data_all[i].extend(row)





"""
plt.scatter(height, signal, c=range(5,number_of_files), cmap='viridis')
plt.xlim(0,55)
plt.ylim(bottom=0)
plt.xlabel("Height (mm)")
plt.ylabel("Max signal strength (AU)")
plt.show()

x = data_all[0]
y = data_all[1]
z = data_all[6]

ax = plt.axes(projection='3d')
# ax.plot_trisurf(x,y,z, cmap='hsv')
ax.scatter3D(x,y,z, '.', c=z, cmap='hsv') # viridis
ax.set_xlabel(r'x')
ax.set_ylabel(r'y')
ax.set_zlabel(r'z')
plt.show()"""
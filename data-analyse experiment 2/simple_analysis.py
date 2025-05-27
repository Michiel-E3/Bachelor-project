import matplotlib.pyplot as plt
import numpy as np

number_of_files = 40

height = []
signal = []

for i in range(6, number_of_files+1):
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
                height_i = float(data_opgeknipt[1])
    open_file.close()

    A0_max = np.max(A0)
    A1_max = np.max(A1)
    A2_max = np.max(A2)
    A3_max = np.max(A3)

    height.append(height_i - 60.05)
    signal.append(np.mean([A0_max, A1_max, A2_max, A3_max]))



plt.scatter(height, signal, c=range(5,number_of_files), cmap='viridis')
plt.xlim(0,55)
plt.ylim(bottom=0)
plt.xlabel("Height (mm)")
plt.ylabel("Max signal strength (AU)")
plt.show()
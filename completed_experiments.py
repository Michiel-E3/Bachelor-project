import matplotlib.pyplot as plt
import numpy as np

number_of_files = 34

L = []

for i in range(1, number_of_files+1):
    open_file = open(f"data/data-{i}.csv", 'r')
    for line in open_file:
        data_opgeknipt = line.split(',')
        L.append(float(data_opgeknipt[1]))
        break
    open_file.close()

L.sort()

plt.hist(L, 20)
plt.show()
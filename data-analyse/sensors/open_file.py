import matplotlib.pyplot as plt
import numpy as np

filename = "data-0.csv"
open_file = open(f"data/{filename}", 'r')

A0 = []
A1 = []
A2 = []
A3 = []

for line in open_file:
    try:
        data_opgeknipt = line.split(',')
        A0.append(float(data_opgeknipt[0]))
        A1.append(float(data_opgeknipt[1]))
        A2.append(float(data_opgeknipt[2]))
        A3.append(float(data_opgeknipt[3]))
    except: pass
open_file.close()

data = np.array([A0,A1,A2,A3])

avg = np.mean(data, axis=1)
err = np.std(data, axis=1) / np.sqrt(len(data[0]))

for avg_i, err_i in zip(avg, err):
    print(f"avg = {avg_i} +- {err_i}")
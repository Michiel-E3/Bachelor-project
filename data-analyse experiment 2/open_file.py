import matplotlib.pyplot as plt
import numpy as np

filename = "data-5.csv"
open_file = open(f"data/{filename}", 'r')

t = []
A0 = []
A1 = []
A2 = []

for line in open_file:
    data_opgeknipt = line.split(',')
    try:
        data_opgeknipt = line.split(',')
        t.append(float(data_opgeknipt[0]))
        A0.append(float(data_opgeknipt[1]))
        A1.append(float(data_opgeknipt[2]))
        A2.append(float(data_opgeknipt[3]))
    except:
        if data_opgeknipt[0] == "height of setup:":
            height = float(data_opgeknipt[1]) - (13.1 + 42.4)
open_file.close()

data = np.array([t,A0,A1,A2])

avg = np.mean(data, axis=1)
err = np.std(data, axis=1) / np.sqrt(len(data[0]))

print(f"height = {height}")
# for avg_i, err_i in zip(avg, err):
#     print(f"avg = {avg_i} +- {err_i}")

endtime = 300

plt.plot(t[:endtime], A0[:endtime], color="blue", label="A0")
plt.plot(t[:endtime], A1[:endtime], color="red", label="A1")
plt.plot(t[:endtime], A2[:endtime], color="green", label="A2")
plt.xlim(0,300)
plt.show()
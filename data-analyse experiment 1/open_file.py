import matplotlib.pyplot as plt
import numpy as np

i = 7
# open_file = open(f"data/{filename}", 'r')
open_file = open(f"C:/Users/Michiel Erkamp/Desktop/Bachelor-project/data experiment 1/data-{i}.csv", 'r')

t = []
A0 = []
A1 = []
A2 = []
A3 = []

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
            height = float(data_opgeknipt[1])
open_file.close()

data = np.array([t,A0,A1,A2,A3])

avg = np.mean(data[1:5], axis=0)
err = np.std(data[1:5], axis=0) / np.sqrt(len(data[0]))

# print(f"height = {height}")
# for avg_i, err_i in zip(avg, err):
#     print(f"avg = {avg_i} +- {err_i}")

print(height)

endtime = 300

plt.plot(t[:endtime], A0[:endtime], color="blue", linestyle="--", linewidth=0.8, label="A0")
plt.plot(t[:endtime], A1[:endtime], color="orange", linestyle="--", linewidth=0.8, label="A1")
plt.plot(t[:endtime], A2[:endtime], color="green", linestyle="--", linewidth=0.8, label="A2")
plt.plot(t[:endtime], A3[:endtime], color="black", linestyle="--", linewidth=0.8, label="A3")
plt.plot(t[:endtime], avg[:endtime], color="red", label="avg")

plt.title(f"Height = {height-60.05}mm")
plt.legend(loc='best')
plt.xlabel("Time (s)")
plt.ylabel("Signal strength (AU)")
plt.show()
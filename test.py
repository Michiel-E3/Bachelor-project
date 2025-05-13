import numpy as np

list = np.array([0,1,0])
triggers = np.array([1,2,1])

stop = 1
for value, trigger in zip(list, triggers):
    if value >= trigger:
        stop *= 0

print(stop)

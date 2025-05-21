import csv
import os
from os.path import exists
from time import sleep

import ADC
import numpy as np

read_ADC = ADC.READ()

# do 100 measurements
measurements = []

for i in range(100):

    readings = read_ADC.values()
    measurements.append(readings)

measurements = np.array(measurements)

# print(measurements[0])

# store to csv

if exists("data") == False:
    os.mkdir("data")

# Check whether file already exists
i = 0
while exists(f"data/data-{i}.csv") == True:
    i += 1

# Save the results in a new csv file
with open(f"data/data-{i}.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        [
            "Value of A0",
            "Value of A1",
            "Value of A2",
            "Value of A3"
        ]
    )
    for measurement in measurements:
        writer.writerow(measurement)

avg = np.mean(measurements, axis=0)
std = np.std(measurements, axis=0)

print("Ai: avg ,\tstd")
for i in range(len(avg)):
    print(f"A{i}: {avg[i]},\t{np.round(std[i],2)}")
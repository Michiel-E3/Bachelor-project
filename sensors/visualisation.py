import time

import ADC
import matplotlib.pyplot as plt
import numpy as np

read_ADC = ADC.READ()

    # Loop to read the analog inputs continuously
while True:
    values = read_ADC.values()
    print("Front: ", values[0])
    print("Left: ", values[1])
    print("Right: ", values[2])
    
    # Delay for 1 second
    time.sleep(1)
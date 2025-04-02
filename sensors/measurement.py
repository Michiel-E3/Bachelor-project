import ADC
import numpy as np

read_ADC = ADC.READ()

# do a measurement:

readings = read_ADC.values() # = [A0, A1, A2, A3]

print(readings[0])

readings = read_ADC.values()

print(readings[0])
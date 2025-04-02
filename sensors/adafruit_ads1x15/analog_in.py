import random


class AnalogIn:
    def __init__(self, ads, channel):
        pass
    
    @property
    def value(self):
        return random.randint(0, 32767)  # Simulating 16-bit ADC values
    
    @property
    def voltage(self):
        return random.uniform(0, 5)  # Simulating voltage between 0 and 5V
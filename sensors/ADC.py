# sudo pip3 install adafruit-circuitpython-ads1x15 --break-system-packages

import time

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
import numpy as np
from adafruit_ads1x15.analog_in import AnalogIn


class READ():
    def __init__(self):
        # Initialize the I2C interface
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create an ADS1115 object
        ads = ADS.ADS1115(i2c)
        
        # Define the analog input channels
        self.channel0 = AnalogIn(ads, ADS.P0)
        self.channel1 = AnalogIn(ads, ADS.P1)
        self.channel2 = AnalogIn(ads, ADS.P2)
        self.channel3 = AnalogIn(ads, ADS.P3)
    
    def values(self):
        readings = np.array([
            self.channel0.value, 
            self.channel1.value, 
            self.channel2.value, 
            self.channel3.value
            ])
        return readings
    
    def value(self, channel: int):
        if channel not in range(4):
            raise ValueError("Channel must be in range [0,3]")

        match channel:
            case 0:
                return self.channel0.value
            case 1:
                return self.channel1.value
            case 2:
                return self.channel2.value
            case 3:
                return self.channel3.value

    def voltages(self):
        readings = np.array(
            [
                self.channel0.voltage, 
                self.channel1.voltage, 
                self.channel2.voltage, 
                self.channel3.voltage
            ]
        )
        return readings
    
    def voltage(self, channel: int):
        if channel not in range(4):
            raise ValueError("Channel must be in range [0,3]")

        match channel:
            case 0:
                return self.channel0.voltage
            case 1:
                return self.channel1.voltage
            case 2:
                return self.channel2.voltage
            case 3:
                return self.channel3.voltage


if __name__ == "__main__":

    read = READ()

    # Loop to read the analog inputs continuously
    while True:
        values = read.values()
        voltages = read.voltages()
        print("Analog Value 0: ", values[0], "\t Voltage 0: ", voltages[0])
        print("Analog Value 1: ", values[1], "\t Voltage 1: ", voltages[1])
        print("Analog Value 2: ", values[2], "\t Voltage 2: ", voltages[2])
        print("Analog Value 3: ", values[3], "\t Voltage 3: ", voltages[3])
        
        # Delay for 1 second
        time.sleep(1)
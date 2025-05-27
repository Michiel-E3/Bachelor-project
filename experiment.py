import csv
import os
import threading
import time
from os.path import exists

import numpy as np

import ADC
import RPi.GPIO as GPIO


def dispensing(rotations, speed):
    global t_start

    in1 = 17
    in2 = 18
    in3 = 27
    in4 = 22

    # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
    step_sleep = 0.0015

    step_count = round(4096 * rotations) # 5.625*(1/64) per step, 4096 steps is 360°

    # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
    step_sequence = [[1,0,0,1],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1]]

    # setting up
    GPIO.setmode(GPIO.BCM)
    GPIO.setup( in1, GPIO.OUT )
    GPIO.setup( in2, GPIO.OUT )
    GPIO.setup( in3, GPIO.OUT )
    GPIO.setup( in4, GPIO.OUT )

    # initializing
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    
    motor_pins = [in1,in2,in3,in4]
    motor_step_counter = 0
    step = 0
    t_start = round(time.time())

    while not stop_threading.is_set() and step < step_count:
        for pin in range(len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        motor_step_counter = (motor_step_counter - 1) % 8
        time.sleep(step_sleep)
        step += 1
        # if step%1024 == 0:
        #     print(f"rotated: {step/4096}")
    
    """
    while step > 0:
        for pin in range(len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep(step_sleep)
        step -= 1
        # if step%1024 == 0:
        #     print(f"rotated: {step/4096}")"""

    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()


def measuring():
    global height
    global t_start
    global triggers
    global read_ADC

    time.sleep(0.1)

    measurements = []

    while not stop_threading.is_set():
        values = read_ADC.values()
        t = round(time.time()) - t_start
        measurements.append(np.concatenate(([t], values)))
        print(f"{triggers[0]}\t{triggers[1]}\t{triggers[2]}")
        print(f"{values[0]}\t{values[1]}\t{values[2]}\t at t = {t}")
        """
        # check for stop criterion 1
        if len(measurements[-120:-60]) == 60:
            past_avg = np.mean(measurements[-120:-60], axis=0)[-4:]
        else:
            past_avg = [32767, 32767, 32767, 32767]
        current_avg = np.mean(measurements[-60:], axis=0)[-4:]
        # print(past_avg)
        # print(current_avg)
        rel_change = (current_avg - past_avg)/past_avg
        print(f"{round(rel_change[0],3)}\t{round(rel_change[1],3)}\t{round(rel_change[2],3)}\t{round(rel_change[3],3)}")
        # experiment is over
        if all(-0.01 < x < 0.01 for x in rel_change):
            print("equilibrium reached")
            stop_threading.set()"""

        # check for stop criterion 2
        stop = 1
        for value, trigger in zip(values[0:3], triggers[0:3]):
            if value >= trigger:
                stop *= 0
        if t > 180: # also stop after 5 mins
            stop = 1
        if stop == 1 and t > 60:
            print("trigger value reached")
            stop_threading.set()
        
        try:
            height
            print("*")
        except:
            print("x")
        time.sleep(1)
    
    # save height and measurements

    if exists("data") == False:
        os.mkdir("data")
    
    # Check whether file already exists
    i = 0
    while exists(f"data/data-{i}.csv") == True:
        i += 1
    
    while True:
        try:
            print(height)
            break
        except:
            time.sleep(0.1)

    # Save the results in a new csv file
    with open(f"data/data-{i}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["height of setup:", height])
        writer.writerow(
            [
                "time",
                "value of sensor0",
                "value of sensor1",
                "value of sensor2"
            ]
        )
        for measurement in measurements:
            writer.writerow(measurement[0:4]) # check dit


# Define a function for user input
def wait_for_enter():
    global height
    # Prompt for sensor height
    height = input("Height of sensors in mm:")
    print(height)
    input("Press Enter to stop the program early\n")
    stop_threading.set()


if __name__ == "__main__":
    
    read_ADC = ADC.READ()
    
    values = read_ADC.values()
    """
    while not(all(x < 1500 for x in values[0:3])):
        time.sleep(1)
        values = read_ADC.values()
        print(values[0:3])
    
    print("setting triggers")
    
    baselines = []

    for _ in range(100):
        values = read_ADC.values()
        baselines.append(values)
        # print(values)
        time.sleep(0.1)
        
    baseline = np.mean(baselines, axis=0)
    triggers = np.round(baseline + 2*np.std(baselines, axis=0))
    print(np.round(baseline))
    print(triggers)"""
    
    triggers = np.array([1000,1000,1000,1000])

    # Flag to signal when to stop reading
    stop_threading = threading.Event()

    rotations = 5
    speed = 1

    # Start dispensing thread
    thread_dispensing = threading.Thread(target=dispensing, args=(rotations, speed))
    thread_dispensing.start()

    # start measuring
    input("press enter to start measuring")

    # Start measuring thread
    thread_measuring = threading.Thread(target=measuring)
    thread_measuring.start()

    # Start the input thread
    thread_input = threading.Thread(target=wait_for_enter, daemon=True)
    thread_input.start()

    # Wait until any thread sets the event (user or experiment logic)
    while not stop_threading.is_set():
        time.sleep(0.1)

    print("Stopping threads...")

    thread_dispensing.join()
    thread_measuring.join()
    print("Threads have been stopped.")

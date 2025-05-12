import threading
import time
import RPi.GPIO as GPIO
import sensors.ADC
import numpy as np

def dispensing(rotations, speed):
    in1 = 17
    in2 = 18
    in3 = 27
    in4 = 22

    # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
    step_sleep = 0.002 / speed

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
    GPIO.setmode( GPIO.BCM )
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

    while not stop_threading.is_set() and step < step_count:
        for pin in range(len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        motor_step_counter = (motor_step_counter - 1) % 8
        # time.sleep(step_sleep)
        step += 1
        if step%1024 == 0:
            print(f"rotated: {step/4096}")

    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()


def measuring(height):
    print(height)

    read_ADC = sensors.ADC.READ()
    t_start = round(time.time())

    measurements = []

    while not stop_threading.is_set():
        values = read_ADC.values()
        t = round(time.time()) - t_start
        measurements.append(np.concatenate(([t], values)))
        print(f"{values[0]}\t{values[1]}\t{values[2]}\t{values[3]}\t at t = {t}")
        time.sleep(1)
    
    # save height and measurements
    


if __name__ == "__main__":
    
    # Flag to signal when to stop reading
    stop_threading = threading.Event()

    height = input("Height of sensors in mm:")
    rotations = 1
    speed = 100

    thread_dispensing = threading.Thread(target=dispensing, args=(rotations, speed))
    thread_measuring = threading.Thread(target=measuring, args=(height,))

    thread_dispensing.start()
    thread_measuring.start()

    # Wait for Enter key press
    input("Press Enter to stop the program\n")

    # Signal the thread to stop
    stop_threading.set()
    print("Stopping threads...")
    
    thread_dispensing.join()
    thread_measuring.join()
    print("Threads have been stopped.")
import time
#import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

import random

encoderA = 5 # pin of hall effect A
encoderB = 6 # pin of hall effect B

"""GPIO.setmode(GPIO.BOARD)
GPIO.setup(encoderA, GPIO.IN)
GPIO.setup(encoderB, GPIO.IN)
GPIO.setup(7, GPIO.OUT) # motor control GPIO pin
"""
counter = 0 # position/counter
reqCounter = 0 # wanted counter to hit wanted degree

cpr = 12 # counts per rotation
mgr = 298 # motor gear ratio, 298:1
cgr = 86 / 20 # camera spur/bevel gear ratio, x:xx

mpr = cpr * mgr *cgr # total counter per output rotation
degree = 360

cpd = mpr / degree # counts per degree
dpc = degree / mpr # degrees per count

"""def readEncoder(pin):
    global counter
    if pin == 5:
        if GPIO.input(5) == GPIO.HIGH:
            if GPIO.input(6) == GPIO.LOW:
                counter += 1
            else:
                counter -= 1
    return counter"""

def virtualEncoder():
    global counter

    if (random.randint(0,10) > 1):
        counter += 1
    else:
        counter -= 1

"""

Parameters:
- direction [int]: 0 = right, 1 = left
"""
def rotateCam(direction, degree = 60):
    global cpd
    global counter
    global reqCounter

    counter = 0 # reset counter from previous runs
    reqCounter = round(degree * cpd)
    print(reqCounter)

    if (direction == 0):
        # turn on motor that turns right
        print("motor on, turning right")
        pass
    elif (direction == 1):
        # turn on motor that turns left
        print("motor off, turning left")
        pass
    
    while (counter < reqCounter):
        #GPIO.add_event_detect(encoderA, GPIO.RISING, callback=readEncoder)
        virtualEncoder()
        print(counter)
        time.sleep(0.1)
    
    # turn off motor
    print("motor off")

rotateCam(0, 10)
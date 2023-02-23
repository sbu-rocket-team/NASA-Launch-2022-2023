import time

import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

from NASAcode.tools import motorControl as mc

import random


encoderA = 5 # pin of hall effect

"""GPIO.setmode(GPIO.BOARD)
GPIO.setup(encoderA, GPIO.IN)
GPIO.setup(7, GPIO.OUT) # motor control GPIO pin
"""

"""https://www.pololu.com/product/4761"""

MAXROT = 240 # either directions

CPR = 6 # counts per rotation for 2 hall effects, halved if only 1... encoder used is 12 cpr
MGR = (25 * 34 * 37 * 35 * 38) / (12 * 9 * 10 * 13 * 10) # actual motor gearbox ratio
CGR = 86 / 20 # camera spur/bevel gear ratio, x:xx

MPR = round(CPR * MGR * CGR) # total counter per output rotation
CPD = MPR / 360 # counts per degree

COUNTDELAY = 40 # for 20D motor, need to test for micro

savedDegree = 0 # basically savedCounter ... -240 to 240, postive to the right
counter = 0 # position/counter
reqCounter = 0 # wanted counter to reach desire degree

def readEncoder(pin):
    global counter
    if pin == 5:
        if GPIO.input(5) == GPIO.HIGH:
            counter += 1
        else:
            counter -= 1
    return counter

def virtualEncoder():
    global counter

    if (random.randint(0,10) > 1):
        counter += 1

"""
Parameters:
- direction [char]: "R"ight, "L"eft
"""
def rotateCam(direction, degree = 60):
    print("Rotating", direction, degree)
    degree = degree % 360
    print("Actual rotation:", degree)

    global CPD
    global counter
    global reqCounter
    global savedDegree
    global MAXROT

    if ((degree > 180) and (abs(savedDegree) != 180)):
        if (direction == "R"):
            direction = "L"
        elif (direction == "L"):
            direction = "R"
        degree = 360 - degree
        print("fasta the other way,", direction, degree)
    elif ((degree == 180) and (abs(savedDegree) == 180)):
        if (savedDegree < 0):
            direction = "R"
        elif (savedDegree > 0):
            direction = "L"

    counter = 0 # reset counter from previous runs

    reqCounter = round(degree * CPD) - COUNTDELAY

    if (direction == "R"):
        # turn on motor that turns right
        newDegree = savedDegree + degree
        print("New Angle:", newDegree)

        if (abs(newDegree) > MAXROT):
            print("No further right, now left")
            reDegree = MAXROT + degree
            reqCounter = 0

            rotateCam("L", reDegree)
        else:
            # turn motor on here
            savedDegree += degree
            print("motor on, turning right")
    elif (direction == "L"):
        # turn on motor that turns left
        newDegree = savedDegree - degree
        print("New Angle:", newDegree)

        if (abs(newDegree) > MAXROT):
            print("No further left, now right")
            reDegree = degree - MAXROT
            reqCounter = 0

            rotateCam("R", reDegree)
        else:
            # turn motor on here
            savedDegree -= degree
            print("motor on, turning left")
    
    while (counter < reqCounter):
        #GPIO.add_event_detect(encoderA, GPIO.RISING, callback=readEncoder)
        virtualEncoder()
    
    # turn off motor
    print("Counters:", counter)
    print("motor off")

"""
# end result, R 60
rotateCam("R", 240)
print("Current Angle:", savedDegree)
print()

rotateCam("R", 60)
print("Current Angle:", savedDegree)
print()

rotateCam("R", 60)
print("Current Angle:", savedDegree)
print()

rotateCam("L", 300)
print("Current Angle:", savedDegree)
print()
"""

"""
# end result, R 60
rotateCam("L", 120)
print("Current Angle:", savedDegree, "\n")
rotateCam("R", 300)
print("Current Angle:", savedDegree, "\n")
rotateCam("L", 120)
print("Current Angle:", savedDegree, "\n")
"""

"""
# end result, left 60
rotateCam("L", 120)
print("Current Angle:", savedDegree, "\n")
rotateCam("R", 360)
print("Current Angle:", savedDegree, "\n")
rotateCam("R", 120)
print("Current Angle:", savedDegree, "\n")
rotateCam("R", 180)
print("Current Angle:", savedDegree, "\n")
rotateCam("L", 240)
print("Current Angle:", savedDegree, "\n")
"""

"""
rotateCam("L", 120)
print("Current Angle:", savedDegree, "\n")
rotateCam("R", 300)
print("Current Angle:", savedDegree, "\n")
rotateCam("L", 180)
print("Current Angle:", savedDegree, "\n")
"""
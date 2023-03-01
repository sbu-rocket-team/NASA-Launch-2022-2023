"""
Property Of: SBU Rocket Team

Written By: Jewick Shi
Edited By: Ethan Carr
"""
import time

import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

from NASAcode.tools import motor_functions as motF
import pinout as po

"""https://www.pololu.com/product/4761"""

MAXROT = 240 # either directions

CPR = 6 # counts per rotation for 2 hall effects, halved if only 1... encoder used is 12 cpr
MGR = (25 * 34 * 37 * 35 * 38) / (12 * 9 * 10 * 13 * 10) # actual motor gearbox ratio
CGR = 86 / 20 # camera spur/bevel gear ratio, x:xx

MPR = round(CPR * MGR * CGR) # total counter per output rotation
CPD = MPR / 360 # counts per degree

COUNTDELAY = 40 # for 20D motor, need to test for micro

def readEncoder(pin):
    global counter
    if pin == po.ENCODER:
        if GPIO.input(pin) == GPIO.HIGH:
            counter += 1

"""
Parameters:
- direction [char]: "R"ight, "L"eft
"""
def rotateCam(direction, currentAngle, degree = 60, encoderPin = po.ENCODER, encoderMotorPhase = po.ROT_DIR, encoderMotorEnable = po.ROT_PWM):
    print("Rotating", direction, degree)
    degree = degree % 360
    print("Actual rotation:", degree)

    global CPD
    global MAXROT

    counter = 0 # position/counter
    reqCounter = 0 # wanted counter to reach desire degree

    if ((degree > 180) and (abs(currentAngle) != 180)):
        if (direction == "R"):
            direction = "L"
        elif (direction == "L"):
            direction = "R"
        degree = 360 - degree
    elif ((degree == 180) and (abs(currentAngle) == 180)):
        if (currentAngle < 0):
            direction = "R"
        elif (currentAngle > 0):
            direction = "L"

    reqCounter = round(degree * CPD) - COUNTDELAY

    if (direction == "R"):
        newDegree = currentAngle + degree
        print("New Angle:", newDegree)

        if (abs(newDegree) > MAXROT):
            print("No further right, now left")
            reDegree = MAXROT + degree
            reqCounter = 0

            rotateCam("L", reDegree)
        else:    # turn motor on here
            motF.smoothStart(encoderMotorPhase, encoderMotorEnable, "R") #
            currentAngle += degree
            print("motor on, turning right")
    elif (direction == "L"):
        newDegree = currentAngle - degree
        print("New Angle:", newDegree)

        if (abs(newDegree) > MAXROT):
            print("No further left, now right")
            reDegree = degree - MAXROT
            reqCounter = 0

            rotateCam("R", reDegree)
        else: # turn motor on here
            motF.smoothStart(encoderMotorPhase, encoderMotorEnable, "L") #
            currentAngle -= degree
            print("motor on, turning left")
    
    while (counter < reqCounter):
        GPIO.add_event_detect(encoderPin, GPIO.RISING, callback=readEncoder)
    
    motF.motorOFF(po.ROT_ENABLE) # turn off motor
    print("Counters:", counter)
    print("motor off")
    return currentAngle
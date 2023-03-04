"""
Property Of: SBU Rocket Team

Written By: Jewick Shi
Edited By: Ethan Carr
"""
import time

import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

from NASAcode.tools import motor_functions as motF, pinout as po

"""https://www.pololu.com/product/4761"""

MAXROT = 240 # either directions

CPR = 6 # counts per rotation for 2 hall effects, halved if only 1... encoder used is 12 cpr
MGR = (25 * 34 * 37 * 35 * 38) / (12 * 9 * 10 * 13 * 10) # actual motor gearbox ratio
CGR = 43 / 12 # camera spur/bevel gear ratio, x:xx

MPR = round(CPR * MGR * CGR) # total counter per output rotation
CPD = MPR / 360 # counts per degree

COUNTDELAY = 40 # for 20D motor, need to test for micro

def readEncoder(pin, rCount):
    counter = 0
    prev = 0
    while(counter < rCount):
        val = GPIO.input(po.ENCODER)
        if(val == 1 & val != prev):
            counter += 1
        
        prev = val

"""     # Old code!
def rotate60(direction):
    fudge = 40
    motF.motorON2(po.ROT_DIR, po.ROT_PWM,direction,101)
    #if(direction == p.ROT_LEFT):

    #elif(direction == p.ROT_RIGHT)
    ct = 0
    cts = 6300/6
    prev = 0
    while(ct < (cts-fudge)):
        val = GPIO.input(po.ENCODER)
        if(val == 1 & val != prev):
            ct += 1
        
        prev = val
    motF.off(po.ROT_DIR, po.ROT_PWM)
"""


"""
Parameters:
- direction [char]: "R"ight, "L"eft
"""
def rotateCam(direction, currentAngle, degree = 60, recall = False, encoderPin = po.ENCODER, encoderMotorPhase = po.ROT_DIR, encoderMotorEnable = po.ROT_PWM):
    #print("Rotating", direction, degree)
    degree = degree % 360
    #print("Actual rotation:", degree)

    global CPD
    global MAXROT

    reqCounter = 0 # wanted counter to reach desire degree
    reverseDir = False

    reqCounter = round(degree * CPD) - COUNTDELAY
    
    if (not (degree >= 180)):
        if (direction == "R"):
            newDegree = currentAngle + degree
            if (abs(newDegree) > MAXROT):
                reverseDir = True
        
        elif (direction == "L"):
            newDegree = currentAngle - degree
            if (abs(newDegree) > MAXROT):
                reverseDir = True
        returnDegree = newDegree
    elif (currentAngle >= abs(180)):
        if (direction == "R"):

            newDegree = 360 - degree
    
    if (reverseDir):
        if (direction == "R"):
            direction = "L"
            returnDegree = -360 + newDegree
        elif (direction == "L"):
            direction = "R"
            returnDegree = 360 + newDegree
        
        degreeDif = abs(returnDegree) + abs(currentAngle)
        reqCounter = round(degreeDif * CPD) - COUNTDELAY
    
    """    
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

        if ((abs(newDegree) > MAXROT) and (not recall)):
            print("No further right, now left")
            reDegree = MAXROT + degree
            reqCounter = 0

            rotateCam("L", currentAngle, reDegree, True)
        else:    # turn motor on here
            motF.motorON(encoderMotorPhase, encoderMotorEnable, "R", 100) #
            currentAngle += degree
            print("motor on, turning right")
    elif (direction == "L"):
        newDegree = currentAngle - degree
        print("New Angle:", newDegree)

        if ((abs(newDegree) > MAXROT) and (not recall)):
            print("No further left, now right")
            reDegree = degree - MAXROT
            reqCounter = 0

            rotateCam("R", currentAngle, reDegree, True)
        else: # turn motor on here
            motF.motorON(encoderMotorPhase, encoderMotorEnable, "L", 100) #
            currentAngle -= degree
            print("motor on, turning left")
    """
    
    #while (counter < reqCounter):
    #    GPIO.add_event_detect(encoderPin, GPIO.RISING, callback=readEncoder)
    motF.motorON(encoderMotorPhase, encoderMotorEnable, direction, 100)
    readEncoder(po.ENCODER, reqCounter)
    motF.motorOff(po.ROT_PWM) # turn off motor
    print()
    return returnDegree


def rotateTest():
    # Testing out the rotation capabilities of the stuffs
    currentDegree = 0
    currentDegree = rotateCam("R", currentDegree, 60)
    time.sleep(0.5)
    currentDegree = rotateCam("L", currentDegree, 60)
    time.sleep(0.5)
    # Should be at original location low

    currentDegree = rotateCam("L", currentDegree, 60)
    time.sleep(0.5)
    currentDegree = rotateCam("R", currentDegree, 60)
    time.sleep(0.5)

    # and then should be back at zero again :)
import time

import RPi.GPIO as GPIO

from NASAcode.tools import setup_gpio
from NASAcode.tools import pinout as po
from NASAcode.tools import log_functions as log
FREQ = 120
MIN_SPD = 40
TARGERT = "Motors"
# https://www.pololu.com/product/2135

setup_gpio.setup()

"""
Mode HIGH/1...
xIN1 = Phase pin = 0/1 ... forward/backward
xIN2 = Enable pin = PWN (0-100) ... Speed

(xIN1, xIN2) = (pPin, ePin)

(LOW, #) == forward @ #% speed
(HIGH, #) == backward @ #% speed

"""

"""

Parameters:
- pPin [int]: Phase pin determines the direction of the motor, 0/1 = forward/backward
- ePin [int]: Enable pin to control the speed of the motor through PWM, 0-100%
- direction [char]: "R" or "L" for right or left relatively
- intSped [int]: Starting speed of the motor, if no endSpd is specified is also the settled speed
- endSped [int]: Settling speed of the motor, 
"""
def motorON(pPin, ePin, direction, intSpd=100, endSpd=-1, time=-1, FREQ = 120, MIN_SPD = 40):
    log.log(0,TARGERT,"Turning on motor: " + po.pin2string(ePin) + ", "+po.dir2string(ePin,direction))
    pwm = None

    if (endSpd == -1):
        endSpd = intSpd

    if (intSpd >= MIN_SPD):
        if (direction == "R"):
            GPIO.output(pPin, 1)
            #GPIO.output(pPin, po.ROT_RIGHT)
            #pwm = GPIO.PWM(ePin, FREQ)
            #pwm.start(intSpd)
        elif (direction == "L"):
            GPIO.output(pPin, 0)
            #GPIO.output(pPin, po.ROT_LEFT)
            #pwm = GPIO.PWM(ePin, FREQ)
            #pwm.start(intSpd)
        #changeSpd(pwm, intSpd, endSpd)
        GPIO.output(ePin, 1)

    return pwm
"""
DOCUMENT TODO
"""
def smoothStart(pPin, ePin, direction):
    motorON(pPin, ePin, direction, 50, 100)

# delete? added your changes above
""" 
on drv,
phase, direction of the motor (high forward, low backwards)
enable, the speed of the motor (0 off, high 100%)
"""
def motorON2(dir_pin, pwm_pin, direction, speed=100):
    minPWM = 40 # Just a guess, might wanna play around with this and see what value works best.
    
    GPIO.output(dir_pin, direction)
    if(speed > 100):
        GPIO.output(pwm_pin, 1)
    elif(speed<minPWM): # Protect from stalling the motors at low voltages
        print("Speed submitted is below the min value")
        return False
    else:
        pwm = GPIO.PWM(pwm_pin, FREQ)
        pwm.start(minPWM)
        changeSpd(pwm, minPWM, speed)
    return True

def motorOff(ePin):
    GPIO.output(ePin, 0)
    log.log(0,TARGERT,"Turning off motor " + po.pin2string(ePin))

"""
DOCUMENT TODO
"""
def changeSpd(pwm, startSpd, endSpd):
    interval = 1
    
    if (endSpd > 100):
        endSpd = 100
    
    if (endSpd != -1):
        if (endSpd > startSpd):
            interval = round((endSpd - startSpd) / 9)
        else:
            interval = round((startSpd - endSpd) / 9)

    startSpd += interval
    endSpd += interval        

    for i in range(startSpd, endSpd, interval):
        if (i > 100):
            pwm.ChangeDutyCycle(100)
            break
        pwm.ChangeDutyCycle(i)
        time.sleep(0.5)


#################
def run_test(enable, phase):
    pins = [enable, phase]            
    GPIO.output(pins, GPIO.HIGH)


     
def off(direction, pwm):
    pins = [direction, pwm]          
    GPIO.output(pins, GPIO.LOW)  
    log.log(0,TARGERT,"Turning off motor " + po.pin2string(pwm))

def moveRack(direction, timeOn = 0.5):
    if (direction == "U"):
        motorON(po.RP_DIR, po.RP_PWM, "L")
    elif (direction == "D"):
        motorON(po.RP_DIR, po.RP_PWM, "R")
    time.sleep(timeOn)
    motorOff(po.RP_PWM)

    """
    time_up = 0.5
    motorON2(po.RP_DIR, po.RP_PWM, po.RP_UP,101)
    time.sleep(time_up)
    off(po.RP_DIR, po.RP_PWM)
    """

def moveLeadscrew(direction, timeOn = 20):
    if (direction == "O"):
        motorON(po.LEADSCREW_DIR, po.LEADSCREW_PWM, "L")
    elif (direction == "C"):
        motorON(po.LEADSCREW_DIR, po.LEADSCREW_PWM, "R")
    time.sleep(timeOn)
    motorOff(po.LEADSCREW_PWM)

    

def testRack():
    # This will raise the camera up, and then set it down.
    #log.log(0,TARGERT,"Testing rack and pinion")
    time_up = 0.25
    time_diff = 0.05

    motorON(po.RP_DIR, po.RP_PWM, po.RP_UP)
    time.sleep(time_up)
    off(po.RP_DIR, po.RP_PWM)    

    time.sleep(1)

    motorON(po.RP_DIR, po.RP_PWM, po.RP_DOWN)
    time.sleep(time_up - time_diff)
    off(po.RP_DIR, po.RP_PWM)


def testLeads():
    # This will open for 1 second, close for 1 second
    time_up = 1
    time_diff = 0

    motorON(po.LEADSCREW_DIR, po.LEADSCREW_PWM, po.LEADSCREW_OPEN)
    time.sleep(time_up)
    off(po.LEADSCREW_DIR, po.LEADSCREW_PWM)    

    time.sleep(1)

    motorON(po.LEADSCREW_DIR, po.LEADSCREW_PWM, po.LEADSCREW_CLOSE)
    time.sleep(time_up - time_diff)
    off(po.LEADSCREW_DIR, po.LEADSCREW_PWM)


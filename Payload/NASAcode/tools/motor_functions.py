import time

import RPi.GPIO as GPIO

from NASAcode.tools import setup_gpio

FREQ = 120
MIN_SPD = 40
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
def motorON(pPin, ePin, direction, intSpd, endSpd=-1, time=-1):
    global FREQ
    global MIN_SPD

    GPIO.output(ePin, 1)
    pwm = None

    if (endSpd == -1):
        endSpd = intSpd

    if (intSpd >= MIN_SPD):
        if (direction == "R"):
            GPIO.output(pPin, 0)
            pwm = GPIO.PWM(ePin, FREQ)
            pwm.start(intSpd)
        elif (direction == "L"):
            GPIO.output(pPin, 1)
            pwm = GPIO.PWM(ePin, FREQ)
            pwm.start(intSpd)
        changeSpd(pwm, intSpd, endSpd)

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
import time

import RPi.GPIO as GPIO

FREQ = 120

#enable pins
enablePinD = None 
enablePinMLift = None
enablePinMRot = None

#identify the right motor pins
motorPinD = None
motorPinMLift = None
motorPinMRot = None

# as tuples just to reudce .setup lines
pinDList = [enablePinD, motorPinD]
pinMLList = [enablePinMLift, motorPinMLift]
pinMRList = [enablePinMRot, motorPinMRot]

pinList = [pinDList, pinMLList, pinMRList]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinList, GPIO.OUT)

# https://www.pololu.com/product/2135

"""
Mode HIGH...
xIN1 = Phase pin = ON/OFF
xIN2 = Enable pin = Speed

(xIN1, xIN2)

(LOW, #) == forward @ #% speed
(HIGH, #) == backward @ #% speed

"""

"""

Parameters:
- pPin [int]: Phase pin (actually enable) to turn the motor on/off
- ePin [int]: Enable pin (actually phase) to control the speed of the motor
- direction [char]: "F" or "B" for forward/right or backwards/left relatively
- intSped [int]: Starting speed of the motor, if no endSpd is specified is also the settled speed
- endSped [int]: Settling speed of the motor, 
"""
def motorON(pPin, ePin, direction, intSpd, endSpd = -1):
    global FREQ
    eSpeed = intSpd
    GPIO.output(ePin, 1)

    if (endSpd == -1):
        endSpd = intSpd

    if (direction == "F"):
        GPIO.output(pPin, 0)
        pwm = GPIO.PWM(ePin, FREQ)
        pwm.start(eSpeed)
    elif (direction == "B"):
        GPIO.output(pPin, 1)
        pwm = GPIO.PWM(ePin, FREQ)
        pwm.start(eSpeed)
    rampSpd(pwm, intSpd, endSpd)

def mtorOff(ePin):
    GPIO.output(ePin, 0)

def rampSpd(pwm, startSpd, endSpd):
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

def cleanPins(pinList):
    GPIO.cleanup(pinList)
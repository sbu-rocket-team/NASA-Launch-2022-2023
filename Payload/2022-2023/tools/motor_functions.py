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
pinList = [enablePinD, enablePinMLift, enablePinMRot, motorPinD, motorPinMLift, motorPinMRot]
pinDList = [enablePinD, motorPinD]
pinMLList = [enablePinMLift, motorPinMLift]
pinMRList = []

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
    rampUp(pwm, intSpd, endSpd)

def mtorOff(ePin):
    GPIO.output(ePin, 0)

def rampUp(pwm, startSpd, endSpd):
    for i in range(startSpd, endSpd, 5):
        pwm.ChangeDutyCycle(i)
        time.sleep(0.5)

def cleanPins(pinList):
    GPIO.cleanup(pinList)
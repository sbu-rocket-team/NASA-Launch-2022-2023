import time
import RPi.GPIO as GPIO

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


GPIO.setmode(GPIO.BOARD)

GPIO.setup(pinList, GPIO.OUT)

"""
General On/Off
"""
# lead screw motor
GPIO.output(pinDList, 1)
time.sleep(2)
GPIO.output(pinDList, 0)

time.sleep(2)

# camera lift motor
GPIO.output(pinMLList, 1)
time.sleep(2)
GPIO.output(pinMLList, 0)

time.sleep(2)

# now both
GPIO.output(pinDList, 1)
GPIO.output(pinMLList, 1)
time.sleep(2)
GPIO.output(pinDList, 0)
GPIO.output(pinMLList, 0)

time.sleep(2)

"""
PWM
"""
#Use PWM for rotation motor
freq = 60

GPIO.output(enablePinMRot, 1)

motorRot = GPIO.PWM(motorPinMRot, freq)
motorRot.start(100) # turn on with 100% duty cycle
# motor1.ChangeFrequency(freq)
# motor1.ChanegDutyCycle(dc)
time.sleep(2)
motorRot.stop()

# autobots roll out
while 1:
    for dc in range(0, 101, 5):
        motorRot.ChangeDutyCycle(dc)
        time.sleep(0.1)
    for dc in range(100, -1, -5):
        motorRot.ChangeDutyCycle(dc)
        time.sleep(0.1)

motorRot.stop()

# Clears only the motor pins
# tbh idk if we need
GPIO.cleanup(pinList)
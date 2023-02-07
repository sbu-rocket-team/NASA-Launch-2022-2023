
# Code to control DC gearmotors using DRV8835 dual motor drivers

# Code written by Jewick, edited by EC.

import RPi.GPIO as GPIO
from time import sleep

def getpins(args):
    if len(args) == 1:
        pins = args[0]    
    elif len(args) == 2:
        pins = [args[0], args[1]]

    return pins

def run_test(*args):
    pins = getpins(*args)            
    GPIO.output(pins, GPIO.HIGH)


def off(*args):
    pins = getpins(*args)       
    
    GPIO.output(pins, GPIO.LOW)  


def pwm_on(pin, duty, start, end, step, time):

    pwm = GPIO.PWM(pin, duty)
    pwm.start(start)

    for i in range(start,end,step):
        pwm.ChangeDutyCycle(i)
        sleep(time/((end-start)/step))


def run_smoothstart(*args):
    pins = getpins(*args)    

    enable = pins[0] # PWM Control
    phase = pins[1]

    pwm_on(enable,120,50,100,5,2)



'''
Motor Logic: Using PHASE/ENABLE mode

phase LOW, ENABLE


'''
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
       
def run_test(enable, phase):
    pins = [enable, phase]            
    GPIO.output(pins, GPIO.HIGH)

     
def off(enable, phase):
    pins = [enable, phase]          

    GPIO.output(pins, GPIO.LOW)  


def pwm_on(pin, duty, start, end, step, time):

    pwm = GPIO.PWM(pin, duty)
    pwm.start(start)
    for i in range(start,end,step):
        pwm.ChangeDutyCycle(i)
        sleep(time/((end-start)/step))


def run_smoothstart(enable, phase):

    pwm_on(enable,120,50,100,5,2)

def run_backforth(enable, phase):

    run_smoothstart(enable, phase)
    #sleep(1)
    off(enable, phase)
    GPIO.output(phase, GPIO.HIGH)
    run_smoothstart(enable, phase)
    #sleep(1)
    off(enable, phase)

'''
Motor Logic: Using PHASE/ENABLE mode
phase LOW, ENABLE
phase LOW, enable HIGH (PWM) --> Forward, speed at pwm%
phase HIGH, enable HIGH (PWM) --> Reverse, speed at pwm%
'''
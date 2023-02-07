import pinout
import setupGPIO
import RPi.GPIO as GPIO
from time import sleep

setupGPIO.setup()

GPIO.output(pinout.ROT_ENABLE, GPIO.HIGH)
GPIO.output(pinout.ROT_PWM, GPIO.HIGH)
sleep(1)
GPIO.output(pinout.ROT_ENABLE, GPIO.LOW)
GPIO.output(pinout.ROT_PWM, GPIO.LOW)
import RPi.GPIO as GPIO
from tools import pinout, setup_gpio as sg # Custom file of pinout definitons
from time import sleep

sg.setup()

def buzzbeep(rep):
    for i in range(rep):
        GPIO.output(pinout.LED, GPIO.HIGH)
        GPIO.output(pinout.BUZZER, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(pinout.LED, GPIO.LOW)
        GPIO.output(pinout.BUZZER, GPIO.LOW)
        sleep(0.5)

    
buzzbeep(3)

GPIO.cleanup()

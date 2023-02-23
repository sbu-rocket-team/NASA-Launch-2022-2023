import RPi.GPIO as GPIO
from NASAcode.tools import pinout
#from NASAcode.tools import virtGPIO as GPIO

GPIO.setmode(GPIO.BOARD) # Sets pinout to BCM
GPIO.setwarnings(False)
GPIO.setup(pinout.BUZZER, GPIO.OUT)
GPIO.setup(pinout.LED, GPIO.OUT)
GPIO.setup(pinout.ROT_DIR, GPIO.OUT)
GPIO.setup(pinout.ROT_PWM, GPIO.OUT)
GPIO.setup(pinout.RP_DIR, GPIO.OUT)
GPIO.setup(pinout.RP_PWM, GPIO.OUT)
GPIO.setup(pinout.LEADSCREW_DIR, GPIO.OUT)
GPIO.setup(pinout.LEADSCREW_PWM, GPIO.OUT)

GPIO.output(pinout.BUZZER, GPIO.LOW)
GPIO.output(pinout.LED, GPIO.LOW)
GPIO.output(pinout.ROT_DIR, GPIO.LOW)
GPIO.output(pinout.ROT_PWM, GPIO.LOW)
GPIO.output(pinout.RP_DIR, GPIO.LOW)
GPIO.output(pinout.RP_PWM, GPIO.LOW)
GPIO.output(pinout.LEADSCREW_DIR, GPIO.LOW)
GPIO.output(pinout.LEADSCREW_PWM, GPIO.LOW)

GPIO.cleanup()
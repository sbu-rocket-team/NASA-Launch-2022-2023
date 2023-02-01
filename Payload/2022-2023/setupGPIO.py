import pinout
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) # Sets pinout to BCM


GPIO.setup(pinout.BUZZER, GPIO.OUT)
GPIO.setup(pinout.LED, GPIO.OUT)
GPIO.setup(pinout.ROT_ENABLE, GPIO.OUT)
GPIO.setup(pinout.ROT_PWM, GPIO.OUT)
GPIO.setup(pinout.RP_ENABLE, GPIO.OUT)
GPIO.setup(pinout.RP_PWM, GPIO.OUT)
GPIO.setup(pinout.LEADSCREW_ENABLE, GPIO.OUT)
GPIO.setup(pinout.LEADSCREW_PWM, GPIO.OUT)

GPIO.setup(ENCODER, GPIO.IN)
GPIO.setup(RP_LIM, GPIO.IN)



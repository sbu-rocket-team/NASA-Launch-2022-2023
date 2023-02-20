import pinout
import RPi.GPIO as GPIO

# Dont know if i need to initialize any SPI or I2C stuff?
# xian zai wo yo bing chilling!
def setup():
    GPIO.setmode(GPIO.BOARD) # Sets pinout to BCM
    GPIO.setwarnings(False)
    GPIO.setup(pinout.BUZZER, GPIO.OUT)
    GPIO.setup(pinout.LED, GPIO.OUT)
    GPIO.setup(pinout.ROT_ENABLE, GPIO.OUT)
    GPIO.setup(pinout.ROT_PWM, GPIO.OUT)
    GPIO.setup(pinout.ROT_PHASE, GPIO.OUT)
    GPIO.setup(pinout.RP_ENABLE, GPIO.OUT)
    GPIO.setup(pinout.RP_PWM, GPIO.OUT)
    GPIO.setup(pinout.RP_PHASE, GPIO.OUT)
    GPIO.setup(pinout.LEADSCREW_ENABLE, GPIO.OUT)
    GPIO.setup(pinout.LEADSCREW_PWM, GPIO.OUT)
    GPIO.setup(pinout.LEADSCREW_PHASE, GPIO.OUT)

    GPIO.setup(pinout.ENCODER, GPIO.IN)
    GPIO.setup(pinout.RP_LIM, GPIO.IN)

def cleanup():
    GPIO.cleanup()
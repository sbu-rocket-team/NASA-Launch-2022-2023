"""
Property Of: SBU Rocket Team

Written By: Ethan Carr
"""

# Map of all of the payload GPIO pins back to the rasp-pi. 
# Makes it a little easier to call the pins.

# THESE ARE NUMBERED ON BOARD CONFIGURATION  !! NOT BCM !!

# For MPU
I2C_SCL = 5
I2C_SDA = 3

# For Diag
BUZZER = 13
LED = 15

# These pinouts are correct, call PWM for turning on motor
# and then set DIR to high or low for direction.
# Rotation Table
ROT_PWM = 33 
ROT_DIR = 29
ENCODER = 7
ROT_LEFT = 0
ROT_RIGHT = 1

# Rack and Pinion
RP_PWM = 32
RP_DIR = 16
RP_LIM = 31
RP_UP = 0
RP_DOWN = 1

# Lead Screws
LEADSCREW_PWM = 18
LEADSCREW_DIR = 22 # HIGH is closing, LOW is opening
LEADSCREW_OPEN = 0
LEADSCREW_CLOSE = 1

# Camera (old and unused)
CAM_MOSI = 19
CAM_MISO = 21
CAM_SCLK = 23
CAM_CS = 24


# For logging stuff.

def pin2string(pin):
    if(pin == BUZZER):
        return "Buzzer"
    elif(pin == LED):
        return "LED"
    elif(pin == ROT_PWM):
        return "Camera rotation"
    elif(pin == LEADSCREW_PWM):
        return "Lead screws"
    elif(pin == RP_PWM):
        return "Rack + pinion"
    else:
        return "Unknown"

def dir2string(pin,dir):
    if(pin == ROT_PWM):
        if(dir == ROT_LEFT or dir == "L"):
            return "left"
        elif(dir == ROT_RIGHT or dir == "R"):
            return "right"
    elif(pin == LEADSCREW_PWM):
        if(dir == LEADSCREW_CLOSE):
            return "close"
        elif(dir == LEADSCREW_OPEN):
            return "open"
    elif(pin == RP_PWM):
        if(dir == RP_DOWN):
            return "down"
        elif(dir == RP_UP):
            return "up"
    else:
        return "Unknown"
    return "Unknown"
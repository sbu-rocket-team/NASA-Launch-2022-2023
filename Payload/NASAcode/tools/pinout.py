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



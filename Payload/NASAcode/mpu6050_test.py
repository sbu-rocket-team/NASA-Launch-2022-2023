# 2022-2023 Payload Software

# Testing the function of the MPU6050 3-axis gyroscope/accelerometer. 
# Code written by Jewick, edited by E.C


# IN ORDER TO RUN ON PI
# sudo apt install python3-smbus python3-pip 
# pip install mpu6050-raspberrypi numpy


from mpu6050 import mpu6050
from time import sleep #sleep([seconds]) used to pause ... arduino delay()
from tools import mpu_functions as mpuF, misc_functions as miscF, setup_gpio as sg
import numpy as np


MPU = mpu6050(0x68)
sg.setup()

i = 0
while(i < 100):
    reading = mpuF.getAccelVal()
    if abs(reading) > 10:
        miscF.beepON()
    else:
        miscF.beepOFF()

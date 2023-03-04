# 2022-2023 Payload Software

# Testing the function of the MPU6050 3-axis gyroscope/accelerometer. 
# Code written by Jewick, edited by E.C


# IN ORDER TO RUN ON PI
# sudo apt install python3-smbus python3-pip 
# pip install mpu6050-raspberrypi numpy



from time import sleep #sleep([seconds]) used to pause ... arduino delay()
from mpu6050 import mpu6050
from NASAcode.tools import mpu_functions as mpuF, misc_functions as miscF, setup_gpio as sg

sg.setup()
#MPU = mpu6050(0x68)


time_delay = 1
samplerate = 30 # hz
maxi = samplerate * time_delay
i = 0
while(i < maxi):
    reading = mpuF.getAccelVal()
    print(reading)
    if abs(reading) > 15:
        miscF.beepON()
    else:
        miscF.beepOFF()
    sleep(1/samplerate)
    i += 1

sg.cleanup()

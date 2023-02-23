
import time
from time import sleep

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)


#   Known to be working.
#
#   # Testing Camera Functions
#   from NASAcode.tools import cam_functions as camF
#   
#   camera =camF.initializeCam((2560,1440))
#   
#   fileName = "1440pTest-"+current_time+".jpeg"
#   destination = "TestImages"
#   
#   camF.takePic(camera, fileName,destination)
#   print("Image taken! Sent to " + destination + " under " + fileName)


# Testing MPU-6050
from mpu6050 import mpu6050
from NASAcode.tools import mpu_functions as mpuF, misc_functions as miscF, setup_gpio as sg

MPU = mpu6050(0x68)
sg.setup()

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

import time
from time import sleep

# Testing local time for timestamping
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print("Current time: " + current_time)

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

print("Setting up MPU")
MPU = mpu6050(0x68)
sg.setup()

time_delay = 1
samplerate = 30 # hz
maxi = samplerate * time_delay
samples = []
i = 0
while(i < maxi):
    reading = mpuF.getAccelVal()
    samples.append(reading)
    #print(reading)
    if abs(reading) > 15:
        miscF.beepON()
    else:
        miscF.beepOFF()
    sleep(1/samplerate)
    i += 1
avg = sum(samples)/(len(samples))
print("MPU readings obtained, average acceleration: " + avg + " over " + time_delay + " seconds.")

# Testing raising and lowering rack and pinion
from NASAcode.tools import motor_functions as motF
print("Testing Rack and Pinion")
motF.testRack()


# Testing the camera rotation functions
print("Testing camera rotation")
print("R-60, L-60, L-60, R-60")
from NASAcode.tools import encoder_functions as encF
encF.rotateTest()






sg.cleanup()
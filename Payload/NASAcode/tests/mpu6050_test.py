# 2022-2023 Payload Software

# Testing the function of the MPU6050 3-axis gyroscope/accelerometer. 
# Code written by Jewick, edited by E.C


# IN ORDER TO RUN ON PI
# sudo apt install python3-smbus python3-pip 
# pip install mpu6050-raspberrypi numpy



from time import sleep #sleep([seconds]) used to pause ... arduino delay()
from NASAcode.tools import mpu_functions as mpuF, misc_functions as miscF, setup_gpio as sg, txt_functions as txtF

import statistics

sg.setup()
#MPU = mpu6050(0x68)


time_delay = 1
samplerate = 30 # hz
maxi = samplerate * time_delay
samples = []
i = 0

while(i < maxi):
    reading = mpuF.getAccelVal()
    #print(reading)
    samples.append(reading)
    if abs(reading) > 15:
        miscF.beepON()
    else:
        miscF.beepOFF()
    sleep(1/samplerate)
    i += 1
avg = sum(samples)/len(samples)
standdev = statistics.stdev(samples)
print(str(avg) + ", " + str(standdev))



done = False
while(done != True):
    time_delay = 1
    samplerate = 100 # hz
    maxi = samplerate * time_delay
    samples = []
    i = 0
    while(i < maxi):
        reading = mpuF.getAccelVal()
        #print(reading)
        samples.append(reading)
        if abs(reading) > 15:
           miscF.beepON()
        else:
            miscF.beepOFF()
        sleep(1/samplerate)
        i += 1
    avg = sum(samples)/len(samples)
    standdev = statistics.stdev(samples)
    print(str(avg) + ", " + str(standdev))
    if(standdev >= 7.5):
        done = True

sg.cleanup()
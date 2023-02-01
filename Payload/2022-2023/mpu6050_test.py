# 2022-2023 Payload Software

# Testing the function of the MPU6050 3-axis gyroscope/accelerometer. 
# Code written by Jewick, edited by E.C


# IN ORDER TO RUN ON PI
# sudo apt install python3-smbus
# pip install mpu6050-raspberrypi

from mpu6050 import mpu6050
from time import sleep #sleep([seconds]) used to pause ... arduino delay()
import numpy as np


MPU = mpu6050(0x68)


def getAccelGyroMagVal():
    mpu_accel = MPU.get_accel_data()
    mpu_gyro = MPU.get_gyro_data()
    
    accelVec = np.array([mpu_accel["x"], mpu_accel["y"], mpu_accel["z"]])
    gyroVec = np.array([mpu_gyro["x"], mpu_gyro["y"], mpu_gyro["z"]])
    
    accelMag = np.linalg.norm(accelVec)
    gyroMag = np.linalg.norm(gyroVec)

    
    print(str(accelMag) + ", " + str(gyroMag))
    #sleep(5/1000)

    #print("Acceleration Vector")
    #print(accelVec)
    #print("Acceleration Mag")
    #print(accelMag)

    #print("Gyro Vector")
    #print(gyroVec)
    #print("Acceleration Vector")
    #print(gyroMag)

i = 0
while i < 100:
	getAccelGyroMagVal()
	#i = i + 1
	 
getAccelGyroMagVal()

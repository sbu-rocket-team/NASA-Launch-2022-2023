import time

import mpu6050 as imu

import numpy as np

MPU = imu.mpu6050(0x68)

#mpu stuff
"""""
MPU 6050
https://www.youtube.com/watch?v=JTFa5l7zAA4
https://github.com/m-rtijn/mpu6050
https://pypi.org/project/mpu6050-raspberrypi/
https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi

base on how itll be set up... if rocket is laying on the ground length-wise
x ... towards sky
y ... width of the rocket
z ... length of the rocket
"""

"""
DOCUMENT
"""
def getMPUTemp():
    return MPU.get_temp()

"""
Gets the magnitude of the acceleration and angular vectors.

Returns:
- accelMag [float?]: Magnitude of the acceleration vector
- gyroMag [float?]: Magnitude of the angular vector
"""
def getAccelGyroMagVal():
    mpu_accel = MPU.get_accel_data()
    mpu_gyro = MPU.get_gyro_data()

    accelVec = np.array([mpu_accel["x"], mpu_accel["y"], mpu_accel["z"]]) 
    gyroVec = np.array([mpu_gyro["x"], mpu_gyro["y"], mpu_gyro["z"]]) 
    
    accelMag = np.linalg.norm(accelVec)
    gyroMag = np.linalg.norm(gyroVec)

    return accelMag, gyroMag

"""
Gets the component velocities in 1 second intervals. Returns any combination of the three axis.

Parameters:
- xComp [Bool]: True if looking for x-component, default False
- yComp [Bool]: True if looking for y-component, default False
- zComp [Bool]: True if looking for z-component, default False

Returns:
- xVel [float?]: Average velocity in the x-direction
- yVel [float?]: Average velocity in the y-direction
- zVel [float?]: Average velocity in the z-direction
"""
def getVel(xComp = False, yComp = False, zComp = False):
    if (xComp and yComp and zComp):
        timeRef1 = time.perf_counter()
        xVal1 = MPU.get_accel_data()["x"]
        yVal1 = MPU.get_accel_data()["y"]
        zVal1 = MPU.get_accel_data()["z"]
        time.sleep(1)
        xVal2 = MPU.get_accel_data()["x"]
        yVal2 = MPU.get_accel_data()["y"]
        zVal2 = MPU.get_accel_data()["z"]
        timeRef2 = time.perf_counter()
        
        timeRefDif = timeRef2 - timeRef1
        xValDif = xVal2 - xVal1
        yValDif = yVal2 - yVal1
        zValDif = zVal2 - zVal1

        xVel = xValDif/timeRefDif
        yVel = yValDif/timeRefDif
        zVel = zValDif/timeRefDif

        return xVel, yVel, zVel
    elif (xComp and yComp):
        timeRef1 = time.perf_counter()
        xVal1 = MPU.get_accel_data()["x"]
        yVal1 = MPU.get_accel_data()["y"]
        time.sleep(1)
        xVal2 = MPU.get_accel_data()["x"]
        yVal2 = MPU.get_accel_data()["y"]
        timeRef2 = time.perf_counter()
        
        timeRefDif = timeRef2 - timeRef1
        xValDif = xVal2 - xVal1
        yValDif = yVal2 - yVal1
        
        xVel = xValDif/timeRefDif
        yVel = yValDif/timeRefDif

        return xVel, yVel
    elif (xComp and zComp):
        timeRef1 = time.perf_counter()
        xVal1 = MPU.get_accel_data()["x"]
        zVal1 = MPU.get_accel_data()["z"]
        time.sleep(1)
        xVal2 = MPU.get_accel_data()["x"]
        zVal2 = MPU.get_accel_data()["z"]
        timeRef2 = time.perf_counter()
        
        timeRefDif = timeRef2 - timeRef1
        xValDif = xVal2 - xVal1
        zValDif = zVal2 - zVal1

        xVel = xValDif/timeRefDif
        zVel = zValDif/timeRefDif

        return xVel, zVel
    elif (yComp and zComp):
        timeRef1 = time.perf_counter()
        yVal1 = MPU.get_accel_data()["y"]
        zVal1 = MPU.get_accel_data()["z"]
        time.sleep(1)
        yVal2 = MPU.get_accel_data()["y"]
        zVal2 = MPU.get_accel_data()["z"]
        timeRef2 = time.perf_counter()
        
        timeRefDif = timeRef2 - timeRef1
        yValDif = yVal2 - yVal1
        zValDif = zVal2 - zVal1

        yVel = yValDif/timeRefDif
        zVel = zValDif/timeRefDif

        return yVel, zVel
    elif (xComp):
        timeRef1 = time.perf_counter()
        xVal1 = MPU.get_accel_data()["x"]
        time.sleep(1)
        xVal2 = MPU.get_accel_data()["x"]
        timeRef2 = time.perf_counter()
        
        timeRefDif = timeRef2 - timeRef1
        xValDif = xVal2 - xVal1

        xVel = xValDif/timeRefDif

        return xVel
    elif (yComp):
        timeRef1 = time.perf_counter()
        yVal1 = MPU.get_accel_data()["y"]
        time.sleep(1)
        yVal2 = MPU.get_accel_data()["y"]
        timeRef2 = time.perf_counter()
        
        timeRefDif = timeRef2 - timeRef1
        yValDif = yVal2 - yVal1

        yVel = yValDif/timeRefDif

        return yVel
    elif (zComp):
        timeRef1 = time.perf_counter()
        zVal1 = MPU.get_accel_data()["z"]
        time.sleep(1)
        zVal2 = MPU.get_accel_data()["z"]
        timeRef2 = time.perf_counter()
        
        timeRefDif = timeRef2 - timeRef1
        zValDif = zVal2 - zVal1

        zVel = zValDif/timeRefDif

        return zVel
    else:
        return None

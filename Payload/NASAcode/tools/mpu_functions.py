"""
Property Of: SBU Rocket Team

Written By: Jewick Shi
Edited By: Ethan Carr
"""
import time
from mpu6050 import mpu6050
from NASAcode.tools import log_functions as log
import numpy as np

MPU = mpu6050(0x68)
time.sleep(1)
TARGET = "MPU-6050" # For identifying logs
log.log(0,TARGET,"MPU Initialized.")

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
    temp = MPU.get_temp()
    log.log(0,TARGET,"Measured temp: " + str(temp))
    return temp

"""
Gets the magnitude of the acceleration and angular vectors.

Returns:
- accelMag [float?]: Magnitude of the acceleration vector
- gyroMag [float?]: Magnitude of the angular vector
"""
def getAccelGyroMagVal(Acceleration=True, Gyro=True):
    mpu_accel = MPU.get_accel_data()
    mpu_gyro = MPU.get_gyro_data()

    accelVec = np.array([mpu_accel["x"], mpu_accel["y"], mpu_accel["z"]]) 
    gyroVec = np.array([mpu_gyro["x"], mpu_gyro["y"], mpu_gyro["z"]]) 
    
    accelMag = np.linalg.norm(accelVec)
    gyroMag = np.linalg.norm(gyroVec)

    if (Acceleration and Gyro):
        return accelMag, gyroMag
    elif (Acceleration):
        return accelMag
    elif (Gyro):
        return gyroMag
    else:
        return None

# what this for???
def getAccelVal():
    mpu_accel = MPU.get_accel_data()
    accelVec = np.array([mpu_accel["x"], mpu_accel["y"], mpu_accel["z"]]) 
    accelMag = np.linalg.norm(accelVec)
    return accelMag

"""
Gets the component accelerations. Returns any combination of the three axis.

Parameters:
- xComp [Bool]: True if looking for x-component, default False
- yComp [Bool]: True if looking for y-component, default False
- zComp [Bool]: True if looking for z-component, default False

Returns:
- xVel [float?]: Average acceleration in the x-direction
- yVel [float?]: Average acceleration in the y-direction
- zVel [float?]: Average acceleration in the z-direction
"""
def getAccel(xComp=True, yComp=True, zComp=True):
    accel = MPU.get_accel_data()

    if (xComp and yComp and zComp):
        return accel["x"], accel["y"], accel["z"]
    elif (xComp and yComp):
        return accel["x"], accel["y"]
    elif (xComp and zComp):
        return accel["x"], accel["z"]
    elif (yComp and zComp):
        return accel["y"], accel["z"]
    elif (xComp):
        return accel["x"]
    elif (yComp):
        return accel["y"]
    elif (zComp):
        return accel["z"]
    else:
        return None

"""
Gets the component velocities in 1 second intervals. Returns any combination of the three axis.

Parameters:
- xComp [Bool]: True if looking for x-component, default False
- yComp [Bool]: True if looking for y-component, default False
- zComp [Bool]: True if looking for z-component, default False
- dt [int]: time difference between velocities

Returns:
- xVel [float?]: Average velocity in the x-direction
- yVel [float?]: Average velocity in the y-direction
- zVel [float?]: Average velocity in the z-direction
"""
## was actually calculating jerk before ... j = da/dt
def getVel(xComp=True, yComp=True, zComp=True, dt=1):
    xVals = []
    yVals = []
    zVals = []
    timeRef1 = time.perf_counter()

    for i in range(0, dt):
        accel = MPU.get_accel_data()
        xVals[i] = accel["x"]
        yVals[i] = accel["y"]
        zVals[i] = accel["z"]
        time.sleep(0.1)
    timeRef2 = time.perf_counter()
        
    timeRefDif = timeRef2 - timeRef1
    
    xAvg = np.mean(xVals)
    yAvg = np.mean(yVals)
    zAvg = np.mean(zVals)

    xVel = xAvg * timeRefDif
    yVel = yAvg * timeRefDif
    zVel = zAvg * timeRefDif

    if (xComp and yComp and zComp):
        return xVel, yVel, zVel
    elif (xComp and yComp):
        return xVel, yVel
    elif (xComp and zComp):
        return xVel, zVel
    elif (yComp and zComp):
        return yVel, zVel
    elif (xComp):
        return xVel
    elif (yComp):
        return yVel
    elif (zComp):
        return zVel
    else:
        return None
    
def getVel2(xComp=True, yComp=True, zComp=True, dt=1):
    Ax = []
    Ay = []
    Az = []
    t = []

    accel = MPU.get_accel_data()
    t.append(time.time())
    Ax.append(accel["x"])
    Ay.append(accel["y"])
    Az.append(accel["z"])
    time.sleep(dt)
    
    accel = MPU.get_accel_data()
    t.append(time.time())
    Ax.append(accel["x"])
    Ay.append(accel["y"])
    Az.append(accel["z"])
    
    Vx = np.zeros_like(t)
    Vy = np.zeros_like(t)
    Vz = np.zeros_like(t)
    for i in range(1, len(t)):
        Vx[i] = np.trapz(Ax[:i+1], t[:i+1])
        Vy[i] = np.trapz(Ay[:i+1], t[:i+1])
        Vz[i] = np.trapz(Az[:i+1], t[:i+1])

    xVel = Vx[1]
    yVel = Vy[1]
    zVel = Vz[1]
    if (xComp and yComp and zComp):
        return xVel, yVel, zVel
    elif (xComp and yComp):
        return xVel, yVel
    elif (xComp and zComp):
        return xVel, zVel
    elif (yComp and zComp):
        return yVel, zVel
    elif (xComp):
        return xVel
    elif (yComp):
        return yVel
    elif (zComp):
        return zVel
    else:
        return None

"""
Gets the component angular change. Returns any combination of the three axis.

Parameters:
- xComp [Bool]: True if looking for x-component, default False
- yComp [Bool]: True if looking for y-component, default False
- zComp [Bool]: True if looking for z-component, default False

Returns:
- xVel [float?]: Angular change in the x-direction
- yVel [float?]: Angular change in the y-direction
- zVel [float?]: Angular change in the z-direction
"""
def getGyro(xComp=True, yComp=True, zComp=True):
    gyro = MPU.get_gyro_data()
    if (xComp and yComp and zComp):
        return gyro["x"], gyro["y"], gyro["z"]
    elif (xComp and yComp):
        return gyro["x"], gyro["y"]
    elif (xComp and zComp):
        return gyro["x"], gyro["z"]
    elif (yComp and zComp):
        return gyro["y"], gyro["z"]
    elif (xComp):
        return gyro["x"]
    elif (yComp):
        return gyro["y"]
    elif (zComp):
        return gyro["z"]
    else:
        return None
    
def mpuTest():
    log.log(0,TARGET,"Starting MPU test")
    time_delay = 1
    samplerate = 30 # hz
    maxi = samplerate * time_delay
    samples = []
    i = 0
    while(i < maxi):
        reading = getAccelVal()
        samples.append(reading)

        time.sleep(1/samplerate)
        i += 1
    avg = sum(samples)/(len(samples))
    log.log(0,TARGET,"MPU readings obtained, average acceleration: " + str(avg) + " over " + str(time_delay) + " seconds.")
    return avg

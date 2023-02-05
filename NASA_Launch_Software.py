import math
import random
import string
import sys
import time

import numpy as np
import cv2
import matplotlib.pyplot as plt

#from mpu6050 import mpu6050

callSign = "KQ4CTL"
matchingInstr = True
hasFlown = False
deployed = False
finishedTask = False

#MPU = mpu6050(0x68)
accelStart = None
gryoStart = None

#Arducam OV5642 Plus

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
Gets the magnitude of the acceleration and angular vectors.

Returns:
- accelMag [float?]: Magnitude of the acceleration vector
- gyroMag [float?]: Magnitude of the angular vector
"""

# hsaoihdoiuahd
"""
def getAccelGyroMagVal():
    mpu_accel = MPU.get_accel_data()
    mpu_gyro = MPU.get_gyro_data()

    accelVec = np.array([mpu_accel["x"], mpu_accel["y"], mpu_accel["z"]]) 
    gyroVec = np.array([mpu_gyro["x"], mpu_gyro["y"], mpu_gyro["z"]]) 
    
    accelMag = np.linalg.norm(accelVec)
    gyroMag = np.linalg.norm(gyroVec)

    return accelMag, gyroMag"""

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
# coiascjoiasd
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
"""

"""
Gets the time that passed since start of program in hr:min:sec

Parameters:
- timeStart [float]: Start time of program //from time()
- timeRef [float]: Reference time to be obtained

Returns:
- timeStr [String]: Time value in the format of "HH:MM:SS". Does not count the days.
"""
def timeElapsed(timeStart, timeRef):
    timeDif = timeRef - timeStart
    
    secs = int(timeDif) % 60
    mins = int(timeDif / 60) % 60
    hours = int(timeDif / (60*60)) % 24
    
    timeStr = str(hours).zfill(2) + ":" + str(mins).zfill(2) + ":" + str(secs).zfill(2)
    
    return timeStr

def getTransmittion():
    pass

"""
need to add in 
gets 2 instructions out of the radio signal...
6 mins record to guarntee at least 2 readings... best case 3 full proper, avg case 2 full 1 partial
"""
def getInstructionList(inString):
    tempStr = inString[:]
    tempStr = tempStr.upper()

    tempList = tempStr.rsplit(" ")

    callSignList = [i for i in tempList if len(i) > 2]

    nextCall = callSignList[callSignList.index(callSign)+1]
    
    callIndex1 = tempList.index(callSign)

    nextCallIndex1 = tempList.index(nextCall)
    listEnd = False

    if ((nextCallIndex1 < callIndex1) | (nextCallIndex1 == callIndex1)):
        nextCallIndex1 = tempList.index(nextCall, nextCallIndex1+1)
        listEnd = True

    outList1 = tempList[callIndex1+1:nextCallIndex1]
    outList1.reverse()
    
    callIndex2 = tempList.index(callSign, callIndex1+1)

    if (listEnd):
        outList2 = tempList[callIndex2+1:-1]
    else:
        nextCallIndex2 = tempList.index(nextCall, nextCallIndex1+1)

        outList2 = tempList[callIndex2+1:nextCallIndex2]

    outList2.reverse()

    return outList1, outList2

"""
need to improve maybe do 3?
# outputs the command with the most similarity
# if first 2 are the same continue to perform task
# if not the same, get signal again and compare again
"""
def compareInstructions(inList1, inList2):
    matching = True
    differences = 0
    if (len(inList1) == len(inList2)) and (len(inList1) != 0):
        for i in range(len(inList1)):
            if inList1[i].upper() != inList2[i].upper():
                matching = False
                differences += 1
    else:
        matching = False
        differences = -1

    return matching, differences

# executes base on command ... need to make commands for each case
"""
Document
"""
def executeInstructions(instructionList):
    tempList = instructionList[:]
    listLen = len(tempList)

    while listLen > 0:
        instrCase = tempList.pop()
        
        match instrCase:
            case "A1":
                # Turn 60* right
                print("apple")
            case "B2":
                # Turn 60* left
                print("banana")
            case "C3":
                # Take picture
                print("cake")
            case "D4":
                # Color to Greyscale
                print("duck")
            case "E5":
                # Greyscale to Color
                print("eel")
            case "F6":
                # Rotate 180* ... flip upside down
                print("fruit")
            case "G7":
                # Apply chosen filters
                print("gg ez")
            case "H8":
                # Remove all filters
                print("Henry VIII")

        listLen = len(tempList)

"""
Random team and instruction generator

Parameters:
- teams [int]: Number of teams, default of 1
- length [int]: Number of instructions, default of 1
- limit [int]: Types of instructions, default of 8

Return:
- Instr [String]: A string of commands with randomized teams and instructions
"""
def genRandInstr(teams = 1, length = 1, limit = 8):
    reqTeam = "KQ4CTL"
    reqUsed = False
    Instr = ""
    
    if limit > 8:
        limit = 8
    
    for i in range(teams):
        if (i != 0):
                Instr += " "

        if ((random.randint(0,teams) < int(teams/2)) or i == teams-1) and (not reqUsed):
            Instr += reqTeam
            reqUsed = True
        else:
            tempRandStr1 = ''.join(random.choices(string.ascii_uppercase, k=2))
            tempRandStr2 = ''.join(random.choices(string.ascii_uppercase, k=3))
            Instr += tempRandStr1 + "4" + tempRandStr2
        
        for j in range(length):
            tempRand = random.randint(1,limit)
            Instr += " "
            
            match tempRand:
                case 1:
                    Instr += "A1"
                case 2:
                    Instr += "B2"
                case 3:
                    Instr += "C3"
                case 4:
                    Instr += "D4"
                case 5:
                    Instr += "E5"
                case 6:
                    Instr += "F6"
                case 7:
                    Instr += "G7"
                case 8:
                    Instr += "H8"
    
    Instr = Instr + " " + Instr
    
    return Instr

"""
Creates random differences within the sequence

Parameters:
- inList [String List]: list of instructions
- chance [int]: chance (1 to 100) of change to occure per instruction, default of 10
"""
def createError(inList, chance = 10):
    for i in range(len(inList)):
        if (random.randint(1,100) <= chance):
            tempRand = random.randint(1,8)
            match tempRand:
                case 1:
                    inList[i] = "A1"
                case 2:
                    inList[i] = "B2"
                case 3:
                    inList[i] = "C3"
                case 4:
                    inList[i] = "D4"
                case 5:
                    inList[i] = "E5"
                case 6:
                    inList[i] = "F6"
                case 7:
                    inList[i] = "G7"
                case 8:
                    inList[i] = "H8"
            
            if (random.randint(1,100) <= 50):
                inList[i] = inList[i].lower()


#main tasks

#accelStart, gryoStart = getAccelGyroMagVal()
accelMag1, gryoMag1 = 9.8, 0 # m/s2, *
zVel1, zVel2= -15, -15 # m/s

while (not (hasFlown & deployed)):
    """
    TODO: condition logic
    """
    if (not hasFlown):
        if (zVel1 <= -15):
            print("sleeping")
            time.sleep(10)
            if (zVel2 <= -15):
                print("weeeeeeeeeeeeeeeeeeeeee")
                hasFlown = True
    else:
        # need get stablize ranges
        if (accelMag1 >= 8 and accelMag1 <= 10) and (gryoMag1 >= -1 and gryoMag1 <= 1):
            print("Passed Deployment")
            print()
            deployed = True

while (hasFlown and deployed and (not finishedTask)):
    instr1 = genRandInstr(5, 20)
    
    print("Random instruction strings")
    print(instr1)
    print()

    eventList1_1, eventList1_2 = getInstructionList(instr1)

    print("Instruction Lists")
    print(eventList1_1)
    print()

    tempCopy1 = eventList1_1[:]
    tempCopy2 = eventList1_1[:]
    createError(tempCopy1)
    createError(tempCopy2)
    
    print("Instruction Lists post chance")
    print(tempCopy1)
    print(tempCopy2)
    print()

    # note... does A1 == a1???
    matchingInstr1, DiffInstr1 = compareInstructions(eventList1_1, tempCopy1)
    matchingInstr2, DiffInstr2 = compareInstructions(eventList1_1, tempCopy2)
    
    print("Matching? and # differences")
    print(matchingInstr1)
    print(DiffInstr1)
    print()
    print(matchingInstr2)
    print(DiffInstr2)
    print()

    if (DiffInstr1 < DiffInstr2):
        print("first one less mistake")
        executeList = tempCopy1
    else:
        print("second one less mistake")
        executeList = tempCopy2

    print("\nExecuting Instructions...")
    executeInstructions(executeList)
    print("Passed Operation")
    finishedTask = True

    # what if record for 8 mins... get 3 readings
    # compare the 3 readings

    # either run the readings with the least differences to otheres
    # or run a combined reading, where the same instruction, picked and if completely different, pick 1 randomly
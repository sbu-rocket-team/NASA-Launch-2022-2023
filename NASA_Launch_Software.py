"""
from mpu6050 import mpu6050
from time import sleep #sleep([seconds]) used to pause ... arduino delay()

MPU = mpu6050(0x68)
"""



import math
import random
import string
import sys
import time

import numpy as np
import cv2
import matplotlib.pyplot as plt

#eventList = ["C3", "B2", "B2", "F6", "C3", "F6", "C3", "F6", "C3", "D4", "A1", "C3"]
#eventList1 = []
#eventList2 = []

callSign = "KQ4CTL"
matchingInstr = True
hasFlown = False
deployed = False
finishedTask = False

#Arducam OV5642 Plus

"""
MPU 6050
https://www.youtube.com/watch?v=JTFa5l7zAA4
https://github.com/m-rtijn/mpu6050
https://pypi.org/project/mpu6050-raspberrypi/
https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi

def getAccelGyroMagVal():
    accelVec = np.array(MPU.get_accel_data())
    gyroVec = np.array(MPU.get_gyro_data())
    
    accelMag = np.linalg.norm(accelVec)
    gyroMag = np.linalg.norm(gyroVec)

    print("Acceleration Vector")
    print(accelVec)
    print("Acceleration Mag")
    print(accelMag)

    print("Gyro Vector")
    print(gyroVec)
    print("Acceleration Vector")
    print(gyroMag)
"""
"""
Gets the time that passed since start of program

Parameters:
- timeStart: Start time of program
- timeRef: Reference time to be obtained
"""
def timeElapsed(timeStart, timeRef):
    timeDif = timeRef - timeStart
    
    secs = int(timeRef) % 60
    mins = int(timeRef / 60) % 60
    hours = int(timeRef / (60*60)) % 24
    
    timeStr = str(hours).zfill(2) + ":" + str(mins).zfill(2) + ":" + str(secs).zfill(2)
    
    return timeStr

def getTransmittion():
    pass

# XX4XXX C3 A1 D4 C3 F6 C3 F6 C3 F6 B2 B2 C3
# insert to the front of list as we go down the instruction.

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
- teams: number of teams, default of 1
- length: number of instructions, default of 1
- limit: types of instructions, default of 8
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
- inList: list of instructions
- chance: chance (1 to 100) of change to occure per instruction, default of 10
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
while (not hasFlown):
    hasFlown = True
    deployed = True
    print("Passed 1")
    print()

while (deployed and (not finishedTask)):
    instr1 = genRandInstr(1, 20)
    
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
    print("Passed 2")
    finishedTask = True

    # what if record for 8 mins... get 3 readings
    # compare the 3 readings

    # either run the readings with the least differences to otheres
    # or run a combined reading, where the same instruction, picked and if completely different, pick 1 randomly
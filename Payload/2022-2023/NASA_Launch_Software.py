"""
Group: SBU Rocket Team

Written By: Jewick Shi
Edited By: Ethan Carr
"""

import os
import time

import cv2
import matplotlib.pyplot as plt

from tools import radio_simulator as rS, instruction_functions as instF, img_functions as imgF, misc_functions as miscF, mpu_functions as mpuF


import RPi.GPIO as GPIO
#import picamera

CALLSIGN = "KQ4CTL"

matchingInstr = True
hasFlown = False
deployed = False
finishedTask = False
isGreyscale = False
isCustomFilter = False
flipPic = False

flipCounter = 0
fallVel = -5
relCamRot = 0

# arducam imx477 B0262
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Libcamera-User-Guide/
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/PiCamera2-User-Guide/

#imgFile = None
imgName = "field.jpg"
script_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(script_dir, "TestImages")
imgFile = os.path.join(img_dir, imgName)

accelStart = None
gryoStart = None

# executes base on command ... need to make commands for each case
"""
Document
"""
def executeInstructions(instructionList):
    global timeOn
    global isGreyscale
    global isCustomFilter
    global flipCounter
    global flipPic
    global imgFile
    global relCamRot

    img = None

    tempList = instructionList[:]
    listLen = len(tempList)
    timeTaken = None

    while listLen > 0:
        instrCase = tempList.pop()
        
        match instrCase:
            case "A1":
                # Turn 60* right
                relCamRot += 60
                print("A1 turn 60* right, ", end="")
            case "B2":
                # Turn 60* left
                relCamRot -= 60
                print("B2 turn 60* left, ", end="")
            case "C3":
                # Take picture, but honestly this might do everything lol
                if (relCamRot > 0):
                    #rotateCamera("R", abs(relCamRot))
                    relCamRot = 0
                elif (relCamRot < 0):
                    #rotateCamera("L", abs(relCamRot))
                    relCamRot = 0

                # imgFile = asihuidlaihdsafh
                img = cv2.imread(imgFile, cv2.IMREAD_ANYCOLOR)
                timeTaken = miscF.timeElapsed(timeOn, time.time())
                imgF.saveIMG(img, timeTaken, isGreyscale, isCustomFilter, flipPic)

                plt.figure("Test")
                plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                plt.axis("off")
                plt.show()

                # showImg()...
                print("C3 take pic, ", end="")
            case "D4":
                # Color to Greyscale
                isGreyscale = True
                isCustomFilter = False
                print("D4 to greyscale, ", end="")
            case "E5":
                # Greyscale to Color
                isGreyscale = False
                isCustomFilter = False
                print("E5 to color, ", end="")
            case "F6":
                # Rotate 180* ... flip upside down
                flipCounter += 1
                if (flipCounter % 2 == 1):
                    flipPic = True
                elif (flipCounter % 2 == 0):
                    flipPic = False

                print("F6 rotate 180*, ", end="")
            case "G7":
                # Apply chosen filters
                isCustomFilter = True
                isGreyscale = False
                print("G7 custom filter, ", end="")
            case "H8":
                # Remove all filters
                isGreyscale = False
                isCustomFilter = False
                flipPic = False # I'm assuming this is condsidered a filter?
                print("H8 remove filters, ", end="")
        
        print(str(isGreyscale) + " " + str(isCustomFilter) + " " + str(flipPic))
        listLen = len(tempList)

#main tasks
accelMag, gryoMag = 9.8, 0 # m/s2, *
zVel1, zVel2= -15, -15 # m/s

timeOn = time.time()

while (not (hasFlown & deployed)):
    """
    TODO: condition logic
    """
    if (not hasFlown):
        #zVel1 = getVel(zComp= True)
        if (zVel1 <= fallVel):
            print("waiting to see if stil falling")
            #zVel2 = getVel(zComp= True)
            time.sleep(2)
            if (zVel2 <= fallVel):
                print("weeeeeeeeeeeeeeeeeeeeee")
                hasFlown = True
    else:
        # need get stablize ranges
        #accelMag, gryoMag = getAccelGyroMagVal()
        # might need a resting variable to beeter change
        if (accelMag >= 8 and accelMag <= 10) and (gryoMag >= -1 and gryoMag <= 1):
            print("Passed Deployment \n")

            # open payload
            # lift camera
            deployed = True

while (hasFlown and deployed and (not finishedTask)):
    # get radio signal... read from txt file hopefully
    # parse signal
    # execute signal 
    # call it a day
    instr1 = rS.genRandInstr(5, 20)
    
    print("Random instruction strings")
    print(instr1)
    print()

    eventList1_1, eventList1_2 = instF.getInstructionList(instr1, CALLSIGN)

    print("Instruction Lists")
    print(eventList1_1)
    print()

    tempCopy1 = eventList1_1[:]
    tempCopy2 = eventList1_1[:]
    rS.createError(tempCopy1)
    rS.createError(tempCopy2)
    
    print("Instruction Lists post chance")
    print(tempCopy1)
    print(tempCopy2)
    print()

    # note... does A1 == a1???
    matchingInstr1, DiffInstr1 = instF.compareInstructions(eventList1_1, tempCopy1)
    matchingInstr2, DiffInstr2 = instF.compareInstructions(eventList1_1, tempCopy2)
    
    print("Matching? and # differences")
    print(matchingInstr1, DiffInstr1)
    print(matchingInstr2, DiffInstr2)

    if (DiffInstr1 < DiffInstr2):
        print("first one less mistake")
        executeList = tempCopy1
    else:
        print("second one less mistake")
        executeList = tempCopy2

    print("\nExecuting Instructions... what, grey? custom? flipped?")
    executeInstructions(executeList)
    print("\nPassed Operation")
    finishedTask = True

    # what if record for 8 mins... get 3 readings
    # compare the 3 readings

    # either run the readings with the least differences to otheres
    # or run a combined reading, where the same instruction, picked and if completely different, pick 1 randomly
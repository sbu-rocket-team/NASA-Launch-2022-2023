"""
Property Of: SBU Rocket Team

Written By: Jewick Shi
Edited By: Ethan Carr
"""

import os
import time

import cv2
import matplotlib.pyplot as plt

from tools import mpu_functions as mpuF
from tools import cam_functions as camF
from tools import motor_functions as motF
from tools import instruction_functions as instF
from tools import img_functions as imgF
from tools import misc_functions as misF
from tools import txt_functions as txtF
from tools import pinout as po

# delete these later
from tools import radio_simulator as rS
import graphImages as gI

CALLSIGN = "KQ4CTL"

matchingInstr = True
hasFlown = False
deployed = False
finishedTask = False

filterType = "N"
flipPic = False

flipCounter = 0
relCamRot = 0

FALL_VELOCITY_TH = -5
MIN_ACCEL_TH = 9
MAX_ACCEL_TH = 10
MIN_GYRO_TH = -0.5
MAX_GYRO_TH = 0.5

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVEDIMAGES_DIR = os.path.join(SCRIPT_DIR, "savedImages")
PREIMAGES_DIR = os.path.join(SCRIPT_DIR, "deployImages")
TESTIMAGES_DIR = os.path.join(SCRIPT_DIR, "TestImages")

RADIOTEXT = os.path.join(SCRIPT_DIR, "radioMessage.txt")
OUTPUTTEXT = os.path.join(SCRIPT_DIR, "outputText.txt")

imgName = ""
imgCount = 0

accelStart = None
gryoStart = None

# executes base on command ... need to make commands for each case
"""
Document
"""
def executeInstructions(instructionList, timeOn):
    #global camera
    global flipCounter
    global flipPic
    global relCamRot
    global imgCount
    global filterType
    global SAVEDIMAGES_DIR  # actual
    global OUTPUTTEXT

    global TESTIMAGES_DIR   # virtual

    tempList = instructionList[:]
    listLen = len(tempList)
    timeTaken = None

    while listLen > 0:
        instrCase = tempList.pop()
        

        if (instrCase == "A1"): # Turn 60* right
            relCamRot += 60

        elif (instrCase == "B2"): # Turn 60* left
            relCamRot -= 60

        elif(instrCase == "C3"): # Take picture, but honestly this might do everything lol
            if (relCamRot > 0):
                #rotateCamera("R", abs(relCamRot))
                pass
            elif (relCamRot < 0):
                #rotateCamera("L", abs(relCamRot))
                pass
            
            relCamRot = 0

            timeTaken = misF.timeElapsed(timeOn, time.time())
            imgName = imgF.getImgName(timeTaken, filterType, flipPic, imgCount)
                        
            camF.takePic(camera, imgName, SAVEDIMAGES_DIR)
            txtF.writeFile(OUTPUTTEXT, imgName)

            img = cv2.imread(os.path.join(SAVEDIMAGES_DIR, imgName))
            img = imgF.processIMG(img, timeTaken, filterType, flipPic)
            
            imgCount += 1

        elif(instrCase == "D4"): # Color to Greyscale
            filterType = "G"

        elif(instrCase == "E5"): # Greyscale to Color
            filterType = "N"
            print("E5 to color, ", end="")

        elif(instrCase == "F6"): # Rotate 180* ... flip upside down
            flipCounter += 1
            if (flipCounter % 2 == 1):
                flipPic = True
            elif (flipCounter % 2 == 0):
                flipPic = False

        elif(instrCase == "G7"): # Apply chosen filters
            filterType = "C"

        elif(instrCase == "H8"): # Remove all filters
            filterType = "N"
            flipPic = False # I'm assuming this is condsidered a filter?

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
        if (zVel1 <= FALL_VELOCITY_TH):
            print("waiting to see if stil falling")
            #zVel2 = getVel(zComp= True)
            time.sleep(2)
            if (zVel2 <= FALL_VELOCITY_TH):
                print("weeeeeeeeeeeeeeeeeeeeee")
                hasFlown = True
    else:
        #accelMag, gryoMag = getAccelGyroMagVal()
        if (MIN_ACCEL_TH <= accelMag <= MAX_ACCEL_TH) and (MIN_GYRO_TH <= gryoMag <= MAX_GYRO_TH):
            print("Passed Deployment \n")

            
            camera = camF.initializeCam()
            camF.takePic(camera, "preLead.jpg", PREIMAGES_DIR)

            motF.smoothStart(po.LEADSCREW_PWN, po.LEADSCREW_ENABLE, "F") #idk which
            time.sleep(5)   #need to test to determine appprox
            motF.motorOff(po.LEADSCREW_ENABLE)

            camF.takePic(camera, "postLead.jpg", PREIMAGES_DIR)

            deployImg1_Loc = os.path.join(PREIMAGES_DIR, "preLead.jpg")
            deployImg2_Loc = os.path.join(PREIMAGES_DIR, "postLead.jpg")

            opened = camF.compareImgs(deployImg1_Loc, deployImg2_Loc, imgTH)

            if (opened):
                motF.smoothStart(po.yes, po.yestoo, "F") # idk what the lift pins are and direction
                time.sleep(5)   #need to test to determine approx
                motF.motorOff(po.yestoo)

            deployed = True

txtF.createFile(OUTPUTTEXT)

while (hasFlown and deployed and (not finishedTask)):
    # get radio signal... read from txt file hopefully
    
    instr1 = txtF.readFile(RADIOTEXT)
    #KQ4CTL C3 D4 C3 G7 C3 E5 C3 F6 C3 D4 C3 G7 C3 E5 A1 C3 A1 C3 A1 C3 A1 C3 B2 C3 B2 C3 B2 C3 B2 C3 B2 C3 C3 B2 C3 B2 C3 A1 C3 A1 C3 A1 C3 A1 C3
    txtF.writeFile(OUTPUTTEXT, (instr1 + "\n"))

    eventList1_1, eventList1_2 = instF.getInstructionList(instr1, CALLSIGN)

    executeList = eventList1_1

    executeInstructions(executeList, timeOn)
    
    finishedTask = True

    timeOff = misF.timeElapsed(timeOn, time.time())
    timeOff = "Total Runtime is... " + timeOff
    txtF.writeFile(OUTPUTTEXT, timeOff)

    # what if record for 8 mins... get 3 readings
    # compare the 3 readings

    # either run the readings with the least differences to otheres
    # or run a combined reading, where the same instruction, picked and if completely different, pick 1 randomly
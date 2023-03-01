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
from tools import encoder_functions as encF
from tools import instruction_functions as instF
from tools import img_functions as imgF
from tools import misc_functions as misF
from tools import txt_functions as txtF
from tools import pinout as po

# delete these later
from tools import radio_simulator as rS

CALLSIGN = "KQ4CTL"

# General Booleans
matchingInstr = True
hasFlown = False
deployed = False
finishedTask = False

# Image Filters
imgCount = 0
filterType = "N"
flipPic = False
flipCounter = 0

# Camera rotations
relCamRot = 0

# Threshold values
IMG_BRIGHTNESS_TH = 10
FALL_VELOCITY_TH = -5
MIN_ACCEL_TH = 9
MAX_ACCEL_TH = 10
MIN_GYRO_TH = -0.5
MAX_GYRO_TH = 0.5

# File Directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVEDIMAGES_DIR = os.path.join(SCRIPT_DIR, "savedImages")
PREIMAGES_DIR = os.path.join(SCRIPT_DIR, "deployImages")
TESTIMAGES_DIR = os.path.join(SCRIPT_DIR, "TestImages")

# Timers
LEADSCREWOPEN_TIMER = 30      # need to test to determine appprox
CAMERALIFT_TIMER = 5            # need to test to determine appprox

# Direct Files
RADIOTEXT = os.path.join(SCRIPT_DIR, "radioMessage.txt")
OUTPUTTEXT = os.path.join(SCRIPT_DIR, "outputText.txt")
ACCELOUTPUT = os.path.join(SCRIPT_DIR, "AccelData.txt")
GYROOUTPUT = os.path.join(SCRIPT_DIR, "GyroData.txt")

# i forgor what these are for
accelStart = None
gryoStart = None

# executes base on command ... need to make commands for each case
"""
Document/FINISH TODO
"""
def executeInstructions(instructionList, timeOn):
    global camera
    global flipCounter
    global flipPic
    global relCamRot
    global imgCount
    global filterType
    global SAVEDIMAGES_DIR  # actual
    global OUTPUTTEXT

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
                encF.rotateCam("R", abs(relCamRot)) # idk direction
            elif (relCamRot < 0):
                encF.rotateCamera("L", abs(relCamRot))  # idk direction

            timeTaken = misF.timeElapsed(timeOn, time.time())
            imgName = imgF.getImgName(timeTaken, filterType, flipPic, imgCount)
                        
            camF.takePic(camera, imgName, SAVEDIMAGES_DIR)
            txtF.writeFile(OUTPUTTEXT, imgName)

            img = cv2.imread(os.path.join(SAVEDIMAGES_DIR, imgName))
            img = imgF.processIMG(img, timeTaken, filterType, flipPic)
            
            relCamRot = 0
            imgCount += 1

        elif(instrCase == "D4"): # Color to Greyscale
            filterType = "G"

        elif(instrCase == "E5"): # Greyscale to Color
            filterType = "N"

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

"""#main tasks
timeOn = time.time()
txtF.createFile(ACCELOUTPUT)
txtF.createFile(GYROOUTPUT)

while (not (hasFlown & deployed)):
    # TODO conditions
    if (not hasFlown):
        zVel1 = mpuF.getVel(zComp= True)
        # get velocity, acceleration, gyro... mag or comp ... with time
        if (zVel1 <= FALL_VELOCITY_TH):
            zVel2 = mpuF.getVel(zComp= True)
            time.sleep(2)
            if (zVel2 <= FALL_VELOCITY_TH):
                hasFlown = True
        time.sleep(2)
    else:
        accelMag, gryoMag = mpuF.getAccelGyroMagVal()
        if (MIN_ACCEL_TH <= accelMag <= MAX_ACCEL_TH) and (MIN_GYRO_TH <= gryoMag <= MAX_GYRO_TH):

            camera = camF.initializeCam()
            camF.takePic(camera, "preLead.jpg", PREIMAGES_DIR)

            motF.smoothStart(po.LEADSCREW_DIR, po.LEADSCREW_PWM, "F") #idk which
            time.sleep(LEADSCREWOPEN_TIMER)
            motF.motorOff(po.LEADSCREW_PWM)

            camF.takePic(camera, "postLead.jpg", PREIMAGES_DIR)

            deployImg1_Loc = os.path.join(PREIMAGES_DIR, "preLead.jpg")
            deployImg2_Loc = os.path.join(PREIMAGES_DIR, "postLead.jpg")

            opened = camF.compareImgs(deployImg1_Loc, deployImg2_Loc, IMG_BRIGHTNESS_TH)

            if (opened):
                motF.smoothStart(po.RP_DIR, po.RP_PWM, "F")  # idk what the lift pins are and direction
                time.sleep(CAMERALIFT_TIMER)
                motF.motorOff(po.RP_DIR)
                deployText = "Opening/Deployed at: " + misF.timeElapsed(timeOn, time.time()) + "\n"
            else:
                deployText = "Unopen/Deployed at: " + misF.timeElapsed(timeOn, time.time()) + "\n"

            txtF.writeFile(OUTPUTTEXT, deployText)
            deployed = True

txtF.createFile(OUTPUTTEXT)

while (hasFlown and deployed and (not finishedTask)):
    # get radio signal... read from txt file hopefully
    
    instr1 = txtF.readFile(RADIOTEXT)
    #KQ4CTL C3 D4 C3 G7 C3 E5 C3 F6 C3 D4 C3 G7 C3 E5 A1 C3 A1 C3 A1 C3 A1 C3 B2 C3 B2 C3 B2 C3 B2 C3 B2 C3 C3 B2 C3 B2 C3 A1 C3 A1 C3 A1 C3 A1 C3
    receivedText = "Command received at... " + misF.timeElapsed(timeOn, time.time()) + "\n"
    txtF.writeFile(OUTPUTTEXT, receivedText)
    txtF.writeFile(OUTPUTTEXT, (instr1 + "\n"))

    eventList1_1, eventList1_2 = instF.getInstructionList(instr1, CALLSIGN)

    executeList = eventList1_1

    executeInstructions(executeList, timeOn)
    
    finishedTask = True

    timeOff = misF.timeElapsed(timeOn, time.time())
    timeOff = "Total Runtime is... " + timeOff
    txtF.writeFile(OUTPUTTEXT, timeOff)"""

timeOn = time.time()
txtF.createFile(OUTPUTTEXT)
while (not finishedTask):
    # get radio signal... read from txt file hopefully
    
    instr1 = txtF.readFile(RADIOTEXT)
    #KQ4CTL C3 D4 C3 G7 C3 E5 C3 F6 C3 D4 C3 G7 C3 E5 A1 C3 A1 C3 A1 C3 A1 C3 B2 C3 B2 C3 B2 C3 B2 C3 B2 C3 C3 B2 C3 B2 C3 A1 C3 A1 C3 A1 C3 A1 C3
    receivedText = "Command received at... " + misF.timeElapsed(timeOn, time.time()) + "\n"
    txtF.writeFile(OUTPUTTEXT, receivedText)
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
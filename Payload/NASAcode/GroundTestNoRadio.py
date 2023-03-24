"""
Property Of: SBU Rocket Team

Written By: Jewick Shi
Edited By: Ethan Carr
"""

import os
import time

import cv2
import matplotlib.pyplot as plt

from NASAcode.tools import mpu_functions as mpuF
from NASAcode.tools import cam_functions as camF
from NASAcode.tools import motor_functions as motF
from NASAcode.tools import encoder_functions as encF
from NASAcode.tools import instruction_functions as instF
from NASAcode.tools import img_functions as imgF
from NASAcode.tools import misc_functions as misF
from NASAcode.tools import txt_functions as txtF
from NASAcode.tools import pinout as po
from NASAcode.tools import radio_functions as radF
from NASAcode.tools import log_functions as log

import statistics

CALLSIGN = "KQ4CTL"
TARGET = "GROUNDTEST"
log.blank()

# General Booleans
matchingInstr = True
hasFlown = False
deployed = False
finishedTask = False

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
    global SAVEDIMAGES_DIR
    global OUTPUTTEXT

    # Image Filters
    imgCount = 0
    filterType = "N"
    flipPic = False
    flipCounter = 0

    # Camera rotations
    relCamRot = 0
    currentDegree = 0
    
    # Image time logging
    timeTaken = None
    
    tempList = instructionList[:]
    listLen = len(tempList)

    while listLen > 0:
        instrCase = tempList.pop()

        if (instrCase == "A1"): # Turn 60* right
            relCamRot += 60

        elif (instrCase == "B2"): # Turn 60* left
            relCamRot -= 60

        elif(instrCase == "C3"): # Take picture, but honestly this might do everything lol
            if (relCamRot > 0):
                currentDegree = encF.rotateCam("R", currentDegree, abs(relCamRot))
            elif (relCamRot < 0):
                currentDegree = encF.rotateCam("L", currentDegree, abs(relCamRot))


            # Camera not connected RN
            timeTaken = time.strftime("%H-%M-%S", time.localtime())
            imgName = imgF.getImgName(str(timeTaken), filterType, flipPic, imgCount)

            camF.takePic(imgName, directory = SAVEDIMAGES_DIR)
            txtF.writeFile(OUTPUTTEXT, imgName)
            log.log(0,TARGET,"Taking photo")
            
            img = cv2.imread(os.path.join(SAVEDIMAGES_DIR, imgName))
            img = imgF.processIMG(img, str(timeTaken), filterType, flipPic)
            
            cv2.imwrite(os.path.join(SAVEDIMAGES_DIR, imgName), img)
            time.sleep(0.1)

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

timeOn = time.time()
txtF.createFile(OUTPUTTEXT)

while (not finishedTask):
    # get radio signal... read from txt file hopefully
    
    #instructions = [["A1", "C3", "A1", "C3", "A1", "C3", "A1", "C3", "A1", "C3", "A1", "C3"]]
    instructions = [["C3", "B2", "C3", "A1", "C3"]]
    instructions[0].reverse() # The .reverse() is originally from the instructions parser, but adding here in this file for easy command changes

    # Not using the radio in this one, just testing sequences of commands
    #instructions = radF.listen(5)
    #if len(instructions)==0:
    #    log.log(2,TARGET, "Zero instructions found in radio output. Exiting.")
    #    exit()

    log.log(0,TARGET, "Executing instruction list: " + str(instructions[0]))
    executeInstructions(instructions[0], timeOn) 
    
    finishedTask = True

    timeOff = misF.timeElapsed(timeOn, time.time())
    log.log(0,TARGET,"End of commands, exiting. Total runtime: " + str(timeOff))
    txtF.writeFile(OUTPUTTEXT, "Total Runtime is... " + timeOff)

"""
while (not finishedTask):
    # get radio signal... read from txt file hopefully

    motF.moveRack("U", 0.25)
    time.sleep(1)
    motF.moveRack("D", 0.25)
    
    instr1 = txtF.readFile(RADIOTEXT)
    #KQ4CTL C3 D4 C3 G7 C3 E5 C3 F6 C3 D4 C3 G7 C3 F6 E5 C3
    #KQ4CTL C3 D4 C3 G7 C3 E5 C3 F6 C3 D4 C3 G7 C3 E5 A1 C3 A1 C3 A1 C3 A1 C3 B2 C3 B2 C3 B2 C3 B2 C3 B2 C3 C3 B2 C3 B2 C3 A1 C3 A1 C3 A1 C3 A1 C3
    receivedText = "Command received at... " + misF.timeElapsed(timeOn, time.time()) + "\n"
    txtF.writeFile(OUTPUTTEXT, receivedText)
    txtF.writeFile(OUTPUTTEXT, (instr1 + "\n"))

    eventList1_1, eventList1_2 = instF.getInstructionList(instr1, CALLSIGN)

    executeList = eventList1_1

    executeInstructions(executeList, timeOn)
    
    finishedTask = True

    timeOff = misF.timeElapsed(timeOn, time.time())
    timeOff = "\nTotal Runtime is... " + timeOff
    txtF.writeFile(OUTPUTTEXT, timeOff)
"""

    # what if record for 8 mins... get 3 readings
    # compare the 3 readings

    # either run the readings with the least differences to otheres
    # or run a combined reading, where the same instruction, picked and if completely different, pick 1 randomly


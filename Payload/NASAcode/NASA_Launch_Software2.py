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

import statistics

CALLSIGN = "KQ4CTL"

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

            timeTaken = time.strftime("%H-%M-%S", time.localtime())
            imgName = imgF.getImgName(str(timeTaken), filterType, flipPic, imgCount)

            camF.takePic(imgName, directory = SAVEDIMAGES_DIR)
            txtF.writeFile(OUTPUTTEXT, imgName)

            img = cv2.imread(os.path.join(SAVEDIMAGES_DIR, imgName))
            img = imgF.processIMG(img, str(timeTaken), filterType, flipPic)

            cv2.imwrite(os.path.join(SAVEDIMAGES_DIR, imgName), img)
            
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

"""
#main tasks
timeOn = time.time()
txtF.createFile(ACCELOUTPUT)
txtF.createFile(GYROOUTPUT)

while (not (hasFlown & deployed)):
    # TODO conditions
    if (not hasFlown):
        # get velocity, acceleration, gyro... mag or comp ... with time
        if (0 > mpuF.getVel(zComp= True) >= FALL_VELOCITY_TH):
            time.sleep(2)
            if (0 > mpuF.getVel(zComp= True) >= FALL_VELOCITY_TH):
                hasFlown = True
        time.sleep(2)
    else:
        accelMag, gryoMag = mpuF.getAccelGyroMagVal()
        if (MIN_ACCEL_TH <= accelMag <= MAX_ACCEL_TH) and (MIN_GYRO_TH <= gryoMag <= MAX_GYRO_TH):

            #this section might be changed completely
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

    matching, differences = instF.compareInstructions(eventList1_1, eventList1_2)
    
    # Add in raising rack and pinion

    if (matching and (differences <= 2)):
        executeList = eventList1_1

        executeInstructions(executeList, timeOn)
    
        finishedTask = True

        timeOff = misF.timeElapsed(timeOn, time.time())
        timeOff = "\nTotal Runtime is... " + timeOff
        txtF.writeFile(OUTPUTTEXT, timeOff)"""

timeOn = time.time()
txtF.createFile(OUTPUTTEXT)

# Lil general pad delay
#time.sleep(20)


# I need to do something here to make it start the timer once 
#done = False
#while(done != True):
#    time_delay = 1
#    samplerate = 30 # hz
#    maxi = samplerate * time_delay
#    samples = []
#    i = 0
#    while(i < maxi):
#        reading = mpuF.getAccelVal()
#        samples.append(reading)
#        if abs(reading) > 15:
#           miscF.beepON()
#        else:
#            miscF.beepOFF()
#        sleep(1/samplerate)
#        i += 1
#    avg = sum(samples)/len(samples)
#    standdev = statistics.stdev(samples)
#    print(str(avg) + ", " + str(standdev))
#    if(standdev >= 7.5):
#        done = True


time.sleep(120) # Wait until the rocket's launched

motF.motorON2(dir,pwm,p.LEADSCREW_OPEN,101)
time.sleep(30)
motF.off(dir,pwm)
time.sleep(5)

while (not finishedTask):
    # get radio signal... read from txt file hopefully

    #motF.moveRack("U", 0.5)
    #camF.takePic("testicles.jpg", directory = SAVEDIMAGES_DIR)
    #motF.moveRack("D", 0.5)
    
    instr1 = txtF.readFile(RADIOTEXT)
    #KQ4CTL C3 D4 C3 G7 C3 E5 C3 F6 C3 D4 C3 G7 C3 F6 E5 C3
    #KQ4CTL C3 D4 A1 C3 G7 A1 A1 C3 A1 E5 C3 F6 C3 D4 A1 C3 G7 C3 A1 F6 E5 C3
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
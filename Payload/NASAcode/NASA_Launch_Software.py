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
from tools import instruction_functions as instF
from tools import img_functions as imgF
from tools import misc_functions as misF
from tools import txt_functions as txtF
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
MIN_FALL_VELOCITY_TH = -0.5
MAX_FALL_VELOCITY_TH = -5
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

ACCELGYROOUTPUT = os.path.join(SCRIPT_DIR, "MPUOutputData.txt")

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

        elif(instrCase == "C3"): # Take picture... also perform rotations
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
DOCUMENT
"""
def mpuInfoToSave(txtFile, duration, timeRelStart):
    readIntervals = 0.5 # seconds
    intervals = duration / readIntervals # number of intervals to read

    counter = 0
    while (counter < intervals):
        Ax, Ay, Az = mpuF.getAccel()
        Gx, Gy, Gz = mpuF.getGyro()
        mpuInfo = "%a: %a, %a, %a, %a, %a, %a" %(time.time() - timeRelStart, Ax, Ay, Az, Gx, Gy, Gz)

        txtF.writeFile(txtFile, mpuInfo)

        counter += 1
        time.sleep(readIntervals)

#
#main tasks
timeOn = time.time()
#txtF.createFile(ACCELOUTPUT)
#txtF.createFile(GYROOUTPUT)

txtF.createFile(ACCELGYROOUTPUT)

while (not (hasFlown & deployed)):
    if (not hasFlown):
        if (MIN_FALL_VELOCITY_TH > mpuF.getVel(zComp= True) >= MAX_FALL_VELOCITY_TH):
            #time.sleep(5)
            mpuInfoToSave(ACCELGYROOUTPUT, 5, timeOn)
            if (MIN_FALL_VELOCITY_TH > mpuF.getVel(zComp= True) >= MAX_FALL_VELOCITY_TH):
                hasFlown = True
                flownText = "hasFlown = True: " + misF.timeElapsed(timeOn, time.time()) + "\n"
                txtF.writeFile(OUTPUTTEXT, flownText)
        #time.sleep(2)
        mpuInfoToSave(ACCELGYROOUTPUT, 2, timeOn)
    else:
        mpuInfoToSave(ACCELGYROOUTPUT, 0.5, timeOn)
        accelMag, gryoMag = mpuF.getAccelGyroMagVal()
        if (MIN_ACCEL_TH <= accelMag <= MAX_ACCEL_TH) and (MIN_GYRO_TH <= gryoMag <= MAX_GYRO_TH):
            openText = "Opened at: " + misF.timeElapsed(timeOn, time.time()) + "\n"
            txtF.writeFile(OUTPUTTEXT, openText)
            motF.moveLeadscrew("O")

            # insert camera deployment check 
            opened = True # camera deployment check function return

            """
            checkText = "Opening check at: " + misF.timeElapsed(timeOn, time.time()) + "\n"
            txtF.writeFile(OUTPUTTEXT, openText)

            # camera check

            checkText = "Can open? " + str(opened) + "\n"
            txtF.writeFile(OUTPUTTEXT, openText)
            """

            if (opened):
                deployText = "Lifted at: " + misF.timeElapsed(timeOn, time.time()) + "\n"
                motF.moveRack("U")
            else:
                deployText = "Not lifted at: " + misF.timeElapsed(timeOn, time.time()) + "\n"

            txtF.writeFile(OUTPUTTEXT, deployText)
            deployed = True
        mpuInfoToSave(ACCELGYROOUTPUT, 4.5, timeOn)

txtF.createFile(OUTPUTTEXT)

while (hasFlown and deployed and (not finishedTask)):
    receivedText = "Recieving commands at... " + misF.timeElapsed(timeOn, time.time()) + "\n"

    # get radio signal... @Ethan add youre radio code here
    
    inStr = txtF.readFile(RADIOTEXT)
    
    #KQ4CTL C3 D4 C3 G7 C3 E5 C3 F6 C3 D4 C3 G7 C3 F6 E5 C3
    #KQ4CTL C3 D4 A1 C3 G7 A1 A1 C3 A1 E5 C3 F6 C3 D4 A1 C3 G7 C3 A1 F6 E5 C3
    #KQ4CTL C3 D4 C3 G7 C3 E5 C3 F6 C3 D4 C3 G7 C3 E5 A1 C3 A1 C3 A1 C3 A1 C3 B2 C3 B2 C3 B2 C3 B2 C3 B2 C3 C3 B2 C3 B2 C3 A1 C3 A1 C3 A1 C3 A1 C3
    
    txtF.writeFile(OUTPUTTEXT, receivedText)
    txtF.writeFile(OUTPUTTEXT, (inStr + "\n"))

    eventList1_1, eventList1_2 = instF.getInstructionList(inStr, CALLSIGN)

    matching, differences, invalid1, invalid2 = instF.compareInstructions(eventList1_1, eventList1_2)

    #if (matching and (differences <= 2)):
    if (matching):
        executeList = instF.mergeInstructions(eventList1_1, eventList1_2, invalid1, invalid2)

        executeInstructions(executeList, timeOn)
    
        finishedTask = True

        timeOff = misF.timeElapsed(timeOn, time.time())
        timeOff = "\nTotal Runtime is... " + timeOff
        txtF.writeFile(OUTPUTTEXT, timeOff)
#


"""
timeOn = time.time()
txtF.createFile(OUTPUTTEXT)

# Lil general pad delay
time.sleep(20)


# I need to do something here to make it start the timer once 
done = False
while(done != True):
    time_delay = 1
    samplerate = 100 # hz
    maxi = samplerate * time_delay
    samples = []
    i = 0
    while(i < maxi):
        reading = mpuF.getAccelVal()
        #print(reading)
        samples.append(reading)
        if abs(reading) > 15:
           misF.beepON()
        else:
            misF.beepOFF()
        time.sleep(1/samplerate)
        i += 1
    avg = sum(samples)/len(samples)
    standdev = statistics.stdev(samples)
    print(str(avg) + ", " + str(standdev))
    if(standdev >= 7.5):
        done = True


time.sleep(180) # Wait until the rocket's launched


motF.motorON2(po.LEADSCREW_DIR,po.LEADSCREW_PWM,po.LEADSCREW_OPEN,101)
time.sleep(30)
motF.off(po.LEADSCREW_DIR,po.LEADSCREW_PWM)

time.sleep(10)

while (not finishedTask):
    # get radio signal... read from txt file hopefully

    #motF.moveRack("U", 0.5)
    #camF.takePic("testicles.jpg", directory = SAVEDIMAGES_DIR)
    #motF.moveRack("D", 0.5)
    
    instr1 = txtF.readFile(RADIOTEXT)
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

"""
    # what if record for 8 mins... get 3 readings
    # compare the 3 readings

    # either run the readings with the least differences to otheres
    # or run a combined reading, where the same instruction, picked and if completely different, pick 1 randomly

while (not finishedTask):
    # get radio signal... read from txt file hopefully
    
    instr1 = txtF.readFile(RADIOTEXT)
    receivedText = "Command received at... " + misF.timeElapsed(timeOn, time.time()) + "\n"
    txtF.writeFile(OUTPUTTEXT, receivedText)
    txtF.writeFile(OUTPUTTEXT, (instr1 + "\n"))

    eventList1_1, eventList1_2 = instF.getInstructionList(instr1, CALLSIGN)

    receivedText = "The parsed instructions are ...\n"
    txtF.writeFile(OUTPUTTEXT, receivedText)
    txtF.writeFile(OUTPUTTEXT, eventList1_1[::-1], True)

    executeList = eventList1_1

    executeInstructions(executeList, timeOn)
    
    finishedTask = True

    timeOff = misF.timeElapsed(timeOn, time.time())
    timeOff = "\nTotal Runtime is... " + timeOff
    txtF.writeFile(OUTPUTTEXT, timeOff)
"""
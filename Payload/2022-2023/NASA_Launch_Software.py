"""
Group: SBU Rocket Team

Written By: Jewick Shi
Edited By: Ethan Carr
"""

import os
import time

import cv2
import matplotlib.pyplot as plt

#import RPi.GPIO as GPIO

from tools import radio_simulator as rS

#from tools import mpu_functions as mpuF
#from tools import cam_functions as camF
from tools import instruction_functions as instF
from tools import img_functions as imgF
from tools import misc_functions as miscF
from tools import txt_functions as txtF

CALLSIGN = "KQ4CTL"

matchingInstr = True
hasFlown = False
deployed = False
finishedTask = False

filterType = "N"
isGreyscale = False         # may remove
isCustomFilter = False      # may remove
flipPic = False

flipCounter = 0
fallVel = -5
relCamRot = 0

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVEDIMAGES_DIR = os.path.join(SCRIPT_DIR, "savedImages")
#SAVEDIMAGES_DIR = os.chdir ("/home/pi/[INPUT NAME HERE]")
TESTIMAGES_DIR = os.path.join(SCRIPT_DIR, "TestImages")

RADIOTEXT = os.path.join(SCRIPT_DIR, "pie.txt")
OUTPUTTEXT = os.path.join(SCRIPT_DIR, "outputText.txt")

imgName = ""
imgCount = 0

accelStart = None
gryoStart = None

# executes base on command ... need to make commands for each case
"""
Document
"""
def executeInstructions(instructionList):
    #global camera
    global timeOn
    global isGreyscale      #same
    global isCustomFilter   #same
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

                timeTaken = miscF.timeElapsed(timeOn, time.time())
                imgName = imgF.getImgName(timeTaken, filterType, flipPic, imgCount)
                #os.chdir(SAVEDIMAGES_DIR)      #actual
                #camF.takePic(camera, imgName)  #acutal
                print(imgName)
                txtF.writeFile(OUTPUTTEXT, imgName)

                img = cv2.imread(os.path.join(TESTIMAGES_DIR, "field.jpg"))     #virtual
                #img = cv2.imread(os.path.join(SAVEDIMAGES_DIR, imgName))        #actual

                img = imgF.processIMG(img, timeTaken, filterType, flipPic)
                os.chdir(SAVEDIMAGES_DIR)   #virtual
                cv2.imwrite(imgName, img)   #virtual
                
                imgCount += 1

                plt.figure("Test")
                plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                plt.axis("off")
                plt.show()

                print("C3 take pic, ", end="")
            case "D4":
                # Color to Greyscale
                #isGreyscale = True
                #isCustomFilter = False
                filterType = "G"
                print("D4 to greyscale, ", end="")
            case "E5":
                # Greyscale to Color
                #isGreyscale = False
                #isCustomFilter = False
                filterType = "N"
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
                #isCustomFilter = True
                #isGreyscale = False
                filterType = "C"
                print("G7 custom filter, ", end="")
            case "H8":
                # Remove all filters
                #isGreyscale = False
                #isCustomFilter = False
                filterType = "N"
                flipPic = False # I'm assuming this is condsidered a filter?
                print("H8 remove filters, ", end="")
        
        #print(str(isGreyscale) + " " + str(isCustomFilter) + " " + str(flipPic))
        print()
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
            
            # camera = camF.initializeCam()     # actual
            # take picture to see if opened and if not dont lift? TODO
            
            # lift camera
            deployed = True

txtF.createFile(OUTPUTTEXT)

while (hasFlown and deployed and (not finishedTask)):
    # get radio signal... read from txt file hopefully
    # parse signal
    # execute signal 
    # call it a day
    
    #instr1 = rS.genRandInstr(5, 20)
    instr1 = txtF.readFile(RADIOTEXT)
    txtF.writeFile(OUTPUTTEXT, (instr1 + "\n"))

    print("Random instruction strings")
    print(instr1)
    print()

    eventList1_1, eventList1_2 = instF.getInstructionList(instr1, CALLSIGN)

    print("Instruction Lists")
    print(eventList1_1)
    print()

    executeList = eventList1_1

    print("\nExecuting Instructions... what, grey? custom? flipped?")
    executeInstructions(executeList)
    print("\nPassed Operation")
    finishedTask = True

    # what if record for 8 mins... get 3 readings
    # compare the 3 readings

    # either run the readings with the least differences to otheres
    # or run a combined reading, where the same instruction, picked and if completely different, pick 1 randomly
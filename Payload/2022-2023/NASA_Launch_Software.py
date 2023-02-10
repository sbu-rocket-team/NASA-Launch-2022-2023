"""
Group: SBU Rocket Team

Written By: Jewick Shi
Edited By: Ethan Carr
"""

import math
import random
import string
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt

#from mpu6050 import mpu6050
#import RPi.GPIO as GPIO
#import picamera

WHITE = (255,255,255)
BLACK = (0,0,0)

TEXTFONT = cv2.FONT_HERSHEY_DUPLEX
TEXTLINE = cv2.LINE_AA

callSign = "KQ4CTL"
matchingInstr = True
hasFlown = False
deployed = False
finishedTask = False
isGreyscale = False
isCustomFilter = False
flipPic = False

flipCounter = 0
fallVel = -5
camRot = 0

#imgFile = None
imgFile = 'field.jpg'

# arducam imx477 B0262
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Libcamera-User-Guide/
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/PiCamera2-User-Guide/

#MPU = mpu6050(0x68)
accelStart = None
gryoStart = None

#mpu stuff
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
Changes the brightness and stauration of an image. The multiplier is applied before the addends.

Parameters:
- img [Array*]: Image to be filtered, color format assumed to be BGR
- lightMul [float]: Multiplicative increase of each pixel luminosity, default value of 1
                    [0,1] ... [darker, lighter]
- lightAdd [int]: Additive increase of each pixel luminosity, default value of 0
                  [0,255] ... [darker, lighter]
- lightMul [float]: Multiplicative increase of each pixel saturation, default value of 1
                    [0,1] ... [greyscale, colored]
- lightAdd [int]: Additive increase of each pixel saturation, default value of 0
                  [0,255] ... [greyscale, colored] color

Returns:
- imgfiltered [Array*]: Image filitered base on user parameter
"""
def filterLightSat(img, satMul = 1, satAdd = 0, lightMul = 1, lightAdd = 0):
  imghls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
  h, l, s = cv2.split(imghls)

  s = np.array(s.astype('float32'))
  #s = (s + satAdd) * satMul
  s = (s * satMul) + satAdd
  s = np.clip(s, 0, 255).astype('uint8')

  l = np.array(l.astype('float32'))
  #l = (l + lightAdd) * lightMul
  l = (l * lightMul) + lightAdd
  l = np.clip(l, 0, 255).astype('uint8')

  imgfiltered = cv2.cvtColor(cv2.merge([h, l, s]), cv2.COLOR_HLS2BGR)

  return imgfiltered

"""
DOCUMENT
"""
def fourFilters(img):
  imgSize = img.shape
  imgY, imgX = imgSize[0], imgSize[1]

  imgYHalf = imgY // 2
  imgXHalf = imgX // 2
  imgYQ1 = imgY // 4
  imgXQ1 = imgX // 4
  imgYQ2 = (imgY // 4) * 3
  imgXQ2 = (imgX // 4) * 3


  imgTL = img[:imgYHalf, :imgXHalf]
  imgBL = img[(imgYHalf+1):, :imgXHalf]
  imgTR = img[:imgYHalf, (imgXHalf+1):]
  imgBR = img[(imgYHalf+1):, (imgXHalf+1):]
  imgC = img[imgYQ1:imgYQ2, imgXQ1:imgXQ2]

  imgTL = filterLightSat(imgTL, satMul= 1, satAdd= 255, lightMul=2)
  imgBL = cv2.bitwise_not((filterLightSat(imgBL, satMul= 1, satAdd= 255, lightMul=2)))

  imgTR = cv2.cvtColor(cv2.cvtColor(imgTR, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
  imgBR = cv2.cvtColor(cv2.cvtColor(imgBR, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

  imgTR = filterLightSat(imgTR, satMul= 1, satAdd= 255, lightMul=2)
  imgBR = cv2.bitwise_not((filterLightSat(imgBR, satMul= 1, satAdd= 255, lightMul=2)))


  imgT = cv2.hconcat([imgTL, imgTR])
  imgB = cv2.hconcat([imgBL, imgBR])

  imgComb = cv2.vconcat([imgT, imgB])
  imgComb[imgYQ1:imgYQ2, imgXQ1:imgXQ2] = imgC
  imgComb = cv2.flip(imgComb, 0)

  return imgComb

"""
Stamps the relative time and type of filter used on the image

Parameters:
- img [Array*]: Image that will be modified
- time [String]: The time value that will be stamped
- filterText [String]: Description of filter that was used

Returns:
- imgStamp [Array*]: Image stamped with time and filter values
"""
def stampImg(img, timeStamp, filterText):
  imgSize = img.shape
  imgY, imgX = imgSize[0], imgSize[1]

  textScale = 0.5e-3 * min(imgY, imgX)
  #textThick = math.ceil(1e-3 * min(imgY, imgX))
  textThick = 1

  textBoxStart = (0, imgY)
  dateLocation = (int(0.005 * imgX), int(0.97 * imgY))
  textLocation = (int(0.005*imgX), int(0.99*imgY))

  (labelX, labelY), baseline = cv2.getTextSize(filterText, TEXTFONT, textScale, textThick)
  textBoxEnd = (int(labelX + (0.01*imgX)), int(0.95*imgY))

  cv2.rectangle(img, textBoxStart, textBoxEnd, BLACK, -1)
  cv2.putText(img, filterText, textLocation, TEXTFONT, textScale, WHITE, textThick, TEXTLINE)
  cv2.putText(img, timeStamp, dateLocation, TEXTFONT, textScale, WHITE, textThick, TEXTLINE)

  return img

"""
show image
"""
def showIMG(img, timeStamp, greyScale, custFil, flip):
    filText = ""

    if (not (greyScale or custFil)):
        filText += "No Filter "
    if (custFil and (not (greyScale and flip))):
        img = fourFilters(img)
        filText += "No Filter, Saturated/Brighten, Greyscale, Inverted, Flipped"
    elif (custFil and (not greyScale)):
        img = fourFilters(img)
        filText += "Saturated/Brighten, Greyscale, Inverted, Flipped"
    elif (custFil and (not flip)):
        img = fourFilters(img)
        filText += "No Filter, Saturated/Brighten, Greyscale, Inverted"
    if (greyScale):
        img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        filText += "Greyscale "
    if (flip):
        img = cv2.flip(img, 0)
        filText += "Flipped "
    
    img = stampImg(img, timeStamp, filText)

    plt.figure(1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()

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
    global timeOn
    global isGreyscale
    global isCustomFilter
    global flipCounter
    global flipPic
    global imgFile
    global camRot

    img = None

    tempList = instructionList[:]
    listLen = len(tempList)
    timeTaken = None

    while listLen > 0:
        instrCase = tempList.pop()
        
        match instrCase:
            case "A1":
                # Turn 60* right
                camRot += 60
                print("A1 turn 60* right," + " " + str(isGreyscale) + " " + str(isCustomFilter) + " " + str(flipPic))
            case "B2":
                # Turn 60* left
                camRot -= 60
                print("B2 turn 60* left," + " " + str(isGreyscale) + " " + str(isCustomFilter) + " " + str(flipPic))
            case "C3":
                # Take picture, but honestly this might do everything lol
                if (camRot > 0):
                    #rotateCamera("R", camRot)
                    pass
                elif (camRot < 0):
                    pass
                    #rotateCamera("L", camRot)

                # imgFile = asihuidlaihdsafh
                img = cv2.imread(imgFile, cv2.IMREAD_ANYCOLOR)
                timeTaken = timeElapsed(timeOn, time.time())
                showIMG(img, timeTaken, isGreyscale, isCustomFilter, flipPic)

                # showImg()...
                print("C3 take pic," + " " + str(isGreyscale) + " " + str(isCustomFilter) + " " + str(flipPic))
            case "D4":
                # Color to Greyscale
                isGreyscale = True
                print("D4 to greyscale," + " " + str(isGreyscale) + " " + str(isCustomFilter) + " " + str(flipPic))
            case "E5":
                # Greyscale to Color
                isGreyscale = False
                print("E5 to color," + " " + str(isGreyscale) + " " + str(isCustomFilter) + " " + str(flipPic))
            case "F6":
                # Rotate 180* ... flip upside down
                flipCounter += 1
                if (flipCounter % 2 == 1):
                    flipPic = True
                elif (flipCounter % 2 == 0):
                    flipPic = False
                print("F6 rotate 180*," + " " + str(isGreyscale) + " " + str(isCustomFilter) + " " + str(flipPic))
            case "G7":
                # Apply chosen filters
                isCustomFilter = True
                print("G7 custom filter," + " " + str(isGreyscale) + " " + str(isCustomFilter) + " " + str(flipPic))
            case "H8":
                # Remove all filters
                isGreyscale = False
                isCustomFilter = False
                flipPic = False # I'm assuming this is condsidered a filter?
                print("H8 remove filters," + " " + str(isGreyscale) + " " + str(isCustomFilter) + " " + str(flipPic))
        
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
            print("Passed Deployment")
            print()

            # open payload
            # lift camera
            deployed = True

while (hasFlown and deployed and (not finishedTask)):
    # get radio signal... read from txt file hopefully
    # parse signal
    # execute signal 
    # call it a day
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
    print("what, grey? custom? flipped?")
    executeInstructions(executeList)
    print("\nPassed Operation")
    finishedTask = True

    # what if record for 8 mins... get 3 readings
    # compare the 3 readings

    # either run the readings with the least differences to otheres
    # or run a combined reading, where the same instruction, picked and if completely different, pick 1 randomly
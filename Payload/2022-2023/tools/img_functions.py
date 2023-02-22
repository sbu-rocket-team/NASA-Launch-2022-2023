"""
Property Of: SBU Rocket Team

Written By: Jewick Shi
"""
import os
import math

import cv2
import numpy as np
import matplotlib.pyplot as plt

WHITE = (255,255,255)
BLACK = (0,0,0)

TEXTFONT = cv2.FONT_HERSHEY_DUPLEX
TEXTLINE = cv2.LINE_AA

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
Five section img filtering with a flip across the x-axis...
[Top-Left, Top-Right, Center, Bottom-Left, Bottom-Right] correlates to
[Saturated, Greyscale + Saturated, Normal, Inverted "Top-Left", Inverted "Top-Right"]

Parameter:
- img [Array*]: image to be processed
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
  imgComb = cv2.rotate(imgComb, cv2.ROTATE_90_CLOCKWISE)

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
  (labelX2, labelY2), baseline = cv2.getTextSize(timeStamp, TEXTFONT, textScale, textThick)
  if (labelX2 > labelX):
    textBoxEnd = (int(labelX2 + (0.01*imgX)), int(0.95*imgY))
  else:
    textBoxEnd = (int(labelX + (0.01*imgX)), int(0.95*imgY))

  cv2.rectangle(img, textBoxStart, textBoxEnd, BLACK, -1)
  cv2.putText(img, filterText, textLocation, TEXTFONT, textScale, WHITE, textThick, TEXTLINE)
  cv2.putText(img, timeStamp, dateLocation, TEXTFONT, textScale, WHITE, textThick, TEXTLINE)

  return img

"""
TODO: DOCUMENT


- filter : "N"ormal, "G"reyscale, "C"ustom
- inverted : 
"""
def getImgName(timeStamp, filter, inverted, count):
    imgName = ""
    imgName += timeStamp.replace(":", "")

    if (filter == "N"):
       imgName += "_normal"
    elif (filter == "G"):
       imgName += "_greyscale"
    elif (filter == "C"):
       imgName += "_custom"

    if (inverted):
       imgName += "_flipped"
    
    imgName += "_" + str(count).zfill(3) + ".jpg"

    return imgName

"""
TODO: DOCUMENT


- filter : "N"ormal, "G"reyscale, "C"ustom
- inverted : 
"""
def processIMG(img, timeStamp, filter, flip):
    filterText = ""

    if (flip):
       filterText += " flipped"
       img = cv2.flip(img, 0)

    if (filter == "N"):
        filterText = "Normal"
    elif (filter == "G"):
        filterText = "Greyscale"
        img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    elif (filter == "C"):
       filterText = "(Normal, (Saturated/Brightened, Greyscale) + Inversed) * Rotated"
       img = fourFilters(img)

    img = stampImg(img, timeStamp, filterText)

    return img

"""
DOCUMENT TODO
"""
def compareImgs(imgFile1, imgFile2, threshold):
    img1 = cv2.imread(imgFile1)
    img2 = cv2.imread(imgFile2)

    imgDif = cv2.subtract(img1, img2)
    imgDif = cv2.cvtColor(imgDif, cv2.COLOR_BGR2GRAY)

    #saideb
    #imgNorm = cv2.normalize(imgDif, cv2.NORMINF)   # choice 1 # this method might be wrong
    imgNorm = np.mean(imgDif)   # choice 2 # i think this would be better

    if (imgNorm < threshold):
        return True
    elif (imgNorm > threshold):
        return False
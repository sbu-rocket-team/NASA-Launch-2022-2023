import sys
import math
import time
import os

import cv2
import numpy as np
import matplotlib.pyplot as plt

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOw = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)

TEXTFONT = cv2.FONT_HERSHEY_DUPLEX
TEXTLINE = cv2.LINE_AA #line_4 : 2px, solid , line_aa : 3px, solid mid, blur sides ; line_8 : 1 px solid

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
def filterLightSat(img, lightMul = 1, lightAdd = 0, satMul = 1, satAdd = 0):
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
Saving Image to a uniquely named file

Parameter:
- img [Array*]: Image to be saved
- name [String]: Name of the file
- filtered [int]: Filter recognition

Output:
- Saved image file
"""
def saveImage(img, name, filtered):
  match filtered:
    case 0:
      filtered = "norm"
    case 1:
      filtered = "grey"
    case 2:
      filtered = "custom"

  name = name.replace(":", "")
  name = "img_" + name + "_" + filtered + ".jpg"
  cv2.imwrite(name, img)


def fourFilters(img, timeStamp):
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

img_ac = "ArmoredCock.jpg"
img_mc = "MC.jpg"
img_f = "field.jpg"

script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(os.path.abspath(script_dir))
img_dir = os.path.join(script_dir, "TestImages")

imgFileAC = os.path.join(img_dir, img_ac)
imgFileMC = os.path.join(img_dir, img_mc)
imgFileF = os.path.join(img_dir, img_f)

imgAC = cv2.imread(imgFileAC, cv2.IMREAD_ANYCOLOR)
imgMC = cv2.imread(imgFileMC, cv2.IMREAD_ANYCOLOR)
imgF = cv2.imread(imgFileF, cv2.IMREAD_ANYCOLOR)

#imgACG = cv2.cvtColor(cv2.cvtColor(imgAC, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
imgACG = cv2.cvtColor(cv2.imread(imgFileAC, cv2.IMREAD_GRAYSCALE), cv2.COLOR_GRAY2BGR)
imgMCG = cv2.cvtColor(cv2.imread(imgFileMC, cv2.IMREAD_GRAYSCALE), cv2.COLOR_GRAY2BGR)
imgFG = cv2.cvtColor(cv2.imread(imgFileF, cv2.IMREAD_GRAYSCALE), cv2.COLOR_GRAY2BGR)

currentTime = time.strftime("%H:%M:%S")

"""Filtering"""
imgACCust = fourFilters(imgAC, currentTime)
imgMCCust = fourFilters(imgMC, currentTime)
imgFCust = fourFilters(imgF, currentTime)

imgACGCust = fourFilters(imgACG, currentTime)
imgMCGCust = fourFilters(imgMCG, currentTime)
imgFGCust = fourFilters(imgFG, currentTime)

"""Adding Stamps"""
nothingStamp = "No Filters"
blurStamp = "Gaussian Blur (21x21, 99)"
satStamp = "Saturated/Brightened"
flipStamp = "Flipped"
CustomStamp = "Normal, Saturated/Brightened, Greyscale, Inverted, Flipped"

imgACG = stampImg(imgACG, currentTime, "Greyscale")
imgMCG = stampImg(imgMCG, currentTime, "Greyscale")
imgFG = stampImg(imgFG, currentTime, "Greyscale")

imgACCust = stampImg(imgACCust, currentTime, CustomStamp)
imgMCCust = stampImg(imgMCCust, currentTime, CustomStamp)
imgFCust = stampImg(imgFCust, currentTime, CustomStamp)

imgACGCust = stampImg(imgACGCust, currentTime, CustomStamp)
imgMCGCust = stampImg(imgMCGCust, currentTime, CustomStamp)
imgFGCust = stampImg(imgFGCust, currentTime, CustomStamp)

"""Saving img"""
#saveImage(imgAC, currentTime, 0)
#saveImage(imgACSat, currentTime, 0)

"""Displaying img"""
IMGROW = 3
IMGCOL = 3

plt.figure("Custom")
plt.subplots_adjust(left=0, right=1)
plt.subplot(1,3,1)
plt.axis("off")
plt.imshow(cv2.cvtColor(imgACCust, cv2.COLOR_BGR2RGB))
plt.subplot(1,3,2)
plt.axis("off")
plt.imshow(cv2.cvtColor(imgMCCust, cv2.COLOR_BGR2RGB))
plt.subplot(1,3,3)
plt.axis("off")
plt.imshow(cv2.cvtColor(imgFCust, cv2.COLOR_BGR2RGB))

plt.figure("Grey")
plt.subplots_adjust(left=0, right=1)
plt.subplot(1,3,1)
plt.axis("off")
plt.imshow(cv2.cvtColor(imgACG, cv2.COLOR_BGR2RGB))
plt.subplot(1,3,2)
plt.axis("off")
plt.imshow(cv2.cvtColor(imgMCG, cv2.COLOR_BGR2RGB))
plt.subplot(1,3,3)
plt.axis("off")
plt.imshow(cv2.cvtColor(imgFG, cv2.COLOR_BGR2RGB))

plt.figure("Custom Grey")
plt.subplots_adjust(left=0, right=1)
plt.subplot(1,3,1)
plt.axis("off")
plt.imshow(cv2.cvtColor(imgACGCust, cv2.COLOR_BGR2RGB))
plt.subplot(1,3,2)
plt.axis("off")
plt.imshow(cv2.cvtColor(imgMCGCust, cv2.COLOR_BGR2RGB))
plt.subplot(1,3,3)
plt.axis("off")
plt.imshow(cv2.cvtColor(imgFGCust, cv2.COLOR_BGR2RGB))

plt.show()

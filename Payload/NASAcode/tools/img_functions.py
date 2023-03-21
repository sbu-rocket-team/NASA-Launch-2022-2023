"""
Property Of: SBU Rocket Team

Written By: Jewick Shi
"""
import os
import math

import cv2
import numpy as np

from NASAcode.tools import log_functions as log

WHITE = (255,255,255)
BLACK = (0,0,0)

TEXTFONT = cv2.FONT_HERSHEY_DUPLEX
TEXTLINE = cv2.LINE_AA

TARGET = "Filters"

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
   # converts to another color space that affects brightness and saturation
   imghls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
   # splits the image
   h, l, s = cv2.split(imghls)

   # changes to a datatype with more resolution before converting back to orignal value
   s = np.array(s.astype('float32'))
   s = (s * satMul) + satAdd
   s = np.clip(s, 0, 255).astype('uint8')

   l = np.array(l.astype('float32'))
   l = (l * lightMul) + lightAdd
   l = np.clip(l, 0, 255).astype('uint8')

   # recombine split  colorspace 
   imgfiltered = cv2.cvtColor(cv2.merge([h, l, s]), cv2.COLOR_HLS2BGR)

   return imgfiltered

"""
Five section img filtering with a 90 degree CW rotation...
[Top-Left, Top-Right, Center, Bottom-Left, Bottom-Right] correlates to 
[Saturated, Greyscale + Saturated, Normal, Inverted "Top-Left", Inverted "Top-Right"]

Parameter:
- img [Array*]: image to be processed
- lightMul [float]: Multiplicative increase of each pixel luminosity, default value of 1
                    [0,1] ... [darker, lighter]
- lightAdd [int]: Additive increase of each pixel luminosity, default value of 0
                  [0,255] ... [darker, lighter]
- lightMul [float]: Multiplicative increase of each pixel saturation, default value of 1
                    [0,1] ... [greyscale, colored]
- lightAdd [int]: Additive increase of each pixel saturation, default value of 0
                  [0,255] ... [greyscale, colored] color
Returns:
- imgComb [Array*]: Image filitered base on user parameter
"""
def fourFilters(img, satMul=1, satAdd=255, lightMul=2, lightAdd=0):
   # gets the image dimensions
   imgSize = img.shape
   imgY, imgX = imgSize[0], imgSize[1]

   # gets the different points along the image
   imgYHalf = imgY // 2
   imgXHalf = imgX // 2
   imgYQ1 = imgY // 4
   imgXQ1 = imgX // 4
   imgYQ2 = (imgY // 4) * 3
   imgXQ2 = (imgX // 4) * 3

   # segmenting the image
   imgTL = img[:imgYHalf, :imgXHalf]
   imgBL = img[(imgYHalf+1):, :imgXHalf]
   imgTR = img[:imgYHalf, (imgXHalf+1):]
   imgBR = img[(imgYHalf+1):, (imgXHalf+1):]
   imgC = img[imgYQ1:imgYQ2, imgXQ1:imgXQ2]

   # applying filter to one side
   imgTL = filterLightSat(imgTL, satMul, satAdd, lightMul, lightAdd)
   imgBL = cv2.bitwise_not((filterLightSat(imgBL, satMul, satAdd, lightMul, lightAdd)))

   # applying filter to the other side as greyscale
   imgTR = cv2.cvtColor(cv2.cvtColor(imgTR, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
   imgBR = cv2.cvtColor(cv2.cvtColor(imgBR, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

   imgTR = filterLightSat(imgTR, satMul, satAdd, lightMul, lightAdd)
   imgBR = cv2.bitwise_not((filterLightSat(imgBR, satMul, satAdd, lightMul, lightAdd)))

   # combine image together
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
   # gets image dimmensions for sizing parameters
   imgSize = img.shape
   imgY, imgX = imgSize[0], imgSize[1]

   # scales the text to be more reasonably size base on image size
   textScale = 0.5e-3 * min(imgY, imgX)
   textThick = 1

   # get the location to write the text
   textBoxStart = (0, imgY)
   dateLocation = (int(0.005 * imgX), int(0.97 * imgY))
   textLocation = (int(0.005*imgX), int(0.99*imgY))

   # creates a background for the text to be shown
   (labelX, labelY), baseline = cv2.getTextSize(filterText, TEXTFONT, textScale, textThick)
   (labelX2, labelY2), baseline = cv2.getTextSize(timeStamp, TEXTFONT, textScale, textThick)
   if (labelX2 > labelX):
      textBoxEnd = (int(labelX2 + (0.01*imgX)), int(0.95*imgY))
   else:
      textBoxEnd = (int(labelX + (0.01*imgX)), int(0.95*imgY))

   # stamps the image with time and filter
   cv2.rectangle(img, textBoxStart, textBoxEnd, BLACK, -1)
   cv2.putText(img, filterText, textLocation, TEXTFONT, textScale, WHITE, textThick, TEXTLINE)
   cv2.putText(img, timeStamp, dateLocation, TEXTFONT, textScale, WHITE, textThick, TEXTLINE)

   return img


#textThick = math.ceil(1e-3 * min(imgY, imgX))
"""
TODO: DOCUMENT


- filter : "N"ormal, "G"reyscale, "C"ustom
- inverted : 
"""
def getImgName(timeStamp, filter, inverted, count):
   imgName = ""
   # adds the time to create a unique id
   imgName += timeStamp.replace(":", "")

   # adds the type of image it is
   if (filter == "N"):
      imgName += "_normal"
   elif (filter == "G"):
      imgName += "_greyscale"
   elif (filter == "C"):
      imgName += "_custom"

   # adds if it was flipped
   if (inverted):
      imgName += "_flipped"
   
   # adds the image count order, and file type
   imgName += "_" + str(count).zfill(3) + ".jpg"

   return imgName

"""
TODO: DOCUMENT


- filter : "N"ormal, "G"reyscale, "C"ustom
- inverted : 
"""
def processIMG(img, timeStamp, filter, flip=False):
   log.log(0,TARGET,"Processing image, beginning")
   filterText = ""

   # develops the filter stamp text and calls methods for specifc filters
   if (filter == "N"):
      # nothing is done
      filterText = "Normal"
   elif (filter == "G"):
      # converts to grayscale
      filterText = "Greyscale"
      img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
   elif (filter == "C"):
      # calls the custom filter
      filterText = "(Normal, (Saturated/Brightened, Greyscale) + Inversed) * Rotated"
      img = fourFilters(img)
   
   # filps the image if necessary
   if (flip):
      filterText += " & Flipped"
      img = cv2.flip(img, 0)

   # stamps the filter text and time it was taken
   img = stampImg(img, timeStamp, filterText)
   log.log(0,TARGET,"Image processed.")
   return img

"""
DOCUMENT TODO

for threshold ...
0 if same picture
+ if brighter
- if darker
"""
def compareImgs(imgFile1, imgFile2, threshold=0):
   img1 = cv2.cvtColor(cv2.imread(imgFile1), cv2.COLOR_BGR2HLS)
   img2 = cv2.cvtColor(cv2.imread(imgFile2), cv2.COLOR_BGR2HLS)

   _, l1, _ = cv2.split(img1)
   _, l2, _ = cv2.split(img2)

   l1Norm = np.mean(l1)
   l2Norm = np.mean(l2)

   print(l1Norm) # remove later
   print(l2Norm)

   imgDif = l2Norm - l1Norm

   if (imgDif >= threshold):
      return True
   elif (imgDif <= threshold):
      return False
   

def testFilters():
   import time
   current_time = time.strftime("%H:%M:%S",time.localtime())   
   log.log(0,TARGET,"Running test suite of filters.")
   img = cv2.imread(os.path.join("TestImages", "camTest.jpeg"))
   cv2.imwrite(os.path.join("TestImages", getImgName(str(current_time), "N", True, 690)), processIMG(img,current_time,"N",True))
   cv2.imwrite(os.path.join("TestImages", getImgName(str(current_time), "G", False, 691)), processIMG(img,current_time,"G"))
   cv2.imwrite(os.path.join("TestImages", getImgName(str(current_time), "C", False, 692)), processIMG(img,current_time,"C"))
   
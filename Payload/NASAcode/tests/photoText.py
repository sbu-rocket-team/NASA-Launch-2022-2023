import sys
import math
import time

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
Crates a square Guassian kernel

Parameteres:
- width [int]: Size of the kernel
- sigma [int]: Intensity of blur

Returns:
- kernel_2d [2d Array]: width by width square array with decreasing intensity value from the center
"""
def genGaussianKernel(width, sigma):
    # define your 2d kernel here
    base_kernel = np.empty((width,width))
    # Gaussian Kernel 2D (G(x,y)) = e^(-(x^2 + y^2) / 2*signma^2) / 2*pi()*sigma^2
    sigma_sqr = sigma**2
    G_coe = 1 / (2*math.pi*sigma_sqr)
    G_e_coe = 2*sigma_sqr
    center = width//2  #round down as index starts @0
    
    for i in range(width):
      for j in range (width):
        power = - ((i - center)**2 + (j - center)**2) / G_e_coe
        base_kernel[i,j] = G_coe * (math.e ** power)
        
    base_kernel_sum = np.sum(base_kernel)
    kernel_2d = base_kernel / base_kernel_sum
    return kernel_2d

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
  dateLocation = (int(0.005 * imgX), int(0.99 * imgY))
  textLocation = (int(0.005*imgX), int(0.97*imgY))

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
      filtered = "sat-lig"
    case 3:
      filtered = "grey_sat-lig"

  name = name.replace(":", "")
  name = "img_" + name + "_" + filtered + ".jpg"
  cv2.imwrite(name, img)

# cv2.bitwise_not(img) to invert img color
# cv2.flip(img, 0) to flip, [0, 1] = [x, y]-axis

img_ac = "Armored Cock.jpg"
img_mc = "MC.jpg"
img_f = "field.jpg"

imgAC = cv2.imread(img_ac, cv2.IMREAD_ANYCOLOR)
imgMC = cv2.imread(img_mc, cv2.IMREAD_ANYCOLOR)
imgF = cv2.imread(img_f, cv2.IMREAD_ANYCOLOR)

imgACG = cv2.cvtColor(cv2.imread(img_ac, cv2.IMREAD_GRAYSCALE), cv2.COLOR_GRAY2BGR)
#imgACG = cv2.cvtColor(cv2.cvtColor(imgAC, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
imgMCG = cv2.cvtColor(cv2.imread(img_mc, cv2.IMREAD_GRAYSCALE), cv2.COLOR_GRAY2BGR)
imgFG = cv2.cvtColor(cv2.imread(img_f, cv2.IMREAD_GRAYSCALE), cv2.COLOR_GRAY2BGR)

currentTime = time.strftime("%H:%M:%S")

"""Filtering"""
kernel = genGaussianKernel(21,99)

# Blur
imgACBlur = cv2.filter2D(imgAC, -1, kernel)
imgMCBlur = cv2.filter2D(imgMC, -1, kernel)
imgFBlur = cv2.filter2D(imgF, -1, kernel)

imgACGBlur = cv2.filter2D(imgACG, -1, kernel)
imgMCGBlur = cv2.filter2D(imgMCG, -1, kernel)
imgFGBlur = cv2.filter2D(imgFG, -1, kernel)

# Saturation
imgACSat = filterLightSat(imgAC, satMul= 1, satAdd= 255, lightMul=2)
imgMCSat = filterLightSat(imgMC, satMul= 1, satAdd= 255, lightMul=2)
imgFSat = filterLightSat(imgF, satMul= 1, satAdd= 255, lightMul=2)

imgACGSat = filterLightSat(imgACG, satMul= 1, satAdd= 255, lightMul=2)
imgMCGSat = filterLightSat(imgMCG, satMul= 1, satAdd= 255, lightMul=2)
imgFGSat = filterLightSat(imgFG, satMul= 1, satAdd= 255, lightMul=2)

"""Adding Stamps"""
nothingStamp = "No Filters"
blurStamp = "Gaussian Blur (21x21, 99)"
satStamp = "Saturated/Brightened"
flipStamp = "Flipped"

imgAC = stampImg(imgAC, currentTime, nothingStamp)
imgACBlur = stampImg(imgACBlur, currentTime, blurStamp)
imgACSat = stampImg(imgACSat, currentTime, satStamp)

imgACG = stampImg(imgACG, currentTime, nothingStamp)
imgACGBlur = stampImg(imgACGBlur, currentTime, blurStamp)
imgACGSat = stampImg(imgACGSat, currentTime, satStamp)

imgMC = stampImg(imgMC, currentTime, nothingStamp)
imgMCBlur = stampImg(imgMCBlur, currentTime, blurStamp)
imgMCSat = stampImg(imgMCSat, currentTime, satStamp)

imgMCG = stampImg(imgMCG, currentTime, nothingStamp)
imgMCGBlur = stampImg(imgMCGBlur, currentTime, blurStamp)
imgMCGSat = stampImg(imgMCGSat, currentTime, satStamp)

imgF = stampImg(imgF, currentTime, nothingStamp)
imgFBlur = stampImg(imgFBlur, currentTime, blurStamp)
imgFSat = stampImg(imgFSat, currentTime, satStamp)

imgFG = stampImg(imgFG, currentTime, nothingStamp)
imgFGBlur = stampImg(imgFGBlur, currentTime, blurStamp)
imgFGSat = stampImg(imgFGSat, currentTime, satStamp)

"""Saving img"""
#saveImage(imgAC, currentTime, 0)
saveImage(imgACSat, currentTime, 0)

"""Displaying img"""
IMGROW = 3
IMGCOL = 3

plt.figure(1)
plt.subplots_adjust(0, 0, 1, 1, 0, 0)
plt.subplot(IMGROW, IMGCOL, 1)
plt.imshow(cv2.cvtColor(imgAC, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 2)
plt.imshow(cv2.cvtColor(imgMC, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 3)
plt.imshow(cv2.cvtColor(imgF, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(IMGROW, IMGCOL, 4)
plt.imshow(cv2.cvtColor(imgACBlur, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 5)
plt.imshow(cv2.cvtColor(imgMCBlur, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 6)
plt.imshow(cv2.cvtColor(imgFBlur, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(IMGROW, IMGCOL, 7)
plt.imshow(cv2.cvtColor(imgACSat, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 8)
plt.imshow(cv2.cvtColor(imgMCSat, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 9)
plt.imshow(cv2.cvtColor(imgFSat, cv2.COLOR_BGR2RGB))
plt.axis("off")


plt.figure(2)
plt.subplots_adjust(0, 0, 1, 1, 0, 0)
plt.subplot(IMGROW, IMGCOL, 1)
plt.imshow(cv2.cvtColor(imgACG, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 2)
plt.imshow(cv2.cvtColor(imgMCG, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 3)
plt.imshow(cv2.cvtColor(imgFG, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(IMGROW, IMGCOL, 4)
plt.imshow(cv2.cvtColor(imgACGBlur, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 5)
plt.imshow(cv2.cvtColor(imgMCGBlur, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 6)
plt.imshow(cv2.cvtColor(imgFGBlur, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(IMGROW, IMGCOL, 7)
plt.imshow(cv2.cvtColor(imgACGSat, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 8)
plt.imshow(cv2.cvtColor(imgMCGSat, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(IMGROW, IMGCOL, 9)
plt.imshow(cv2.cvtColor(imgFGSat, cv2.COLOR_BGR2RGB))
plt.axis("off")

# for flipped and inverted images

imgACFI = cv2.flip(cv2.bitwise_not(imgAC), 0)
imgACSatFI = cv2.flip(cv2.bitwise_not(imgACSat), 0)
imgACGFI = cv2.flip(cv2.bitwise_not(imgACG), 0)
imgACSatGFI = cv2.flip(cv2.bitwise_not(imgACGSat), 0)

imgMCFI = cv2.flip(cv2.bitwise_not(imgMC), 0)
imgMCSatFI = cv2.flip(cv2.bitwise_not(imgMCSat), 0)
imgMCGFI = cv2.flip(cv2.bitwise_not(imgMCG), 0)
imgMCSatGFI = cv2.flip(cv2.bitwise_not(imgMCGSat), 0)

imgFFI = cv2.flip(cv2.bitwise_not(imgF), 0)
imgFSatFI = cv2.flip(cv2.bitwise_not(imgFSat), 0)
imgFGFI = cv2.flip(cv2.bitwise_not(imgFG), 0)
imgFSatGFI = cv2.flip(cv2.bitwise_not(imgFGSat), 0)

TR = 4
TC = 3 
# plt.subplot(TR, TC, )

plt.figure(3)
plt.subplots_adjust(0, 0, 1, 1, 0, 0)
plt.subplot(TR, TC, 1)
plt.imshow(cv2.cvtColor(imgACFI, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(TR, TC, 4)
plt.imshow(cv2.cvtColor(imgACSatFI, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(TR, TC, 7)
plt.imshow(cv2.cvtColor(imgACGFI, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(TR, TC, 10)
plt.imshow(cv2.cvtColor(imgACSatGFI, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(TR, TC, 2)
plt.imshow(cv2.cvtColor(imgMCFI, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(TR, TC, 5)
plt.imshow(cv2.cvtColor(imgMCSatFI, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(TR, TC, 8)
plt.imshow(cv2.cvtColor(imgMCGFI, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(TR, TC, 11)
plt.imshow(cv2.cvtColor(imgMCSatGFI, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(TR, TC, 3)
plt.imshow(cv2.cvtColor(imgFFI, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(TR, TC, 6)
plt.imshow(cv2.cvtColor(imgFSatFI, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(TR, TC, 9)
plt.imshow(cv2.cvtColor(imgFGFI, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(TR, TC, 12)
plt.imshow(cv2.cvtColor(imgFSatGFI, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.show()
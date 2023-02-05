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
Changes the brightness and stauration of an image

Parameters:
- img [Array*]: Image to be filtered, color format assumed to be BGR
- lightMul [float]: Multiplicative increase of each pixel luminosity, default value of 1
                    [0,1] ... [darker, lighter], primary
- lightAdd [int]: Additive increase of each pixel luminosity, default value of 0
                  [0,255] ... [darker, lighter], secondary
- lightMul [float]: Multiplicative increase of each pixel saturation, default value of 1
                    [0,1] ... [greyscale, colored], primary
- lightAdd [int]: Additive increase of each pixel saturation, default value of 0
                  [0,255] ... [greyscale, colored] color, secondary

Returns:
- imgfiltered [Array*]: Image filitered base on user parameter
"""
def filterLightSat(img, lightMul = 1, lightAdd = 0, satMul = 1, satAdd = 0):
  imghls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
  h, l, s = cv2.split(imghls)

  s = np.array(s.astype('float32'))
  s = (s + satAdd) * satMul
  s = np.clip(s, 0, 255).astype('uint8')

  l = np.array(l.astype('float32'))
  l = (l + lightAdd) * lightMul
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
- filtered [String]: Filter recognition

Output:
- Saved image file
"""
def saveImage(img, name, filtered):
  name = name.replace(":", "")
  name = name + "_" + filtered + ".jpg"
  cv2.imwrite(name, img)

img_ac = "Armored Cock.jpg"
img_mc = "MC.jpg"
#img = ".jpg"

imgAC = cv2.imread(img_ac, cv2.IMREAD_ANYCOLOR)
imgMC = cv2.imread(img_mc, cv2.IMREAD_ANYCOLOR)
#img = cv2.imread(img, cv2.IMREAD_ANYCOLOR)

#currentDateTime = time.ctime()
currentTime = time.strftime("%H:%M:%S")

"""Filtering"""
kernel = genGaussianKernel(11,3)

# Blur
imgACBlur = cv2.filter2D(imgAC, -1, kernel)
imgMCBlur = cv2.filter2D(imgMC, -1, kernel)

# Saturation
imgACSat = filterLightSat(imgAC, lightMul= 1, lightAdd= 128, satMul= 1, satAdd= 255)
imgMCSat = filterLightSat(imgMC, lightMul= 1, lightAdd= 128, satMul= 1, satAdd= 255)

"""Adding Stamps"""
nothingStamp = "No Filters"
blurStamp = "Gaussian Blur (11x11, 3)"
satStamp = "Saturated/Brightened"

imgAC = stampImg(imgAC, currentTime, nothingStamp)
imgACBlur = stampImg(imgACBlur, currentTime, blurStamp)
imgACSat = stampImg(imgACSat, currentTime, satStamp)

imgMC = stampImg(imgMC, currentTime, nothingStamp)
imgMCBlur = stampImg(imgMCBlur, currentTime, blurStamp)
imgMCSat = stampImg(imgMCSat, currentTime, satStamp)

"""Saving img"""
#saveImage(imgAC, currentTime, "Plain")
#saveImage(imgACBlur, currentTime, "Blurred")

"""Displaying img"""
plt.figure(1)
plt.subplots_adjust(0, 0, 1, 1, 0, 0)
plt.subplot(1,2,1)
plt.imshow(cv2.cvtColor(imgAC, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(1,2,2)
plt.imshow(cv2.cvtColor(imgMC, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.suptitle("Normal")

plt.figure(2)
plt.subplots_adjust(0, 0, 1, 1, 0, 0)
plt.subplot(1,2,1)
plt.imshow(cv2.cvtColor(imgACBlur, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(1,2,2)
plt.imshow(cv2.cvtColor(imgMCBlur, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.suptitle("Blurred")

plt.figure(3)
plt.subplots_adjust(0, 0, 1, 1, 0, 0)
plt.subplot(1,2,1)
plt.imshow(cv2.cvtColor(imgACSat, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.subplot(1,2,2)
plt.imshow(cv2.cvtColor(imgMCSat, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.suptitle("Saturated")

plt.show()
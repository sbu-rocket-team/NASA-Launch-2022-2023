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

def editImg(imgFile, filtered = False):
  img = cv2.imread(imgFile, cv2.IMREAD_ANYCOLOR)

  height, width, depth = img.shape

  pass

kernel = genGaussianKernel(11,3)

img_ac = "Armored Cock.jpg"
img_mc = "MC.jpg"

#img = cv2.imread(img_ac, cv2.IMREAD_GRAYSCALE)
img = cv2.imread(img_mc, cv2.IMREAD_ANYCOLOR)

img_y, img_x, img_c = img.shape

textFont = cv2.FONT_HERSHEY_DUPLEX
textScale = 0.5e-3 * min(img_y, img_x)
#textThick = math.ceil(1e-3 * min(img_y, img_x))
textThick = 1
textLine = cv2.LINE_AA #line_4 : 2px, solid , line_aa : 3px, solid mid, blur sides ; line_8 : 1 px solid

recStart = (0, img_y)

"""Normal"""
#currentDateTime = time.ctime()
currentTime = time.strftime("%H:%M:%S")

dateLoc = (int(0.005*img_x), int(0.99*img_y))
recDateEnd = (int(0.05*img_x), int(0.97*img_y))

cv2.rectangle(img, recStart, recDateEnd, BLACK, -1)
cv2.putText(img, currentTime, dateLoc, textFont, textScale, WHITE, textThick, textLine)

"""Filter: Gaussian Blur"""
kernel = genGaussianKernel(11,3)

imgBlur = cv2.filter2D(img, -1, kernel)

filterText = "Gaussian Blur (11x11, 3)"
filterLoc = (int(0.005*img_x), int(0.97*img_y))
#recFilterEnd = (int(0.13*img_x), int(0.95*img_y))

(label_width, label_height), baseline = cv2.getTextSize(filterText, textFont, textScale, textThick)
print(label_height)
print(label_width)

recFilterEnd = (int(label_width + (0.01*img_x)), int(0.95*img_y))

cv2.rectangle(imgBlur, recStart, recFilterEnd, BLACK, -1)
cv2.putText(imgBlur, filterText, filterLoc, textFont, textScale, WHITE, textThick, textLine)
cv2.putText(imgBlur, currentTime, dateLoc, textFont, textScale, WHITE, textThick, textLine)

"""Saving img"""
newName = "testing.jpg"
cv2.imwrite(newName, img)

"""Displaying img"""
plt.figure(1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Normal")

plt.figure(2)
plt.imshow(cv2.cvtColor(imgBlur, cv2.COLOR_BGR2RGB))
plt.title("Blurred")
plt.axis("off")
plt.show()
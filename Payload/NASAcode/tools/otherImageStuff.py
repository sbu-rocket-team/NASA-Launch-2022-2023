import os
import math

import numpy as np
import matplotlib.pyplot as plt
import cv2

import img_functions as imgF

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR) # Up one directory

#SAVEDIMAGES_DIR = os.path.join(SCRIPT_DIR, "savedImages")
SAVEDIMAGES_DIR = os.path.join(PARENT_DIR, "savedImages")
TESTIMAGES_DIR = os.path.join(PARENT_DIR, "TestImages")

"""
DOCUMENT TODO
"""
def showImages(folderDir, join):
   if (join):
      numImg = 0
      imgIndex = 1

      for images in os.listdir(folderDir):
         if (images.endswith(".jpg")):
            numImg += 1
      
      plotSize = math.ceil(numImg**0.5)
   
      plt.figure("Show images")

      for images in os.listdir(folderDir):
         if (images.endswith(".jpg")):
            plt.subplot(plotSize, plotSize, imgIndex)
            img = cv2.imread(os.path.join(SAVEDIMAGES_DIR, images))
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.axis("off")
            imgIndex += 1

   else:
      imgIndex = 1
      for images in os.listdir(folderDir):
         if (images.endswith(".jpg")):
            plt.figure(imgIndex)
            img = cv2.imread(os.path.join(SAVEDIMAGES_DIR, images))
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.axis("off")
            imgIndex += 1
   
   plt.show()


    
showImages(SAVEDIMAGES_DIR, False)

imgN = os.path.join(TESTIMAGES_DIR, "field.jpg")
imgD = os.path.join(TESTIMAGES_DIR, "fieldBlack.jpg")
imgB = os.path.join(TESTIMAGES_DIR, "fieldBrightest.jpg")

# threshold for 30? ... need testing
#ans = imgF.compareImgs(imgD, imgN)

#print(ans)
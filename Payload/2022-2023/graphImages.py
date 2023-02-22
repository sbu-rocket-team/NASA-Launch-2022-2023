import os
import math

import matplotlib.pyplot as plt
import cv2

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVEDIMAGES_DIR = os.path.join(SCRIPT_DIR, "savedImages")

"""
DOCUMENT TODO
"""
def showImages(folderDir):
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
        
   plt.show()
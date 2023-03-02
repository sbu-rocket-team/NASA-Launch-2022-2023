import os
import math

import numpy as np
import matplotlib.pyplot as plt
import cv2

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR) # Up one directory

TESTIMAGES_DIR = os.path.join(PARENT_DIR, "TestImages")

THRESH = 127
OPENTHRESH_LENGTH = 192

imgC = cv2.imread(os.path.join(TESTIMAGES_DIR, "fieldC.jpg"))
imgPC = cv2.imread(os.path.join(TESTIMAGES_DIR, "fieldPC.jpg"))
imgPO = cv2.imread(os.path.join(TESTIMAGES_DIR, "fieldPO.jpg"))
imgO = cv2.imread(os.path.join(TESTIMAGES_DIR, "fieldO.jpg"))

imgC_hls = cv2.cvtColor(imgC, cv2.COLOR_BGR2HLS)
imgPC_hls = cv2.cvtColor(imgPC, cv2.COLOR_BGR2HLS)
imgPO_hls = cv2.cvtColor(imgPO, cv2.COLOR_BGR2HLS)
imgO_hls = cv2.cvtColor(imgO, cv2.COLOR_BGR2HLS) # 1065

_, lC, _ = cv2.split(imgC_hls)
_, lPC, _ = cv2.split(imgPC_hls)
_, lPO, _ = cv2.split(imgPO_hls)
_, lO, _ = cv2.split(imgO_hls)

_, tC = cv2.threshold(lC, THRESH, 255, cv2.THRESH_BINARY)
_, tPC = cv2.threshold(lPC, THRESH, 255, cv2.THRESH_BINARY)
_, tPO = cv2.threshold(lPO, THRESH, 255, cv2.THRESH_BINARY)
_, tO = cv2.threshold(lO, THRESH, 255, cv2.THRESH_BINARY)

mC = cv2.mean(tC)
mPC = cv2.mean(tPC)
mPO = cv2.mean(tPO)
mO = cv2.mean(tO)

"""
h, w = np.shape(tO)

pm = True
pL = w

front = 1
half = w // 2
back = w

pThresh = 0.5

while (pm):
    print("start")
    print(front)
    print(half)
    print(back)
    print("pixel length")
    print(pL)

    imgLS = tO[:, front:half]
    imgRS = tO[:, half:back]
    
    pLS = np.linalg.norm(cv2.mean(imgLS))
    pRS = np.linalg.norm(cv2.mean(imgRS))
    
    print("norms")
    print("left", pLS)
    print("right", pRS)

    plt.figure("Left")
    plt.imshow(imgLS)
    plt.axis("off")

    plt.figure("Right")
    plt.imshow(imgRS)
    plt.axis("off")

    plt.show()

    if (pLS < pRS):
        if (pLS <= pThresh):
            pm = False
            break

        temp = half
        half = (front + half) // 2
        back = temp

        pL = temp

    elif (pRS < pLS):
        if (pRS <= pThresh):
            pm = False
            break

        temp = half
        half = (half + back) // 2
        front = temp

        pL = temp

    if (front == back):
        pm = False
        print("finalized:")
        print(front)
        print(half)
        print(back)
    
    print("pixel length")
    print(pL)
    print()
    """

def binaryOpeningSearch(img, start, middle, end, pThresh = 0.5):
    front = start
    half = middle
    back = end

    imgLS = img[:, front:half]
    imgRS = img[:, half:back]
    
    pLS = np.linalg.norm(cv2.mean(imgLS))
    pRS = np.linalg.norm(cv2.mean(imgRS))

    print("norms, left, right")
    print(pLS, pRS)

    plt.figure(1)
    plt.imshow(imgLS)
    plt.axis("off")

    plt.figure(2)
    plt.imshow(imgRS)
    plt.axis("off")

    plt.show()

    if ((front == back) or (pRS == pLS) or (abs(front - back) == 2)):
        if (pRS < pLS):
            return end
        else:
            return start
    
    if (pLS < pRS):
        if (pLS <= pThresh):
            front = half
            half = (half + back) // 2
            
            return binaryOpeningSearch(img, front, half, back)
        
        back = half
        half = (front + half) // 2

        return binaryOpeningSearch(img, front, half, back)

    elif (pRS < pLS):
        if (pRS <= pThresh):
            back = half
            half = (front + half) // 2

            return binaryOpeningSearch(img, front, half, back)

        front = half
        half = (half + back) // 2

        return binaryOpeningSearch(img, front, half, back)

a = tPC
_, w = np.shape(a)
a = binaryOpeningSearch(a, 1, w // 2, w)
print(a)

row = 4
col = 3

plt.figure(1)
plt.subplot(row, col, 1)
plt.imshow(cv2.cvtColor(imgC, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.subplot(row, col, 2)
plt.imshow(cv2.cvtColor(lC, cv2.COLOR_GRAY2RGB))
plt.axis('off')
plt.subplot(row, col, 3)
plt.imshow(cv2.cvtColor(tC, cv2.COLOR_GRAY2RGB))
plt.axis('off')

plt.subplot(row, col, 4)
plt.imshow(cv2.cvtColor(imgPC, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.subplot(row, col, 5)
plt.imshow(cv2.cvtColor(lPC, cv2.COLOR_GRAY2RGB))
plt.axis('off')
plt.subplot(row, col, 6)
plt.imshow(cv2.cvtColor(tPC, cv2.COLOR_GRAY2RGB))
plt.axis('off')

plt.subplot(row, col, 7)
plt.imshow(cv2.cvtColor(imgPO, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.subplot(row, col, 8)
plt.imshow(cv2.cvtColor(lPO, cv2.COLOR_GRAY2RGB))
plt.axis('off')
plt.subplot(row, col, 9)
plt.imshow(cv2.cvtColor(tPO, cv2.COLOR_GRAY2RGB))
plt.axis('off')

plt.subplot(row, col, 10)
plt.imshow(cv2.cvtColor(imgO, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.subplot(row, col, 11)
plt.imshow(cv2.cvtColor(lO, cv2.COLOR_GRAY2RGB))
plt.axis('off')
plt.subplot(row, col, 12)
plt.imshow(cv2.cvtColor(tO, cv2.COLOR_GRAY2RGB))
plt.axis('off')

#plt.show()

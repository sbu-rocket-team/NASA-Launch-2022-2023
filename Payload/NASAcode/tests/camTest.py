import time
import os

import matplotlib as plt
import cv2

from picamera2 import Picamera2 as pc2
#import libcamera as lc

def camIntConf(camRes = (1920, 1080)):
    pcam = pc2()
    pcam_config = pcam.create_still_configuration(main={"size": camRes})
    pcam.configure(pcam_config)
    return pcam

def captureImg(camera, imgName = "image.jpg"):
    # chances that these two might need to be moved to captureImg()         (your chances were correct)
    camera.start()
    time.sleep(2)  #bare min of 2 sec to allow camera to be properly set up
    camera.capture_file(imgName)
    camera.stop()
    #ime.sleep(2) # Dont really need a delay here ya?

IMGNAME = 'imgEdit.jpg'

flipPic = False
imgFile = "test-1.jpg"
picRes = (1920, 1080)

piCam = camIntConf()
#pcam.set_controls({"AfMode": lc.controls.AfModeEnum.Continuous}) # is autofocus needed ... 
captureImg(piCam)
print("Capped!")
time.sleep(10)
captureImg(piCam, "image2.jpg")


# fiosadoiasdhf
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(os.path.abspath(script_dir))
img_dir = os.path.join(script_dir, "TestImages")

imgFileAC = os.path.join(img_dir, IMGNAME)
import time
import os

import matplotlib as plt
import cv2

import picamera2 as pc2
#import libcamera as lc

def camIntConf(camRes = (1920, 1080)):
    pcam = pc2.Picamera2.Picamera2()
    pcam_config = pc2.create_still_configuration(main={"size": camRes})
    pcam.configure(pcam_config)
    # chances that these two might need to be moved to captureImg()
    pcam.start()
    time.sleep(2) #bare min of 2 sec to allow camera to be properly set up

    return pcam

def captureImg(camera, imgName = "image.jpg"):
    camera.capture_file(imgName)
    camera.stop()

IMGNAME = 'imgEdit.jpg'

flipPic = False
imgFile = "test.jpg"
picRes = (1920, 1080)

piCam = camIntConf()
#pcam.set_controls({"AfMode": lc.controls.AfModeEnum.Continuous}) # is autofocus needed ... 
captureImg(piCam)

#time.sleep(10)
#captureImg(piCam)


# fiosadoiasdhf
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(os.path.abspath(script_dir))
img_dir = os.path.join(script_dir, "TestImages")

imgFileAC = os.path.join(img_dir, IMGNAME)
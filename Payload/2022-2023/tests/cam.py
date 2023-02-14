import time
import os

import matplotlib as plt
import cv2

import Picamera2 as pc2
import libcamera as lc

IMGNAME = 'imgEdit.jpg'
flipPic = False

imgFile = "test.jpg"

pcam = pc2.Picamera2()
pcam_config = Picamera2.still_configuration(main={"size": (1920, 1080)})
pcam.configure(pcam_config)
pcam.set_controls({"AfMode": lc.controls.AfModeEnum.Continuous}) # is autofocus needed ... 
pcam.start()
time.sleep(2) #bare min of 2 sec
pcam.capture_file(imgFile)
pcam.close()

# fiosadoiasdhf
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(os.path.abspath(script_dir))
img_dir = os.path.join(script_dir, "TestImages")

imgFileAC = os.path.join(img_dir, IMGNAME)
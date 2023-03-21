import time
import os
import shutil as mv

from picamera2 import Picamera2 as pc2
from NASAcode.tools import log_functions as log
# arducam imx477 B0262
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Libcamera-User-Guide/
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/PiCamera2-User-Guide/
# https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf    < Appendix B, Configuration parameters.

TARGET = "Camera"

def takePic(imgName, res = (1920,1080), directory = os.path.dirname(os.path.abspath(__file__))):
    log.log(0,TARGET,"Preparing to take a picture")
    pcam = pc2()
    pcam_config = pcam.create_still_configuration(main={"size": res})
    pcam.configure(pcam_config)
    time.sleep(2)
    log.log(0,TARGET,"Camera configured")

    pcam.start()
    time.sleep(1)
    log.log(0,TARGET,"Camera Started.")
    os.chdir(directory)
    pcam.capture_file(imgName)
    pcam.close() # Needs to close as stills configuration only allows one frame buffer allocated
    log.log(0,TARGET,"Image Captured, "+imgName+", in "+directory)

def camTest():

    fileName = "camTest.jpeg"
    destination = "TestImages"

    takePic(fileName,(2560,1440),destination)
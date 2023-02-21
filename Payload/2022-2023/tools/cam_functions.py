import time
import os

from picamera2 import Picamera2 as pc2

# arducam imx477 B0262
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Libcamera-User-Guide/
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/PiCamera2-User-Guide/

def initializeCam():
    pcam = pc2()
    pcam_config = pcam.create_still_configuration(main={"size": (1920, 1080)})
    pcam.configure(pcam_config)
    pcam.start()
    time.sleep(2)
    return pcam

def takePic(camera, imgName):
    camera.capture_file(imgName)
    camera.close()
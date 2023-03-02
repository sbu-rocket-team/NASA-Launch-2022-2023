import time
import os
import shutil as mv

from picamera2 import Picamera2 as pc2

# arducam imx477 B0262
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Libcamera-User-Guide/
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/PiCamera2-User-Guide/
# https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf    < Appendix B, Configuration parameters.

pcam = 0

def initializeCam(res = (1920,1080)):
    global pcam
    pcam = pc2()
    pcam_config = pcam.create_still_configuration(main={"size": res})
    pcam.configure(pcam_config)
    time.sleep(2)
    return pcam

def takePic(imgName, directory = os.path.dirname(os.path.abspath(__file__))):
    pcam.start()
    time.sleep(1)
    os.chdir(directory)
    pcam.capture_file(imgName)
    pcam.close() # Needs to close as stills configuration only allows one frame buffer allocated

def clear():
    global pcam
    pcam = 0
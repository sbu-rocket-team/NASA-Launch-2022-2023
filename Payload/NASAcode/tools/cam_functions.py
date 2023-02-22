import time
import os
import shutil as mv

from picamera2 import Picamera2 as pc2

# arducam imx477 B0262
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Libcamera-User-Guide/
# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/PiCamera2-User-Guide/
# https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf    < Appendix B, Configuration parameters.

def initializeCam(res = (1920,1080)):
    pcam = pc2()
    pcam_config = pcam.create_still_configuration(main={"size": res})
    pcam.configure(pcam_config)
    return pcam

def takePic(camera, imgName,destination=""):
    camera.start()
    time.sleep(2)
    camera.capture_file(imgName)
    if(destination!=""):
        mv.move("./"+imgName,"./NASAcode/"+str(destination))
        time.sleep(0.01) # Need to move the files.
    camera.close() # Needs to close as stills configuration only allows one frame buffer allocated

import time

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)


#   Known to be working.
#
#   # Testing Camera Functions
#   from NASAcode.tools import cam_functions as camF
#   
#   camera =camF.initializeCam((2560,1440))
#   
#   fileName = "1440pTest-"+current_time+".jpeg"
#   destination = "TestImages"
#   
#   camF.takePic(camera, fileName,destination)
#   print("Image taken! Sent to " + destination + " under " + fileName)


# Testing MPU-6050
from NASAcode.tools import mpu_functions as mpuF




# Setting up GPIO and logs stuffs
from NASAcode.tools import setup_gpio as sg, log_functions as log
print("Setting up GPIO Pinouts")
TARGET = "TEST"
sg.setup()



# Testing local time for timestamping
import time
current_time = time.strftime("%H:%M:%S",time.localtime())
log.log(0,TARGET,"Current time: " + current_time)



# Testing Camera Functions
from NASAcode.tools import cam_functions as camF
log.log(0,TARGET,"Testing Camera Functions")
camF.camTest()



# Testing Image functions
from NASAcode.tools import img_functions as imgF
log.log(0,TARGET,"Testing out Image Functions")


# Testing MPU-6050
from NASAcode.tools import mpu_functions as mpuF
log.log(0,TARGET,"Testing MPU-6050 Functions")
mpuF.mpuTest()



# Testing Radio?
# from NASAcode.tools.im



# Testing lead screws?
from NASAcode.tools import motor_functions as motF
log.log(0,TARGET,"Testing Lead Screws")
motF.testLeads()

# Testing raising and lowering rack and pinion
log.log(0,TARGET,"Testing Rack and Pinion")
motF.testRack()



# Testing the camera rotation functions
log.log(0,TARGET,"Testing camera rotation, R-20, L-20, L-20, R-20")
from NASAcode.tools import encoder_functions as encF
encF.rotateTest()



# Testing again buzzers and LED's 
# (signaling completed test campaign)


sg.cleanup()

# Setting up GPIO and logs stuffs
from NASAcode.tools import setup_gpio as sg, log_functions as log
TARGET = "TEST SUITE"
log.blank()
log.log(0,TARGET,"Running CompTest, setting up GPIO Pinouts")
sg.setup()

# Testing local time for timestamping
import time
current_time = time.strftime("%H:%M:%S",time.localtime())
log.log(0,TARGET,"Current time: " + current_time)

def cam_test():
    # Testing Camera Functions
    from NASAcode.tools import cam_functions as camF
    log.log(0,TARGET,"Testing Camera Functions")
    camF.camTest()

def img_test():
    # Testing Image functions
    from NASAcode.tools import img_functions as imgF
    log.log(0,TARGET,"Testing out Image Functions")
    imgF.testFilters()

def mpu_test():
    # Testing MPU-6050
    from NASAcode.tools import mpu_functions as mpuF
    log.log(0,TARGET,"Testing MPU-6050 Functions")
    mpuF.mpuTest()

def radio_test():
    # Testing Radio?
    from NASAcode.tools import radio_functions as radF
    log.log(0,TARGET,"Testing Radio Functions")
    radF.listen(15)

def leads_test():
    # Testing lead screws?
    from NASAcode.tools import motor_functions as motF
    log.log(0,TARGET,"Testing Lead Screws")
    motF.testLeads()

def rack_test():
    # Testing raising and lowering rack and pinion
    from NASAcode.tools import motor_functions as motF
    log.log(0,TARGET,"Testing Rack and Pinion")
    motF.testRack()

def rotation_test():
    # Testing the camera rotation functions
    log.log(0,TARGET,"Testing camera rotation, R-20, L-20, L-20, R-20")
    from NASAcode.tools import encoder_functions as encF
    encF.rotateTest()

def buzzer_test():
    # Testing again buzzers and LED's 
    # (signaling completed test campaign)
    from NASAcode.tools import misc_functions as miscF
    for i in range(10):
        miscF.beepON()
        miscF.blinkON()
        time.sleep(0.01)
        miscF.beepOFF()
        miscF.blinkOFF()
        time.sleep(0.01)


def test(cases):
    if(cases == ["all"]):
        cases = ["cam", "img", "mpu", "radio", "leads", "rack", "rotation", "buzzer"]
    elif(cases == ["motors"]):
        cases = ["leads", "rack", "rotation"]
    elif(cases == ["electronics"]):
        cases = ["cam","img","mpu","radio","buzzer"]
    
    for case in cases:
        
        if(case == "cam"):
            cam_test()
        elif(case == "img"):
            img_test()
        elif(case == "mpu"):
            mpu_test()
        elif(case == "radio"):
            radio_test()
        elif(case == "leads"):
            leads_test()
        elif(case == "rack"):
            rack_test()
        elif(case == "rotation"):
            rotation_test()
        elif(case == "buzzer"):
            buzzer_test()
        else:
            log.log(3,TARGET,"Unknown test command in CompTest")
    sg.cleanup()
    return True


import sys
args = sys.argv[1:]
log.log(0,TARGET,"Running suite: " + str(args))
test(args)
log.log(0,TARGET,"CompTest Completed.")

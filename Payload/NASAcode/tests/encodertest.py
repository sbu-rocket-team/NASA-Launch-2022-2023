from NASAcode.tools import pinout as p, setup_gpio as sg, motor_functions as mc
from time import sleep

from NASAcode.tools import encoder_functions as encF

sg.setup()

def motorON(time):
    mc.run_test(p.ROT_DIR, p.ROT_PWM)
    sleep(time)
    mc.off(p.ROT_ENABLE, p.ROT_PWM)

#motorON(1)

def encoderTest(time):
    samplerate = 500
    mc.run_test(p.ROT_DIR, p.ROT_PWM)
    ct = 0
    prev = 0
    for i in range(samplerate):
        sleep(time/samplerate)
        val = sg.GPIO.input(p.ROT_DIR)
        if(val == 1 & val != prev):
            ct += 1
        
        prev = val
        
    print(ct)
    mc.off(p.ROT_DIR, p.ROT_PWM)

#encoderTest(1)

def encoderTest2(cts):
    mc.run_test(p.ROT_DIR, p.ROT_PWM)
    ct = 0
    prev = 0
    while(ct < cts):
        val = sg.GPIO.input(p.ROT_DIR)
        if(val == 1 & val != prev):
            ct += 1
        
        prev = val
    mc.off(p.ROT_DIR, p.ROT_PWM)

#encoderTest2(1281)

def encoderTest2_2(cts):
    mc.motorON(p.ROT_DIR, p.ROT_PWM, "L", 50)
    ct = 0
    prev = 0
    while(ct < cts):
        val = sg.GPIO.input(p.ROT_DIR)
        if(val == 1 & val != prev):
            ct += 1
        
        prev = val
    mc.motorOff(p.ROT_PWM)

encoderTest2_2(1281)

ct = 0
rct = 0

def readEncoder(pin):
    global ct
    global rct

    while (ct < rct):
        if pin == p.ROT_DIR:
            if sg.GPIO.input(pin) == sg.GPIO.HIGH:
                ct += 1

sg.GPIO.add_event_detect(p.ROT_DIR, sg.GPIO.RISING, callback=readEncoder)

def encoderTest3(cts):
    turnOff = True

    mc.run_test(p.ROT_ENABLE, p.ROT_PWM)
    global ct
    
    while (turnOff):
        sleep(0.01)
        if (ct > cts):
            mc.off(p.ROT_ENABLE, p.ROT_PWM)
            turnOff = False
            
encoderTest3()

currentDegree = 0

def encoderTest4():
    global currentDegree
    print(currentDegree)
    currentDegree = encF.rotateCam("R", currentDegree, 90)
    print(currentDegree)

def encoderTest5():
    global currentDegree
    print(currentDegree)
    currentDegree = encF.rotateCam("R", currentDegree)
    print(currentDegree)
    currentDegree = encF.rotateCam("R", currentDegree)
    print(currentDegree)
    currentDegree = encF.rotateCam("R", currentDegree)
    print(currentDegree)
    currentDegree = encF.rotateCam("R", currentDegree)
    print(currentDegree)
    currentDegree = encF.rotateCam("R", currentDegree)
    print(currentDegree)

sg.cleanup()

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
        val = sg.GPIO.input(p.ENCODER)
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
        val = sg.GPIO.input(p.ENCODER)
        if(val == 1 & val != prev):
            ct += 1
        
        prev = val
    mc.off(p.ROT_DIR, p.ROT_PWM)

encoderTest2(100)

ct = 0

def readEncoder(pin):
    global ct
    if pin == p.ENCODER:
        if sg.GPIO.input(pin) == sg.GPIO.HIGH:
            ct += 1

def encoderTest3(cts):
    mc.run_test(p.ROT_ENABLE, p.ROT_PWM)
    global ct
    prev = 0
    while(ct < cts):
        sg.GPIO.add_event_detect(p.ENCODER, sg.GPIO.RISING, callback=readEncoder)
    mc.off(p.ROT_ENABLE, p.ROT_PWM)

currentDegree = 0

def encoderTest4():
    print(currentDegree)
    currentDegree = encF.rotateCam("R", currentDegree, 90)
    print(currentDegree)

def encoderTest5():
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

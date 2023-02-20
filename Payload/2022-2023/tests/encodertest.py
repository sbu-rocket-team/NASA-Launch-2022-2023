from ..tools import pinout as p, setup_gpio as sg, motor_functions as mc
from time import sleep

sg.setup()

def motorON(time):
    mc.run_test(p.ROT_ENABLE, p.ROT_PHASE)
    sleep(time)
    mc.off(p.ROT_ENABLE, p.ROT_PHASE)

#motorON(1)

def encoderTest(time):
    samplerate = 500
    mc.run_test(p.ROT_ENABLE, p.ROT_PHASE)
    ct = 0
    prev = 0
    for i in range(samplerate):
        sleep(time/samplerate)
        val = sg.GPIO.input(p.ENCODER)
        if(val == 1 & val != prev):
            ct += 1
        
        prev = val
        
    print(ct)
    mc.off(p.ROT_ENABLE, p.ROT_PHASE)

#encoderTest(1)

def encoderTest2(cts):
    mc.run_test(p.ROT_ENABLE, p.ROT_PHASE)
    ct = 0
    prev = 0
    while(ct < cts):
        val = sg.GPIO.input(p.ENCODER)
        if(val == 1 & val != prev):
            ct += 1
        
        prev = val
    mc.off(p.ROT_ENABLE, p.ROT_PHASE)

encoderTest2(2500)

sg.cleanup()

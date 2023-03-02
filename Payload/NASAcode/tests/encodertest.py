from NASAcode.tools import pinout as p, setup_gpio as sg, motor_functions as mc
from time import sleep

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

sg.cleanup()

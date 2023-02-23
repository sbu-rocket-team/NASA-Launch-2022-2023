from ..tools import pinout as p, setup_gpio as sg, motor_functions as mc
from time import sleep

sg.setup()

pwm = p.LEADSCREW_PWM
dir = p.LEADSCREW_DIR

#mc.motorON2(dir,pwm,p.LEADSCREW_OPEN,101)
#sleep(5)
#mc.off(dir,pwm)
#sleep(1)
mc.motorON2(dir,pwm,p.LEADSCREW_OPEN,101)
sleep(1)
mc.off(dir,pwm)

sg.cleanup()
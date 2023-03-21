from NASAcode.tools import pinout as p, setup_gpio as setup_gpio, motor_functions as mf
from time import sleep

setup_gpio.setup()

mf.motorON2(p.RP_DIR, p.RP_PWM, p.RP_UP)
sleep(0.5)
mf.off(p.RP_DIR, p.RP_PWM)

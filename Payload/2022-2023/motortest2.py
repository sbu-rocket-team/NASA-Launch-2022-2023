import pinout
import setup_gpio
import motorcontrol as mc
from time import sleep

setup_gpio.setup()

# Enable is PWM, phase in binary for direction
rot = [pinout.ROT_ENABLE, pinout.ROT_PHASE]

#mc.run_test(rot)
mc.run_smoothstart(rot)
sleep(2)
mc.off(pinout.ROT_ENABLE, pinout.ROT_PHASE)

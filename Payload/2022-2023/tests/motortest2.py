import pinout
import setup_gpio
import motorcontrol as mc
from time import sleep
setup_gpio.setup()

rot = [pinout.ROT_ENABLE, pinout.ROT_PHASE]

#mc.run_test(rot)
mc.run_smoothstart(rot)
#mc.run_smoothstart(pinout.ROT_ENABLE, pinout.ROT_PHASE)
mc.run_backforth(pinout.ROT_ENABLE, pinout.ROT_PHASE)
sleep(2)
mc.off(pinout.ROT_ENABLE, pinout.ROT_PHASE)
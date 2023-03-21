import time

from gpiozero import CPUTemperature as CPUTemp

from NASAcode.tools import pinout
from NASAcode.tools import setup_gpio as sg
from NASAcode.tools.setup_gpio import GPIO


"""
Gets the time that passed since start of program in hr:min:sec

Parameters:
- timeStart [float]: Start time of program //from time()
- timeRef [float]: Reference time to be obtained

Returns:
- timeStr [String]: Time value in the format of "HH:MM:SS". Does not count the days.
"""
def timeElapsed(timeStart, timeRef):
    timeDif = timeRef - timeStart
    
    secs = int(timeDif) % 60
    mins = int(timeDif / 60) % 60
    hours = int(timeDif / (60*60)) % 24
    
    timeStr = str(hours).zfill(2) + ":" + str(mins).zfill(2) + ":" + str(secs).zfill(2)
    
    return timeStr

def overheat(temp):
    from NASAcode.tools import mpu_functions as mpuF
    if (CPUTemp() >= temp):
        time.sleep(10)


def getTransmittion():
    pass

def beepON():
    GPIO.output(pinout.BUZZER, 1)

def beepOFF():
    GPIO.output(pinout.BUZZER, 0)

def blinkON():
    GPIO.output(pinout.LED, 1)    

def blinkOFF():
    GPIO.output(pinout.LED, 0)
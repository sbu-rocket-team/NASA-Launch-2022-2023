import datetime
import os
from NASAcode.tools import txt_functions as txtF

date = datetime.datetime.now().strftime("%Y-%m-%d")

# General format of the logs: "(DATE)-(TIME) | (MESSAGE LEVEL) | (TARGET) | (MESSAGE)"

INFO = 0
WARNING = 1
ERROR = 2

# Location of log files
MAIN_LOGDIR = "../logs"
MAIN_LOG = "payload"+date+".log"

# Ensuring the daily log is created and available
direc = MAIN_LOGDIR+"/"+MAIN_LOG
full_dir = "/home/pi/NASAcode/"+str(direc[2:])
if(os.path.exists(full_dir)==False):
   print("New log created! " + full_dir)
   txtF.createFile(direc)


def log(level,target,message):
    ti = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = enum2str(level)
    dat = str(ti) + " | " + str(level) + " | " + str.upper(target) + " | " + str(message)

    print(dat)
    txtF.writeFile(direc,dat)
    return dat

def blank():
    print("")
    txtF.writeFile(direc,"")

def enum2str(level):
    if(level == 0):
        return "INFO"
    elif(level == 1):
        return "WARNING"
    elif(level == 2):
        return "ERROR"
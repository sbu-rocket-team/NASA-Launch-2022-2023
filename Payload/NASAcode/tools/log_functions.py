import datetime
import os
from NASAcode.tools import txt_functions as txtF

date = datetime.datetime.now().strftime("%Y-%m-%d")

# General format of the logs: "(DATE)-(TIME) | (MESSAGE LEVEL) | (TARGET) | (MESSAGE)"

INFO = 0
WARNING = 1
ERROR = 2

# Location of log files
MAIN_LOGDIR = "logs"
MAIN_LOG = "payload"+date+".log"

# Ensuring the daily log is created and available
direc = MAIN_LOGDIR+"/"+MAIN_LOG
if(os.path.exists()==False):
   txtF.createFile(direc)


def log(level,target,message):
    ti = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = enum2str(level)
    dat = ti + " | " + level + " | " + str.upper(target) + " | " + message

    print(dat)
    txtF.writeFile(direc,dat)
    return dat



def enum2str(level):
    if(level == 0):
        return "INFO"
    elif(level == 1):
        return "WARNING"
    elif(level == 2):
        return "ERROR"
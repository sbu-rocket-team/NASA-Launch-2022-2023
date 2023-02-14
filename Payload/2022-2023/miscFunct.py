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

def getTransmittion():
    pass

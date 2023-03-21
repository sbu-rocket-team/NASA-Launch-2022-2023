# IDK what this needs to be atm, but want to set up the references already
import subprocess
from NASAcode.tools import log_functions as log


TARGET = "RADIO"
TIMEOUT = 0.1 * 60; # 10 seconds for testing, change to minutes for deployment
FREQ = 146.470e6
SAMPLERATE = 15e3
GAIN = 20
OUTPUTFILE = "output.txt"

def listen(timeout = TIMEOUT, freq = FREQ, samples = SAMPLERATE, gain = GAIN):
    # Do something
    log.log(0,TARGET,"Starting radio listen, " + str(freq) + ", " + str(samples))

    # Ensure the script is executable, then execute
    subprocess.run(["chmod +x /home/pi/NASAcode/radio/radio.sh",''],shell=True)
    subprocess.run(["/home/pi/NASAcode/radio/radio.sh",''],shell=True)

    # output is saved to output.txt
    text = parse()

    log.log(0,TARGET,"Completed Radio Listen for " + str(timeout) + " seconds on " + str(freq))
    return text



def parse():
    # Do something
    return True


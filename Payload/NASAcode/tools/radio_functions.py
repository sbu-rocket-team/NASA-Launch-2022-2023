# IDK what this needs to be atm, but want to set up the references already
import subprocess
from NASAcode.tools import log_functions as log



TARGET = "RADIO"
#CALLSIGN = "KE2ANM"
CALLSIGN = "KQ4CTL"
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
    command = "/home/pi/NASAcode/radio/radio.sh " + str(int(timeout)) + " " + str(int(freq)) + " " + str(int(samples)) + " " + str(int(gain))
    subprocess.run([command],shell=True)

    # output is saved to output.txt
    text = parse()

    log.log(0,TARGET,"Completed Radio Listen for " + str(timeout) + " seconds on " + str(freq))
    return text



def parse():
    # Do something

    #out = open("output.txt", "r")

    out = open("./NASAcode/radio/output.txt")
    blob = out.read()
    lines = blob.split('\n')[1:]
    args_list = []
    for line in lines:
        
        
        if len(line) > 5 :
            # Its a message
            log.log(0,TARGET,"Read line from APRS: " + str(line))
            line = line[1:]
            if("FSK1200" not in line): # Removing the junk message header.
                if(CALLSIGN in line):
                    #Its our message!

                    if("{" in line): # Filter out the message thing if its in there.
                        line = line[:line.index("{")]
                    

                    # For a :(message) and space delimited
                    line = line[line.index(':')+1:]
                    args = line.split(" ")
                    args.reverse()
                    done = False
                    while done==False:
                        if('' in args):
                            args.remove('')
                        else:
                            done = True
                    
                    # Maybe validate they are all legit commands?
                    
                    log.log(0,TARGET,"Decoded message as: " + str(args))
                    args_list.append(args)
                    
        
    return args_list


parse()
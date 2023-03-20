#!/bin/bash
# Bash script to automate running RTL_FM, collecting audio, and then extract an APRS commands

# Variables
timeout_val=${1:-5}


# Record the audio from rtl_fm, using demod thru rtl
timeout $timeout_val rtl_fm -f 146.470M -M fm -s 15000 -r 15000 -T -E dc | sox -t raw -e signed -c 1 -b 16 -r 15000  - recording146470.wav 

# Perform some audio manipulation to account for shortfalls of rtl-fm
sox -t wav recording146470.wav recording146470mixed.wav gain 20 norm 0.1
sox -t wav recording146470mixed.wav -esigned-integer -b16 -r 22050 -t raw rec146470.raw

# Make sure the output file exists, then write to file
touch output.txt
timeout 2 multimon-ng -t raw rec146470.raw -a FMSFSK -a AFSK1200 output.txt

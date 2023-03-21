#!/bin/bash
# Bash script to automate running RTL_FM, collecting audio, and then extract an APRS commands

# When running do:
# bash radio.sh (timeout) (freq) (samplerate) (post-gain)       or defaults optimized for 2m APRS

# Variables
timeout_val=${1:-5}
freq=${2:-146.470M}
samples=${3:-15000}
gain=${4:-20}

# Record the audio from rtl_fm, using demod thru rtl
timeout $timeout_val rtl_fm -f $freq -M fm -s $samples -r $samples -T -E dc | sox -t raw -e signed -c 1 -b 16 -r $samples  - recording146470.wav 

# Perform some audio manipulation to account for shortfalls of rtl-fm
sox -t wav recording146470.wav recording146470mixed.wav gain $gain norm 0.1
sox -t wav recording146470mixed.wav -esigned-integer -b16 -r 22050 -t raw rec146470.raw

# Make sure the output file exists, then write to file
touch output.txt
timeout 2 multimon-ng -t raw rec146470.raw -a FMSFSK -a AFSK1200 output.txt

#!/bin/bash
cd home/pi/Documents/HCBellsPython/
if ! screen -list | grep -q "BellRinger"; then
    screen -dmS "BellRinger" sh -c "./Documents/HCBellsPython/BellRinger.sh; exec bash" >> StartScriptLog.txt
    #screen -dmS "DataManager" sh -c "./DataManager; exec bash"
fi

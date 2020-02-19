#!/bin/bash
cd home/pi/Documents/HCBellsPython/
if ! screen -list | grep -q "BellRinger"; then
    screen -dmS "BellRinger" sh -c "./Documents/HCBellsPython/BellRinger.sh; exec bash" >> StartScriptLog.txt
    screen -dmS "InternetStatus" sh -c "./Documents/HCBellsPython/InternetStatus.sh; exec bash"
fi

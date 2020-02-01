#!/bin/bash
screen -dmS "BellRinger" sh -c "./BellRinger.sh; exec bash" >> StartScriptLog.txt
#screen -dmS "DataManager" sh -c "./DataManager; exec bash"

#!/usr/bin/python
from subprocess import Popen
import sys
import time

##This script just runs the data manger script,
##but restarts it if it crashes/wants to restart
##Start the DataManger to get Debugging info

filename = "BellRinger.py"
while True:
    datetimestr = time.strftime("%Y-%m-%d")
    print("\nStarting " + filename)
    p = Popen("python3 " + filename + " 2>&1 | tee -a logs/BellRinger-"+datetimestr+".log", shell=True)
    print("Started")
    p.wait()

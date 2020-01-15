#!/usr/bin/python
from subprocess import Popen
import sys
import time
##This script just runs the data manger script,
##but restarts it if it crashes/wants to restart
##Start the DataManger to get Debugging info time.time()-StartTime

filename = "DataManager.py"
StartTime = round(time.time())
DiffTime = [100,100]
while True:
    print (DiffTime)
    DiffTime.append(round(time.time())-StartTime)
    print (DiffTime)
    DiffTime.pop(0)
    if sum(DiffTime)< 30:
        print (DiffTime)
    print("Time scince boot: "+ str(DiffTime))
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    print("Started")
    p.wait()

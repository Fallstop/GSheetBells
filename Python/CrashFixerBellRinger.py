#!/usr/bin/python
from subprocess import Popen
import sys

##This script just runs the data manger script,
##but restarts it if it crashes/wants to restart
##Start the DataManger to get Debugging info

filename = "BellRinger.py"
while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    print("Started")
    p.wait()

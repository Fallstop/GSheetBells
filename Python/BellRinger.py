import time
import datetime
from GoogleSheetAPI import *
try:
    import RPi.GPIO as GPIO
    print("Initiating GPIO")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)
except:
    print("GPIO off")
print("Bell Ringer Started")
def GetTime(): ##Function for reciveing
    Time = time.asctime().split() 
    Time = Time[3]
    Time = Time[:-3]
    return(Time)
def RingBell(TimeToRingFor):
    print("Ringing Bell for:",TimeToRingFor," seconds")
    try:
        GPIO.output(18,GPIO.HIGH)
        time.sleep(TimeToRingFor)
        GPIO.output(18,GPIO.LOW)
    except:
        print("Ring Ring?")
        time.sleep(TimeToRingFor)
    print("Stoped Ringing Bell")
def CheckBell():
    currentTime = GetTime()
    print(currentTime)
    bellTimes = retriveBellTimes() #First position is the config for how long to ring, rest are belltimes 
    i = 1
    while i < len(bellTimes):
        if bellTimes[i] == currentTime:
            RingBell(bellTimes[0])
            break
    print("Did not find a match")
def CheckRingNow():
    ##TODO
    print("CheckRingNow is still under develment")
OldTime = GetTime()
print(GetDay())
while True:
    Time = GetTime()
    if OldTime != Time:
        CheckBell()
    time.sleep(1)


import time
import pandas as df
import numpy as np
def GetTime(): ##Function for reciveing
    Time = time.asctime().split() 
    Time = Time[3]
    Time = Time[:-3]
    return(Time)
def ReadData():
    try:
        print("Read Sucseded")
        return(df.read_csv("BellStorage.csv",header=None)) ##File with times and dates for all bells
    except:
        print("Read failed")
        time.sleep(5)
        ReadData()
def RingBell(TimeToRingFor):
    ##TO DO
    print("Ringing")
    time.sleep(TimeToRingFor)
    print("StopRinging")
def CheckBell(Time,Data):
    i = 0
    while i < Data.shape[0]:
        print("Line:",i,"Time:",Data.iloc[i,0])
        i += 1
    for x in Data:
        print(Data.iloc[x,0])
Data = ReadData()
Time = GetTime()
Day = 1
CheckBell(Time,Data)

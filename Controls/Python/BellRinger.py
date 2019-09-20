import time
import pandas as df
import numpy as np
import datetime
def GetTime(): ##Function for reciveing
    Time = time.asctime().split() 
    Time = Time[3]
    Time = Time[:-3]
    return(Time)
def GetDay(): ##Function for getting day
    Day = datetime.datetime.today().weekday()
    ##Time = Time[3]
    ##Time = Time[:-3]
    return(Day + 1)
def ReadData():
    try:
        print("Reading data")
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
def CheckBell(Time,Day,Data):
    
    BeginTime = time.time()
    i = 1
    BellDayData = Data[[1]].copy()
    BellDayData = BellDayData.iloc[:,0]
    BellDayData = BellDayData.str.split(pat = "/")
    while i < BellDayData.shape[0]:
        if Data.iloc[i,0] == Time:
            x = 0
            BellDay = BellDayData.iloc[i]
            while x < len(BellDay) and Day >= int(BellDay[x]):
                if int(BellDay[x]) == Day:
                    RingBell(Data.iloc[i,2])
                    print("CheckBell Function found a match in",round(time.time()-BeginTime,5),"secs at ",Time)
                    break
                x += 1
        i += 1
    print("Check Bell function did not find a match in",round((time.time()-BeginTime),5),"secs at ",Time)
OldTime = GetTime()
print(GetDay())
while True:
    Time = GetTime()
    Data = ReadData()
    if OldTime != Time:
        CheckBell(Time,Day,Data)
    Day = 3
    time.sleep(1)


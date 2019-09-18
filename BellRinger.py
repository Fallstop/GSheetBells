import time
import pandas as df
import numpy as np
def GetTime(): ##Function for reciveing
    Time = time.asctime().split() 
    Time = Time[3]
    Time = Time[:-3]
    print(Time)
def ReadData():
    try:
        print("Read Sucseded")
        return(df.read_csv("BellStorage.csv",header=None)) ##File with times and dates for all bells
    except:
        print("Read failed")
        time.sleep(5)
        ReadData()
Data = ReadData()
print(Data)

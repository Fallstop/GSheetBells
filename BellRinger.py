import time
def GetTime():
    Time = time.asctime().split()
    Time = Time[3]
    Time = Time[:-3]
    print(Time)

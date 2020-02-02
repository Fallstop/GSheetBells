import time
import datetime
print ("Bellringer startup, time:",str(datetime.datetime.now())[:-7])
import pandas as df
import numpy as np
from GoogleSheetAPI import *
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
try:
    import RPi.GPIO as GPIO
    print("Initiating GPIO")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(12,GPIO.OUT)
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
        GPIO.output(12,GPIO.HIGH)
        time.sleep(TimeToRingFor)
        GPIO.output(12,GPIO.LOW)
    except:
        print("Ring Ring?")
        time.sleep(TimeToRingFor)
    print("Stoped Ringing Bell")
def CheckBell():
    global bellTimeDay
    global bellTimes
    currentTime = GetTime()
    print(currentTime)
    try: #Try get the online Version
        bellTimes = retriveBellTimesOnline() #First position is the config for how long to ring, rest are belltimes
        bellTimeDay = datetime.datetime.today().weekday()
    except: 
        print("No Internet!")
        print("Using offline preset!")
        bellTimes = retriveBellTimesOffline()
	
    print("Got Sheet data,",len(bellTimes),"items long.")
    i = 1
    while i < len(bellTimes):
        if bellTimes[i] == currentTime:
            print("Found a match")
            RingBell(int(bellTimes[0]))
            return()
        i+=1
    return()
    print("Did not find a match")
def retriveBellTimesOnline(): #From Google Sheets
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SPREADSHEET_ID = '1JmhFI1zfQ7La_QXS8TCnj1R6B8r_KNLe8jk24eF6E64'
    response = []
    #Get Correct range
    DayRangeNames = ["mondayAPI","tuesdayAPI","wensdayAPI","thursdayAPI","fridayAPI","saterdayAPI","sundayAPI"]
    RangeName = DayRangeNames[(datetime.datetime.today().weekday())]
    print(RangeName)
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    
    # Call the Sheets API
    sheet = service.spreadsheets()
    #Get config
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range="config").execute()
    values = result.get('values', [])
    if not values:
        print('No config found.')
    else:
        for row in values:
            response.append(row[0])#Add to start
    #Get Times
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No times found.')
    else:
        for row in values:
            response.append(row[0])
    return(response)


def retriveBellTimesOffline():
    global bellTimes
    global bellTimeDay
    if bellTimeDay == datetime.datetime.today().weekday():
        return(bellTimes)
    #From OfflineBellBackup
    try:
        print("Reading data")
        data = df.read_csv("OfflineBellBackup/normAllDays.csv",header=None) ##File with times and dates for all bells
    except Exception as e:
        print("Read failed:",e)
        return([3])
    print(data)
    day = datetime.datetime.today().weekday()
    dayBellTimes = data.iloc[:,day]
    print (dayBellTimes)
    bellTimes = [data.iloc[0,7]]
    print(bellTimes)
    dayBellTimesList = dayBellTimes.values.tolist()
    i = 0
    while i < len(dayBellTimesList):
        if str(dayBellTimesList[i]) == "nan":
            break
        else:
            print(dayBellTimesList[i])
            bellTimes.append(str(dayBellTimesList[i]))
        i+=1
    print(bellTimes)
    bellTimeDay = datetime.datetime.today().weekday()
    return(bellTimes)


#Main code (Made entirely out of functions)
OldTime = GetTime()
bellTimes = [3]
bellTimeDay = 8
while True:
    Time = GetTime()
    if OldTime != Time:
        CheckBell()
        OldTime = GetTime()
    time.sleep(1)


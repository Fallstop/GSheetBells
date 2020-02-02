import time
import datetime
from GoogleSheetAPI import *
import pickle
import os.path
import datetime
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
def CheckBell(bellTimes):
    currentTime = GetTime()
    print(currentTime)
    try:
        bellTimes = retriveBellTimes() #First position is the config for how long to ring, rest are belltimes 
    except:
        print("No Internet!")
	
    print("Got Sheet data,",len(bellTimes),"items long.")
    i = 1
    while i < len(bellTimes):
        if bellTimes[i] == currentTime:
            print("Found a match")
            RingBell(int(bellTimes[0]))
            return(bellTimes)
        i+=1
    return(bellTimes)
    print("Did not find a match")
def retriveBellTimes(): #From Google Sheets
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
OldTime = GetTime()
bellTimes = [3]
while True:
    Time = GetTime()
    if OldTime != Time:
        bellTimes = CheckBell(bellTimes)
        OldTime = GetTime()
    time.sleep(1)


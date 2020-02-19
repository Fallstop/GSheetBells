import time
import datetime
print ("Bellringer startup, time:",str(datetime.datetime.now())[:-7])
import pandas as pd
import numpy as np
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(12,GPIO.OUT)
    print("GPIO initiated")
except:
    print("GPIO off")

def getOfflineHash():
    try:
        hashFile = open("offlineBellBackup/hash.txt","r")
        hashText = hashFile.read()
        hashFile.close()
        return(hashText)
    except:
        return("HashNotFound")
def writeOfflineHash(hashText):
    try:
        hashFile = open("offlineBellBackup/hash.txt","w+")
        hashFile.write(hashText)
        hashFile.close()
        return("Saved hash")
    except Exception as e:
        return("Hash save failed",e)
def writeOfflineBellTimes(bellTimes):
    #Used if new bell times are found
    try:
        csv = pd.DataFrame.from_dict(bellTimes)
        csv.to_csv("offlineBellBackup/normAllDays.csv",index=False,header=False)
        print("Done saving bell time backup")
        return()
    except Exception as e:
        print("Write file exception on bell time backup")
        print(e)
def getOfflineBellTimes():
    #Used on start up to get back up
    try:
        bellTimesArray = []
        csvFile = open("offlineBellBackup/normAllDays.csv","r")
        csvText = csvFile.readlines()
        for row in csvText:
            bellTimesArray.append(row.rstrip('\n').split(","))
        print("Got offline backup")
        return(bellTimesArray)
    except Exception as e:
        print("Read file exception on bell time backup")
        print(e)

def GetTime(): ##Function for formating time
    Time = time.asctime().split() 
    Time = Time[3]
    Time = Time[:-3]
    return(Time)
def RingBell():
    print()
    print("Ringing Bell")
    try:
        GPIO.output(12,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(12,GPIO.LOW)
    except:
        print("GPIO OFF, Ring Ring?")
        time.sleep(7)
    print("Stoped Ringing Bell")
    print()
def CheckBell(checkChanges):
    ################
    #GET BELL TIMES
    ################
    global bellTimes
    currentTime = GetTime()
    print("Current time:",currentTime)
    if checkChanges:
        print("Atempting to check for changes")
        try: #Try get the online Version
            bellTimesTemp = retriveBellTimesOnline() #First position is the config for how long to ring, rest are belltimes
            if bellTimesTemp:
                print(bellTimesTemp)
                bellTimes = bellTimesTemp
        except Exception as e:
            print("Failed to get updated sheet, Exception:",e)
            print("Proberly No Internet!")
            print("Using offline backup!")
            bellTimes = getOfflineBellTimes()
    bellTimesDF = pd.DataFrame(bellTimes)
    bellDayTimes = bellTimesDF.fillna(0.0).iloc[:,datetime.datetime.today().weekday()].values.tolist()
    
    bellDayTimes.pop(0)
    print("Got Sheet data,",len(bellDayTimes),"items long.")
    #######################################
    #CHECK BELL TIMES AGAINST CURRENT TIME
    #######################################
    i = 0
    while i < len(bellDayTimes):
        if bellDayTimes[i] == currentTime:
            print("Found a match")
            RingBell()
            return()
        i+=1
    print("Did not find a match")
    print()
    return()
def retriveBellTimesOnline(): #From Google Sheets
    #############
    #SETUP
    #############
    
    global currentHash
    global bellTimes
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SPREADSHEET_ID = '1JmhFI1zfQ7La_QXS8TCnj1R6B8r_KNLe8jk24eF6E64'
    
    day = datetime.datetime.today().weekday()
    RangeName = "timeDataAPI"
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
    
    ##############
    #SETUP DONE
    ##############
    
    #Get hash
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range="dataHashAPI").execute()
    values = result.get('values', [])
    if not values:
        print('No hash found.')
        raise Exception("No hash found from sheet")
    else:
        for row in values:
            if currentHash == row[0] and row[0] != "#NAME?"  :
                print("No Changes")
                return(False)
            else:
                currentHash = row[0]
                print("New hash found, Hash:", currentHash)
                #Changes have been made, get the new times
                
                result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RangeName).execute()
                values = result.get('values', [])
                
                if not values:
                    print('No times found.')
                    raise Exception("No times found from sheet")
                else:
                    bellTimes = []
                    for row in values:
                        bellTimes.append(row)
                    print("Hash:",currentHash)
                    print(writeOfflineHash(currentHash))
                    print(bellTimes)
                    writeOfflineBellTimes(bellTimes) #Update Backup
                    print()
                    return(bellTimes)


        
        

#Main code (Made entirely out of functions)

#Initial
currentHash = getOfflineHash()
print("Hash Stored:", currentHash)
OldTime = GetTime()
bellTimes = getOfflineBellTimes() #Placeholder that won't error or ring

print("Bell Ringer Started")
#Main bell check loop
while True:
    Time = GetTime()
    if OldTime != Time:
        if (int(Time[3:])+1)%15==0:
            CheckBell(checkChanges = True)
        else:
            CheckBell(checkChanges = False)
        OldTime = GetTime()
    time.sleep(1)


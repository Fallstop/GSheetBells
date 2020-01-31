def retriveBellTimes():
    import pickle
    import os.path
    import datetime
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
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

if __name__ == '__main__':
    print(retriveBellTimes())

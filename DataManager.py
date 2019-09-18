import pandas as df
import numpy as np
import os
import time

def FixCommands():
    print("Cannot write to Commands")
    CommandFile = open("Commands.txt","w+") ##Wirtes ontop of the txt or generates new
    CommandFile.write("0,1,2") ##Top of data sheet to declear rows and space for RingNow/Mute
    CommandFile.close() ##Save
    print("Command Refreshed")
    raise Exception("Command file corrupted, Refreshing and restarting")

try: ##Teasting if the data is currupt (eg: no headers or it has been delated), Data is already gone if it dosen't read
    data = df.read_csv("BellStorage.csv",header=None) ##File that stores the bell times and dates and other info
except: ##If we can't edit Bell Storage csv, we need to refresh the file
    print("Cannot write to BellStorage.csv")
    StorageFile = open("BellStorage.csv","w+") ##Wirtes ontop of the txt or generates new
    StorageFile.write("0,0,0,0") ##Header info
    StorageFile.close() ##Save
    print("Bell Storage Refreshed")
    raise Exception("Bell Storage csv corrupted, Refreshing and restarting")

try: ##Teasting if the file is currupt (eg: no headers or it has been delated), BTW this would cause a boot loop befor
    commands = df.read_csv("Commands.txt") ##Instructions for program
except: ##If we can't edit command txt, we need to refresh the file
    FixCommands()
blank =df.read_csv("Blank.csv",header=None) ##Blank, is used to attach to the end of Bell storage when a new line is going to be added

print(data)
print(commands)
NumOfCommands = commands.shape[0] ##How big many commands are there
print("Num Of Commands: ",NumOfCommands)
DataPos = 0 ##Where in the data do we write to for the next bell 
while True: ##Infinte loop to have always listing for new commands
    commands = df.read_csv("Commands.txt") ##Check for new commands
    NumOfCommands = commands.shape[0] ##            ^^
    if NumOfCommands != 0: ##If there is a new command
        print("New Command")
        if data.shape[0] > DataPos: ##If we not already posetioned at the end
            while data.iloc[DataPos,0] != "NaN": ##Scan down data untill we reach a empty spot
                DataPos += 1
                if data.shape[0] == DataPos:
                    break
        
        print("DataPos:",DataPos)
        
        if commands.iloc[0,0] == "AddNew": ##Add New bell, 3 segments of data to intergrate
            if data.shape[0] <= DataPos:
                data = data.append(blank, ignore_index = True)
            try:
                Time =  commands.iloc[0,1]
                Dates = commands.iloc[0,2]
                RingTime = commands.iloc[0,3]
            except:
                FixCommands()
            data.iloc[DataPos,0] = Time
            data.iloc[DataPos,1] = Dates ##Apply to data sheet
            data.iloc[DataPos,2] = RingTime 
            print("Data After appalying Commmand")
            print(data)
            ##Remove command and save data
            commands = commands.drop(0)
            print("Commands",commands) 
            commands.to_csv('Commands.txt', index=False)
            data.to_csv('BellStorage.csv', index=False,header=False)
        
        elif commands.iloc[0,0] == "Remove": ##Remove bell, 2 segments of data to identify the bell
            print("Running Remove command")
            EixtLoop = False
            try:
                Time =  commands.iloc[0,1]
                Dates = commands.iloc[0,2]
            except:
                FixCommands()
            
            i = 1
            while i < len(data) and EixtLoop == False: ##Loop through data
                if data.iloc[i,0] == Time and data.iloc[i,1] == Dates: ##If found, remove and exit loop
                    data = data.drop(i) 
                    print("Found Remove target")
                    print(data)
                    EixtLoop = True
                else:
                    i+= 1 ##If not, increment
            ##Remove command and save data
            commands = commands.drop(0)
            commands.to_csv('Commands.txt', index=False)
            data.to_csv('BellStorage.csv', index=False,header=False)
            DataPos -= 1
        elif commands.iloc[0,0] == "RingNow":
            try:
                RingTime = commands.iloc[0,1]
            except:
                FixCommands()
            
            data.iloc[0,0] = RingTime
            ##Remove command and save data
            commands = commands.drop(0)
            commands.to_csv('Commands.txt', index=False)
            data.to_csv('BellStorage.csv', index=False,header=False)
        elif commands.iloc[0,0] == "MuteToggle":
            try:
                if data.iloc[0,1] == "0":
                    data.iloc[0,1] = 1
                    print("Mute Turned on")
                else:
                    data.iloc[0,1] = 0
                    print("Mute Turned off")
                    print(data.iloc[0,1])
            except:
                FixCommands()
            
            ##Remove command and save data
            commands = commands.drop(0)
            commands.to_csv('Commands.txt', index=False)
            data.to_csv('BellStorage.csv', index=False,header=False)
        else:
            ##Remove command, save data and throw exception to restart
            try: ##Teasting if the file is currupt (eg: "fg,fsdf,sdf,sd,f,s,df,sdf,s,df,sdf" with more inputs than headers will make a exception), BTW this would cause a boot loop befor
                commands = commands.drop(0)
                commands.to_csv('Commands.txt', index=False)
            except: ##If we can't edit command txt, we need to refresh the file
                FixCommands()
            print("Weird command found")
            raise Exception("Command not reconised, dropping and restarting")


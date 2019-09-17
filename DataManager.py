import pandas as df
import numpy as np
import time
data = df.read_csv("BellStorage.csv",header=None) ##File that stores the bell times and dates and other info
blank =df.read_csv("Blank.csv",header=None) ##Blank, is used to attach to the end of Bell storage when a new line is going to be added
commands = df.read_csv("Commands.txt") ##Instructions for program
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
            
            data = data.append(blank, ignore_index = True)
            Time =  commands.iloc[0,1]
            Dates = commands.iloc[0,2]
            RingTime = commands.iloc[0,3]
            data.iloc[DataPos,0] = Time
            data.iloc[DataPos,1] = Dates ##Apply to data sheet
            data.iloc[DataPos,2] = RingTime 
            print("Data After appalying Commmand")
            print(data)
            commands = commands.drop(0) ##remove command
            print("Commands",commands) 
            commands.to_csv('Commands.txt', index=False) ## files
            data.to_csv('BellStorage.csv', index=False,header=False)
        
        elif commands.iloc[0,0] == "Remove": ##Remove bell, 2 segments of data to identify the bell
            print("Running Remove command")
            EixtLoop = False
            Time =  commands.iloc[0,1]
            Dates = commands.iloc[0,2]
            i = 1
            while i < len(data) and EixtLoop == False: ##Loop through data
                if data.iloc[i,0] == Time and data.iloc[i,1] == Dates: ##If found, remove and exit loop
                    data = data.drop(i) 
                    print("Found Remove target")
                    print(data)
                    EixtLoop = True
                else:
                    i+= 1 ##If not, increment
            commands = commands.drop(0)
            commands.to_csv('Commands.txt', index=False)
            data.to_csv('BellStorage.csv', index=False,header=False)
            DataPos -= 1
        elif commands.iloc[0,0] == "RingNow":
            RingTime = commands.iloc[0,1]
            data.iloc[0,0] = RingTime
            commands = commands.drop(0)
            commands.to_csv('Commands.txt', index=False)
            data.to_csv('BellStorage.csv', index=False,header=False)
        elif commands.iloc[0,0] == "MuteToggle":
            if data.iloc[0,1] == "0":
                data.iloc[0,1] = 1
                print("Mute Turned on")
            else:
                data.iloc[0,1] = 0
                print("Mute Turned off")
                print(data.iloc[0,1])
            commands = commands.drop(0)
            commands.to_csv('Commands.txt', index=False)
            data.to_csv('BellStorage.csv', index=False,header=False)
        else:
            commands = commands.drop(0)
            commands.to_csv('Commands.txt', index=False)
            print("Weird command found")
            raise Exception("Command not reconised, dropping and restarting")


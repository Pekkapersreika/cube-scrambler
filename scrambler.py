import tkinter as tk
from tkinter import *
import random
import csv
import os


fakeCsv = []
#start = ""
#stop = ""
#Calculates the final time of the solve
def final_time(input_start, input_stop):
    global start
    global stop

    finaltime = float(input_start)-float(input_stop)
    finaltime = float(round(finaltime,3))
    result = ""
    result += (str(finaltime))

    StopWatch.config(text = result)
    start = ""
    stop = ""
    scrambleDict["Time"] = result
    if(sessionDictionary['Solves'] == "-"):
        sessionDictionary['Solves'] = str(1)
    else:
        sessionDictionary['Solves'] = str(int(sessionDictionary['Solves']) + 1)
    #fakeCsv.append(scrambleDict)
    update_scrambles()
    update_widgets() 
    set_scramble()
    window.bind("<space>", start_time)
#Starts the timer
def start_time(event = None):
    global start
    global running
    import time
    start = time.time()
    StopWatch.config(text = "Timing")
    window.bind("<space>", stop_time)
#Stops the timer
def stop_time(event = None):
    global stop
    import time
    stop = time.time()
    final_time(start, stop)
#Gets the next scramble
def get_scramble():
    global scrambleDict
    scrambleDict = {"Solve" : "",
                "Scramble" : "",
                "Time" : ""}
    scramble = ""
    
    movesList = ["U", "U'", "U2",
                 "D", "D'", "D2",
                 "R", "R'", "R2",
                 "L", "L'", "L2",
                 "F", "F'", "F2",
                 "B", "B'", "B2"]
    scrambleLength = 20

    for x in range(scrambleLength):
        scramble += random.choice(movesList) + " "
    scrambleDict["Solve"] = sessionDictionary["Solves"]
    scrambleDict["Scramble"] = scramble
    return scramble
#Sets the scramble to Scramble label
def set_scramble():
    Scramble.config(text=get_scramble())
#Create Session.csv
def create_sessioncsv():
    createSessionDict = {
            'Solves': '-',
            'Best': '-',
            'Best Ao5': '-',
            'Best Ao12': '-',
            'Session Avg': '-',
            'Worst': '-',
            'Ao5': '-',
            'Ao12': '-'
        }
    field_names = list(createSessionDict.keys())
    with open(os.path.join(os.path.dirname(__file__), 'Session.csv'), mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = field_names, delimiter= ';')
        writer.writeheader()
        writer.writerow(createSessionDict)
    session_dictionary()
#Create Scrambles.csv
def create_scramblecsv():
    field_names = ['Solve', 'Scramble', 'Time']
    with open(os.path.join(os.path.dirname(__file__), 'Scrambles.csv'), mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = field_names, delimiter= ';')
        writer.writeheader()
    update_scrambles()
#Session dictionary
def session_dictionary():
    #Creates a dictionary from Session.csv
    global sessionDictionary
    sessionDictionary = {}
    if(os.path.isfile(os.path.join(os.path.dirname(__file__), 'Session.csv')) == TRUE):
        with open(os.path.join(os.path.dirname(__file__), 'Session.csv'), mode='r', encoding='utf-8') as file:
            csvFile = csv.DictReader(file, delimiter = ';')
            for row in csvFile:
                sessionDictionary = row
    else:
        create_sessioncsv()

#Updates widgets
def update_widgets():
    Solves.config(text = "Solves: " + sessionDictionary['Solves'])
    Best.config(text = "Best: " + sessionDictionary['Best'])
    BestAo5.config(text = "Best Ao5: " + sessionDictionary['Best Ao5'])
    BestAo12.config(text = "Best Ao12: " + sessionDictionary['Best Ao12'])
    SessionAvg.config(text = "Session Avg: " + sessionDictionary['Session Avg'])
    Worst.config(text = "Worst: " + sessionDictionary['Worst'])
    Ao5.config(text = "Ao5: " + sessionDictionary['Ao5'])
    Ao12.config(text = "Ao12: " + sessionDictionary['Ao12'])
#Updates Scrambles.csv
def update_scrambles():
    field_names = list(scrambleDict.keys())
    if(os.path.isfile(os.path.join(os.path.dirname(__file__), 'Scrambles.csv')) == TRUE):
        with open(os.path.join(os.path.dirname(__file__), 'Scrambles.csv'), mode='a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = field_names, delimiter= ';')
            writer.writerow(scrambleDict)
    else:
        create_scramblecsv()
#On window close updates the session csv
def update_session():
    field_names = list(sessionDictionary.keys())
    with open(os.path.join(os.path.dirname(__file__), 'Session.csv'), mode='a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = field_names, delimiter= ';')
        writer.writerow(sessionDictionary)
    window.destroy()

window = tk.Tk()
window.geometry("600x900")
window.title("Cube scrambler")
window.configure(background="#323232")
session_dictionary()

Scramble = tk.Label(text=get_scramble(),
         background="#323232",
         foreground="#fff",
         font="Sagoe 18")

StopWatch = tk.Label(text="0.0",
         background="#323232",
         foreground="#fff",
         font="Lcd 50")

Solves = tk.Label(text="Solves: " + str(sessionDictionary['Solves']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")

Best = tk.Label(text="Best: "  + str(sessionDictionary['Best']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")

BestAo5 = tk.Label(text="Best Ao5: "  + str(sessionDictionary['Best Ao5']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")

BestAo12 = tk.Label(text="Best Ao12: "  + str(sessionDictionary['Best Ao12']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")

SessionAvg = tk.Label(text="Session Avg: "  + str(sessionDictionary['Session Avg']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")

Worst = tk.Label(text="Worst: "  + str(sessionDictionary['Worst']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")

Ao5 = tk.Label(text="Ao5: "  + str(sessionDictionary['Ao5']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")

Ao12 = tk.Label(text="Ao12: "  + str(sessionDictionary['Ao12']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")

Scramble.place(relx=0.5, rely=0.25, anchor="center")
window.bind("<space>", start_time)
StopWatch.place(relx=0.5, rely=0.5, anchor="center")
Solves.place(relx=0.10, rely=0.75, anchor="nw")
Best.place(relx=0.10, rely=0.8, anchor="nw")
BestAo5.place(relx=0.10, rely=0.85, anchor="nw")
BestAo12.place(relx=0.10, rely=0.9, anchor="nw")
SessionAvg.place(relx=0.9, rely=0.75, anchor="ne")
Worst.place(relx=0.9, rely=0.8, anchor="ne")
Ao5.place(relx=0.9, rely=0.85, anchor="ne")
Ao12.place(relx=0.9, rely=0.9, anchor="ne")

window.protocol("WM_DELETE_WINDOW", update_session)
window.mainloop()
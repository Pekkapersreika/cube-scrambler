import tkinter as tk
from tkinter import *
import random
import csv
import os

start = ""
stop = ""
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
    sessionDictionary['Solves'] = str(int(sessionDictionary['Solves']) + 1)
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
    return scramble
#Sets the scramble to Scramble label
def set_scramble():
    Scramble.config(text=get_scramble())
#Session dictionary
def session_dictionary():
    #Creates a dictionary from Session.csv
    global sessionDictionary
    sessionDictionary = {}
    with open(os.path.join(os.path.dirname(__file__), 'Session.csv'), mode='r', encoding='utf-8') as file:
        csvFile = csv.DictReader(file, delimiter = ';')
        for row in csvFile:
            sessionDictionary = row
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

window.mainloop()
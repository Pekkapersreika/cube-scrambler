import tkinter as tk
from tkinter import *
import random

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


window = tk.Tk()
window.geometry("600x900")
window.title("Cube scrambler")
window.configure(background="#323232")

Scramble = tk.Label(text=get_scramble(),
         background="#323232",
         foreground="#fff",
         font="Sagoe 18")
Scramble.place(relx=0.5, rely=0.25, anchor="center")

StopWatch = tk.Label(text="0.0",
         background="#323232",
         foreground="#fff",
         font="Lcd 50")

Solves = tk.Label(text="Solves:",
         background="#323232",
         foreground="#fff",
         font="Sagoe 15").place(relx=0.10, rely=0.75, anchor="nw")

Best = tk.Label(text="Best:",
         background="#323232",
         foreground="#fff",
         font="Sagoe 15").place(relx=0.10, rely=0.8, anchor="nw")

BestAo5 = tk.Label(text="Best Ao5:",
         background="#323232",
         foreground="#fff",
         font="Sagoe 15").place(relx=0.10, rely=0.85, anchor="nw")

BestAo12 = tk.Label(text="Best Ao12:",
         background="#323232",
         foreground="#fff",
         font="Sagoe 15").place(relx=0.10, rely=0.9, anchor="nw")

SessionAvg = tk.Label(text="Session Avg:",
         background="#323232",
         foreground="#fff",
         font="Sagoe 15").place(relx=0.9, rely=0.75, anchor="ne")

Worst = tk.Label(text="Worst:",
         background="#323232",
         foreground="#fff",
         font="Sagoe 15").place(relx=0.9, rely=0.8, anchor="ne")

Ao5 = tk.Label(text="Ao5:",
         background="#323232",
         foreground="#fff",
         font="Sagoe 15").place(relx=0.9, rely=0.85, anchor="ne")

Ao12 = tk.Label(text="Ao12:",
         background="#323232",
         foreground="#fff",
         font="Sagoe 15").place(relx=0.9, rely=0.9, anchor="ne")

window.bind("<space>", start_time)
StopWatch.place(relx=0.5, rely=0.5, anchor="center")
window.mainloop()
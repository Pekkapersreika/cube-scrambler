import tkinter as tk
import random
import csv
import os
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker

# Dictionary to keep track of line visibility in the plot
line_visibility = {'Line2D(Time)': True, 'Line2D(Ao5)': False, 'Line2D(Ao12)': False}

# Function to calculate the final time
def final_time(input_start, input_stop):
    finaltime = float(input_start) - float(input_stop)
    finaltime = float(round(finaltime, 2) / -1)
    result = str(finaltime)
    sessionTimes.append(finaltime)
    StopWatch.config(text=result)
    scrambleDict["Time"] = result
    if sessionDictionary['Best'] == '-':
        sessionDictionary['Best'] = result
    if sessionDictionary['Worst'] == '-':
        sessionDictionary['Worst'] = result
    if sessionDictionary['Solves'] == '-':
        sessionDictionary['Solves'] = str(1)
    else:
        sessionDictionary['Solves'] = str(int(sessionDictionary['Solves']) + 1)
    check_results(finaltime)
    update_scrambles()
    update_widgets()
    set_scramble()
    window.bind("<space>", start_time)

# Function to start the timer
def start_time(event=None):
    global start
    start = time.time()
    StopWatch.config(text="Timing")
    window.bind("<space>", stop_time)

# Function to stop the timer
def stop_time(event=None):
    stop = time.time()
    final_time(start, stop)

# Function to generate a random scramble
def get_scramble():
    global scrambleDict
    scrambleDict = {"Solve": "", "Scramble": "", "Time": ""}
    scramble = ""
    scrambleList = []
    index = 0
    movesList = ["U", "U'", "U2",
                 "D", "D'", "D2",
                 "R", "R'", "R2",
                 "L", "L'", "L2",
                 "F", "F'", "F2",
                 "B", "B'", "B2"]
    scrambleLength = 20
    while index < scrambleLength:
        scrambleList.append(random.choice(movesList))
        if index == 0 and len(scrambleList) == 1:
            index += 1
        else:
            if scrambleList[index][0] == scrambleList[index - 1][0]:
                del scrambleList[-1]
            else:
                index += 1
    if sessionDictionary["Solves"] == "-":
        scrambleDict["Solve"] = "1"
    else:
        scrambleDict["Solve"] = str(int(sessionDictionary["Solves"]) + 1)
    scramble = ' '.join(scrambleList)
    scrambleDict["Scramble"] = scramble
    return scramble

# Function to set the scramble in the GUI
def set_scramble():
    Scramble.config(text=get_scramble())

# Function to create a CSV file for the session
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
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
        writer.writeheader()
        writer.writerow(createSessionDict)
    session_dictionary()

# Function to create a CSV file for scrambles
def create_scramblecsv():
    field_names = ['Solve', 'Scramble', 'Time']
    with open(os.path.join(os.path.dirname(__file__), 'Scrambles.csv'), mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
        writer.writeheader()
    update_scrambles()

# Function to load session dictionary from CSV
def session_dictionary():
    global sessionDictionary
    sessionDictionary = {}
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'Session.csv')):
        with open(os.path.join(os.path.dirname(__file__), 'Session.csv'), mode='r', encoding='utf-8') as file:
            csvFile = csv.DictReader(file, delimiter=';')
            for row in csvFile:
                sessionDictionary = row
    else:
        create_sessioncsv()

# Function to initialize times list from CSV
def initialize_times_list():
    global sessionTimes
    sessionTimes = []
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'Scrambles.csv')):
        with open(os.path.join(os.path.dirname(__file__), 'Scrambles.csv'), mode='r', encoding='utf-8', newline='') as file:
            csvFile = csv.DictReader(file, delimiter=';')
            for row in csvFile:
                sessionTimes.append(float(row['Time']))
    else:
        sessionTimes = []

# Function to update widgets with session information
def update_widgets():
    Solves.config(text="Solves: " + sessionDictionary['Solves'])
    Best.config(text="Best: " + sessionDictionary['Best'])
    BestAo5.config(text="Best Ao5: " + str(sessionDictionary['Best Ao5']))
    BestAo12.config(text="Best Ao12: " + str(sessionDictionary['Best Ao12']))
    SessionAvg.config(text="Session Avg: " + str(sessionDictionary['Session Avg']))
    Worst.config(text="Worst: " + sessionDictionary['Worst'])
    Ao5.config(text="Ao5: " + str(sessionDictionary['Ao5']))
    Ao12.config(text="Ao12: " + str(sessionDictionary['Ao12']))

# Function to update the scrambles CSV
def update_scrambles():
    field_names = list(scrambleDict.keys())
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'Scrambles.csv')):
        with open(os.path.join(os.path.dirname(__file__), 'Scrambles.csv'), mode='a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
            writer.writerow(scrambleDict)
    else:
        create_scramblecsv()

# Function to update the session CSV
def update_session():
    field_names = list(sessionDictionary.keys())
    with open(os.path.join(os.path.dirname(__file__), 'Session.csv'), mode='a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
        writer.writerow(sessionDictionary)
    window.destroy()

# Function to check results and update session dictionary
def check_results(timeToCheck):
    if float(sessionDictionary['Best']) > timeToCheck:
        sessionDictionary['Best'] = str(timeToCheck)
    if float(sessionDictionary['Worst']) < timeToCheck:
        sessionDictionary['Worst'] = str(timeToCheck)
    calc_average()
    calc_ao5()
    calc_ao12()

# Function to calculate the session average
def calc_average():
    if len(sessionTimes) > 3:
        result = 0
        best = float(sessionDictionary['Best'])
        worst = float(sessionDictionary['Worst'])
        for time in sessionTimes:
            result += float(time)
        result = result - best
        result = result - worst
        result = result / (len(sessionTimes) - 2)
        sessionDictionary['Session Avg'] = round(result, 2)

# Function to calculate the Ao5
def calc_ao5():
    if len(sessionTimes) > 4:
        ao5List = sessionTimes[(len(sessionTimes) - 5)::]
        ao5List.sort()
        best = ao5List[0]
        worst = ao5List[4]
        result = 0
        for item in ao5List:
            result += item
        result = result - best
        result = result - worst
        result = result / 3
        sessionDictionary['Ao5'] = round(result, 2)
        if sessionDictionary['Best Ao5'] == '-' or float(sessionDictionary['Best Ao5']) > float(sessionDictionary['Ao5']):
            sessionDictionary['Best Ao5'] = round(result, 2)

# Function to calculate the Ao12
def calc_ao12():
    if len(sessionTimes) > 11:
        ao12List = sessionTimes[(len(sessionTimes) - 12)::]
        ao12List.sort()
        best = ao12List[0]
        worst = ao12List[11]
        result = 0
        for item in ao12List:
            result += item
        result = result - best
        result = result - worst
        result = result / 10
        sessionDictionary['Ao12'] = round(result, 2)
        if sessionDictionary['Best Ao12'] == '-' or float(sessionDictionary['Best Ao12']) > float(sessionDictionary['Ao12']):
            sessionDictionary['Best Ao12'] = round(result, 2)

# Function to plot the graph
def plot_graph(event=None):
    global scatter, timeLine, ao5Line, ao12Line, line_visibility
    hide_stuff()
    window.geometry("1000x900")
    nmbr = []
    i = 1
    for item in sessionTimes:
        nmbr.append(i)
        i += 1
    df1 = {
        'Solve': nmbr,
        'Time': sessionTimes,
    }
    ao5_list = []
    ao5_indices = []
    if len(sessionTimes) >= 5:
        for j in range(len(sessionTimes) - 4):
            ao5_list.append(sum(sessionTimes[j:j + 5]) / 5)
            ao5_indices.append(j + 4)
    ao12_list = []
    ao12_indices = []
    if len(sessionTimes) >= 12:
        for j in range(len(sessionTimes) - 11):
            ao12_list.append(sum(sessionTimes[j:j + 12]) / 12)
            ao12_indices.append(j + 11)
    i = 0
    figure = plt.Figure(figsize=(10, 10), facecolor="#323232")
    scatter = FigureCanvasTkAgg(figure, window)
    scatter.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")
    ax1 = figure.add_subplot(111)
    timeLine, = ax1.plot(df1['Solve'], df1['Time'], color='#fff', marker='.', label='Time')
    ao5Line, = ax1.plot(ao5_indices, ao5_list, color='red', marker='', label='Ao5', visible=line_visibility["Line2D(Ao5)"])
    ao12Line, = ax1.plot(ao12_indices, ao12_list, color='green', marker='', label='Ao12', visible=line_visibility["Line2D(Ao12)"])
    xcoords = df1['Solve']
    ycoords = df1["Time"]
    for item in ycoords:
        ax1.text(xcoords[i], item + 0.005, str(item), horizontalalignment="center")
        i += 1
    ax1.set_xlabel('Number of solves')
    ax1.set_ylabel('Time')
    ax1.set_title('Times in session')
    ax1.set_facecolor("#323232")
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax1.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    leg = ax1.legend()
    leg.get_frame().set_alpha(0.4)
    leg.legendHandles[1].set_visible(True)
    leg.legendHandles[2].set_visible(True)
    lines = [timeLine, ao5Line, ao12Line]
    lined = dict()
    for legline, origline in zip(leg.get_lines(), lines):
        legline.set_picker(5)
        lined[legline] = origline
    def onpick(event):
        global line_visibility
        origline = lined[event.artist]
        vis = not origline.get_visible()
        origline.set_visible(vis)
        if origline == timeLine:
            for text in ax1.texts:
                text.set_visible(vis)
        if vis:
            event.artist.set_alpha(1.0)
        else:
            event.artist.set_alpha(0.2)
        line_name = str(origline)
        line_visibility[line_name] = vis
        scatter.draw()
    scatter.mpl_connect('pick_event', onpick)
    window.bind("<c>", show_stuff)

# Function to hide widgets
def hide_stuff():
    Scramble.place_forget()
    StopWatch.place_forget()
    Solves.place_forget()
    Best.place_forget()
    BestAo5.place_forget()
    BestAo12.place_forget()
    SessionAvg.place_forget()
    Worst.place_forget()
    Ao5.place_forget()
    Ao12.place_forget()

# Function to show widgets
def show_stuff(event=None):
    global scatter, timeLine, ao5Line, ao12Line
    window.geometry("600x900")
    scatter.get_tk_widget().destroy()
    Scramble.place(relx=0.5, rely=0.25, anchor="center")
    window.bind("<space>", start_time)
    window.bind("<c>", plot_graph)
    StopWatch.place(relx=0.5, rely=0.5, anchor="center")
    Solves.place(relx=0.10, rely=0.75, anchor="nw")
    Best.place(relx=0.10, rely=0.8, anchor="nw")
    BestAo5.place(relx=0.10, rely=0.85, anchor="nw")
    BestAo12.place(relx=0.10, rely=0.9, anchor="nw")
    SessionAvg.place(relx=0.9, rely=0.75, anchor="ne")
    Worst.place(relx=0.9, rely=0.8, anchor="ne")
    Ao5.place(relx=0.9, rely=0.85, anchor="ne")
    Ao12.place(relx=0.9, rely=0.9, anchor="ne")

# Initializing the Tkinter window
window = tk.Tk()
window.geometry("600x900")
window.title("Cube scrambler")
window.configure(background="#323232")
session_dictionary()
initialize_times_list()

# Creating and placing labels for GUI
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

# Placing labels in the window
Scramble.place(relx=0.5, rely=0.25, anchor="center")
window.bind("<space>", start_time)
window.bind("<c>", plot_graph)
StopWatch.place(relx=0.5, rely=0.5, anchor="center")
Solves.place(relx=0.10, rely=0.75, anchor="nw")
Best.place(relx=0.10, rely=0.8, anchor="nw")
BestAo5.place(relx=0.10, rely=0.85, anchor="nw")
BestAo12.place(relx=0.10, rely=0.9, anchor="nw")
SessionAvg.place(relx=0.9, rely=0.75, anchor="ne")
Worst.place(relx=0.9, rely=0.8, anchor="ne")
Ao5.place(relx=0.9, rely=0.85, anchor="ne")
Ao12.place(relx=0.9, rely=0.9, anchor="ne")

# Binding the window closure to update_session function
window.protocol("WM_DELETE_WINDOW", update_session)
window.mainloop()  # Starting the Tkinter event loop

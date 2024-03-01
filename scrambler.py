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
    session_times.append(finaltime)
    StopWatch.config(text=result)
    scramble_dict["Time"] = result
    if session_dictionary['Best'] == '-':
        session_dictionary['Best'] = result
    if session_dictionary['Worst'] == '-':
        session_dictionary['Worst'] = result
    if session_dictionary['Solves'] == '-':
        session_dictionary['Solves'] = str(1)
    else:
        session_dictionary['Solves'] = str(int(session_dictionary['Solves']) + 1)
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
    global scramble_dict
    scramble_dict = {"Solve": "", "Scramble": "", "Time": ""}
    scramble = ""
    scramblelist = []
    index = 0
    movesList = ["U", "U'", "U2",
                 "D", "D'", "D2",
                 "R", "R'", "R2",
                 "L", "L'", "L2",
                 "F", "F'", "F2",
                 "B", "B'", "B2"]
    scrambleLength = 20
    while index < scrambleLength:
        scramblelist.append(random.choice(movesList))
        if index == 0 and len(scramblelist) == 1:
            index += 1
        else:
            if scramblelist[index][0] == scramblelist[index - 1][0]:
                del scramblelist[-1]
            else:
                index += 1
    if session_dictionary["Solves"] == "-":
        scramble_dict["Solve"] = "1"
    else:
        scramble_dict["Solve"] = str(int(session_dictionary["Solves"]) + 1)
    scramble = ' '.join(scramblelist)
    scramble_dict["Scramble"] = scramble
    return scramble

# Function to set the scramble in the GUI
def set_scramble():
    Scramble.config(text=get_scramble())

# Function to create a CSV file for the session
def create_sessioncsv():
    create_session_dict = {
            'Solves': '-',
            'Best': '-',
            'Best Ao5': '-',
            'Best Ao12': '-',
            'Session Avg': '-',
            'Worst': '-',
            'Ao5': '-',
            'Ao12': '-'
        }
    field_names = list(create_session_dict.keys())
    with open(os.path.join(os.path.dirname(__file__), 'Session.csv'), mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
        writer.writeheader()
        writer.writerow(create_session_dict)
    init_session_dictionary()

# Function to create a CSV file for scrambles
def create_scramblecsv():
    field_names = ['Solve', 'Scramble', 'Time']
    with open(os.path.join(os.path.dirname(__file__), 'Scrambles.csv'), mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
        writer.writeheader()
    update_scrambles()

# Function to load session dictionary from CSV
def init_session_dictionary():
    global session_dictionary
    session_dictionary = {}
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'Session.csv')):
        with open(os.path.join(os.path.dirname(__file__), 'Session.csv'), mode='r', encoding='utf-8') as file:
            csvFile = csv.DictReader(file, delimiter=';')
            for row in csvFile:
                session_dictionary = row
    else:
        create_sessioncsv()

# Function to initialize times list from CSV
def initialize_times_list():
    global session_times
    session_times = []
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'Scrambles.csv')):
        with open(os.path.join(os.path.dirname(__file__), 'Scrambles.csv'), mode='r', encoding='utf-8', newline='') as file:
            csvFile = csv.DictReader(file, delimiter=';')
            for row in csvFile:
                session_times.append(float(row['Time']))
                time_frames(row["Solve"], row["Scramble"], row["Time"])
    else:
        session_times = []

# Function to update widgets with session information
def update_widgets():
    Solves.config(text="Solves: " + session_dictionary['Solves'])
    Best.config(text="Best: " + session_dictionary['Best'])
    BestAo5.config(text="Best Ao5: " + str(session_dictionary['Best Ao5']))
    BestAo12.config(text="Best Ao12: " + str(session_dictionary['Best Ao12']))
    SessionAvg.config(text="Session Avg: " + str(session_dictionary['Session Avg']))
    Worst.config(text="Worst: " + session_dictionary['Worst'])
    Ao5.config(text="Ao5: " + str(session_dictionary['Ao5']))
    Ao12.config(text="Ao12: " + str(session_dictionary['Ao12']))

# Function to update the scrambles CSV
def update_scrambles():
    field_names = list(scramble_dict.keys())
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'Scrambles.csv')):
        with open(os.path.join(os.path.dirname(__file__), 'Scrambles.csv'), mode='a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
            writer.writerow(scramble_dict)
        time_frames(scramble_dict["Solve"], scramble_dict["Scramble"], scramble_dict["Time"])

    else:
        create_scramblecsv()

# Function to update the session CSV
def update_session():
    field_names = list(session_dictionary.keys())
    with open(os.path.join(os.path.dirname(__file__), 'Session.csv'), mode='a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
        writer.writerow(session_dictionary)
    window.destroy()

# Function to check results and update session dictionary
def check_results(timeToCheck):
    if float(session_dictionary['Best']) > timeToCheck:
        session_dictionary['Best'] = str(timeToCheck)
    if float(session_dictionary['Worst']) < timeToCheck:
        session_dictionary['Worst'] = str(timeToCheck)
    calc_average()
    calc_ao5()
    calc_ao12()

# Function to calculate the session average
def calc_average():
    if len(session_times) > 3:
        result = 0
        best = float(session_dictionary['Best'])
        worst = float(session_dictionary['Worst'])
        for time in session_times:
            result += float(time)
        result = result - best
        result = result - worst
        result = result / (len(session_times) - 2)
        session_dictionary['Session Avg'] = round(result, 2)

# Function to calculate the Ao5
def calc_ao5():
    if len(session_times) > 4:
        ao5List = session_times[(len(session_times) - 5)::]
        ao5List.sort()
        best = ao5List[0]
        worst = ao5List[4]
        result = 0
        for item in ao5List:
            result += item
        result = result - best
        result = result - worst
        result = result / 3
        session_dictionary['Ao5'] = round(result, 2)
        if session_dictionary['Best Ao5'] == '-' or float(session_dictionary['Best Ao5']) > float(session_dictionary['Ao5']):
            session_dictionary['Best Ao5'] = round(result, 2)

# Function to calculate the Ao12
def calc_ao12():
    if len(session_times) > 11:
        ao12List = session_times[(len(session_times) - 12)::]
        ao12List.sort()
        best = ao12List[0]
        worst = ao12List[11]
        result = 0
        for item in ao12List:
            result += item
        result = result - best
        result = result - worst
        result = result / 10
        session_dictionary['Ao12'] = round(result, 2)
        if session_dictionary['Best Ao12'] == '-' or float(session_dictionary['Best Ao12']) > float(session_dictionary['Ao12']):
            session_dictionary['Best Ao12'] = round(result, 2)

# Function to plot the graph
def plot_graph(event=None):
    global scatter, line_visibility
    hide_stuff()
    window.geometry("1000x900")
    nmbr = []
    i = 1
    for item in session_times:
        nmbr.append(i)
        i += 1
    df1 = {
        'Solve': nmbr,
        'Time': session_times,
    }
    ao5_list = []
    ao5_indices = []
    if len(session_times) >= 5:
        for j in range(len(session_times) - 4):
            ao5_list.append(sum(session_times[j:j + 5]) / 5)
            ao5_indices.append(j + 4)
    ao12_list = []
    ao12_indices = []
    if len(session_times) >= 12:
        for j in range(len(session_times) - 11):
            ao12_list.append(sum(session_times[j:j + 12]) / 12)
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
    #statsmenu.delete("Graph")

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
    hide_graph()
    hide_times()
def hide_times():
    try:
        solveLabel.place_forget()
        scrambleLabel.place_forget()    
        timeLabel.place_forget()
    except NameError:
        pass
    for item in labels:
        item.place_forget()

def hide_graph():
    global scatter
    window.geometry("600x900")
    try:
        scatter.get_tk_widget().destroy()
    except NameError:
        pass
# Function to show widgets
def show_timer(event=None):
    hide_stuff()
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


def show_times(event=None):
    global solveLabel, scrambleLabel, timeLabel

    # Ensure widgets are hidden
    hide_stuff()
    # Create and place labels
    solveLabel = tk.Label(window,
                          text="Solve:",
                          bg="#323232",
                          fg="#fff",
                          font="Sagoe 15")
    solveLabel.place(relx=0, rely=0, anchor="nw")

    scrambleLabel = tk.Label(window,
                          text="Scramble:",
                          bg="#323232",
                          fg="#fff",
                          font="Sagoe 15")
    scrambleLabel.place(relx=0.48, rely=0, anchor="n")

    timeLabel = tk.Label(window,
                          text="Time:",
                          bg="#323232",
                          fg="#fff",
                          font="Sagoe 15")
    timeLabel.place(relx=0.975, rely=0, anchor="ne")

    # Place labels dynamically
    y = 0
    i = 0
    step = 1 / (len(session_times) + 0.75)
    dynamic_height = 27.4 * len(session_times)
    inner_frame.config(height=dynamic_height)
    while i < len(labels) - 2:
        labels[i].place(relx=0, rely=y, anchor="nw")
        labels[i + 1].place(relx=0.48, rely=y, anchor="n")
        labels[i + 2].place(relx=0.975, rely=y, anchor="ne")
        y += step
        i += 3
    #while i < len(labels):
    #    labels[i].pack(fill="x")
    #    i += 1

    # Create canvas and inner frame
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    if (len(session_times) > 32):
        scrollbar.pack(side="right", fill="y")

    inner_frame.update_idletasks()  # Ensure widgets inside inner_frame are properly sized
    canvas.create_window((0, 0), window=inner_frame, anchor="nw", width=window.winfo_width())
    #inner_frame.config(width=100)
    #inner_frame.place(relx=0, rely=0)
    if (scrollbar.winfo_exists()):
    # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.config(scrollregion=canvas.bbox("all"))

    # Place container
    container.place(relx=0, rely=0.025, relwidth=1, relheight=1, anchor="nw")

def time_frames(solve, scramble, time):
    global labels
    time_frame = tk.Frame(inner_frame, height=28.125)

    #solveLabel = tk.Label(time_frame,
    #                      text=solve,
    #                      bg="#323232",
    #                      fg="#fff",
    #                      font="Sagoe 15",
    #                      width=3)
#
    ## Adjust the width of the scramble frame
    #scrambleLabel = tk.Label(time_frame,
    #                         text=scramble,
    #                         bg="#323232",
    #                         fg="#fff",
    #                         font="Sagoe 14",
    #                         width=45)
#
    #timeLabel = tk.Label(time_frame,
    #                     text=time,
    #                     bg="#323232",
    #                     fg="#fff",
    #                     font="Sagoe 15",
    #                     width=4)
    #
    solveLabel = tk.Label(inner_frame,
                          text=solve,
                          bg="#323232",
                          fg="#fff",
                          font="Sagoe 15")

    # Adjust the width of the scramble frame
    scrambleLabel = tk.Label(inner_frame,
                             text=scramble,
                             bg="#323232",
                             fg="#fff",
                             font="Sagoe 14",
                             width=45)

    timeLabel = tk.Label(inner_frame,
                         text=time,
                         bg="#323232",
                         fg="#fff",
                         font="Sagoe 15",
                         width=4)
    #solveLabel.place(relx=0, rely=0, anchor="nw")
    #scrambleLabel.place(relx=0.5, rely=0, anchor="n")
    #timeLabel.place(relx=1.0, rely=0, anchor="ne")
    #labels.append(time_frame)

    labels.append(solveLabel)
    labels.append(scrambleLabel)
    labels.append(timeLabel)

# Initializing the Tkinter window
window = tk.Tk()
window.geometry("600x900")
window.title("Cube scrambler")
window.configure(background="#323232")
window.update()
init_session_dictionary()


# Creating and placing labels for GUI
menubar = tk.Menu(window, tearoff=0)
menubar.add_command(label="Timer", command=show_timer)
statsmenu = tk.Menu(menubar, tearoff=0)
statsmenu.add_command(label="Times", command=show_times)
statsmenu.add_command(label="Graph", command=plot_graph)
#menubar.add_cascade(label="Timer", menu=timermenu)
menubar.add_cascade(label="Statistics", menu=statsmenu)
Scramble = tk.Label(text=get_scramble(),
         background="#323232",
         foreground="#fff",
         font="Sagoe 18")
StopWatch = tk.Label(text="0.0",
         background="#323232",
         foreground="#fff",
         font="Lcd 50")
Solves = tk.Label(text="Solves: " + str(session_dictionary['Solves']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")
Best = tk.Label(text="Best: "  + str(session_dictionary['Best']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")
BestAo5 = tk.Label(text="Best Ao5: "  + str(session_dictionary['Best Ao5']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")
BestAo12 = tk.Label(text="Best Ao12: "  + str(session_dictionary['Best Ao12']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")
SessionAvg = tk.Label(text="Session Avg: "  + str(session_dictionary['Session Avg']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")
Worst = tk.Label(text="Worst: "  + str(session_dictionary['Worst']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")
Ao5 = tk.Label(text="Ao5: "  + str(session_dictionary['Ao5']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")
Ao12 = tk.Label(text="Ao12: "  + str(session_dictionary['Ao12']),
         background="#323232",
         foreground="#fff",
         font="Sagoe 15")
container = tk.Frame(window, bg="#323232", borderwidth=0, highlightthickness=0)
canvas = tk.Canvas(container, bg="#323232", borderwidth=0, highlightthickness=0)
inner_frame = tk.Frame(canvas, bg="#323232")
#inner_frame = tk.Frame(canvas, bg="blue", height=window.winfo_height(), width=window.winfo_width())
#canvas.configure(scrollregion=canvas.bbox("all"))
labels = []
initialize_times_list()

show_timer()

# Binding the window closure to update_session function
window.protocol("WM_DELETE_WINDOW", update_session)
window.config(menu=menubar)
window.mainloop()  # Starting the Tkinter event loop

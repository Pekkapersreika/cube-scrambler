import tkinter as tk

window = tk.Tk()
window.geometry("600x900")
window.title("Cube scrambler")
window.configure(background="#323232")

Scramble = tk.Label(text="Scramble placeholder",
         background="#323232",
         foreground="#fff",
         font="Sagoe 20").place(relx=0.5, rely=0.25, anchor="center")

StopWatch = tk.Label(text="0.0",
         background="#323232",
         foreground="#fff",
         font="Lcd 50").place(relx=0.5, rely=0.5, anchor="center")

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

window.mainloop()
# Cube Timer

This is a simple cube timer application built using Python's Tkinter library for the GUI and matplotlib for plotting graphs. The timer allows users to time their Rubik's Cube solves, keep track of their session statistics, and visualize their solve times.

## Features

- Timer functionality with spacebar to start and stop timing.
- Random scramble generation for each solve.
- Session statistics tracking, including best time, worst time, average time, best Ao5 (Average of 5), best Ao12 (Average of 12), session average, Ao5, and Ao12.
- Visualization of solve times using a line plot graph.
- Exporting session data to CSV files for future analysis.

## Usage

1. Clone the repository to your local machine:

 ```console
 git clone https://github.com/Pekkapersreika/cube-scrambler.git
```

2. Run the application:

   Run by double clicking scrambler.exe in your destination folder

3. Use the spacebar to start and stop the timer, and 'c' to plot the graph. Click on the legend to toggle lines on or off

## File Structure

- `scrambler.exe`: Main application.
- `_internal`: Folder containing needed files to run
- `Session.csv`: CSV file to store session statistics in the _internal folder.
- `Scrambles.csv`: CSV file to store scramble data in the _internal folder.

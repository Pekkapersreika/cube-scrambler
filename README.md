# Cube Timer

This is a simple cube timer application built using Python's Tkinter library for the GUI and matplotlib for plotting graphs. The timer allows users to time their Rubik's Cube solves, keep track of their session statistics, and visualize their solve times.

## Features

- Timer functionality with spacebar to start and stop timing.
- Random scramble generation for each solve.
- Session statistics tracking, including best time, worst time, average time, best Ao5 (Average of 5), best Ao12 (Average of 12), session average, Ao5, and Ao12.
- Visualization of solve times using a line plot graph.
- Exporting session data to CSV files for future analysis.

## Requirements

- Python 3.x
- tkinter (for GUI)
- matplotlib (for plotting graphs)

## Usage

1. Clone the repository to your local machine:

 ```console
 git clone https://github.com/Pekkapersreika/cube-scrambler.git
```

3. Navigate to the project directory:

```console
cd yourpath\cube-scrambler
 ```

4. Run the application:

  ```console
python scrambler.py
```

5. Use the spacebar to start and stop the timer, and 'c' to plot the graph. Click on the legend to toggle lines on or off

## File Structure

- `scrambler.py`: Main Python script containing the cube timer application.
- `Session.csv`: CSV file to store session statistics.
- `Scrambles.csv`: CSV file to store scramble data.

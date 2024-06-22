Operating the GUI

Components
1. Amplitude Spin Box: Allows the user to set the amplitude of the sine wave. The range is
from 0 to 10000 and accepts float values.
2. Offset Spin Box: Allows the user to set the offset of the sine wave. The range is from 0
to 10000 and accepts float values.
3. Frequency Spin Box: Allows the user to set the frequency of the sine wave. The range is
from 0 to 10000 and accepts float values.
4. Start/Stop Button: Toggles the plotting of the sine wave. When pressed, it starts plotting
the sine wave. Pressing it again stops the plotting.
5. Plot Widget: Displays the real-time sine wave.
   
Instructions
1. Set Parameters:
o Use the amplitude spin box to set the desired amplitude.
o Use the offset spin box to set the desired offset.
o Use the frequency spin box to set the desired frequency.
2. Start Plotting:
o Press the "Start" button to begin plotting the sine wave. The button text will
change to "Stop".
o The y-axis range will dynamically adjust to offset - 4 * amplitude to offset + 4 * amplitude.
3. Stop Plotting:
o Press the "Stop" button to stop plotting the sine wave. The button text will change
back to "Start".
4. View Plot:
o Observe the plot widget. The x-axis spans the last 3 seconds of data, and the yaxis
adjusts based on the amplitude and offset settings.
Code Structure

Main Components
1. Window Class:
o Inherits from QWidget.
o Contains the main GUI layout and components.
o Handles user interactions and updates the plot based on user input.
2. Worker Class:
o Inherits from QThread.
o Generates sine wave data in a separate thread to keep the GUI responsive.
o Emits the generated data to the main thread for plotting.

Detailed Code Explanation
1. Imports:
o Necessary modules are imported, including PyQt5 for the GUI, numpy for
numerical operations, datetime for time handling, and pyqtgraph for plotting.
2. Window Class Initialization:
o __init__: Sets up the GUI components, connects signals and slots, and initializes
the worker thread.
o togglePlotting: Toggles the plotting state and starts/stops the worker thread.
o startPlotting: Starts plotting, sets the y-axis range, and initializes the worker
thread with the current parameters.
o stopPlotting: Stops plotting, makes spin boxes editable, and stops the worker
thread.
o save_data: Calls the worker's save_data method to save the generated data.
o update_plot: Updates the plot widget with new data and handles the x-axis
panning.
3. Worker Class Initialization:
o __init__: Initializes the worker thread, including parameters for amplitude,
offset, frequency, and data storage.
o render: Sets the rendering parameters and starts the thread.
o stop: Stops the thread by setting the exiting flag.
o run: Main loop for generating sine wave data and emitting it for plotting. This
runs in a separate thread.
o save_data: Saves the generated data to a .npy file with a timestamped filename.

Running the Application
1. Main Entry Point:
o The main entry point of the application initializes the QApplication, creates an
instance of the Window class, and runs the application loop.

Notes
> The data is saved every 60 seconds in .npy format with a timestamped filename.
> Any data produced within a 60-second save window is also saved if the program is
stopped between saves.

import sys
import numpy as np
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyqtgraph as pg

# Main Window class
class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        self.thread = Worker()  # Create a Worker thread instance
        self.plotting = False  # Flag to check if plotting is active
        self.timer = QTimer(self)  # QTimer to trigger data saving periodically
        self.timer.timeout.connect(self.save_data)  # Connect timer to save_data method

        # Create and set up UI components
        aLabel = QLabel("Amplitude:")
        oLabel = QLabel("Offset:")
        fLabel = QLabel("Frequency:")
        tLabel = QLabel("Sine Wave Real-Time")
        yLabel = QLabel("Amplitude")
        xLabel = QLabel("                Time (s)")
        self.aSpinBox = QDoubleSpinBox()
        self.oSpinBox = QDoubleSpinBox()
        self.fSpinBox = QDoubleSpinBox()
        
        # Set maximum values for spin boxes and default values
        self.aSpinBox.setMaximum(10000.0)
        self.aSpinBox.setValue(1.0)
        self.oSpinBox.setMaximum(10000.0)
        self.oSpinBox.setValue(0.0)
        self.fSpinBox.setMaximum(10000.0)
        self.fSpinBox.setValue(1.0)
        
        self.startStopButton = QPushButton("&Start")  # Start/Stop button
        self.viewer = pg.PlotWidget()  # Plot widget for displaying the sine wave
        self.viewer.setXRange(0, 3)  # Set initial x-axis range to 3 seconds
        
        self.thread.output.connect(self.update_plot)  # Connect thread output signal to update_plot method
        self.startStopButton.clicked.connect(self.togglePlotting)  # Connect button to togglePlotting method
        
        # Layout setup
        layout = QGridLayout()
        layout.addWidget(aLabel, 0, 0)
        layout.addWidget(self.aSpinBox, 0, 1)
        layout.addWidget(oLabel, 1, 0)
        layout.addWidget(self.oSpinBox, 1, 1)
        layout.addWidget(fLabel, 2, 0)
        layout.addWidget(self.fSpinBox, 2, 1)
        layout.addWidget(self.startStopButton, 3, 1)
        layout.addWidget(tLabel, 0, 5)
        layout.addWidget(xLabel, 10, 5)
        layout.addWidget(yLabel, 4, 2)
        layout.addWidget(self.viewer, 1, 3, 4, 5)

        self.setLayout(layout)  # Set the layout for the window
        self.setWindowTitle("Sine Wave Plotter")  # Set window title

    # Toggle the plotting state
    def togglePlotting(self):
        if not self.plotting:
            self.startPlotting()
        else:
            self.stopPlotting()

    # Start the plotting
    def startPlotting(self):
        self.aSpinBox.setReadOnly(True)  # Make amplitude input read-only
        self.oSpinBox.setReadOnly(True)  # Make offset input read-only
        self.fSpinBox.setReadOnly(True)  # Make frequency input read-only
        self.startStopButton.setText("Stop")  # Change button text to "Stop"
        self.plotting = True  # Set plotting flag to True
        amplitude = self.aSpinBox.value()
        offset = self.oSpinBox.value()
        self.viewer.setYRange(offset - 4 * amplitude, offset + 4 * amplitude)  # Set y-axis range based on amplitude and offset
        self.thread.render(self.viewer.size(), amplitude, offset, self.fSpinBox.value())  # Start the worker thread
        self.timer.start(60000)  # Save data every 60 seconds

    # Stop the plotting
    def stopPlotting(self):
        self.aSpinBox.setReadOnly(False)  # Make amplitude input editable
        self.oSpinBox.setReadOnly(False)  # Make offset input editable
        self.fSpinBox.setReadOnly(False)  # Make frequency input editable
        self.startStopButton.setText("Start")  # Change button text to "Start"
        self.plotting = False  # Set plotting flag to False
        self.thread.stop()  # Stop the worker thread
        self.save_data()  # Save any remaining data
        self.timer.stop()  # Stop the timer

    # Save data by calling worker's save_data method
    def save_data(self):
        self.thread.save_data()

    # Update the plot with new data
    def update_plot(self, x, y):
        if x[-1] <= 3:
            self.viewer.setXRange(0, 3)  # Keep x-axis fixed for the first 3 seconds
        else:
            self.viewer.setXRange(x[-1] - 3, x[-1])  # Pan the plot to follow the sine wave after 3 seconds
        self.viewer.plot(x, y, clear=True)

# Worker thread class
class Worker(QThread):
    output = pyqtSignal(np.ndarray, np.ndarray)  # Signal to emit sine wave data

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.exiting = False  # Flag to control the thread loop
        self.size = QSize(0, 0)  # Size of the plotting area
        self.amplitude = 0.0  # Amplitude of the sine wave
        self.offset = 0.0  # Offset of the sine wave
        self.frequency = 0.0  # Frequency of the sine wave
        self.data = []  # List to store sine wave data
        self.start_time = None  # Store the start time

    # Initialize rendering parameters and start the thread
    def render(self, size, amplitude, offset, frequency):
        self.size = size
        self.amplitude = amplitude
        self.offset = offset
        self.frequency = frequency
        self.exiting = False
        self.start_time = datetime.datetime.now()  # Record the start time
        self.start()

    # Stop the thread
    def stop(self):
        self.exiting = True

    # Main loop for generating sine wave data
    def run(self):
        while not self.exiting:
            current_time = datetime.datetime.now()
            elapsed_time = (current_time - self.start_time).total_seconds()
            x = np.linspace(max(0, elapsed_time - 3), elapsed_time, 1000)  # Generate x values from 0 to elapsed time
            y = self.amplitude * np.sin(2 * np.pi * self.frequency * x) + self.offset  # Generate y values for the sine wave
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")  # Get current timestamp
            self.data.append((timestamp, y.tolist()))  # Append timestamp and y values to data list
            self.output.emit(x, y)  # Emit the data for plotting
            QThread.msleep(50)  # Sleep for 50 milliseconds

    # Save data to a .npy file
    def save_data(self):
        date_str = datetime.datetime.now().strftime("%m%d%Y")  # Get current date as string
        structured_data = np.array(self.data, dtype=object)  # Convert data list to a numpy array
        np.save(f"sinewave_data_{date_str}.npy", structured_data)  # Save the array to a .npy file

# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create application
    window = Window()  # Create main window
    window.show()  # Show the window
    sys.exit(app.exec_())  # Run the application



import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import copy
import glob
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
from collections import deque
import matplotlib.animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from SerialUtils import *

def conv(lst):
    a = [str(x) for x in lst]
    print("".join(a))

class GUI(QMainWindow):
    def __init__(self):
        # Initialize the main window
        super(GUI, self).__init__()
        self.resize(800 , 600)
        self.setWindowTitle("Serial Interface")
        self.message = "Hello!"
        self._main = QWidget()
        self.setCentralWidget(self._main)
        self.layout = QVBoxLayout(self._main)
        self.recording = False


        # Get the port from a Dialog menu
        self.data = deque(maxlen=20000)
        self.saveData = []
        self.connect()

        # init layout
        self.vbox = QVBoxLayout()
        self.layout.addLayout(self.vbox)

        # Create figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.horizontal = QHBoxLayout()
        self.layout.addLayout(self.horizontal)
        self.horizontal.addWidget(self.canvas)

        # Set up animation and plot bounds
        ax = self.figure.add_subplot(111)
        self.ax = ax
        self.serialPlotter, = ax.plot([], [], lw=2)

        ax.set_ylim(0, 3500) # Analog
        # ax.set_ylim(-1, 2) # Digital
        ax.set_xlim(0, 200000)
        ani = matplotlib.animation.FuncAnimation(self.figure, self.updatefig,
                                                 interval=1, blit=True,
                                                 repeat_delay=1)
        self.colors = matplotlib.pyplot.rcParams['axes.prop_cycle'].by_key()['color']


        self.curFileName = ""
        self.SerialSendPanel()


    def updatefig(self, *args):
        a = list(self.data)
        self.serialPlotter.set_data(list(range(len(a))),a)
        return self.serialPlotter,

    def SerialSendPanel(self):
        # Create recording side and sending side
        hbox = QHBoxLayout()
        recordPanel = QVBoxLayout()
        sendPanel = QVBoxLayout()
        hbox.addLayout(recordPanel)
        hbox.addLayout(sendPanel)

        # Recording setup
        self.saveButton = QPushButton("Begin Recording") # bind function
        self.saveButton.clicked.connect(self.toggleRecording)
        self.fileField = QLineEdit()
        self.fileField.editingFinished.connect(self.setInputFile)
        self.curFile = QLabel("Filename: ")

        recordPanel.addWidget(self.saveButton)
        recordPanel.addWidget(self.fileField)
        recordPanel.addWidget(self.curFile)

        # recordPanel.addWidget(self.recordingState)


        # Serial sending setup
        self.sendButton = QPushButton("Send \"%s!\"" % self.message)
        self.sendButton.clicked.connect(lambda: self.sendSerial(self.message))
        sendPanel.addWidget(self.sendButton)


        self.vbox.addLayout(hbox)

    def sendSerial(self, message):
        self.serialThread.send_message(message)
        self.serialThread.RTS = True

    def setInputFile(self):
        if self.fileField.text() != "":
            self.curFileName = self.fileField.text() + ".txt"
            self.curFile.setText("Filename: " + self.curFileName)
            print("changed file to ", self.curFileName)
            self.fileField.clear()
            self.fileField.clearFocus()
            self.update()
            QApplication.processEvents()



    def toggleRecording(self):
        if self.serialThread.recording: # if stopping:
            self.serialPlotter.set_color(self.colors[0])
            self.serialThread.stop_recording()
            
            self.data = self.serialThread.dataHolder
            self.ax.relim()
            # self.ax.autoscale_view()

            self.curFileName = ""
            self.curFile.clear()
            self.curFile.setText("Filename: ")
            self.update()
            QApplication.processEvents()
        else:
            self.setInputFile()
            self.serialPlotter.set_color(self.colors[1])
            if self.curFileName != "":
                self.serialThread.start_recording(self.curFileName)
            else:
                self.serialThread.start_recording()


    def connect(self):
        connectDialog = Dialog()
        if connectDialog.exec_():
            self.selectedPort = connectDialog.dd.currentText()
            # self.serialThread = SerialThread(self.selectedPort,self.data, 115200)
            self.serialThread = SerialThread(self.selectedPort,self.data, 1152000)
            self.serialThread.start()
            self.show()
        else:
            sys.exit()



# Popup for selecting COM port
class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        layout = QVBoxLayout()

        # Make dropdown
        dropdownChoices = glob.glob("/dev/tty*")[::-1]
        self.dd = QComboBox()
        self.dd.addItems(dropdownChoices)
        self.formGroupBox = QGroupBox("")
        formbox = QFormLayout()
        formbox.addRow(QLabel("Available Ports"), self.dd)
        self.formGroupBox.setLayout(formbox)
        layout.addWidget(self.formGroupBox)

        # Create select and cancel button
        buttonHolder = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonHolder.accepted.connect(self.accept)
        buttonHolder.rejected.connect(self.reject)
        layout.addWidget(buttonHolder)

        # Set the layout
        self.setLayout(layout)
        self.setWindowTitle("Select COM Port")


def main():
   app = QApplication(sys.argv)
   ex = GUI()

   sys.exit(app.exec_())

if __name__ == '__main__':
   main()

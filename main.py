

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import serial
import sys
import glob
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
import os


import pyqtgraph as pg

import web3 as web

import numpy as np



class Data():
    def __init__(self):

        self.npoints = 0

        self.maxnpoints = 100000
        self.millis = np.empty(self.maxnpoints)

        self.date = np.empty(self.maxnpoints)
        self.time = np.empty(self.maxnpoints)

        self.seconds = np.empty(self.maxnpoints)
        self.latitude = np.empty(self.maxnpoints)
        self.longitude = np.empty(self.maxnpoints)
        self.speed = np.empty(self.maxnpoints,dtype=float)
        self.course = np.empty(self.maxnpoints,dtype=float)
        self.altitude = np.empty(self.maxnpoints,dtype=float)
        self.yaw = np.empty(self.maxnpoints,dtype=float)
        self.pitch = np.empty(self.maxnpoints,dtype=float)
        self.roll = np.empty(self.maxnpoints,dtype=float)
        self.fixqual = np.empty(self.maxnpoints,dtype=float)

        x = self.statistics()

    def statistics(self):
        self.date.mean = 4




def serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*') + glob.glob('/dev/ttyUSB[A-Za-z]*') + glob.glob('/dev/ttyACM[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class rightdockWidget(QWidget):
    def __init__(self, parent = None):
        super(rightdockWidget,self).__init__(parent)

        #Descriptive Labels
        self.latitudeLabel = QLabel("Latitude")
        self.longitudeLabel = QLabel("Longitude")
        self.speedLabel = QLabel("Speed:")
        self.timeLabel = QLabel("Time:")
        self.courseLabel = QLabel("Course:")
        self.yawLabel = QLabel("Yaw:")
        self.pitchLabel = QLabel("Pitch:")
        self.rollLabel = QLabel("Roll:")

        #Labels to hold the received value
        self.latvalLabel = QLabel()
        self.longvalLabel = QLabel()
        self.speedvalLabel = QLabel()
        self.timevalLabel = QLabel()
        self.coursevalLabel = QLabel()
        self.yawvalLabel = QLabel()
        self.pitchvalLabel = QLabel()
        self.rollvalLabel = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.latitudeLabel)
        layout.addWidget(self.latvalLabel)
        layout.addWidget(self.longitudeLabel)
        layout.addWidget(self.longvalLabel)
        layout.addWidget(self.speedLabel)
        layout.addWidget(self.speedvalLabel)
        layout.addWidget(self.timeLabel)
        layout.addWidget(self.timevalLabel)
        layout.addWidget(self.courseLabel)
        layout.addWidget(self.coursevalLabel)
        layout.addWidget(self.yawLabel)
        layout.addWidget(self.yawvalLabel)
        layout.addWidget(self.pitchLabel)
        layout.addWidget(self.pitchvalLabel)
        layout.addWidget(self.rollLabel)
        layout.addWidget(self.rollvalLabel)
        layout.addStretch()

        self.setLayout(layout)

class leftdockWidget(QWidget):

    signal_pushed = pyqtSignal()


    def __init__(self, parent = None):
        super(leftdockWidget,self).__init__(parent)

        #Descriptive Labels

        self.pbutton = QPushButton("Press:")

        layout = QVBoxLayout()
        layout.addWidget(self.pbutton)

        layout.addStretch()

        self.setLayout(layout)










class configSerialDialog(QDialog):
    def __init__(self,parent=None):
        super(configSerialDialog, self).__init__(parent)


        self.titleLabel = QLabel("Serial Setup")
        self.portlabel = QLabel("Serial Port:")
        self.comboboxPortlist = QComboBox()
        self.speedlabel = QLabel("Baudrate:")
        self.comboboxPortlist.addItems(serial_ports())
        self.comboboxSpeed = QComboBox()
        self.comboboxSpeed.addItems(("9600","19200","38400","56800","115200"))
        self.bytesizeLabel = QLabel("Bytesize")
        self.comboboxBytesize = QComboBox()
        self.comboboxBytesize.addItems(("8","5","6","7"))
        self.parityLabel = QLabel("Parity")
        self.comboboxParity = QComboBox()
        self.comboboxParity.addItems(("None","Even","Odd","Space","Mark"))
        self.stopbitLabel = QLabel("Stopbit")
        self.comboboxStopbit = QComboBox()
        self.comboboxStopbit.addItems(("1","1.5","2"))

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel| QDialogButtonBox.NoButton| QDialogButtonBox.Ok)

        buttonlayout = QGridLayout()
        buttonlayout.addWidget(self.titleLabel, 0, 0, 1, 2)
        buttonlayout.addWidget(self.portlabel,1,0)
        buttonlayout.addWidget(self.comboboxPortlist, 1, 1)
        buttonlayout.addWidget(self.speedlabel, 2, 0)
        buttonlayout.addWidget(self.comboboxSpeed, 2, 1)
        buttonlayout.addWidget(self.bytesizeLabel,3,0)
        buttonlayout.addWidget(self.comboboxBytesize,3,1)
        buttonlayout.addWidget(self.parityLabel,4,0)
        buttonlayout.addWidget(self.comboboxParity,4,1)
        buttonlayout.addWidget(self.stopbitLabel,5,0)
        buttonlayout.addWidget(self.comboboxStopbit,5,1)
        buttonlayout.addWidget(self.buttonBox,7,0,1,3)




        self.setLayout(buttonlayout)
        self.setWindowTitle("Serial Port Setup")

        self.connect(self.buttonBox,SIGNAL("accepted()"),SLOT("accept()"))
        self.connect(self.buttonBox,SIGNAL("rejected()"),SLOT("reject()"))




class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        #Program variables
        self.serialtimer = QTimer()
        self.serial1 = serial.Serial(None)
        self.serial1.timeout = 0.05

        self.filename = None

        ###########################################
        #Layout
        ###########################################

        #Upper tabs
        self.browser = QTextBrowser()
        self.browser.setMinimumSize(800, 400)
        self.webbrowser = QWebView()
        self.webbrowser.setHtml(web.html)
        #self.webbrowser.setUrl(QUrl("https://google-developers.appspot.com/maps/documentation/javascript/examples/map-simple"))
        self.uppertab = QTabWidget()
        self.uppertab.addTab(self.browser,"Serial Terminal")
        self.uppertab.addTab(self.webbrowser,"Maps")

        #Added comment

        #Graps for plotting
        self.yawgraph = pg.GraphicsWindow()
        self.yawgraph.setMinimumHeight(200)
        self.p1otyaw = self.yawgraph.addPlot(title="Yaw")
        self.rollgraph = pg.GraphicsWindow()
        self.rollgraph.setMinimumHeight(200)
        self.p1otroll = self.rollgraph.addPlot(title="Roll")
        self.pitchgraph = pg.GraphicsWindow()
        self.pitchgraph.setMinimumHeight(200)
        self.p1otpitch = self.pitchgraph.addPlot(title="Pitch")
        self.speedgraph = pg.GraphicsWindow()
        self.speedgraph.setMinimumHeight(200)
        self.p1otspeed = self.speedgraph.addPlot(title="Speed")
        self.coursegraph = pg.GraphicsWindow()
        self.coursegraph.setMinimumHeight(200)
        self.p1otcourse = self.coursegraph.addPlot(title="Course")



        #Tabs for graphs
        self.tabedgraph = QTabWidget()
        self.tabedgraph.addTab(self.yawgraph,"Yaw")
        self.tabedgraph.addTab(self.pitchgraph,"Pitch")
        self.tabedgraph.addTab(self.rollgraph,"Roll")
        self.tabedgraph.addTab(self.speedgraph,"Speed")
        self.tabedgraph.addTab(self.coursegraph,"Course")



        #Window Splitter
        self.mainWindowSplitter = QSplitter(Qt.Vertical)
        self.mainWindowSplitter.addWidget(self.uppertab)
        self.mainWindowSplitter.addWidget(self.tabedgraph)

        self.setCentralWidget(self.mainWindowSplitter)
        self.setWindowTitle("Serial Browser")

        ############################################
        #Actions
        #############################################

        openfileAction = self.createAction("Open File",self.openFile,"Ctrl + O","Icons/folder.svg")
        newfileAction = self.createAction("New File",self.newFile,"Ctrl + N","Icons/file.svg")
        savefileAction = self.createAction("Save File",self.saveFile,"Ctrl + S","Icons/data-transfer-download.svg")
        saveAsfileAction = self.createAction("Save File As",self.saveAs,"Ctrl + Q","Icons/data-transfer-download.svg")

        clearAction = self.createAction("Clear data",self.clearData,None,"Icons/trash.svg")


        serialconnectAction = self.createAction("&Connect", self.connectSerial,"Ctrl+C", "Icons/account-login.svg", "Connect")
        serialsetupAction = self.createAction("&Port Setup", self.configureSerial,"Ctrl+G", "Icons/wrench.svg", "Configure")
        serialdiscAction = self.createAction("&Disconnect", self.disconnectSerial,"Ctrl+D", "Icons/x.svg", "Disconnect")

        ##############################################
        #Menu and Toolbars setup
        ##############################################
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(openfileAction)
        self.fileMenu.addAction(newfileAction)
        self.fileMenu.addAction(savefileAction)
        self.fileMenu.addAction(saveAsfileAction)

        self.serialMenu = self.menuBar().addMenu("&Serial")
        self.serialMenu.addAction(serialconnectAction)
        self.serialMenu.addAction(serialsetupAction)
        self.serialMenu.addAction(serialdiscAction)

        self.actionMenu = self.menuBar().addMenu("&Actions")
        self.actionMenu.addAction(clearAction)


        self.serialToolbar = self.addToolBar("Edit")
        self.serialToolbar.setObjectName("SerialToolBar")
        self.serialToolbar.addAction(serialconnectAction)
        self.serialToolbar.addAction(serialdiscAction)
        self.serialToolbar.addAction(serialsetupAction)
        self.setWindowIcon(QIcon("Icons/Logo.png"))

        self.fileToolbar = self.addToolBar("File")
        self.fileToolbar.setObjectName("File Toolbar")
        self.fileToolbar.addAction(newfileAction)
        self.fileToolbar.addAction(openfileAction)
        self.fileToolbar.addAction(savefileAction)

        self.actionToolbar = self.addToolBar("Actions")
        self.actionToolbar.addAction(clearAction)

        ################################################
        #Main Window Docks
        ################################################
        logDockWidget = QDockWidget("Status", self)
        logDockWidget.setObjectName("StatusWidget")
        logDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        logDockWidget.setMinimumWidth(120)
        self.dock = rightdockWidget()
        logDockWidget.setWidget(self.dock)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)

        serialDockWidget = QDockWidget("Control",self)
        serialDockWidget.setObjectName("Serial Sender Widget")
        serialDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        serialDockWidget.setMinimumWidth(120)
        self.dock2 = leftdockWidget()
        serialDockWidget.setWidget(self.dock2)
        self.addDockWidget(Qt.LeftDockWidgetArea,serialDockWidget)


        self.connect(self.dock2.pbutton,SIGNAL("clicked()"),self.update_geo)
        self.connect(self.serialtimer,SIGNAL("timeout()"), self.readSerial)

    def showmarker(self):
        frame = self.webbrowser.page().currentFrame()
        frame.evaluateJavaScript(QString("addMarker("+unicode(-33.89)+","+unicode(151.275)+")"))

    def update_geo(self):
        # Capture coordinates of the last marker on the map.
        mark = self.webbrowser.page().mainFrame().evaluateJavaScript('document.getElementById("locationData").value').toString()
        # Convert string to list of floats, stripping parentheses.
        marker = str(mark).strip('()').split(', ')
        #decimals = [float(c) for c in marker]
        print(mark)



    def openFile(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', os.path.expanduser('~'))
        try:
            f = open(self.filename)
        except:
            return

        for line in f:
            if self.parseString(line):
                self.browser.insertPlainText(line)

        print(data.npoints)
        self.updateGraph()
        self.browser.verticalScrollBar().setValue(self.browser.verticalScrollBar().maximum())



    def newFile(self):
        print("New file!")

    def saveFile(self):
        if self.filename is None:
            self.saveAs()#self.filename = QFileDialog.getSaveFileName(self, 'Save File', os.path.expanduser('~'))
        else:
            f = open(self.filename, 'w')
            filedata = self.browser.toPlainText()
            f.write(filedata)
            f.close()

    def saveAs(self):
        self.filename = QFileDialog.getSaveFileName(self, 'Save File', os.path.expanduser('~'))
        self.saveFile()




    def updateGraph(self):
        self.p1otyaw.plot(data.millis[0:data.npoints-1], data.yaw[0:data.npoints-1], clear=True)
        self.p1otroll.plot(data.millis[0:data.npoints-1], data.roll[0:data.npoints-1], clear=True)
        self.p1otpitch.plot(data.millis[0:data.npoints-1], data.pitch[0:data.npoints-1], clear=True)
        self.p1otcourse.plot(data.millis[0:data.npoints-1], data.course[0:data.npoints-1], clear=True)
        self.p1otspeed.plot(data.millis[0:data.npoints-1], data.speed[0:data.npoints-1], clear=True)






    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def configureSerial(self):
        self.serialtimer.stop()
        dialog = configSerialDialog()
        if dialog.exec_():
            self.serial1.port = str(dialog.comboboxPortlist.currentText())
            self.serial1.baudrate = dialog.comboboxSpeed.currentText()

    def connectSerial(self):
        try:
            if not self.serial1.isOpen():
                self.serial1.open()
                self.serial1.flushInput()
                while self.serial1.inWaiting():
                    self.serial1.read(1)
                self.serialtimer.start(100)
        except:
            pass

    def disconnectSerial(self):
        if self.serial1.isOpen():
            self.serial1.close()
            self.serialtimer.stop()


    def updateUi(self):

        if data.latitude[data.npoints-1] > 0:
            self.dock.latvalLabel.setText(str(data.latitude[data.npoints-1])+" N")
        else:
            self.dock.latvalLabel.setText(str(abs(data.latitude[data.npoints-1]))+" S")

        if data.longitude[data.npoints-1] > 0:
            self.dock.longvalLabel.setText(str(data.longitude[data.npoints-1])+" E")
        else:
            self.dock.longvalLabel.setText(str(abs(data.longitude[data.npoints-1]))+" W")

        self.dock.speedvalLabel.setText(str(data.speed[data.npoints-1]))
        self.dock.coursevalLabel.setText(str(data.course[data.npoints-1]))
        self.dock.yawvalLabel.setText(str(data.yaw[data.npoints-1]))
        self.dock.rollvalLabel.setText(str(data.roll[data.npoints-1]))
        self.dock.pitchvalLabel.setText(str(data.pitch[data.npoints-1]))



    def readSerial(self):
        if not hasattr(self, "counter"):
            self.counter = 0  # it doesn't exist yet, so initialize it

        if self.counter > 5: #Ignores first 5 lines/calls
            text = self.serial1.readline()
            if self.parseString(text):
                self.browser.insertPlainText(text)
                self.browser.verticalScrollBar().setValue(self.browser.verticalScrollBar().maximum())
                self.updateUi()
                self.updateGraph()

        self.counter += 1

    def parseString(self, text): #TODO: Incorporate overflow control

        try:
            elements = text.split(',')
        except:
            return False

        if len(elements) == 18:
            #self.date
            #self.time
            data.seconds[data.npoints] = (float(elements[5])+float(elements[4])*60)*60 + float(elements[6])
            data.millis[data.npoints] = long(elements[0])


            latsign = 1
            lonsign = 1

            if elements[13] == 'W':
                lonsign = -1
            if elements[11] == 'S':
                latsign = -1

            data.speed[data.npoints] = elements[7]
            data.course[data.npoints] = elements[8]
            data.altitude[data.npoints] = elements[9]
            data.latitude[data.npoints] = float(elements[10])*latsign
            data.longitude[data.npoints] = float(elements[12])*lonsign
            data.fixqual[data.npoints] = elements[14]
            data.yaw[data.npoints] = elements[17]
            data.pitch[data.npoints] = elements[16]
            data.roll[data.npoints] = elements[15]

            data.npoints += 1

            return True

    def clearData(self):
        self.filename = None
        data.__init__()
        self.browser.clear()
        self.updateGraph()
        self.updateUi()







if __name__ == '__main__':
    data = Data()
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()

    app.exec_()
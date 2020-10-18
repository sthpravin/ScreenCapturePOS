import os
import sys
import cv2
import time
import tempfile
import threading
import pyperclip
import pytesseract
import numpy as np
import tkinter as tk
from shutil import rmtree
from PIL import Image, ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ecr_demo import h_lrc, ecrDemo


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'


class Capture_MainWindowUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(509, 234)
        MainWindow.resize(255, 117)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        # self.pushButton.setGeometry(QtCore.QRect(140, 40, 211, 61))
        self.pushButton.setGeometry(QtCore.QRect(70, 20, 105, 30))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralWidget)
        # self.menuBar = QtWidgets.QMenuBar(MainWindow)
        # self.menuBar.setGeometry(QtCore.QRect(0, 0, 509, 38))
        # self.menuBar.setObjectName("menuBar")
        # MainWindow.setMenuBar(self.menuBar)
        # self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        # self.mainToolBar.setObjectName("mainToolBar")
        # MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        # self.statusBar = QtWidgets.QStatusBar(MainWindow)
        # self.statusBar.setObjectName("statusBar")
        # MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Capture"))


class Pay_MainWindowUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(623, 273)
        MainWindow.resize(400, 100)
        MainWindow.setMaximumSize(QtCore.QSize(623, 16777215))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.payButton = QtWidgets.QPushButton(self.centralWidget)
        # self.payButton.setGeometry(QtCore.QRect(10, 70, 101, 61))
        self.payButton.setGeometry(QtCore.QRect(5, 25, 100, 50))
        self.payButton.setObjectName("payButton")
        self.labelStatus = QtWidgets.QLabel(self.centralWidget)
        # self.labelStatus.setGeometry(QtCore.QRect(460, 0, 81, 41))
        self.labelStatus.setGeometry(QtCore.QRect(280, 0, 100, 20))
        self.labelStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.labelStatus.setObjectName("labelStatus")
        self.viewStatus = QtWidgets.QLabel(self.centralWidget)
        # self.viewStatus.setGeometry(QtCore.QRect(410, 40, 201, 121))
        self.viewStatus.setGeometry(QtCore.QRect(280, 25, 100, 50))
        self.viewStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.viewStatus.setText("")
        self.viewStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.viewStatus.setWordWrap(True)
        self.viewStatus.setObjectName("viewStatus")
        self.payAmount = QtWidgets.QLabel(self.centralWidget)
        # self.payAmount.setGeometry(QtCore.QRect(130, 70, 261, 61))
        self.payAmount.setGeometry(QtCore.QRect(120, 25, 150, 50))
        self.payAmount.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Black))
        self.payAmount.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.payAmount.setText("")
        self.payAmount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.payAmount.setObjectName("payAmount")
        MainWindow.setCentralWidget(self.centralWidget)
        # self.menuBar = QtWidgets.QMenuBar(MainWindow)
        # self.menuBar.setGeometry(QtCore.QRect(0, 0, 623, 38))
        # self.menuBar.setObjectName("menuBar")
        # MainWindow.setMenuBar(self.menuBar)
        # self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        # self.mainToolBar.setObjectName("mainToolBar")
        # MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.payButton.setText(_translate("MainWindow", "Pay"))
        self.labelStatus.setText(_translate("MainWindow", "Status"))


class Snipper(QtWidgets.QWidget):
    snipped_signal = QtCore.pyqtSignal(tuple)
    def __init__(self, app):

        super().__init__()

    def start(self):
        root = tk.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.snipped_value = ""

        # self.show()

    def read_image(self, img):
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return pytesseract.image_to_string(gray, config=tessdata_dir_config), gray
        except TypeError:
            print("No image grabbed")
            return " ", 0 
        

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        text, img = self.read_image(np.array(img))
        self.snipped_value = text
        # pyperclip.copy(text)
        print("Snipped Value:::", text)
        print(x1, y1, x2, y2)
        QApplication.restoreOverrideCursor()

        # qp = QtGui.QPainter(self)
        # qp.setPen(QtGui.QPen(QtCore.black, 5, QtCore.SolidLine))
        # #painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        # qp.setBrush(QtGui.QBrush(QtCore .green, QtCore.DiagCrossPattern))
        # qp.drawRect(x1, y1, x2, y2)

        self.snipped_signal.emit((text, x1, y1, x2, y2))
        #cv2.imshow('Captured Image', img)
        #cv2.waitKey(10000)
        #cv2.destroyAllWindows()

    # def update(self):
    #     self.close()
    #     img = ImageGrab.grab(bbox=self.bbox)
    #     text, img = self.read_image(np.array(img))
    #     self.snipped_signal.emit(text)



class CaptureWindow(QtWidgets.QMainWindow, Capture_MainWindowUI):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.pushbutton_handler)

    def pushbutton_handler(self):
        self.switch_window.emit()


class PayWindow(QtWidgets.QMainWindow, Pay_MainWindowUI):
    
    # switch_window = QtCore.pyqtSignal()

    def __init__(self, app):
        self.app = app
        self.bbox = ()
        self.value = 0
        self.amount = 0
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        self.payButton.clicked.connect(self.paybutton_handler)

    def set_pay_value(self, value):
        self.bbox = (value[1], value[2], value[3], value[4])
        self.value = value[0]
        self.payAmount.setText(value[0])
        self.update()

    def show_current_value(self):
        self.payAmount.setText(self.value)
        self.update()

    def update_pay_value(self):
        # self.close()
        # time.sleep(.5)
        img = ImageGrab.grab(bbox=self.bbox)
        # img.save("box-{}.jpg".format(int(time.time())))
        gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, config=tessdata_dir_config)
        print("bbox value::", self.bbox)
        self.payAmount.setText(text)
        self.amount = text
        self.update()
        self.show()

    def paybutton_handler(self):
        self.update_pay_value()

        # try:

        amount = self.amount

        # print("amount in paybutton_handler::", amount, type(amount))

        ##init
        #self.myEcrDemo.processCommand(1)
        ##credit sale
        #self.myEcrDemo.processCommand(2)
        ##credit adjust tip
        # self.myEcrDemo.processCommand(3)
        # ##debit sale
        # res = self.myEcrDemo.processCommand(4)
        # ##ebt sale
        # self.myEcrDemo.processCommand(5)
        # ##gift redeem
        # self.myEcrDemo.processCommand(6)

        # Execute payment by starting a new thread
        self.thread = ecrDemo()
        self.thread.posurl = "127.0.0.1"
        self.thread.posport = 10009
        self.thread.amount = self.amount
        self.thread.status_signal.connect(self.update_status)
        self.thread.start()
        self.thread.exit()


    def update_status(self, res):
        self.viewStatus.setText(res)
        # self.update()
        # self.show()
        

class Controller:

    def __init__(self, app):
        self.app = app
        self.capture_window = CaptureWindow()
        self.snipper = Snipper(self.app)
        self.pay_window = PayWindow(self.app)

    def show_capture_window(self):
        
        self.capture_window.switch_window.connect(self.show_screen_grab)
        self.capture_window.show()

    def show_screen_grab(self):
        self.capture_window.close()
        self.snipper.start()
        self.snipper.snipped_signal.connect(self.show_pay_window)
        self.snipper.show()

    def show_pay_window(self, value):
        self.snipper.close()
        self.pay_window.set_pay_value(value)
        self.pay_window.show()

    def restore_pay_window(self):
        self.pay_window.show_current_value()
        self.pay_window.show()

# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     # Force the style to be the same on all OSs:
#     app.setStyle("Fusion")

#     # Now use a palette to switch to dark colors:
#     palette = QPalette()
#     palette.setColor(QPalette.Window, QColor(53, 53, 53))
#     palette.setColor(QPalette.WindowText, QtCore.Qt.white)
#     palette.setColor(QPalette.Base, QColor(25, 25, 25))
#     palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
#     palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
#     palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
#     palette.setColor(QPalette.Text, QtCore.Qt.white)
#     palette.setColor(QPalette.Button, QColor(53, 53, 53))
#     palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
#     palette.setColor(QPalette.BrightText, QtCore.Qt.red)
#     palette.setColor(QPalette.Link, QColor(42, 130, 218))
#     palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
#     palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
#     app.setPalette(palette)
#     controller = Controller(app)
#     controller.show_capture_window()
#     sys.exit(app.exec_())


def main(app, tray):
    controller = Controller(app)

    # Create the menu
    menu = QMenu()

    showPayWindowAction = QAction("Show Window")
    showPayWindowAction.triggered.connect(controller.restore_pay_window)
    menu.addAction(showPayWindowAction)

    captureResetAction = QAction("Reset Capture Area")
    captureResetAction.triggered.connect(controller.show_screen_grab)
    menu.addAction(captureResetAction)



    exitAction = menu.addAction("Exit")
    exitAction.triggered.connect(sys.exit)
    
    tray.setContextMenu(menu)
    
    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QPalette.Text, QtCore.Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)
    
    controller.show_capture_window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # main()
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Create the icon
    if getattr(sys, 'frozen', False):
        icon = QIcon(os.path.join(sys._MEIPASS, "files\\icon.png"))
    else:
        icon = QIcon("files\\icon.png")
    

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # # Create the menu
    # menu = QMenu()
    # captureResetAction = QAction("Reset Capture Area")
    # captureResetAction.triggered.connect
    # menu.addAction(captureResetAction)
    # exitAction = menu.addAction("exit")
    # exitAction.triggered.connect(sys.exit)
    # print("app::", app)

    # Add the menu to the tray
    

    tray.activated.connect(main(app, tray))
    tray.messageC.connect(main(app, tray))
    # app.exec_()
    # sys.exit(app.exec_())

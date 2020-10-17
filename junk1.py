from PyQt5 import QtCore, QtGui

class Worker(QtCore.QObject):
    threadInfo = QtCore.pyqtSignal(object, object)

    @QtCore.pyqtSlot()
    def emitInfo(self):
        self.threadInfo.emit(self.objectName(), QtCore.QThread.currentThreadId())

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.button = QtGui.QPushButton('Test', self)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.button)
        self.thread = QtCore.QThread(self)
        self.worker1 = Worker()
        self.worker1.setObjectName('Worker1')
        self.worker1.moveToThread(self.thread)
        self.worker1.threadInfo.connect(self.handleShowThreads)
        self.button.clicked.connect(self.worker1.emitInfo)
        self.worker2 = Worker()
        self.worker2.setObjectName('Worker2')
        self.worker2.threadInfo.connect(self.handleShowThreads)
        self.button.clicked.connect(self.worker2.emitInfo)
        self.thread.start()

    def handleShowThreads(self, name, identifier):
        print('Main: %s' % QtCore.QThread.currentThreadId())
        print('%s: %s\n' % (name, identifier))

    def closeEvent(self, event):
        self.thread.quit()
        self.thread.wait()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
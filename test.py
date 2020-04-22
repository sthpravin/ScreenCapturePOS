from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys 

app = QApplication([])
app.setQuitOnLastWindowClosed(False)


def print_s():
    print("clicked")


# Create the icon
icon = QIcon("icon.png")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Create the menu
menu = QMenu()
action = QAction("A menu item")
menu.addAction(action)
exitAction = menu.addAction("exit")
exitAction.triggered.connect(sys.exit)

tray.activated.connect(print_s)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec_()
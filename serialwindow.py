from PyQt5 import QtCore, QtGui, QtWidgets
from serial_ui import Ui_serial_ui

class SerialWindow(QtWidgets.QWidget,Ui_serial_ui):
    def __init__(self, parent=None):
        super(SerialWindow, self).__init__(parent)
        self.setupUi(self)

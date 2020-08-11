import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem

from PyQt5.QtGui import QImage, QPixmap, QIcon
from topwindow import Ui_TopWindow
from serialwindow import SerialWindow
from tcpudpwindow import TcpUdpWindow
from usbwindow import UsbWindow


class MainWindow(QtWidgets.QMainWindow,Ui_TopWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QIcon(".\logo_min.jpg"))
        #self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

        self.statusbar.setStyleSheet("background-color: rgb(104, 33, 122);")

        self.serial_ui = SerialWindow()
        self.tcpudp_ui = TcpUdpWindow()
        self.usb_ui = UsbWindow()

        self.stackWidget = QtWidgets.QStackedWidget()
        self.gridLayout.addWidget(self.stackWidget)
        self.stackWidget.addWidget(self.serial_ui)
        self.stackWidget.addWidget(self.tcpudp_ui)
        self.stackWidget.addWidget(self.usb_ui)

        self.SerialUI()

        self.SerialpushButton.clicked.connect(self.SerialUI)
        self.TCPpushButton.clicked.connect(self.TCPUI)
        self.USBpushButton.clicked.connect(self.USBUI)

    def SerialUI(self):
        self.stackWidget.setCurrentIndex(0)
        self.SerialpushButton.setStyleSheet("font: 22pt \"华文中宋\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(64, 65, 66);\n"
                                         "")
        self.TCPpushButton.setStyleSheet("font: 22pt \"华文中宋\";\n"
                                         "color: rgb(0, 0, 0);\n"
                                         "")
        self.USBpushButton.setStyleSheet("font: 22pt \"华文中宋\";\n"
                                            "color: rgb(0, 0, 0);\n"
                                            "")

    def TCPUI(self):
        self.stackWidget.setCurrentIndex(1)
        self.TCPpushButton.setStyleSheet("font: 22pt \"华文中宋\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(64, 65, 66);\n"
                                         "")
        self.USBpushButton.setStyleSheet("font: 22pt \"华文中宋\";\n"
                                         "color: rgb(0, 0, 0);\n"
                                         "")
        self.SerialpushButton.setStyleSheet("font: 22pt \"华文中宋\";\n"
                                            "color: rgb(0, 0, 0);\n"
                                            "")

    def USBUI(self):
        self.stackWidget.setCurrentIndex(2)
        self.USBpushButton.setStyleSheet("font: 22pt \"华文中宋\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(64, 65, 66);\n"
                                         "")
        self.TCPpushButton.setStyleSheet("font: 22pt \"华文中宋\";\n"
                                         "color: rgb(0, 0, 0);\n"
                                         "")
        self.SerialpushButton.setStyleSheet("font: 22pt \"华文中宋\";\n"
                                            "color: rgb(0, 0, 0);\n"
                                            "")




        # self.icon_image = QImage()
        # self.icon_image.load(".\logo_min.jpg")
        # self.scene = QGraphicsScene()
        # self.scene.addPixmap(QPixmap.fromImage(self.icon_image))
        # self.graphicsView.setScene(self.scene)

        #elf.setWindowIcon(QIcon('./logo.ico'))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem

from PyQt5.QtGui import QImage, QPixmap, QIcon
from topwindow import Ui_TopWindow
from serialwindow import SerialWindow
import cv2

class MainWindow(QtWidgets.QMainWindow,Ui_TopWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.serial_ui = SerialWindow()

        self.stackWidget = QtWidgets.QStackedWidget()
        self.gridLayout.addWidget(self.stackWidget)


        self.statusbar.setStyleSheet("background-color: rgb(104, 33, 122);")


        self.icon_image = QImage()
        self.icon_image.load(".\logo_min.jpg")
        self.scene = QGraphicsScene()
        self.scene.addPixmap(QPixmap.fromImage(self.icon_image))
        self.graphicsView.setScene(self.scene)

        #elf.setWindowIcon(QIcon('./logo.ico'))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
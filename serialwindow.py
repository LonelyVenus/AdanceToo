from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from serial_ui import Ui_serial_ui
from PyQt5.QtWidgets import QMessageBox, QInputDialog

import serial
import serial.tools.list_ports

class SerialWindow(QtWidgets.QWidget,Ui_serial_ui):
    def __init__(self, parent=None):
        super(SerialWindow, self).__init__(parent)
        self.setupUi(self)
        self.InitSignalConnect()
        self.comExpandtabWidget.setVisible(False)
        self.comBaudcomboBox.setCurrentText('9600')

        #定时扫描当前可用串口号
        self.Com_Dict = {}
        self.port_list = list()
        self.PortCheck()
        self.scanTimer = QTimer()
        self.scanTimer.timeout.connect(self.PortCheck)
        self.scanTimer.start(2000)

        #串口声明
        self.ser = serial.Serial()



    def InitSignalConnect(self):
        self.comExpandpushButton.clicked.connect(self.ExpandToolCtl)
        self.comOpenpushButton.clicked.connect(self.PortOpenAndClose)
        self.comBaudcomboBox.currentIndexChanged.connect(self.BaudrateCustom)


    def BaudrateCustom(self):
        if self.comBaudcomboBox.currentIndex() == 0:  #Custom baudrate
            num, ok = QInputDialog.getInt(self, '自定义波特率', '输入波特率')
            if ok:
                if num >= 50:
                    self.comBaudcomboBox.setItemText(self.comBaudcomboBox.count()-1, str(num))
                    self.comBaudcomboBox.setCurrentText(str(num))
                    self.comBaudcomboBox.setStyleSheet("font: 10pt \"Times New Roman\";\n"
                                                           "background-color: rgb(255, 255, 255);\n"
                                                           "color: rgb(255, 0, 0);")
                else:
                    QMessageBox.warning(self, "warning", "Minimum 50, Set default:9600")
                    self.comBaudcomboBox.setCurrentText('9600')
            else:
                QMessageBox.warning(self, "warning", "It's none, Set default:9600")
                self.comBaudcomboBox.setCurrentText('9600')
        else:
            self.comBaudcomboBox.setStyleSheet("font: 10pt \"Times New Roman\";\n"
                                               "background-color: rgb(255, 255, 255);\n"
                                               "color: rgb(0, 0, 0);")
    def ExpandToolCtl(self):
        if(self.comExpandtabWidget.isVisible()):
            self.comExpandtabWidget.setVisible(False)
        else:
            self.comExpandtabWidget.setVisible(True)

    def PortCheck(self):
        if self.port_list == list(serial.tools.list_ports.comports()):
            return
        self.port_list = list(serial.tools.list_ports.comports())
        self.comIDcomboBox.clear()
        for port in self.port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.comIDcomboBox.addItem(port[0] + ' ' + port.description.split(' (COM',1)[0])
        if len(self.Com_Dict) == 0:
            self.comIDcomboBox.addItem("未检测到端口")

        #ComboBox下拉框宽度自适应设置
        maxlen = 0
        for i in range(self.comIDcomboBox.count()):
            if (maxlen < len(self.comIDcomboBox.itemText(i))):
                maxlen = len(self.comIDcomboBox.itemText(i))
        ptVal = self.comIDcomboBox.fontInfo().pointSize()
        self.comIDcomboBox.view().setFixedWidth(ptVal*maxlen*0.75)

    def PortOpenAndClose(self):
        if len(self.Com_Dict) == 0:
            return None
        if self.comOpenpushButton.text() == "打开串口" :
            self.comOpenpushButton.setText("关闭串口")
            self.ser.port = self.comIDcomboBox.currentText().split(' ',1)[0]
            self.ser.baudrate = int(self.comBaudcomboBox.currentText())
            self.ser.bytesize = int(self.comBitlencomboBox.currentText())
            self.ser.stopbits = int(self.comStoplencomboBox.currentText())

            try:
                self.ser.open()
            except:
                QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
                return None

        else:
            self.comOpenpushButton.setText("打开串口")
            try:
                self.ser.close()
            except:
                return None
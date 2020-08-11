from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QSize,QEvent,Qt
from serial_ui import Ui_serial_ui
from PyQt5.QtWidgets import QMessageBox, QInputDialog,QDialog
from PyQt5.QtGui import QImage, QPixmap, QMouseEvent
import time

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
        self.comIDcomboBox.installEventFilter(self)

        #串口声明
        self.ser = serial.Serial()

        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(QtGui.QPixmap("off_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.icon2 = QtGui.QIcon()
        self.icon2.addPixmap(QtGui.QPixmap("on_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.comOpenpushButton.setIcon(self.icon1)
        self.comOpenpushButton.setIconSize(QtCore.QSize(32, 32))

        # 定时器接收数据
        self.recv_timer = QTimer(self)
        self.recv_timer.timeout.connect(self.SerialRecv)


    def eventFilter(self, obj, event):
        if obj == self.comIDcomboBox:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.PortCheck()
        return QtWidgets.QWidget.eventFilter(self, obj, event)

    def InitSignalConnect(self):
        self.comExpandpushButton.clicked.connect(self.ExpandToolCtl)
        self.comOpenpushButton.clicked.connect(self.PortOpenAndClose)
        self.comBaudcomboBox.currentIndexChanged.connect(self.BaudrateCustom)
        self.comSendpushButton.clicked.connect(self.SerialSend)
        self.comOpenFilepushButton.clicked.connect(self.OpenSendFile)




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
            self.comOpenpushButton.setStyleSheet("font: 15pt \"黑体\";\n"
                                                 "color: rgb(0, 0, 0);\n"
                                                 "background-color: rgb(248, 177, 1);")
            self.comOpenpushButton.setIcon(self.icon2)
            self.ser.port = self.comIDcomboBox.currentText().split(' ',1)[0]
            self.ser.baudrate = int(self.comBaudcomboBox.currentText())
            self.ser.bytesize = int(self.comBitlencomboBox.currentText())
            self.ser.stopbits = int(self.comStoplencomboBox.currentText())

            try:
                self.ser.open()
                recv_timeout = int(self.comRecvTimeoutEdit.text())
                self.recv_timer.start(recv_timeout)
            except:
                self.comOpenpushButton.setText("打开串口")
                self.recv_timer.stop()
                self.comOpenpushButton.setStyleSheet("font: 15pt \"黑体\";\n"
                                                     "color: rgb(0, 0, 0);\n"
                                                     "background-color: rgb(55, 54, 52);")
                self.comOpenpushButton.setIcon(self.icon1)
                QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
                return None

        else:
            self.comOpenpushButton.setText("打开串口")
            self.comOpenpushButton.setStyleSheet("font: 15pt \"黑体\";\n"
                                                 "color: rgb(0, 0, 0);\n"
                                                 "background-color: rgb(55, 54, 52);")
            self.comOpenpushButton.setIcon(self.icon1)
            self.recv_timer.stop()
            try:
                self.ser.close()
            except:
                return None

    def SerialSend(self):
        if self.ser.isOpen():
            input_s = self.ComSendtextEdit.toPlainText()
            if input_s != "":
                # 非空字符串
                if self.comSendHexcheckBox.isChecked():
                    # hex发送
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, 'wrong data', '请输入十六进制数据，以空格分开!')
                            return None
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                    display_str = '[hex]'+''.join(['%02X ' % b for b in input_s])
                else:
                    # ascii发送
                    input_s = input_s.encode('utf-8')
                    display_str = str(input_s, encoding = "utf-8")
                try:
                    num = self.ser.write(input_s)
                except:
                    return
                cur_time = str(time.strftime('%H:%M:%S',time.localtime(time.time()))+'.'+str(int((time.time()*1000)%1000)))
                self.ComRecvtextBrowser.append('['+cur_time+']'+'发'+'->'+' '+ display_str )

        else:
            pass

        # 接收数据
    def SerialRecv(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.recv_timer.stop()
            self.comOpenpushButton.setText("打开串口")
            self.comOpenpushButton.setStyleSheet("font: 15pt \"黑体\";\n"
                                                 "color: rgb(0, 0, 0);\n"
                                                 "background-color: rgb(55, 54, 52);")
            self.comOpenpushButton.setIcon(self.icon1)
            try:
                self.ser.close()
            except:
                return None
            return None
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            # hex显示
            cur_time = str(time.strftime('%H:%M:%S', time.localtime(time.time())) + '.' + str(
                int((time.time() * 1000) % 1000)))
            if self.comRecvHexcheckBox.checkState():
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
                self.ComRecvtextBrowser.append('[' + cur_time + ']' + '收' + '->' + ' ' + '[hex]'+out_s)
                #self.ComRecvtextBrowser.insertPlainText(out_s)
            else:
                # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                self.ComRecvtextBrowser.append('[' + cur_time + ']' + '收' + '->' + ' ' + data.decode('iso-8859-1'))
        else:
            pass

    def OpenSendFile(self):
        # download_path = QtWidgets.QFileDialog.getExistingDirectory(self,
        #                                                            "打开",
        #                                                            "./")
        download_path = QtWidgets.QFileDialog.getOpenFileName(self,'打开文件','./')
        self.comSendFilePathlineEdit.setText(download_path[0])


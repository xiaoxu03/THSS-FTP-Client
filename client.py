# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1248, 672)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.widgetWindow = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetWindow.sizePolicy().hasHeightForWidth())
        self.widgetWindow.setSizePolicy(sizePolicy)
        self.widgetWindow.setObjectName("widgetWindow")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widgetWindow)
        self.verticalLayout_3.setContentsMargins(0, 0, -1, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widgetInput = QtWidgets.QWidget(self.widgetWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetInput.sizePolicy().hasHeightForWidth())
        self.widgetInput.setSizePolicy(sizePolicy)
        self.widgetInput.setMaximumSize(QtCore.QSize(16777215, 34))
        self.widgetInput.setObjectName("widgetInput")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widgetInput)
        self.horizontalLayout_5.setContentsMargins(0, 2, 0, 2)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(0, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.widgetUsername = QtWidgets.QWidget(self.widgetInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetUsername.sizePolicy().hasHeightForWidth())
        self.widgetUsername.setSizePolicy(sizePolicy)
        self.widgetUsername.setObjectName("widgetUsername")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widgetUsername)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelUsername = QtWidgets.QLabel(self.widgetUsername)
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(14)
        self.labelUsername.setFont(font)
        self.labelUsername.setObjectName("labelUsername")
        self.horizontalLayout_2.addWidget(self.labelUsername)
        self.inputUsername = QtWidgets.QLineEdit(self.widgetUsername)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.inputUsername.setFont(font)
        self.inputUsername.setObjectName("inputUsername")
        self.horizontalLayout_2.addWidget(self.inputUsername)
        self.horizontalLayout_5.addWidget(self.widgetUsername)
        self.widgetPassword = QtWidgets.QWidget(self.widgetInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetPassword.sizePolicy().hasHeightForWidth())
        self.widgetPassword.setSizePolicy(sizePolicy)
        self.widgetPassword.setObjectName("widgetPassword")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widgetPassword)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelPassword = QtWidgets.QLabel(self.widgetPassword)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPassword.sizePolicy().hasHeightForWidth())
        self.labelPassword.setSizePolicy(sizePolicy)
        self.labelPassword.setMinimumSize(QtCore.QSize(30, 0))
        self.labelPassword.setMaximumSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(14)
        self.labelPassword.setFont(font)
        self.labelPassword.setObjectName("labelPassword")
        self.horizontalLayout.addWidget(self.labelPassword)
        self.inputPassword = QtWidgets.QLineEdit(self.widgetPassword)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.inputPassword.setFont(font)
        self.inputPassword.setObjectName("inputPassword")
        self.horizontalLayout.addWidget(self.inputPassword)
        self.horizontalLayout_5.addWidget(self.widgetPassword)
        self.widgetIP = QtWidgets.QWidget(self.widgetInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetIP.sizePolicy().hasHeightForWidth())
        self.widgetIP.setSizePolicy(sizePolicy)
        self.widgetIP.setObjectName("widgetIP")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widgetIP)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelIP = QtWidgets.QLabel(self.widgetIP)
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(14)
        self.labelIP.setFont(font)
        self.labelIP.setObjectName("labelIP")
        self.horizontalLayout_4.addWidget(self.labelIP)
        self.inputIP = QtWidgets.QLineEdit(self.widgetIP)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.inputIP.setFont(font)
        self.inputIP.setObjectName("inputIP")
        self.horizontalLayout_4.addWidget(self.inputIP)
        self.horizontalLayout_5.addWidget(self.widgetIP)
        self.widgetPort = QtWidgets.QWidget(self.widgetInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetPort.sizePolicy().hasHeightForWidth())
        self.widgetPort.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.widgetPort.setFont(font)
        self.widgetPort.setObjectName("widgetPort")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widgetPort)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelPort = QtWidgets.QLabel(self.widgetPort)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPort.sizePolicy().hasHeightForWidth())
        self.labelPort.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.labelPort.setFont(font)
        self.labelPort.setObjectName("labelPort")
        self.horizontalLayout_3.addWidget(self.labelPort)
        self.inputPort = QtWidgets.QLineEdit(self.widgetPort)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputPort.sizePolicy().hasHeightForWidth())
        self.inputPort.setSizePolicy(sizePolicy)
        self.inputPort.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.inputPort.setFont(font)
        self.inputPort.setObjectName("inputPort")
        self.horizontalLayout_3.addWidget(self.inputPort)
        self.horizontalLayout_5.addWidget(self.widgetPort)
        self.buttonLogin = QtWidgets.QPushButton(self.widgetInput)
        self.buttonLogin.setMaximumSize(QtCore.QSize(80, 100))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.buttonLogin.setFont(font)
        self.buttonLogin.setObjectName("buttonLogin")
        self.horizontalLayout_5.addWidget(self.buttonLogin)
        self.buttonConnect = QtWidgets.QPushButton(self.widgetInput)
        self.buttonConnect.setMaximumSize(QtCore.QSize(80, 100))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(14)
        self.buttonConnect.setFont(font)
        self.buttonConnect.setObjectName("buttonConnect")
        self.horizontalLayout_5.addWidget(self.buttonConnect)
        spacerItem1 = QtWidgets.QSpacerItem(0, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.widgetPort.raise_()
        self.widgetUsername.raise_()
        self.widgetPassword.raise_()
        self.widgetIP.raise_()
        self.buttonLogin.raise_()
        self.buttonConnect.raise_()
        self.verticalLayout_3.addWidget(self.widgetInput)
        self.widgetCommand = QtWidgets.QWidget(self.widgetWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetCommand.sizePolicy().hasHeightForWidth())
        self.widgetCommand.setSizePolicy(sizePolicy)
        self.widgetCommand.setMinimumSize(QtCore.QSize(400, 400))
        self.widgetCommand.setObjectName("widgetCommand")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widgetCommand)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textCommand = QtWidgets.QTextBrowser(self.widgetCommand)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textCommand.sizePolicy().hasHeightForWidth())
        self.textCommand.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textCommand.setFont(font)
        self.textCommand.setObjectName("textCommand")
        self.verticalLayout_2.addWidget(self.textCommand)
        self.widgetCommandInput = QtWidgets.QWidget(self.widgetCommand)
        self.widgetCommandInput.setObjectName("widgetCommandInput")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widgetCommandInput)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.labelCommandInput = QtWidgets.QLabel(self.widgetCommandInput)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.labelCommandInput.setFont(font)
        self.labelCommandInput.setObjectName("labelCommandInput")
        self.horizontalLayout_7.addWidget(self.labelCommandInput)
        self.inputCommandInput = QtWidgets.QLineEdit(self.widgetCommandInput)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.inputCommandInput.setFont(font)
        self.inputCommandInput.setObjectName("inputCommandInput")
        self.horizontalLayout_7.addWidget(self.inputCommandInput)
        self.buttonCommandInput = QtWidgets.QPushButton(self.widgetCommandInput)
        self.buttonCommandInput.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(14)
        self.buttonCommandInput.setFont(font)
        self.buttonCommandInput.setObjectName("buttonCommandInput")
        self.horizontalLayout_7.addWidget(self.buttonCommandInput)
        self.verticalLayout_2.addWidget(self.widgetCommandInput)
        self.verticalLayout_3.addWidget(self.widgetCommand)
        self.widgetExploror = QtWidgets.QWidget(self.widgetWindow)
        self.widgetExploror.setMaximumSize(QtCore.QSize(16777215, 500))
        self.widgetExploror.setObjectName("widgetExploror")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widgetExploror)
        self.verticalLayout.setContentsMargins(0, 2, 0, 2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgetDir = QtWidgets.QWidget(self.widgetExploror)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetDir.sizePolicy().hasHeightForWidth())
        self.widgetDir.setSizePolicy(sizePolicy)
        self.widgetDir.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widgetDir.setObjectName("widgetDir")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widgetDir)
        self.horizontalLayout_6.setContentsMargins(0, 2, 0, 2)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.labelDir = QtWidgets.QLabel(self.widgetDir)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.labelDir.setFont(font)
        self.labelDir.setObjectName("labelDir")
        self.horizontalLayout_6.addWidget(self.labelDir)
        self.inputDir = QtWidgets.QLineEdit(self.widgetDir)
        self.inputDir.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.inputDir.setFont(font)
        self.inputDir.setObjectName("inputDir")
        self.horizontalLayout_6.addWidget(self.inputDir)
        self.verticalLayout.addWidget(self.widgetDir)
        self.tableFile = QtWidgets.QTableWidget(self.widgetExploror)
        self.tableFile.setObjectName("tableFile")
        self.tableFile.setColumnCount(0)
        self.tableFile.setRowCount(0)
        self.verticalLayout.addWidget(self.tableFile)
        self.verticalLayout_3.addWidget(self.widgetExploror)
        MainWindow.setCentralWidget(self.widgetWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FTP客户端"))
        self.labelUsername.setText(_translate("MainWindow", "用户名："))
        self.labelPassword.setText(_translate("MainWindow", "密 码："))
        self.labelIP.setText(_translate("MainWindow", "服务器IP："))
        self.labelPort.setText(_translate("MainWindow", "端口号："))
        self.buttonLogin.setText(_translate("MainWindow", "登录"))
        self.buttonConnect.setText(_translate("MainWindow", "连接"))
        self.labelCommandInput.setText(_translate("MainWindow", "命 令："))
        self.buttonCommandInput.setText(_translate("MainWindow", "发送"))
        self.labelDir.setText(_translate("MainWindow", "目 录："))

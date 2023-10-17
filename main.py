from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import socket
import client
import sys


def login():
    global ui
    global control_socket
    username = ui.inputUsername.text()
    password = ui.inputPassword.text()
    ip = ui.inputIP.text()
    port = ui.inputPort.text()
    if username == '':
        msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入用户名')
        msg_box.exec_()
        return
    elif password == '':
        msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入密码')
        msg_box.exec_()
        return
    elif ip == '':
        msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入IP地址')
        msg_box.exec_()
        return
    elif port == '':
        msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入端口号')
        msg_box.exec_()
        return

    control_socket = socket.socket()
    control_socket.connect((ip, int(port)))

    user_response = control_socket.recv(1024).decode()
    print(user_response)
    ui.textCommand.insertPlainText(user_response)

    user_command = 'USER ' + 'anonymous' + '\r\n'
    control_socket.send(user_command.encode())
    user_response = control_socket.recv(1024).decode()
    print(user_response)
    ui.textCommand.insertPlainText(user_response)

    user_command = 'PASS ' + password + '\r\n'
    control_socket.send(user_command.encode())
    user_response = control_socket.recv(1024).decode()
    print(user_response)
    ui.textCommand.insertPlainText(user_response)

    if user_response[0] == '5':
        msg_box = QMessageBox(QMessageBox.Warning, '警告', '密码不是一个合法的邮箱')
        msg_box.exec_()
        return

    user_command = 'QUIT' + '\r\n'
    control_socket.send(user_command.encode())
    user_response = control_socket.recv(1024).decode()
    print(user_response)
    ui.textCommand.insertPlainText(user_response)




if __name__ == '__main__':
    # 全局变量定义
    global ui
    # 创建对象
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = client.Ui_MainWindow()
    ui.setupUi(MainWindow)

    # 初始化设置
    ui.buttonLogin.clicked.connect(login)

    # 渲染窗口
    MainWindow.show()
    sys.exit(app.exec_())



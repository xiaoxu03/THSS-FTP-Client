import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import socket
import client
import sys

global control_socket
global ui


def receive_data():
    global ui
    global control_socket
    while True:
        data = control_socket.recv(1024).decode()

        if not data:
            break

        ui.textCommand.insertPlainText("Server: " + data)
        time.sleep(0.05)

    return data


def send_data(data):
    global ui
    global control_socket
    ui.textCommand.insertPlainText("Client: " + data)
    time.sleep(0.05)
    control_socket.send(data.encode())
    return


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

    user_response = receive_data()

    user_command = 'USER ' + 'anonymous' + '\r\n'
    send_data(user_command)
    user_response = receive_data()

    user_command = 'PASS ' + password + '\r\n'
    send_data(user_command)
    user_response = receive_data()

    if user_response[0] == '5':
        msg_box = QMessageBox(QMessageBox.Warning, '警告', '密码不是一个合法的邮箱')
        msg_box.exec_()
        return

    user_command = 'LIST' + '\r\n'
    send_data(user_command)
    user_response = receive_data()

    user_command = 'QUIT' + '\r\n'
    send_data(user_command)
    user_response = receive_data()

    control_socket.close()


def main():
    # 全局变量定义
    global ui
    # 创建对象
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = client.Ui_MainWindow()
    ui.setupUi(main_window)

    # 初始化设置
    ui.buttonLogin.clicked.connect(login)

    # 渲染窗口
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


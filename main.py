import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from enum import Enum

import socket
import client
import sys


class Mode(Enum):
    NONE = 0
    PASV = 1
    PORT = 2


class Client:
    mode = Mode.NONE
    connect_ip = ""
    connect_port = 0
    control_socket = socket.socket()
    data_socket = socket.socket()
    ui = client.Ui_MainWindow()

    def send_command(self, data):
        self.ui.textCommand.insertPlainText("Client: " + data)
        time.sleep(0.05)
        self.control_socket.send(data.encode())
        return

    def pasv(self):
        self.send_command('PASV\r\n')
        server_response = self.receive_response()
        if server_response[0] == '5':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '无法连接到服务器')
            msg_box.exec_()
            return

    def port(self):
        self.send_command('PORT 127,0,0,1,200,0\r\n')
        self.receive_response()

    def list(self):
        pass

    def receive_response(self):
        data = self.control_socket.recv(1024).decode()
        self.ui.textCommand.insertPlainText("Server: " + data)
        time.sleep(0.05)

        return data

    def login(self):
        username = self.ui.inputUsername.text()
        password = self.ui.inputPassword.text()
        ip = self.ui.inputIP.text()
        port = self.ui.inputPort.text()
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

        self.control_socket.connect((ip, int(port)))

        self.connect_ip = ip
        self.connect_port = int(port)

        user_response = self.receive_response()

        user_command = 'USER ' + 'anonymous' + '\r\n'
        self.send_command(user_command)
        user_response = self.receive_response()

        user_command = 'PASS ' + password + '\r\n'
        self.send_command(user_command)
        user_response = self.receive_response()

        if user_response[0] == '5':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '密码不是一个合法的邮箱')
            msg_box.exec_()
            return

        # self.pasv()
        # user_command = 'LIST' + '\r\n'
        # send_data(user_command)
        # user_response = receive_response()

        user_command = 'QUIT' + '\r\n'
        self.send_command(user_command)
        user_response = self.receive_response()

        self.control_socket.close()


def main():
    # 创建对象
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()

    # 初始化客户端
    my_client = Client()
    ui = my_client.ui

    ui.setupUi(main_window)

    # 初始化设置
    ui.buttonLogin.clicked.connect(my_client.login)

    # 渲染窗口
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

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
    directory = '/'
    connect_ip: str
    connect_port: int
    data_ip: str
    data_port: int
    control_socket: socket.socket
    data_socket: socket.socket
    ui: client.Ui_MainWindow

    def __init__(self, target):
        super().__init__()
        self.ui = client.Ui_MainWindow()
        self.ui.setupUi(target)
        self.ui.tableFile.setColumnCount(5)
        self.ui.tableFile.setHorizontalHeaderLabels(['文件名', '修改时间', '大小', '所有者', '状态'])
        self.ui.tableFile.setSelectionBehavior(1)

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
        start = server_response.find('(') + 1
        end = server_response.find(')')
        port = server_response[start:end].split(',')
        self.data_ip = self.connect_ip
        self.data_port = 256 * int(port[-2]) + int(port[-1])
        self.mode = Mode.PASV

    def port(self):
        self.send_command('PORT 127,0,0,1,200,0\r\n')
        self.receive_response()

    def list(self):
        if self.mode == Mode.NONE:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请指定连接模式为PASV或PORT')
            msg_box.exec_()
            return
        elif self.mode == Mode.PASV:
            self.data_socket = socket.socket()
            self.data_socket.connect((self.data_ip, self.data_port))
            self.send_command('LIST\r\n')
            server_response = self.receive_response()
            if server_response[0] == '5':
                msg_box = QMessageBox(QMessageBox.Warning, '警告', '无法连接到服务器')
                msg_box.exec_()
                return
            while True:
                data = self.data_socket.recv(1024).decode()
                if not data:
                    break
                info = data.split(' ')
                status = info[0]
                owner = info[2]
                size = info[4]
                edit_time = info[5] + ' ' + info[6] + ' ' + info[7]
                name = info[8]
                item_1 = QTableWidgetItem(name)
                item_2 = QTableWidgetItem(edit_time)
                item_3 = QTableWidgetItem(size)
                item_4 = QTableWidgetItem(owner)
                item_5 = QTableWidgetItem(status)
                self.ui.tableFile.insertRow(0)
                self.ui.tableFile.setItem(0, 0, item_1)
                self.ui.tableFile.setItem(0, 1, item_2)
                self.ui.tableFile.setItem(0, 2, item_3)
                self.ui.tableFile.setItem(0, 3, item_4)
                self.ui.tableFile.setItem(0, 4, item_5)

            self.data_socket.close()
            self.mode = Mode.NONE
        elif self.mode == Mode.PORT:
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

        self.control_socket = socket.socket()
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

        self.pasv()

        self.list()

        user_command = 'QUIT' + '\r\n'
        self.send_command(user_command)
        user_response = self.receive_response()

        self.control_socket.close()


def main():
    # 创建对象
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()

    # 初始化客户端
    my_client = Client(main_window)
    ui = my_client.ui

    # 初始化设置
    ui.buttonLogin.clicked.connect(my_client.login)

    # 渲染窗口
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

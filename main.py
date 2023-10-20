import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import requests
import re


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
        self.ui.tableFile.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableFile.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableFile.verticalHeader().hide()
        self.ui.tableFile.setShowGrid(False)
        self.ui.tableFile.verticalHeader().setDefaultSectionSize(12)

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
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = requests.get('https://myip.ipip.net', timeout=5).text
        print(res)
        self.data_ip = re.findall(r"\d+.\d+.\d+.\d+", res)[0]
        self.data_socket.bind((self.data_ip, 0))
        self.data_ip = self.data_socket.getsockname()[0]
        self.data_port = self.data_socket.getsockname()[1]
        self.data_socket.listen(1)
        self.send_command('PORT ' + self.data_ip.replace('.', ',') + ',' + str(int(self.data_port / 256)) +
                          ',' + str(self.data_port % 256) + '\r\n')
        self.receive_response()
        self.mode = Mode.PORT

    def list(self):
        file_info = []
        all_data = ''

        if self.mode == Mode.NONE:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请指定连接模式为PASV或PORT')
            msg_box.exec_()
            return
        elif self.mode == Mode.PASV:
            self.send_command('LIST\r\n')
            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_socket.connect((self.data_ip, self.data_port))
        elif self.mode == Mode.PORT:
            self.send_command('LIST\r\n')
            self.data_socket, addr = self.data_socket.accept()

        self.ui.tableFile.clearContents()

        server_response = self.receive_response()
        if server_response[0] == '5':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '无法连接到服务器')
            msg_box.exec_()
            return

        while True:
            data = self.data_socket.recv(1024).decode()
            if not data:
                break
            all_data += data

        self.data_socket.close()
        self.mode = Mode.NONE

        all_data = all_data.split('\r\n')[0:-1]
        for fdata in all_data:
            info = fdata.split(' ')
            info = [s for s in info if s != '']
            status = info[0]
            owner = info[2]
            size = info[4]
            edit_time = info[5] + ' ' + info[6] + ' ' + info[7]
            name = info[8]
            file_info.append([name, edit_time, size, owner, status])

        for i in range(0, len(file_info)):
            self.ui.tableFile.insertRow(i)
            for j in range(0, len(file_info[i])):
                self.ui.tableFile.setItem(i, j, QTableWidgetItem(file_info[i][j]))

    def retr(self, filename):
        filedir = self.directory
        if filedir[-1] != '/':
            filedir += '/'
        filedir += filename
        if self.mode == Mode.NONE:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请指定连接模式为PASV或PORT')
            msg_box.exec_()
            return
        elif self.mode == Mode.PASV:
            self.send_command('RETR ' + filedir + '\r\n')
            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_socket.connect((self.data_ip, self.data_port))
        elif self.mode == Mode.PORT:
            self.send_command('RETR ' + filedir + '\r\n')
            self.data_socket, addr = self.data_socket.accept()
            self.receive_response()

        with open(filename, 'wb') as f:
            while True:
                data = self.data_socket.recv(1024)
                if not data:
                    break
                f.write(data)

        self.data_socket.close()
        self.receive_response()
        self.mode = Mode.NONE

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

        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        self.port()
        # self.pasv()

        self.list()

        self.pasv()
        self.retr('2.txt')

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

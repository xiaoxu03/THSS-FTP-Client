import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import requests
import re
import os

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
    logged: bool
    control_socket: socket.socket
    data_socket: socket.socket
    ui: client.Ui_MainWindow

    def __init__(self, target):
        super().__init__()
        self.logged = False

        self.ui = client.Ui_MainWindow()
        self.ui.setupUi(target)
        self.ui.progressBar.hide()
        self.ui.tableFile.setColumnCount(5)
        self.ui.tableFile.setHorizontalHeaderLabels(['文件名', '修改时间', '大小', '所有者', '状态'])
        self.ui.tableFile.setSelectionBehavior(1)
        self.ui.tableFile.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableFile.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.inputPassword.setEchoMode(QLineEdit.Password)
        self.ui.tableFile.verticalHeader().hide()
        self.ui.tableFile.setShowGrid(False)
        self.ui.tableFile.verticalHeader().setDefaultSectionSize(12)
        self.ui.buttonConnect.clicked.connect(self.connect)
        self.ui.buttonLogout.clicked.connect(self.logout)
        self.ui.buttonLogout.setEnabled(False)
        self.ui.buttonCommandInput.clicked.connect(self.send_command_from_editor)
        self.ui.inputCommandInput.returnPressed.connect(self.send_command_from_editor)
        self.ui.tableFile.cellDoubleClicked.connect(self.on_double_click)
        self.ui.buttonLogin.clicked.connect(self.login)
        self.ui.buttonUpload.clicked.connect(self.upload)
        self.ui.buttonUpload.setEnabled(False)
        self.ui.buttonCommandInput.setEnabled(False)
        self.ui.inputCommandInput.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ui.inputDir.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def on_double_click(self, row, column):
        if self.ui.tableFile.item(row, 4).text()[0] == 'd':
            self.cwd(self.ui.tableFile.item(row, 0).text())
        else:
            self.pasv()
            self.retr(self.ui.tableFile.item(row, 0).text())

    def send_command(self, data):
        self.ui.textCommand.insertPlainText("Client: " + data)
        time.sleep(0.05)
        self.control_socket.send(data.encode())
        return

    def upload(self):
        file_name, file_type = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                                     "All Files(*)")

        if file_name == '':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请选择文件')
            msg_box.exec_()
            return
        if not self.logged:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请先登录')
            msg_box.exec_()
            return

        self.pasv()
        self.stor(file_name)

    def send_command_from_editor(self):
        if self.ui.inputCommandInput.text() == '':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入要发送的指令')
            msg_box.exec_()
            return
        command = self.ui.inputCommandInput.text()
        self.ui.inputCommandInput.clear()

        if command == 'PASV':
            self.pasv()
        elif command == 'PORT':
            self.port()
        elif command.startswith('USER'):
            self.user(command.split(' ')[1])
        elif command.startswith('PASS'):
            self.pass_(command.split(' ')[1])
        elif command == 'SYST':
            self.syst()
        elif command.startswith('TYPE'):
            type_ = command.split(' ')[1]
            self.type(type_)
        elif command == 'LIST':
            self.list()
        elif command.startswith('RETR'):
            self.retr(command.split(' ')[1])
        elif command.startswith('STOR'):
            self.stor(command.split(' ')[1])
        elif command.startswith('CWD'):
            self.cwd(command.split(' ')[1])
        elif command.startswith('MKD'):
            self.mkd(command.split(' ')[1])
        elif command == 'PWD':
            self.pwd()
        elif command.startswith('RMD'):
            self.rmd(command.split(' ')[1])
        elif command.startswith('RNFR'):
            self.rnfr(command.split(' ')[1])
        elif command.startswith('RNTO'):
            self.rnto(command.split(' ')[1])
        elif command == 'QUIT':
            self.quit()
        else:
            self.send_command(command + '\r\n')
            self.receive_response()

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
        self.data_ip = re.findall(r"\d+.\d+.\d+.\d+", res)[0]
        self.data_socket.bind((self.data_ip, 0))
        self.data_ip = self.data_socket.getsockname()[0]
        self.data_port = self.data_socket.getsockname()[1]
        self.data_socket.listen(1)
        self.send_command('PORT ' + self.data_ip.replace('.', ',') + ',' + str(int(self.data_port / 256)) +
                          ',' + str(self.data_port % 256) + '\r\n')
        self.receive_response()
        self.mode = Mode.PORT

    def user(self, username):
        self.send_command('USER ' + username + '\r\n')
        self.receive_response()

    def pass_(self, password):
        self.send_command('PASS ' + password + '\r\n')
        pass_response = self.receive_response()
        if pass_response.startswith('2'):
            self.logged = True
            self.ui.buttonLogout.setEnabled(True)
            self.ui.buttonLogin.setEnabled(False)
            self.ui.buttonConnect.setEnabled(False)
            self.ui.inputUsername.setEnabled(False)
            self.ui.inputPassword.setEnabled(False)
            self.ui.inputIP.setEnabled(False)
            self.ui.inputPort.setEnabled(False)
            self.ui.buttonUpload.setEnabled(True)
            self.ui.buttonCommandInput.setEnabled(True)
            self.ui.inputCommandInput.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.pasv()
            self.list()
        elif pass_response.startswith('5'):
            self.logged = False
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '密码不是一个正确的邮箱')
            msg_box.exec_()

    def logout(self):
        if self.logged:
            self.send_command('QUIT' + '\r\n')
            if self.receive_response().startswith('5'):
                return
            self.logged = False
            self.ui.inputDir.setText('/')
            self.control_socket.close()
        while self.ui.tableFile.rowCount():
            self.ui.tableFile.removeRow(0)
        self.ui.textCommand.clear()
        self.ui.buttonLogin.setEnabled(True)
        self.ui.buttonConnect.setEnabled(True)
        self.ui.inputUsername.setEnabled(True)
        self.ui.inputPassword.setEnabled(True)
        self.ui.inputIP.setEnabled(True)
        self.ui.inputPort.setEnabled(True)
        self.ui.buttonUpload.setEnabled(False)
        self.ui.buttonCommandInput.setEnabled(False)
        self.ui.buttonLogout.setEnabled(False)
        self.ui.inputCommandInput.setFocusPolicy(Qt.FocusPolicy.NoFocus)


    def syst(self):
        self.send_command('SYST' + '\r\n')
        self.receive_response()

    def type(self, type_):
        self.send_command('TYPE ' + type_ + '\r\n')
        self.receive_response()

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

        while self.ui.tableFile.rowCount():
            self.ui.tableFile.removeRow(0)

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

        self.receive_response()

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

        file_info.sort(key=lambda x: x[0])
        file_info.sort(key=lambda x: x[4][0], reverse=True)

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
        msg = self.receive_response()
        if not msg.startswith('1'):
            msg_box = QMessageBox(QMessageBox.Warning, '错误', '未找到文件')
            msg_box.exec_()
            return

        size_str = msg.split('(')[-1]
        size = int(size_str.split(' ')[0])
        self.ui.progressBar.show()
        self.ui.progressBar.setMaximum(size)
        self.ui.progressBar.setValue(0)
        received = 0

        with open(filename, 'wb') as f:
            while True:
                data = self.data_socket.recv(1024)
                received += len(data)
                self.ui.progressBar.setValue(received)
                if not data:
                    break
                f.write(data)

        self.data_socket.close()
        if self.receive_response().startswith('4'):
            msg_box = QMessageBox(QMessageBox.Warning, '错误', '文件传输中止')
            msg_box.exec_()
            self.ui.progressBar.hide()
            return
        msg_box = QMessageBox(QMessageBox.Warning, '成功', '文件下载成功')
        msg_box.exec_()
        self.ui.progressBar.hide()
        self.mode = Mode.NONE

    def stor(self, filedir):
        file_name = filedir.split('/')[-1]
        if self.mode == Mode.NONE:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请指定连接模式为PASV或PORT')
            msg_box.exec_()
            return
        elif self.mode == Mode.PASV:
            self.send_command('STOR ' + file_name + '\r\n')
            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_socket.connect((self.data_ip, self.data_port))
        elif self.mode == Mode.PORT:
            self.send_command('STOR ' + file_name + '\r\n')
            self.data_socket, addr = self.data_socket.accept()
        if not self.receive_response().startswith('1'):
            msg_box = QMessageBox(QMessageBox.Warning, '错误', '无法上传文件')
            msg_box.exec_()
            return
        self.ui.progressBar.show()
        size = os.path.getsize(filedir)
        self.ui.progressBar.setMaximum(size)
        self.ui.progressBar.setValue(0)

        sent = 0

        with open(filedir, 'rb') as f:
            while True:
                data = f.read(1024)
                sent += len(data)
                self.ui.progressBar.setValue(sent)
                if not data:
                    break
                self.data_socket.send(data)

        self.data_socket.close()
        if not self.receive_response().startswith('2'):
            msg_box = QMessageBox(QMessageBox.Warning, '错误', '文件传输中止')
            msg_box.exec_()
            self.ui.progressBar.hide()
            return
        msg_box = QMessageBox(QMessageBox.Warning, '成功', '文件上传成功')
        msg_box.exec_()
        self.ui.progressBar.hide()
        self.mode = Mode.NONE

    def cwd(self, dirname):
        self.send_command('CWD ' + dirname + '\r\n')
        msg = self.receive_response()
        if msg.startswith('5'):
            return
        elif msg.startswith('2'):
            msg = self.pwd()
            self.directory = msg.split('"')[1]
            self.ui.inputDir.setText(self.directory)
            self.pasv()
            self.list()

    def mkd(self, dirname):
        self.send_command('MKD ' + dirname + '\r\n')
        msg = self.receive_response()
        if msg.startswith('5'):
            return
        elif msg.startswith('2'):
            self.pasv()
            self.list()

    def pwd(self):
        self.send_command('PWD' + '\r\n')
        return self.receive_response()

    def rmd(self, dirname):
        self.send_command('RMD ' + dirname + '\r\n')
        return self.receive_response()

    def rnfr(self, filename):
        self.send_command('RNFR ' + filename + '\r\n')
        return self.receive_response()

    def rnto(self, filename):
        self.send_command('RNTO ' + filename + '\r\n')
        return self.receive_response()

    def quit(self):
        self.send_command('QUIT' + '\r\n')
        msg = self.receive_response()
        self.control_socket.close()
        if msg.startswith('2'):
            self.logged = False
            self.logout()
        return msg

    def receive_response(self):
        self.ui.textCommand.moveCursor(self.ui.textCommand.textCursor().End)
        data = self.control_socket.recv(1024).decode()
        self.ui.textCommand.insertPlainText("Server: " + data)
        time.sleep(0.05)

        return data

    def connect(self):
        ip = self.ui.inputIP.text()
        port = self.ui.inputPort.text()
        if ip == '':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入IP地址')
            msg_box.exec_()
            return
        elif port == '':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入端口号')
            msg_box.exec_()
            return

        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.settimeout(3)
        try:
            self.control_socket.connect((ip, int(port)))
        except socket.timeout:
            msg_box = QMessageBox(QMessageBox.Warning, '连接失败', '无法连接到服务器')
            msg_box.exec_()
            return
        except Exception as e:
            msg_box = QMessageBox(QMessageBox.Warning, '连接失败', '无法连接到服务器')
            msg_box.exec_()
            return
        msg_box = QMessageBox(QMessageBox.Warning, '连接成功', '连接成功')
        msg_box.exec_()

        self.connect_ip = ip
        self.connect_port = int(port)

        self.receive_response()

    def receive_file(self, filename):
        self.send_command('RETR ' + filename + '\r\n')
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.connect((self.data_ip, self.data_port))
        self.receive_response()

        with open(filename, 'wb') as f:
            while True:
                data = self.data_socket.recv(1024)
                if not data:
                    break
                f.write(data)

        self.data_socket.close()
        self.receive_response()

    def login(self):
        username = self.ui.inputUsername.text()
        password = self.ui.inputPassword.text()
        ip = self.ui.inputIP.text()
        port = self.ui.inputPort.text()
        if username == '':
            username = "anonymous"
        if password == "":
            password = "mi@ma"
        if ip == '':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入IP地址')
            msg_box.exec_()
            return
        elif port == '':
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入端口号')
            msg_box.exec_()
            return

        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.settimeout(3)
        try:
            self.control_socket.connect((ip, int(port)))
        except socket.timeout:
            msg_box = QMessageBox(QMessageBox.Warning, '连接失败', '无法连接到服务器')
            msg_box.exec_()
            return
        except Exception as e:
            msg_box = QMessageBox(QMessageBox.Warning, '连接失败', '无法连接到服务器')
            msg_box.exec_()
            return
        msg_box = QMessageBox(QMessageBox.Warning, '连接成功', '连接成功')
        msg_box.exec_()

        self.connect_ip = ip
        self.connect_port = int(port)

        self.receive_response()

        self.user(username)

        self.pass_(password)


def main():
    # 创建对象
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()

    # 初始化客户端
    my_client = Client(main_window)

    # 渲染窗口
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

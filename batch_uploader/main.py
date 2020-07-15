#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
# @Time    : 2020-06-09  21:47
# @Author  : 行颠
# @Email   : 0xe590b4@gmail.com
# @File    : tab1
# @Software: kakura
# @DATA    : 2020-06-09
"""

import os
import json
import uuid
import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from proglog import ProgressBarLogger, RqWorkerProgressLogger
from batch_uploader.mobile import Mobile


def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac

def is_regiter():

    try:
        device = get_mac_address()
        r = requests.get("http://yannanzhaobei.com:8080/test", {"device": device})
        data = json.loads(r.text)
        if data['flag']:
            return  {"flag":True,"msg":"设备已注册"}
        else:
            return  {"flag":False,"msg":"设备未注册,请找管理员"}
    except requests.exceptions.ConnectionError as e:
        return  {"flag":False,"msg":"网络连接有问题,请检查网络状态"}

class MobileWidget(QWidget):

    def __init__(self, parent=None):
        super(MobileWidget, self).__init__(parent)

        self.count = 10
        self.pool = QThreadPool()
        self.pool.globalInstance()
        self.pool.setMaxThreadCount(self.count)  # 设置最大线程数

        self.setPalette(QPalette(Qt.lightGray))
        self.setAutoFillBackground(True)
        self.setMinimumSize(100, 100)

        self.initUi()

    def initUi(self):

        iplabel = QLabel("手机地址", self)
        self.iplineedit = QTextEdit(self)

        self.iplineedit.append("10.0.116.63")

        movielabel = QLabel("视频文件", self)
        self.movielineedit = QLineEdit("/Users/0xe590b4/Downloads/test")
        self.movielineedit.setFocusPolicy(Qt.NoFocus)
        movielabel.setBuddy(self.movielineedit)
        moviepushbutton = QPushButton("浏览")
        moviepushbutton.clicked.connect(self.openShare)

        mobilelabel = QLabel("手机存贮", self)
        self.mobilelineedit = QLineEdit("/mnt/sdcard/autotest")
        self.mobilelineedit.setFocusPolicy(Qt.NoFocus)
        mobilelabel.setBuddy(self.mobilelineedit)
        mobilebutton = QPushButton("浏览")
        #bgmbutton.clicked.connect(self.openMusic)

        uploadbutton = QPushButton("批量上传")
        uploadbutton.clicked.connect(self.uploadVideo)

        sharegrid = QGridLayout()

        sharegrid.addWidget(iplabel, 0, 0)  # 控件名，行，列，占用行数，占用列数，对齐方式
        sharegrid.addWidget(self.iplineedit, 0, 1)  # 控件名，行，列，占用行数，占用列数，对齐方式

        sharegrid.addWidget(movielabel, 1, 0)  # 控件名，行，列，占用行数，占用列数，对齐方式
        sharegrid.addWidget(self.movielineedit, 1, 1)  # 控件名，行，列，占用行数，占用列数，对齐方式
        sharegrid.addWidget(moviepushbutton, 1, 2)  # 控件名，行，列，占用行数，占用列数，对齐方式


        sharegrid.addWidget(mobilelabel, 2, 0)  # 控件名，行，列，占用行数，占用列数，对齐方式
        sharegrid.addWidget(self.mobilelineedit, 2, 1)  # 控件名，行，列，占用行数，占用列数，对齐方式
        sharegrid.addWidget(mobilebutton, 2, 2)  # 控件名，行，列，占用行数，占用列数，对齐方式



        sharegrid.addWidget(uploadbutton, 10, 0, 1, 3)  # 控件名，行，列，占用行数，占用列数，对齐方式

        hbox = QHBoxLayout()
        hbox.addLayout(sharegrid)

        self.sharegroupbox = QGroupBox("")
        self.sharegroupbox.setLayout(hbox)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addWidget(self.sharegroupbox)
        self.show()


    def openShare(self):


        resultDir = QFileDialog.getExistingDirectory(self, '选择文件', '')

        if resultDir == "":
            return False



        self.movielineedit.setText(resultDir)

        """
        注意： 这里要调用其它子窗体的内容
        """
        end_with =['mp4','mvk','rmvb','avi']
        #self.parent().movielistwidget.tablewidget.setRowCount(len(open_share_filename))

        for root, subdirs, files in os.walk(resultDir):

            index = 0
            for name in files:

                ext = name.split(".")[-1]
                if  ext not in end_with:

                    continue
                filename = "{}/{}".format(resultDir, name)
                progressBar = QProgressBar()
                progressBar.setProperty("value", 0)

                newItem0 = QTableWidgetItem('待处理')
                newItem1 = QTableWidgetItem(filename)

                self.parent().movielistwidget.tablewidget.setItem(index, 0, newItem0)
                self.parent().movielistwidget.tablewidget.setItem(index, 1, newItem1)
                self.parent().movielistwidget.tablewidget.setCellWidget(index, 2, progressBar)

                self.parent().movielistwidget.tablewidget.resizeRowToContents(index)

                index = index + 1



    def uploadVideo(self):

        flag = is_regiter()
        if not flag['flag']:
            QMessageBox.information(self, "提示", flag['msg'])
            return False

        iplineedit = self.iplineedit.toPlainText()

        if not iplineedit:
            QMessageBox.information(self, "提示", "写手机地址")
            return False

        local_file_path = self.movielineedit.text()
        if not local_file_path:
            QMessageBox.information(self, "提示", "写本地视频地址")
            return False

        remote_file_path = self.mobilelineedit.text()
        if not remote_file_path:
            QMessageBox.information(self, "提示", "写手机存贮位置")
            return False



        for device in  iplineedit.split():

            print("device:",device)
            #### 创建下载线程
            thread = UploadVideoThread(device,local_file_path,remote_file_path)
            thread.signal.install.connect(self.install_msg)
            thread.signal.push.connect(self.push_msg)
            thread.signal.deploy.connect(self.deploy_msg)
            thread.signal.finished.connect(self.finished_msg)
            self.pool.start(thread)



    def install_msg(self,row, value):
        print(row,value)

    def push_msg(self,row, value):
        print(row,value)

    def deploy_msg(self,row, value):
        print(row,value)

    def finished_msg(self, row):
        print(row, "finished")

class MovieListWidget(QWidget):

    def __init__(self, parent=None):
        super(MovieListWidget, self).__init__(parent)

        self.setPalette(QPalette(Qt.lightGray))
        self.setAutoFillBackground(True)
        self.setMinimumSize(100, 100)

        self.initUi()

    def initUi(self):
        self.tablewidget = QTableWidget()

        self.tablewidget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.tablewidget.setShowGrid(True)
        self.tablewidget.setAlternatingRowColors(True)
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置 不可选择单个单元格，只可选择一行。
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面

        columns = ['ST', "FILENAME", "BAR"]

        self.tablewidget.setColumnCount(len(columns))  # 列数
        self.tablewidget.setRowCount(20)  # 行数
        self.tablewidget.setHorizontalHeaderLabels(columns)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addWidget(self.tablewidget)
        self.show()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1200, 680)
        layout = QGridLayout()

        # 添加自定义部件（MyWidget）
        # self.widget = DownloadWindows()  # 这里可以不要self

        self.movielistwidget = MovieListWidget(self)
        self.mobileWidget = MobileWidget(self)
        # 添加编辑框（QLineEdit）
        # self.lineEdit = QLineEdit("0") # 这里可以不要self

        # 放入布局内
        layout.addWidget(self.movielistwidget, 0, 0)
        layout.addWidget(self.mobileWidget, 0, 2)

        self.setLayout(layout)

        self.setWindowTitle("下载工具")

class Signal(QObject):
    install = pyqtSignal(int, str)
    push = pyqtSignal(int, str)
    deploy = pyqtSignal(int, str)
    finished = pyqtSignal(int)

class UploadVideoThread(QRunnable):

    def __init__(self, device,local_file_path,remote_file_path):

        super(UploadVideoThread, self).__init__()

        self.signal = Signal()

        self.device = device
        self.local_file_path = local_file_path
        self.remote_file_path = remote_file_path

    def get_movie_files(self, dir, suffix):
        res = []
        for root, directory, files in os.walk(dir):
            for filename in files:
                name, suf = os.path.splitext(filename)
                if suf == suffix:
                    res.append(filename)
        return res

    def run(self):

        print(self.local_file_path)
        print(self.remote_file_path)
        m = Mobile(self.device)


        if m.install_app():
            self.signal.install.emit(1,"install sucessful")
        else:
            self.signal.install.emit(0, "install failed")

        for filename in self.get_movie_files(self.local_file_path, ".mp4"):
            print(filename)

            m.push_movies_to_mobile("{}/{}".format(self.local_file_path,filename), "{}/{}".format(self.remote_file_path,filename))
            self.signal.push.emit(2, "{}".format(self.remote_file_path))

        for filename in self.get_movie_files(self.local_file_path, ".mp4"):
            m.push_movie_to_douyin(filename)
            self.signal.deploy.emit(3, "deploy sucessful")

        self.signal.finished.emit(4)

if __name__ == '__main__':
    import sys


    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

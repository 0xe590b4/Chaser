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

import uuid
import urllib
import requests

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from user import getUserVideos
from share import getShareVideo



class UserWidget(QWidget):

    def __init__(self, parent=None):
        super(UserWidget, self).__init__(parent)

        self.setPalette(QPalette(Qt.lightGray))
        self.setAutoFillBackground(True)
        self.setMinimumSize(100, 100)

        self.initUi()

    def initUi(self):

        userlabel = QLabel("个人主页地址", self)
        self.userlineedit = QLineEdit("https://v.douyin.com/JdrGMNx/")
        userlabel.setBuddy(self.userlineedit)

        userpushbutton = QPushButton("提取视频")
        userpushbutton.clicked.connect(self.openUser)

        resultdirlabel = QLabel("下载到文件夹", self)
        self.resultdirlineedit = QLineEdit()
        resultdirlabel.setBuddy(self.resultdirlineedit)

        resultdirbutton = QPushButton("浏览")
        resultdirbutton.clicked.connect(self.openResultDir)

        usergrid = QGridLayout()
        usergrid.addWidget(userlabel, 0, 0)  # 控件名，行，列，占用行数，占用列数，对齐方式
        usergrid.addWidget(self.userlineedit, 0, 1)
        usergrid.addWidget(userpushbutton, 0, 2)

        usergrid.addWidget(resultdirlabel, 1, 0)  # 控件名，行，列，占用行数，占用列数，对齐方式
        usergrid.addWidget(self.resultdirlineedit, 1, 1)
        usergrid.addWidget(resultdirbutton, 1, 2)

        hbox = QHBoxLayout()
        hbox.addLayout(usergrid)

        self.usergroupbox = QGroupBox("")
        self.usergroupbox.setLayout(hbox)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addWidget(self.usergroupbox)
        self.show()

    def openUser(self):


        userlineedit = self.userlineedit.text()

        if not userlineedit:
            QMessageBox.information(self, "提示", "请选择需要下载的视频！")
            return False


        #### 创建下载线程
        self.worker = GetUserAllMoiveList(userlineedit)
        self.worker.download_proess_signal.connect(self.insertTableWidget)
        self.worker.start()

    def insertTableWidget(self, data):

        if data == []:

            QMessageBox.information(self, "提示", "个人主页视频提取失败")
            return  False

        index = 0
        for line in data:
            progressBar = QProgressBar()
            progressBar.setProperty("value", 0)

            newItem0 = QTableWidgetItem('待处理')
            newItem1 = QTableWidgetItem(line)

            self.parent().movielistwidget.tablewidget.setItem(index, 0, newItem0)
            self.parent().movielistwidget.tablewidget.setItem(index, 1, newItem1)
            self.parent().movielistwidget.tablewidget.setCellWidget(index, 2, progressBar)

            self.parent().movielistwidget.tablewidget.resizeRowToContents(index)

            index = index + 1



    def openResultDir(self):

        resultDir = QFileDialog.getExistingDirectory(self, '选择文件', '')

        if resultDir == "":
            return False

        self.resultdirlineedit.setText(resultDir)


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
        self.resize(800, 600)
        layout = QGridLayout()

        # 添加自定义部件（MyWidget）
        # self.widget = DownloadWindows()  # 这里可以不要self

        self.movielistwidget = MovieListWidget(self)
        self.userwidet = UserWidget(self)
        # 添加编辑框（QLineEdit）
        # self.lineEdit = QLineEdit("0") # 这里可以不要self

        self.downloaduserbutton = QPushButton("下载")
        self.downloaduserbutton.clicked.connect(self.downloadUser)

        # 放入布局内
        layout.addWidget(self.movielistwidget, 0, 0)
        layout.addWidget(self.userwidet, 1, 0)
        # layout.addWidget(self.widget, 2, 0)
        layout.addWidget(self.downloaduserbutton, 2, 0)
        self.setLayout(layout)

        self.setWindowTitle("下载工具")

        self.count = 10
        self.pool = QThreadPool()
        self.pool.globalInstance()
        self.pool.setMaxThreadCount(self.count)  # 设置最大线程数

    def downloadUser(self):

        userlineedit = self.userwidet.userlineedit.text()

        if not userlineedit:
            QMessageBox.information(self, "提示", "请选择需要下载的视频！")
            return False

        resultdirlineedit = self.userwidet.resultdirlineedit.text()

        if not resultdirlineedit:
            QMessageBox.information(self, "提示", "请选择下载到的目录！")
            return False

        with open(userlineedit, "r") as f:

            row = 0
            for url in f:
                self.movielistwidget.tablewidget.item(row, 0).setText('下载中')

                thread = DownloadShareMoive(row, url, resultdirlineedit)

                thread.signal.update_pb.connect(self.download_process)

                self.pool.start(thread)

                row = row + 1

    def download_process(self, row, value):

        if value == -1:
            self.movielistwidget.tablewidget.item(row, 0).setText('下载发生错误')
            return False

        self.movielistwidget.tablewidget.cellWidget(row, 2).setValue(value)

        if value == 100:
            self.movielistwidget.tablewidget.item(row, 0).setText('下载完毕')



class GetUserAllMoiveList(QThread):
    download_proess_signal = pyqtSignal(list)  # 创建信号

    def __init__(self, url):
        super(GetUserAllMoiveList, self).__init__()
        self.url = url

    def run(self):

        data = getUserVideos(self.url)
        print(data)

        if data:

            self.download_proess_signal.emit(data)
        else:
            self.download_proess_signal.emit([])

        self.exit(0)


class Signal(QObject):
    update_pb = pyqtSignal(int, int)


class DownloadShareMoive(QRunnable):
    def __init__(self, rows_index, download_url, dst_dir):
        super().__init__()
        self.rows_index = rows_index
        self.download_url = download_url
        self.dst_dir = dst_dir
        self.signal = Signal()  # 信号

        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, sdch, br",
            "accept-language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
            "cache-control": "no-cache",
            # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"

        }

    def run(self):

        data = getShareVideo(self.download_url)

        if data['videos']:

            for real_url in data['videos']:

                req = urllib.request.Request(real_url, headers=self.headers)
                resp = urllib.request.urlopen(req)
                file_size = int(resp.info().get('Content-Length', -1))

                header = {

                    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                }

                videoBin = requests.get(self.download_url, headers=header, stream=True)
                #videoBin = requests.get(real_url, timeout=60, headers=self.headers, stream=True);

                offset = 0
                with(open("{}/{}.mp4".format(self.dst_dir, uuid.uuid4()), 'wb')) as f:
                    for chunk in videoBin.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)

                            offset = offset + len(chunk)
                            proess = offset / int(file_size) * 100

                            self.signal.update_pb.emit(self.rows_index, int(proess))

        else:

            self.signal.update_pb.emit(self.rows_index, -1)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

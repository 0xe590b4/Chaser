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
import time
import json
import uuid
import urllib
import requests

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from share_download.share import getShareVideo



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




class ShareWidget(QWidget):

    def __init__(self, parent=None):
        super(ShareWidget, self).__init__(parent)

        self.setPalette(QPalette(Qt.lightGray))
        self.setAutoFillBackground(True)
        self.setMinimumSize(100, 100)

        self.initUi()

    def initUi(self):

        sharelabel = QLabel("分享视频地址", self)
        self.sharelineedit = QLineEdit()
        self.sharelineedit.setFocusPolicy(Qt.NoFocus)
        sharelabel.setBuddy(self.sharelineedit)

        sharepushbutton = QPushButton("浏览")
        sharepushbutton.clicked.connect(self.openShare)

        resultdirlabel = QLabel("下载到文件夹", self)
        self.resultdirlineedit = QLineEdit()
        self.resultdirlineedit.setFocusPolicy(Qt.NoFocus)
        resultdirlabel.setBuddy(self.resultdirlineedit)

        resultdirbutton = QPushButton("浏览")
        resultdirbutton.clicked.connect(self.openResultDir)

        sharegrid = QGridLayout()
        sharegrid.addWidget(sharelabel, 0, 0)  # 控件名，行，列，占用行数，占用列数，对齐方式
        sharegrid.addWidget(self.sharelineedit, 0, 1)
        sharegrid.addWidget(sharepushbutton, 0, 2)

        sharegrid.addWidget(resultdirlabel, 1, 0)  # 控件名，行，列，占用行数，占用列数，对齐方式
        sharegrid.addWidget(self.resultdirlineedit, 1, 1)
        sharegrid.addWidget(resultdirbutton, 1, 2)

        hbox = QHBoxLayout()
        hbox.addLayout(sharegrid)

        self.sharegroupbox = QGroupBox("")
        self.sharegroupbox.setLayout(hbox)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addWidget(self.sharegroupbox)
        self.show()

    def openShare(self):

        open_share_filename, o = QFileDialog.getOpenFileName(self, '选择文件', '',
                                                             "All files(*.txt)")

        if open_share_filename == "":
            return False

        self.sharelineedit.setText(open_share_filename)

        """
        注意： 这里要调用其它子窗体的内容
        """

        with open(open_share_filename, "r") as f:
            count = len(f.readlines())
            self.parent().movielistwidget.tablewidget.setRowCount(count)

        with open(open_share_filename, "r") as f:

            index = 0
            for line in f:
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
        self.sharewidet = ShareWidget(self)
        # 添加编辑框（QLineEdit）
        # self.lineEdit = QLineEdit("0") # 这里可以不要self

        self.downloadsharebutton = QPushButton("下载")
        self.downloadsharebutton.clicked.connect(self.downloadShare)

        # 放入布局内
        layout.addWidget(self.movielistwidget, 0, 0)
        layout.addWidget(self.sharewidet, 1, 0)
        # layout.addWidget(self.widget, 2, 0)
        layout.addWidget(self.downloadsharebutton, 2, 0)
        self.setLayout(layout)

        self.setWindowTitle("下载工具")

        self.count = 10
        self.pool = QThreadPool()
        self.pool.globalInstance()
        self.pool.setMaxThreadCount(self.count)  # 设置最大线程数

    def downloadShare(self):


        flag = is_regiter()
        if not flag['flag']:
            QMessageBox.information(self, "提示", flag['msg'])
            return False


        sharelineedit = self.sharewidet.sharelineedit.text()

        if not sharelineedit:
            QMessageBox.information(self, "提示", "请选择需要下载的视频！")
            return False

        resultdirlineedit = self.sharewidet.resultdirlineedit.text()

        if not resultdirlineedit:
            QMessageBox.information(self, "提示", "请选择下载到的目录！")
            return False

        rows = self.movielistwidget.tablewidget.rowCount()
        for row in range(0, rows):

            self.movielistwidget.tablewidget.item(row, 0).setText('下载中')

            url = self.movielistwidget.tablewidget.item(row, 1).text()


            thread = DownloadShareMoive(row, url, resultdirlineedit)

            thread.signal.update_pb.connect(self.download_process)

            self.pool.start(thread)



    def download_process(self, row, value):

        if value == -1:
            self.movielistwidget.tablewidget.item(row, 0).setText('下载发生错误')
            return False

        self.movielistwidget.tablewidget.cellWidget(row, 2).setValue(value)

        if value == 100:
            self.movielistwidget.tablewidget.item(row, 0).setText('下载完毕')


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

        try:
            data = getShareVideo(self.download_url)

            if data == 500:
                self.signal.update_pb.emit(self.rows_index, -1)

            if data.get('videos',None):

                for real_url in data['videos']:

                    req = urllib.request.Request(real_url, headers=self.headers)
                    resp = urllib.request.urlopen(req)
                    file_size = int(resp.info().get('Content-Length', -1))

                    videoBin = requests.get(real_url, timeout=60, headers=self.headers, stream=True);

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
        except:
            self.signal.update_pb.emit(self.rows_index, -1)




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

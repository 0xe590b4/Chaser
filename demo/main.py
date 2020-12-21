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
# from batch_maker.mobile import Mobile


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

        self.count = 10
        self.pool = QThreadPool()
        self.pool.globalInstance()
        self.pool.setMaxThreadCount(self.count)  # 设置最大线程数

        self.setPalette(QPalette(Qt.lightGray))
        self.setAutoFillBackground(True)
        self.setMinimumSize(100, 100)

        self.initUi()

    def initUi(self):

        sharelabel = QLabel("视频数据", self)
        self.sharelineedit = QLineEdit()
        self.sharelineedit.setFocusPolicy(Qt.NoFocus)
        sharelabel.setBuddy(self.sharelineedit)
        sharepushbutton = QPushButton("浏览")
        sharepushbutton.clicked.connect(self.openShare)

        bgmlabel = QLabel("背景音乐", self)
        self.bgmlineedit = QLineEdit(self)
        self.bgmlineedit.setFocusPolicy(Qt.NoFocus)
        bgmlabel.setBuddy(self.bgmlineedit)
        bgmbutton = QPushButton("浏览")
        bgmbutton.clicked.connect(self.openMusic)

        resultdirlabel = QLabel("下载到文件夹", self)
        self.resultdirlineedit = QLineEdit()
        self.resultdirlineedit.setFocusPolicy(Qt.NoFocus)
        resultdirlabel.setBuddy(self.resultdirlineedit)

        resultdirbutton = QPushButton("浏览")
        resultdirbutton.clicked.connect(self.openResultDir)

        movievolumelabel = QLabel("电影原声")
        self.movieslider = QSlider(Qt.Horizontal)
        self.movieslider.setMinimum(0)  # 最小值
        self.movieslider.setMaximum(10)  # 最大值
        self.movieslider.setSingleStep(1)  # 步长
        self.movieslider.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.movieslider.setTickInterval(1)  # 设置刻度间隔
        self.movieslider.setValue(5)
        self.movieslider.valueChanged.connect(self.movieChangeVolume)
        self.movievaluelabel = QLabel("5")

        bgmvolumelabel = QLabel("背景音乐")
        self.bgmslider = QSlider(Qt.Horizontal)
        self.bgmslider.setMinimum(0)  # 最小值
        self.bgmslider.setMaximum(10)  # 最大值
        self.bgmslider.setSingleStep(1)  # 步长
        self.bgmslider.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.bgmslider.setTickInterval(1)  # 设置刻度间隔
        self.bgmslider.setValue(5)
        self.bgmslider.valueChanged.connect(self.bgmChangeVolume)
        self.bgmvaluelabel = QLabel("5")

        titlelabel = QLabel("短视频标题", self)
        self.titlelineedit = QLineEdit("燕南赵北")
        titlelabel.setBuddy(self.titlelineedit)

        logolabel = QLabel("短视频LOGO", self)
        self.logolineedit = QLineEdit(self)
        self.logolineedit.setFocusPolicy(Qt.NoFocus)
        logolabel.setBuddy(self.logolineedit)
        logobutton = QPushButton("浏览")
        logobutton.clicked.connect(self.openLogo)

        downloadsharebutton = QPushButton("批量制作")
        downloadsharebutton.clicked.connect(self.downloadShare)

        sharegrid = QGridLayout()

        sharegrid.addWidget(sharelabel, 0, 0)  # 控件名，行，列，占用行数，占用列数，对齐方式
        sharegrid.addWidget(self.sharelineedit, 0, 1)
        sharegrid.addWidget(sharepushbutton, 0, 2)

        sharegrid.addWidget(bgmlabel, 1, 0)  # 控件名，行，列，占用行数，占用列数，对齐方式
        sharegrid.addWidget(self.bgmlineedit, 1, 1)
        sharegrid.addWidget(bgmbutton, 1, 2)

        sharegrid.addWidget(resultdirlabel, 2, 0)
        sharegrid.addWidget(self.resultdirlineedit, 2, 1)
        sharegrid.addWidget(resultdirbutton, 2, 2)

        sharegrid.addWidget(movievolumelabel, 3, 0)
        sharegrid.addWidget(self.movieslider, 3, 1)
        sharegrid.addWidget(self.movievaluelabel, 3, 2)

        sharegrid.addWidget(bgmvolumelabel, 4, 0)
        sharegrid.addWidget(self.bgmslider, 4, 1)
        sharegrid.addWidget(self.bgmvaluelabel, 4, 2)

        sharegrid.addWidget(titlelabel, 5, 0)
        sharegrid.addWidget(self.titlelineedit, 5, 1)

        sharegrid.addWidget(logolabel, 6, 0)  # 控件名，行，列，占用行数，占用列数，对齐方式
        sharegrid.addWidget(self.logolineedit, 6, 1)
        sharegrid.addWidget(logobutton, 6, 2)

        sharegrid.addWidget(downloadsharebutton, 7, 0, 1, 3)  # 控件名，行，列，占用行数，占用列数，对齐方式

        hbox = QHBoxLayout()
        hbox.addLayout(sharegrid)

        self.sharegroupbox = QGroupBox("")
        self.sharegroupbox.setLayout(hbox)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.addWidget(self.sharegroupbox)
        self.show()

    def openLogo(self):

        logo_filename, o = QFileDialog.getOpenFileName(self, '选择文件', '',
                                                       "All files(*.mp4 *.avi *.mkv *.jpg *.png *.jpeg)")

        if logo_filename == "":
            return False

        self.logolineedit.setText(logo_filename)

    def movieChangeVolume(self, volume):
        """

        :param volume:
        :return:
        """

        self.movievaluelabel.setText("{}".format(volume))

    def bgmChangeVolume(self, volume):
        """

        :param volume:
        :return:
        """

        self.bgmvaluelabel.setText("{}".format(volume))

    def openShare(self):

        open_share_filename, t = QFileDialog.getOpenFileNames(self, '选择文件', '', 'All files(*.mp4 , *.avi, *.mkv)')

        if open_share_filename == "":
            return False

        self.sharelineedit.setText(",".join(open_share_filename))

        """
        注意： 这里要调用其它子窗体的内容
        """

        self.parent().movielistwidget.tablewidget.setRowCount(len(open_share_filename))

        index = 0
        for line in open_share_filename:
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

    def openMusic(self):

        open_bgm_filename, o = QFileDialog.getOpenFileName(self, '选择文件', '',
                                                           'Sound Files (*.mp3 *.ogg *.wav *.m4a)')

        if open_bgm_filename == "":
            return False

        self.bgmlineedit.setText(open_bgm_filename)

    def downloadShare(self):

        flag = is_regiter()
        if not flag['flag']:
            QMessageBox.information(self, "提示", flag['msg'])
            return False

        sharelineedit = self.sharelineedit.text()

        if not sharelineedit:
            QMessageBox.information(self, "提示", "请选择需要下载的视频！")
            return False

        resultdirlineedit = self.resultdirlineedit.text()

        if not resultdirlineedit:
            QMessageBox.information(self, "提示", "请选择下载到的目录！")
            return False

        # selected_data = set(index.row() for index in self.movielistwidget.tablewidget.selectedIndexes())
        rows = self.parent().movielistwidget.tablewidget.rowCount()
        for row in range(0, rows):

            if self.parent().movielistwidget.tablewidget.item(row, 1) == None:
                continue

            self.parent().movielistwidget.tablewidget.item(row, 0).setText('下载中')

            data = {

                "start": 1,
                "end": 15,
                "title": self.titlelineedit.text(),
                "src_volume": self.movieslider.value(),
                "dst_volume": self.bgmslider.value(),
                "bgm_filename": self.bgmlineedit.text(),
                "watermark": self.logolineedit.text(),
                "output_video_filename": self.resultdirlineedit.text(),
                "video_name": os.path.basename(self.parent().movielistwidget.tablewidget.item(row, 1).text()),
                "input_video_filename": self.parent().movielistwidget.tablewidget.item(row, 1).text()

            }

            thread = MakeNewMoive(row, data)

            thread.signal.message.connect(self.thread_message)
            thread.signal.progress.connect(self.thread_progress)
            thread.signal.finished.connect(self.thread_finished)

            self.pool.start(thread)

    def thread_message(self, row, value):
        print("message", row, value)

        if value.find("Writing audio"):
            value = "正在处理音频"
        if value.find("Writing video"):
            value = "正在处理视频"
        self.parent().movielistwidget.tablewidget.item(row, 0).setText(value)

    def thread_progress(self, row, value):
        # print("progress",row, value)
        self.parent().movielistwidget.tablewidget.cellWidget(row, 2).setValue(value)

    def thread_finished(self, row):
        # print("finished")
        self.parent().movielistwidget.tablewidget.item(row, 0).setText('下载完毕')


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

        import  time
        time.sleep(5)
        super(MainWindow, self).__init__(parent)
        self.resize(900, 600)
        layout = QGridLayout()

        # 添加自定义部件（MyWidget）
        # self.widget = DownloadWindows()  # 这里可以不要self

        self.movielistwidget = MovieListWidget(self)
        self.sharewidet = ShareWidget(self)
        #self.adbWidget = AdbWidget(self)
        # 添加编辑框（QLineEdit）
        # self.lineEdit = QLineEdit("0") # 这里可以不要self

        # 放入布局内
        layout.addWidget(self.movielistwidget, 0, 0)
        layout.addWidget(self.sharewidet, 0, 1)
        #layout.addWidget(self.adbWidget, 0, 2)

        self.setLayout(layout)

        self.setWindowTitle("批量二次制作")


class Signal(QObject):
    progress = pyqtSignal(int, int)
    message = pyqtSignal(int, str)
    finished = pyqtSignal(int)


class MakeNewMoive(QRunnable):

    def __init__(self, rows_index, data):
        super().__init__()
        self.rows_index = rows_index
        self.data = data
        self.signal = Signal()  # 信号

    def run(self):
        from batch_maker.tools import ShortVideo

        my_logger = MyBarLogger(self.rows_index, self.signal.message, self.signal.progress)

        shortVideo = ShortVideo()
        shortVideo.make_new_video(self.data, my_logger)

        self.signal.finished.emit(self.rows_index)


class MyBarLogger(ProgressBarLogger):
    actions_list = []

    def __init__(self, rows_index, message, progress):
        self.rows_index = rows_index
        self.message = message
        self.progress = progress
        super(MyBarLogger, self).__init__()

    def callback(self, **changes):
        bars = self.state.get('bars')
        index = len(bars.values()) - 1
        if index > -1:
            bar = list(bars.values())[index]
            progress = int(bar['index'] / bar['total'] * 100)
            self.progress.emit(self.rows_index, progress)
        if 'message' in changes: self.message.emit(self.rows_index, changes['message'])





if __name__ == '__main__':
    import sys


    app = QApplication(sys.argv)


    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
# @Time    : 2020-06-28  16:09
# @Author  : 行颠
# @Email   : 0xe590b4@gmail.com
# @File    : demo
# @Software: Chaser
# @DATA    : 2020-06-28
"""

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from config import *


class MainWidget(QMainWindow):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.init_menu()
        self.init_style()
        self.init_player_widget()
        self.init_right_tool()
        self.init_bottom_tool()

        self.statusBar().showMessage('这里是状态栏...')

        self.movie_list_real_data = []
        self.movie_list_name_data = []

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '窗口关闭', '确认关闭操作台吗?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
            # print('Window closed')
        else:
            event.ignore()

    def init_menu(self):

        # 这个菜单

        bar = self.menuBar()  # 获取菜单栏

        openAction = QAction("Open", self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        openAction.triggered.connect(self.fun_open_movies)

        quitAction = QAction("Close", self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.setStatusTip('Close movie')
        quitAction.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        quitAction.triggered.connect(qApp.quit)

        file = bar.addMenu("File")
        file.addAction(openAction)
        file.addAction(quitAction)

        edit = bar.addMenu("Setting")
        edit.addAction("copy")
        edit.addAction("paste")

    def init_style(self):

        self.setWindowTitle(self.tr("视频工具窗口"))

        # import qdarkstyle
        # self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # with open(WINDOWS_CSS, "r") as fh:
        #     self.setStyleSheet(fh.read())

        # self.setAutoFillBackground(True)

        desktop_geometry = QApplication.desktop()  # 获取屏幕大小
        self.width = desktop_geometry.width() * 0.8  # 屏幕的宽
        self.height = desktop_geometry.height() * 0.85  # 屏幕的高
        self.setFixedSize(int(self.width), int(self.height))

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        # QApplication.setStyle(QStyleFactory.create('Windows'))

    def init_player_widget(self):

        # 播放列表
        self.movie_list_widget = QListWidget(self)
        self.movie_list_widget.setAlternatingRowColors(True)
        self.movie_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.movie_list_widget.setMovement(QListView.Free)
        self.movie_list_widget.setMouseTracking(True)

        self.movie_list_widget.setStyleSheet(
            "QListWidget{border:1px solid gray; color:black; }"
            "QListWidget::Item{padding-top:10px; padding-bottom:10px; font-size:18px;font-weight:bold;}"
            "QListWidget::Item:hover{background:skyblue; }"
            "QListWidget::item:selected{background:lightgray; color:red; }"
            "QListWidget::item:selected:!active{border-width:0px; background:lightgreen; }"
        )

        self.movie_list_widget.setFixedWidth(180)
        self.movie_list_widget.itemClicked.connect(self.fun_item_click)

        # 定义视频显示的widget
        video_widget = QVideoWidget()

        # 进度
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.fun_set_position)

        # 播放按钮
        self.playButton = QPushButton(self)
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.fun_play)

        # 操作左右
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)

        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.playButton)

        # 视频和操作上下
        videoLayout = QVBoxLayout()
        videoLayout.addWidget(video_widget)
        videoLayout.addLayout(controlLayout)

        # 播放列表和播放器 左右结构
        hbox = QHBoxLayout()
        hbox.addWidget(self.movie_list_widget)
        hbox.addLayout(videoLayout)

        # setCentralWidget需要的
        centralWidget = QWidget()
        centralWidget.setLayout(hbox)

        self.setCentralWidget(centralWidget)

        # player
        self.playlist = QMediaPlaylist(self)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setPlaylist(self.playlist)

        self.mediaPlayer.setVideoOutput(video_widget)
        self.mediaPlayer.stateChanged.connect(self.fun_media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.fun_position_changed)
        self.mediaPlayer.durationChanged.connect(self.fun_duration_changed)
        self.mediaPlayer.error.connect(self.fun_handle_error)

        self.mediaPlayer.positionChanged.connect(self.on_videoFrameProbed)
        self.mediaPlayer.setNotifyInterval(60)




    def on_videoFrameProbed(self):

        print(QTime.currentTime().toString("hh:mm:ss.zzz"))


    def init_right_tool(self):

        # 停靠窗口2
        self.logo_dock = QDockWidget(self.tr("水印设置"), self)
        self.logo_dock.setObjectName("logo")
        self.logo_dock.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        self.logo_dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.logo_dock.installEventFilter(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.logo_dock)

        # 停靠窗口4
        self.base_dock = QDockWidget(self.tr("基础设置"), self)
        self.base_dock.setObjectName("base")
        self.base_dock.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        self.base_dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.base_dock.installEventFilter(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.base_dock)

        self.logo_dock.setWidget(self.create_logo_group())
        self.base_dock.setWidget(self.create_base_setting_group())

        self.tabifyDockWidget(self.logo_dock, self.base_dock)
        self.logo_dock.raise_()

        self.addDockWidget(Qt.RightDockWidgetArea, self.base_dock)

        self.is_hide_logo = False
        self.is_hide_base = False

    def create_logo_group(self):

        # 1.生成实例 groupBox =》 对应窗口
        self.groupBox6 = QGroupBox()

        # 2.创建一些小部件，比如button或者raido

        self.pos1 = QRadioButton('左上', self)
        self.pos2 = QRadioButton('左下', self)
        self.pos3 = QRadioButton('右上', self)
        self.pos4 = QRadioButton('右下', self)
        self.pos4.toggle()

        self.pos = QButtonGroup(self)
        self.pos.addButton(self.pos1, 0)
        self.pos.addButton(self.pos2, 1)
        self.pos.addButton(self.pos3, 2)
        self.pos.addButton(self.pos4, 3)

        self.logo_label = QLabel("水印文件", self)
        self.logo_line = QLineEdit(LOGO)
        self.logo_line.setFocusPolicy(Qt.NoFocus)
        self.logo_label.setBuddy(self.logo_line)
        self.btn_open_logo = QPushButton("浏览")
        self.btn_open_logo.clicked.connect(self.fun_open_logo_file)

        self.opacity_label = QLabel("透明程度")
        self.opacity_line = QLineEdit("15")
        self.opacity_label.setBuddy(self.opacity_line)

        grid = QGridLayout()

        grid.addWidget(self.logo_label, 0, 0, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式
        grid.addWidget(self.logo_line, 0, 1, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式
        grid.addWidget(self.btn_open_logo, 0, 2, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式

        grid.addWidget(self.opacity_label, 1, 0, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式
        grid.addWidget(self.opacity_line, 1, 1, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式

        grid.addWidget(self.pos1, 2, 0, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式
        grid.addWidget(self.pos2, 2, 1, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式
        grid.addWidget(self.pos3, 3, 0, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式
        grid.addWidget(self.pos4, 3, 1, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式

        # 4. 应用之前设置好的layout
        self.groupBox6.setLayout(grid)

        return self.groupBox6

    def create_base_setting_group(self):

        # 1.生成实例 groupBox =》 对应窗口
        self.groupBox4 = QGroupBox()

        # 2.创建一些小部件，比如button或者raido

        self.colorx_label = QLabel("视频亮度")
        self.colorx = QSlider(Qt.Horizontal)
        self.colorx.setMinimum(0)  # 最小值
        self.colorx.setMaximum(100)  # 最大值
        self.colorx.setSingleStep(1)  # 步长
        self.colorx.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.colorx.setTickInterval(10)  # 设置刻度间隔
        self.colorx.setValue(50)
        # self.colorx.valueChanged.connect(self.set_colorx)

        self.blackwhite_label = QLabel("黑白电影")
        self.blackwhite = QCheckBox()

        # self.blackwhite.stateChanged.connect(self.set_blackwhite)

        self.speedx_label = QLabel("视频加速")
        self.speedx = QSlider(Qt.Horizontal)
        self.speedx.setMinimum(-5)  # 最小值
        self.speedx.setMaximum(5)  # 最大值
        self.speedx.setSingleStep(1)  # 步长
        self.speedx.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.speedx.setTickInterval(1)  # 设置刻度间隔
        self.speedx.setValue(1)
        # self.speedx.valueChanged.connect(self.set_speedx)

        grid = QGridLayout()

        grid.addWidget(self.colorx_label, 0, 0, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式
        grid.addWidget(self.colorx, 0, 1)  # 控件名，行，列，占用行数，占用列数，对齐方式

        grid.addWidget(self.speedx_label, 1, 0, 1, 1, Qt.AlignLeft)
        grid.addWidget(self.speedx, 1, 1)

        grid.addWidget(self.blackwhite_label, 2, 0, 1, 1, Qt.AlignLeft)  # 控件名，行，列，占用行数，占用列数，对齐方式
        grid.addWidget(self.blackwhite, 2, 1)  # 控件名，行，列，占用行数，占用列数，对齐方式

        # 4. 应用之前设置好的layout
        self.groupBox4.setLayout(grid)

        return self.groupBox4

    def eventFilter(self, source, event):

        if (source.objectName() in ["logo", "base"] and event.type() == QEvent.MouseButtonDblClick and isinstance(
                source, QDockWidget)):

            if self.is_hide_logo:

                te2 = self.create_logo_group()
                self.logo_dock.setWidget(te2)

                te4 = self.create_base_setting_group()
                self.base_dock.setWidget(te4)

                self.is_hide_logo = False
                self.is_hide_base = False
            else:

                self.base_dock.setWidget(QWidget())
                self.logo_dock.setWidget(QWidget())

                self.is_hide_logo = True
                self.is_hide_base = True

        return super(MainWidget, self).eventFilter(source, event)

    def init_bottom_tool(self):

        # 停靠窗口3
        dock3 = QDockWidget(self.tr("停靠窗口3"), self)
        dock3.setFeatures(QDockWidget.AllDockWidgetFeatures)
        te3 = QTextEdit(self.tr("窗口3,可在Main Window任意位置停靠，可浮动，可关闭"))
        dock3.setWidget(te3)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock3, Qt.Vertical)

        # 停靠窗口5
        dock5 = QDockWidget(self.tr("停靠窗口5"), self)
        dock5.setFeatures(QDockWidget.AllDockWidgetFeatures)
        te5 = QTextEdit(self.tr("窗口3,可在Main Window任意位置停靠，可浮动，可关闭"))
        dock5.setWidget(te5)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock5, Qt.Vertical)

        self.tabifyDockWidget(dock3, dock5)
        dock3.raise_()

    ## ==============================================================

    def fun_open_logo_file(self):

        open_logo_filename, o = QFileDialog.getOpenFileName(self, '选择文件', '',
                                                            "All files(*.mp4 *.avi *.mkv *.jpg *.png *.jpeg)")

        if open_logo_filename == "":
            return False

        self.logo_line.setText(open_logo_filename)

    def fun_item_click(self, item):
        # print(item, str(item.text()))
        # print(self.movie_list_widget.row(item))

        movie_file = self.movie_list_real_data[self.movie_list_widget.row(item)]

        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(movie_file)))

        self.mediaPlayer.play()
        self.playButton.setEnabled(True)

    def fun_open_movies(self):

        input_videos, t = QFileDialog.getOpenFileNames(self, '选择文件', '', 'All files(*.mp4 , *.avi, *.mkv)')

        if input_videos == []:
            return False

        for n in input_videos:
            self.movie_list_name_data.append(os.path.basename(n))

            self.movie_list_real_data.append(n)

        # 加到左边的tree中
        self.movie_list_widget.addItems(self.movie_list_name_data)

        # 加到播放列表中并自动播放
        for video in self.movie_list_real_data:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(video)))

        self.playlist.setCurrentIndex(0)
        self.mediaPlayer.play()

    def fun_play(self):

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def fun_media_state_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def fun_position_changed(self, position):
        self.positionSlider.setValue(position)

    def fun_duration_changed(self, duration):
        self.positionSlider.setRange(0, duration)

    def fun_set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def fun_set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def fun_handle_error(self):
        self.playButton.setEnabled(True)
        print("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWidget()
    main.show()
    app.exec_()

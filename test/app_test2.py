#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
# @Time    : 2020-07-15  21:30
# @Author  : 行颠
# @Email   : 0xe590b4@gmail.com
# @File    : app_test2.py
# @Software: Chaser
# @DATA    : 2020-07-15

https://zhuanlan.zhihu.com/p/115825045
https://www.cnblogs.com/tuxiaomeng/p/10442514.html

pip install Appium-Python-Client

"""

import time

from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


caps = {
    "platformName": "android", #运行平台 ios还是android
    "deviceName": "292d6d29", # 设备名 adb devices -l
    "platformVersion": "8.0.0", #系统版本 adb shell getprop ro.build.version.release
    'appPackage': 'com.ss.android.ugc.aweme', # 包名 adb shell dumpsys window w |grep \\/ |grep name=
    'appActivity': '.main.MainActivity' #启动入口
 }

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)


def get_name(name):
    '''
    定位页面text元素
    :param name:
    :return:
    '''
    # element = driver.find_element_by_name(name)
    # return element
    element = driver.find_element_by_xpath("//*[@text='%s']")%(name)
    return element

get_name("好的").click()
"""

adb devices -l

https://github.com/yi-heng/Android-Test/blob/master/Template/common/mobile.py

# win
adb.exe shell dumpsys window |findstr mCurrent
# mac
adb shell dumpsys window w |grep \\/ |grep name=

adb -s {0} shell getprop ro.build.version.release

"""
import os
import time
import uiautomator2 as u2
from ppadb.client import Client as AdbClient


class Mobile(object):


    def __init__(self):


        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.devices = self.client.devices()

        self.package_name = "com.ss.android.ugc.aweme"
        self.apk_filename = "/Users/0xe590b4/Downloads/aweme_aweGW_v11.3.0_b5b6cb6.apk"
        self.remote_file_path = "/mnt/sdcard/autotest/"
        self.local_file_path = "/Users/0xe590b4/Downloads/vvv/"

    def info(self):

        for device in self.devices:
            print(device.client)
            print(device.serial)

    def install_app(self):

        #检查软件包是否安装 如果没安装则安装
        for device in self.devices:

            is_installed = device.is_installed(self.package_name)

            if not is_installed:

                device.install(self.apk_filename,grand_all_permissions=True)

    def push_movies_to_mobile(self):

        #将本地的内容推送到远端
        for device in self.devices:

            r = device.shell("mkdir -p  {}".format(self.remote_file_path))

            for filename in os.listdir(self.local_file_path):

                device.push("{}/{}".format(self.local_file_path,filename), "{}/{}".format(self.remote_file_path,filename))

    def push_movie_to_douyin(self):

        for device in self.devices:

            #d = u2.connect('192.168.0.101')
            d = u2.connect_usb(device.serial)

            # 启动App
            d.app_start(self.package_name)

            if d(text="发现通讯录好友", resourceId="com.ss.android.ugc.aweme:id/title").exists(timeout=1):
                d(text="取消", resourceId="com.ss.android.ugc.aweme:id/rk").click()

            if d(text="我知道了").exists(timeout=2):
                d(text="我知道了").click()
            if d(text="权限请求").exists(timeout=1):
                d(resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
                d(text="始终允许").click()

            # 请求定位
            if d(text="权限请求").exists(timeout=1):
                d(resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
                d(text="始终允许").click()

            # 判断权限
            if d(text="权限请求").exists(timeout=0.2):
                d(text="禁止后不再询问", resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
                d(text="始终允许").click()

            if d(text="权限请求").exists(timeout=0.2):
                d(text="禁止后不再询问", resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
                d(text="始终允许").click()
            # 存储
            if d(text="权限请求").exists(timeout=0.2):
                d(text="禁止后不再询问", resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
                d(text="始终允许").click()






            for filename in os.listdir(self.local_file_path):

                d.press("home")
                d(description="文件管理").click()

                d.xpath(
                    '//android.widget.HorizontalScrollView/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]/android.widget.RelativeLayout[1]').click()

                d(text="100autotest").click()

                print("正在处理：",filename)
                while True:

                    if d(text=filename).exists:  # 判断指定的视频是否存在
                        d(text=filename).long_click()  # 如果存在就点击
                        break
                    else:
                        d.swipe_ext("up", 0.5)  # 如果不存在就从下往上滑动


                d(text="发送").click()


                d(text="抖音短视频").click()


                d(text="下一步").click()


                d(text="下一步").click()


                d.send_keys("#我要上热门  昨天北京的雨", clear=True)


                # d(description="发布").click()


            d.app_stop(self.package_name)


if __name__ == '__main__':

    m = Mobile()
    m.push_movie_to_douyin()
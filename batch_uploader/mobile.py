"""

adb devices -l

https://github.com/yi-heng/Android-Test/blob/master/Template/common/mobile.py

https://zhuanlan.zhihu.com/p/77497753

# win
adb.exe shell dumpsys window |findstr mCurrent
# mac
adb shell dumpsys window w |grep \\/ |grep name=

adb -s {0} shell getprop ro.build.version.release

"""
import os
import uiautomator2 as u2
# from ppadb.client import Client as AdbClient


class Mobile(object):


    def __init__(self,device):

        self.package_name = "com.ss.android.ugc.aweme" #com.ss.android.ugc.aweme.splash.SplashAdActivity
        self.apk_filename = "https://s9.pstatp.com/package/apk/aweme/110801/aweme_aweGW_v110801_2563_1594204828.apk?v=1594204832"

        self.adb = u2.connect(device)
        # self.adb = u2.connect_usb(device.serial)


    def install_app(self):

        try:
            self.adb.app_info(self.package_name)

        except:

            try:
                self.adb.app_install(self.apk_filename)
            except:
                return  False

        return True

    def push_movies_to_mobile(self,local_filename, remote_filename):

        remote_dir = os.path.dirname(remote_filename)
        self.adb.shell("mkdir -p  {}".format(remote_dir))

        self.adb.push(local_filename, remote_filename)



    def check(self):

        if self.adb(text="发现通讯录好友", resourceId="com.ss.android.ugc.aweme:id/title").exists(timeout=1):
            self.adb(text="取消", resourceId="com.ss.android.ugc.aweme:id/rk").click()

        if self.adb(text="我知道了").exists(timeout=2):
            self.adb(text="我知道了").click()
        if self.adb(text="权限请求").exists(timeout=1):
            self.adb(resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
            self.adb(text="始终允许").click()

            # 请求定位
        if self.adb(text="权限请求").exists(timeout=1):
            self.adb(resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
            self.adb(text="始终允许").click()

            # 判断权限
        if self.adb(text="权限请求").exists(timeout=0.2):
            self.adb(text="禁止后不再询问", resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
            self.adb(text="始终允许").click()

        if self.adb(text="权限请求").exists(timeout=0.2):
            self.adb(text="禁止后不再询问", resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
            self.adb(text="始终允许").click()
            # 存储
        if self.adb(text="权限请求").exists(timeout=0.2):
            self.adb(text="禁止后不再询问", resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
            self.adb(text="始终允许").click()

            # 存储
        if self.adb(text="允许").exists(timeout=0.2):
            self.adb(text="不再询问", resourceId="com.android.packageinstaller:id/do_not_ask_checkbox").click()
            self.adb(text="允许").click()


    def push_movie_to_douyin(self,filename):


        print("filename",filename)


        self.adb.press("home")
        self.adb(description="文件管理").click()

        self.adb.xpath(
            '//android.widget.HorizontalScrollView/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]/android.widget.RelativeLayout[1]').click()

        #self.adb(text="100autotest").click()

        while True:

            if self.adb(text="autotest").exists:  # 判断指定的视频是否存在
                self.adb(text="autotest").click()  # 如果存在就点击
                break
            else:
                self.adb.swipe_ext("up", 0.5)  # 如果不存在就从下往上滑动

        print("正在处理：",filename)
        while True:

            if self.adb(text=filename).exists:  # 判断指定的视频是否存在
                self.adb(text=filename).long_click()  # 如果存在就点击
                break
            else:
                self.adb.swipe_ext("up", 0.5)  # 如果不存在就从下往上滑动


        self.adb(text="发送").click()


        self.adb(text="抖音短视频").click()

        self.check()

        self.adb(text="下一步").click()


        self.adb(text="下一步").click()


        self.adb.send_keys("#我要上热门  昨天北京的雨", clear=True)

        # self.adb(description="发布").click()

        # 启动App
        #self.adb.app_start(self.package_name)

        # 关闭app
        self.adb.app_stop(self.package_name)


if __name__ == '__main__':

    m = Mobile('192.168.0.100')
    m.install_app()

    remote_file_path = "/mnt/sdcard/autotest"
    local_file_path = "/Users/0xe590b4/Downloads/test"
    m.push_movies_to_mobile(local_file_path,remote_file_path)


    #m.push_movie_to_douyin(local_file_path)
#!/usr/bin/sh

#pip3 install py2app

#py2applet --make-setup main.py
#python3 setup.py py2app -A

rm -rf build
rm -rf dist

pyinstaller \
--exclude-module='FixTk' \
--exclude-module='tcl' \
--exclude-module='tk' \
--exclude-module='_tkinter' \
--exclude-module='tkinter' \
--exclude-module='Tkinter' \
--exclude-module='gi' \
--exclude-module='matplotlib' \
--hidden-import=pkg_resources.py2_warn \
--clean \
--noconsole \
-i logo.icns \
-n user_download \
-w -F main.py



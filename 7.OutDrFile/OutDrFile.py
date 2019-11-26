# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================
# Rev01
# 基本实现 导出DR文件的自动化流程

#==========================================================
from pynput.keyboard import Key, Controller
from win32gui import *
import win32gui, win32con, win32com.client
import time
import re

class DR_FILE_NODE:
    #def __init__(self):
    def allwindowsname(self,hwnd, mouse):
        #self.shortname =''
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            #print(GetClassName(hwnd)+'==>'+GetWindowText(hwnd))

            if 'FUNCTION_BLOCK' in GetWindowText(hwnd):
                self.svwindowtext = GetWindowText(hwnd)
                self.svclassname = GetClassName(hwnd)

            if 'Draw:DR' in GetWindowText(hwnd):
                self.drwindowtext = GetWindowText(hwnd)
                self.drclassname = GetClassName(hwnd)
                self.shortname = re.search('DR([\w\W\[0-9]{4}]*?)', self.drwindowtext, flags=0).group(0)

    def command(self):
        self.svwindowtext = ''
        self.svclassname = ''
        self.drwindowtext = ''
        self.drclassname = ''
        EnumWindows(self.allwindowsname, 0)
        #print("=" * 20)

    def active_dr_builder (self):
        if self.drwindowtext != '' :
            dr_builder_window = win32gui.FindWindow(self.drclassname, self.drwindowtext)
            win32gui.SetForegroundWindow(dr_builder_window)
        else:
            print("Control Drawing Builder is not Open !" )
            exit()

    def close_dr_builder(self):
        if self.drwindowtext != '' :
            dr_builder_window = win32gui.FindWindow(self.drclassname, self.drwindowtext)
            win32gui.PostMessage(dr_builder_window, win32con.WM_CLOSE, 0, 0)
        else:
            print("Control Drawing Builder is not Open !" )
            exit()

    def active_function_block (self):
        if self.svwindowtext != '' :
            function_block_window = win32gui.FindWindow(self.svclassname, self.svwindowtext)
            win32gui.SetForegroundWindow(function_block_window)
        else:
            print("Control Drawing Builder is not Open !" )
            exit()

    def out_txt(self):
        self.keyboard = Controller()
        time.sleep(self.sleeptime)  # 休眠1秒
        self.keyboard.press(Key.alt)
        self.keyboard.press('f')
        self.keyboard.release('f')

        time.sleep(self.sleeptime)
        self.keyboard.press('e')
        self.keyboard.release('e')

        time.sleep(self.sleeptime)
        self.keyboard.press('e')
        self.keyboard.release('e')

        time.sleep(self.sleeptime)
        self.keyboard.release(Key.alt)
        self.keyboard.type(self.shortname)
        print(self.shortname)
        self.shortname = ''

        time.sleep(self.sleeptime)
        self.keyboard.press(Key.alt)
        self.keyboard.press('s')
        self.keyboard.release('s')
        self.keyboard.release(Key.alt)

        time.sleep(self.sleeptime)
        self.keyboard.press(Key.left)
        self.keyboard.release(Key.left)

        time.sleep(self.sleeptime)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def circuit(self,count):
        #count = 2
        self.sleeptime = 0.5

        for _ in range(count):
            time.sleep(2)
            self.command()
            time.sleep(self.sleeptime)
            self.active_dr_builder()
            time.sleep(self.sleeptime)
            self.out_txt()
            time.sleep(self.sleeptime)
            self.close_dr_builder()
            time.sleep(self.sleeptime)
            self.active_function_block()
            time.sleep(self.sleeptime)
            self.keyboard.press(Key.down)
            self.keyboard.release(Key.down)
            time.sleep(self.sleeptime)
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)

if __name__ == "__main__":
    app = DR_FILE_NODE()
    #EnumWindows(app.allwindowsname, 0)  #遍历所有
    app.circuit(40)


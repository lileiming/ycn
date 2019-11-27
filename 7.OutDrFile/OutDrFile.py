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
        self.__delay()
        if self.drwindowtext != '' :
            dr_builder_window = win32gui.FindWindow(self.drclassname, self.drwindowtext)
            win32gui.PostMessage(dr_builder_window, win32con.WM_CLOSE, 0, 0)
        else:
            print("Control Drawing Builder is not Open !" )
            exit()

    def active_function_block (self):
        self.__delay()
        if self.svwindowtext != '' :
            function_block_window = win32gui.FindWindow(self.svclassname, self.svwindowtext)
            win32gui.SetForegroundWindow(function_block_window)
        else:
            print("Control Drawing Builder is not Open !" )
            exit()

    def press_key(self,combination = '',*abc):
        self.__delay()
        self.keyboard = Controller()
        if combination != '':
            self.keyboard.press(combination)

        for _ in abc:
            print(_)
            self.press_abc(_)
            self.__delay()

        if combination != '':
            self.keyboard.release(combination)

    def press_abc(self,_character):
        keyboard = Controller()
        keyboard.press(_character)
        keyboard.release(_character)

    def __delay(self,delaytime = 1):
        time.sleep(delaytime)

    def out_txt(self):
        self.press_key(Key.alt,'f','e','e')
        self.keyboard.type(self.shortname)
        print(self.shortname)
        self.shortname = ''
        self.press_key(Key.alt, 's')
        self.press_key(Key.left,Key.enter)
        #self.press_key(Key.enter)


    def circuit(self,count):
        for _ in range(count):
            self.__delay(2)
            self.command()
            self.active_dr_builder()
            self.out_txt()
            self.close_dr_builder()
            self.active_function_block()
            self.press_key(Key.down,Key.enter)
            #self.press_key(Key.enter)

    def foo(self,hwnd, mous):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            print(GetClassName(hwnd)+'==>'+GetWindowText(hwnd))
            #print(type(GetClassName(hwnd)))
        #pass
    def active_(self):
        shell = win32com.client.Dispatch("WScript.Shell")
        #shell.SendKeys('%')
        shell.Run("C:\CENTUMVP\program\BKHCallSysFunc O " + '18-PDISA-18103 TUN -SM')
        #pass

if __name__ == "__main__":
    app = DR_FILE_NODE()
    #app.circuit(40)
    EnumWindows(app.foo, 0)
    #app.active_()



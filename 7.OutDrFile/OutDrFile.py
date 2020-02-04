# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================
# Rev01
# 基本实现 导出DR文件的自动化流程

#==========================================================
from pynput.keyboard import Key, Controller
from pynput import keyboard
from win32gui import *
import win32gui, win32con, win32com.client
import time
import re
from tkinter import *
# 导入ttk
from tkinter import ttk
import YokoRead   #自定义模块

class DR_FILE_NODE:
    #def __init__(self):
    def all_windows_name(self,hwnd, mouse):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            #print(GetClassName(hwnd)+'==>'+GetWindowText(hwnd))
            if 'FUNCTION_BLOCK' in GetWindowText(hwnd):
                self.svwindowtext = GetWindowText(hwnd)
                self.svclassname = GetClassName(hwnd)
            if 'Draw:DR' in GetWindowText(hwnd):
                self.drwindowtext = GetWindowText(hwnd)
                self.drclassname = GetClassName(hwnd)
                #self.shortname = re.search('DR([\w\W\[0-9]{4}]*?)', self.drwindowtext, flags=0).group(0)
                self.shortname = re.search('[\w\W\[0-9]{6}]*?(?=.edf)', self.drwindowtext, flags=0).group(0)

    def command(self):
        self.svwindowtext = ''
        self.svclassname = ''
        self.drwindowtext = ''
        self.drclassname = ''
        EnumWindows(self.all_windows_name, 0)
        #print("=" * 20)

    def active_dr_builder (self):
        if self.drwindowtext != '' :
            dr_builder_window = win32gui.FindWindow(self.drclassname, self.drwindowtext)
            win32gui.SetForegroundWindow(dr_builder_window)
        else:
            print("Control Drawing Builder is not Open !1" )
            exit()

    def close_dr_builder(self):
        self.__delay()
        if self.drwindowtext != '' :
            dr_builder_window = win32gui.FindWindow(self.drclassname, self.drwindowtext)
            win32gui.PostMessage(dr_builder_window, win32con.WM_CLOSE, 0, 0)
        else:
            print("Control Drawing Builder is not Open !2" )
            exit()

    def active_function_block (self):
        self.__delay()
        if self.svwindowtext != '' :
            function_block_window = win32gui.FindWindow(self.svclassname, self.svwindowtext)
            win32gui.SetForegroundWindow(function_block_window)
        else:
            print("Control Drawing Builder is not Open !3" )
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

    def __delay(self,delaytime = 0.2):
        time.sleep(delaytime)

    def out_txt(self):
        self.press_key(Key.alt,'f','e','e')
        self.keyboard.type(self.shortname)
        print(self.shortname)
        self.shortname = ''
        self.press_key(Key.alt, 's')
        self.press_key(Key.left,Key.enter)
        #self.press_key(Key.enter)

    def circuit(self,count):   #循环流程
        for _ in range(count):
            self.__delay(2)
            self.command()
            self.active_dr_builder()
            self.out_txt()
            self.close_dr_builder()
            self.active_function_block()
            #self.__delay(5)  or  self.listener_() # 按空格键 程序继续
            self.__delay(5)
            self.press_key(Key.down,Key.enter)

    def foo(self,hwnd, mous):
        #遍历所有打开窗口
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
             print(GetClassName(hwnd)+'==>'+GetWindowText(hwnd))
            #print(type(GetClassName(hwnd)))
        #pass
    def active_(self):
        # 打开其他应用
        shell = win32com.client.Dispatch("WScript.Shell")
        #shell.SendKeys('%')
        shell.Run("C:\CENTUMVP\program\BKHCallSysFunc O " + '18-PDISA-18103 TUN -SM')
        #pass

    def listener_(self):
        def on_release(key):
            #print('{0} released'.format(key))
            if key == keyboard.Key.space:
                return False

        with keyboard.Listener(on_release=on_release) as listener:
                listener.join()

class Windows_NODE(DR_FILE_NODE):
    def __init__(self, master):
        self.master = master
        self.initWidgets()
        help_doc = '本程序为快速组态导入导出工具. \n\n使用方法：\n\n1.填写到处DR文件数量.\n2.打开 Control Drawing Builder(DR文件组态界面).\n\
3.点击导出按钮执行程序.\n'
        self.Text.insert('insert', help_doc)

    def initWidgets(self):
        # 创建中下
        bot_frame1 = LabelFrame(self.master, text='使用方法')
        bot_frame1.pack(fill=X, side=TOP, padx=15, pady=0)
        self.Scroll = Scrollbar(bot_frame1)

        self.Text = Text(bot_frame1, width=85, height=15, yscrollcommand=self.Scroll.set)
        self.Text.pack(side=LEFT, padx=0, pady=5)
        self.Scroll = Scrollbar(bot_frame1)
        self.Scroll.pack(side=LEFT, fill=Y)
        self.Scroll.config(command=self.Text.yview)

        # 创建底部
        bot_frame = LabelFrame(self.master)
        bot_frame.pack(fill=X, side=TOP, padx=15, pady=8)

        self.e = StringVar()
        ttk.Label(bot_frame, width=10, textvariable=self.e).pack(side=LEFT)
        self.e.set("导出数量:")

        self.e1 = StringVar()
        self.entry = ttk.Entry(bot_frame, width=20, textvariable=self.e1)
        self.e1.set("0")
        self.entry.pack(side=LEFT, pady=10)

        ttk.Button(bot_frame, text='导出', command=self.start).pack(side=RIGHT)


    def start(self):
        try:
            num = int(self.entry.get())
            print(num)
        except ValueError :
            print("请输入数字.")
            self.entry.delete(0,END)
            num = 0

        self.circuit(num)
        EnumWindows(self.foo, 0)  # 遍历所有窗口
        pass



if __name__ == "__main__":

    #print(app.listener_())
    #app.active_()

    root = Tk()
    root.geometry('480x300')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoRead._ALRM_NODE_.limited_time(root)
    root.title("DR文件导出工具 V1.00"+"    到期日:"+limit_time)
    root.mainloop()


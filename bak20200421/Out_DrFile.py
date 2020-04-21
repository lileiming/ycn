# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
#==========================================================
# Rev01
# 基本实现 导出DR文件的自动化流程

#==========================================================
from pynput.keyboard import Key, Controller
from pynput import keyboard
from win32gui import *
import win32gui, win32con, win32com.client
from tkinter import *
from tkinter import ttk
from time import sleep
import YokoRead   #自定义模块
from YokoRead import time_Decorator,thread_Decorator


class Windows_NODE(YokoRead.FILE_NODE):
    def __init__(self, master):
        self.master = master
        self.initWidgets()
        help_doc = '本程序为快速组态导入导出工具（DR/IOM/SW）. \n\n' \
                   '(DR文件)使用方法：\n\n' \
                   '1.填写导出DR文件数量.\n' \
                   '2.打开 Control Drawing Builder(DR文件组态界面).\n' \
                   '3.点击导出按钮执行程序.\n' \
                   '4.将本窗口隐藏至最小化.\n\n' \
                   'IOM/SW开关导出类似.\n\n'

        self.Text.insert('insert', help_doc)

    def initWidgets(self):
        # 创建中下
        bot_frame1 = LabelFrame(self.master, text='使用方法')
        bot_frame1.pack(fill=X, side=TOP, padx=15, pady=0)
        self.Scroll = Scrollbar(bot_frame1)

        self.Text = Text(bot_frame1, width=83, height=23, yscrollcommand=self.Scroll.set)
        self.Text.pack(side=LEFT, padx=0, pady=5)
        self.Scroll = Scrollbar(bot_frame1)
        self.Scroll.pack(side=LEFT, fill=Y)
        self.Scroll.config(command=self.Text.yview)

        # 创建底部
        bot_frame = LabelFrame(self.master)
        bot_frame.pack(fill=X, side=TOP, padx=15, pady=2)

        self.e = StringVar()
        ttk.Label(bot_frame, width=15, textvariable=self.e).pack(side=LEFT)
        self.e.set("导入/导出数量:")

        self.e1 = StringVar()
        self.entry = ttk.Entry(bot_frame, width=15, textvariable=self.e1)
        self.e1.set("0")
        self.entry.pack(side=LEFT, pady=10)
        #yoko_fn = YokoRead._FILE_NODE_
        ttk.Button(bot_frame, text='导出', command=lambda:self.func_start_dr(1)).pack(side=RIGHT, padx=10)
        ttk.Button(bot_frame, text='导入', command=lambda:self.func_start_dr(0)).pack(side=RIGHT, padx=10)

    #lambda: self.thread_it(self.start)
    @thread_Decorator
    @time_Decorator
    def func_start_dr(self,parm_mode):
        try:
            var_num = int(self.entry.get())
            #print(var_num)
        except ValueError :
            self.func_text_update("请输入数字.\n")
            self.entry.delete(0,END)
            var_num = 0
        self.func_circuit(var_num,parm_mode)
        #self.func_circuit(var_num)
        EnumWindows(self.func_scan_windows, 0)  # 遍历所有窗口
        pass

    def func_text_update(self,show):
        if show == 'START_':
            self.Text.insert(END, "=============程序开始=============\n")
        elif show == 'STOP_':
            self.Text.insert(END, "=============程序结束=============\n")
        elif show == 'filename':
            self.Text.insert(END, f'INFO:{self.short_name} 导出完成\n')
        elif show == 'filename_in':
            self.Text.insert(END, f'INFO:{self.short_name} 导入完成\n')
        else:
            self.Text.insert(END,show)
            self.Text.insert(END, "=============程序终止=============\n")

        self.Text.update()
        self.Text.see(END)

    def func_all_windows_name(self,hwnd, mouse):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            #print(GetClassName(hwnd)+'==>'+GetWindowText(hwnd))
            # DR文件部分
            if 'FUNCTION_BLOCK' in GetWindowText(hwnd):
                self.sv_window_text = GetWindowText(hwnd)
                self.sv_class_name = GetClassName(hwnd)
            elif 'Draw:DR' in GetWindowText(hwnd):
                self.dr_window_text = GetWindowText(hwnd)
                self.dr_class_name = GetClassName(hwnd)
                #shortname = re.search('DR([\w\W\[0-9]{4}]*?)', self.dr_window_text, flags=0).group(0)
                self.short_name = re.search(r'[\w\W\[0-9]{6}]*?(?=.edf)', self.dr_window_text, flags=0).group(0)
            #IOM文件部分
            elif 'NODE' in GetWindowText(hwnd):
                self.sv_window_text = GetWindowText(hwnd)
                self.sv_class_name = GetClassName(hwnd)
            elif 'IOM Builder' in GetWindowText(hwnd):
                self.dr_window_text = GetWindowText(hwnd)
                self.dr_class_name = GetClassName(hwnd)
                name_NS = re.search(r'(?<=Stn:).*(?=.edf)', self.dr_window_text, flags=0).group(0)
                #sn_FCS = re.search(r'(?<=FCS)[0-9]{4}', name_NS, flags=0).group(0)
                #sn_FCS = re.search(r'.*(?= Train:)', name_NS, flags=0).group(0)
                sn_Node = re.search(r'(?<=Node:)[0-9]{1,2}', name_NS, flags=0).group(0)
                sn_Solt = re.search(r'(?<=File:)[1-8]', name_NS, flags=0).group(0)
                self.short_name = f'N{sn_Node}S{sn_Solt}'
            elif 'BKESysView' in GetWindowText(hwnd):
                self.dr_window_text = GetWindowText(hwnd)
                self.dr_class_name = GetClassName(hwnd)
            #SW开关部分
            elif 'SWITCH' in GetWindowText(hwnd):
                self.sv_window_text = GetWindowText(hwnd)
                self.sv_class_name = GetClassName(hwnd)
            elif 'File:SwitchDef' in GetWindowText(hwnd):
                self.dr_window_text = GetWindowText(hwnd)
                self.dr_class_name = GetClassName(hwnd)
                self.short_name = f'{self.sw_num}SW' #因为中文输入容易错

    def func_command(self):
        self.sv_window_text = ''
        self.sv_class_name = ''
        self.dr_window_text = ''
        self.dr_class_name = ''
        EnumWindows(self.func_all_windows_name, 0)
        #print("=" * 20)

    def func_active_builder (self):
        if self.dr_window_text != '' :
            dr_builder_window = win32gui.FindWindow(self.dr_class_name, self.dr_window_text)
            win32gui.SetForegroundWindow(dr_builder_window)
            if self.dr_window_text == 'BKESysView':
                self.func_press_key(Key.enter,Key.down, Key.enter)
                pass
        else:
            err_text = "Windows not Open !1\n"
            self.func_text_update(err_text)
            exit()

    def func_close_builder(self):
        self.func_delay()
        if self.dr_window_text != '' :
            dr_builder_window = win32gui.FindWindow(self.dr_class_name, self.dr_window_text)
            win32gui.PostMessage(dr_builder_window, win32con.WM_CLOSE, 0, 0)
        else:
            err_text = "Windows is not Open !2\n"
            self.func_text_update(err_text)
            exit()

    def func_active_function_block (self):
        self.func_delay()
        if self.sv_window_text != '' :
            function_block_window = win32gui.FindWindow(self.sv_class_name, self.sv_window_text)
            win32gui.SetForegroundWindow(function_block_window)
        else:
            err_text = "Windows is not Open !3\n"
            self.func_text_update(err_text)
            exit()

    def func_press_key(self,combination = '',*abc):
        self.func_delay()
        self.keyboard = Controller()
        if combination != '':
            self.keyboard.press(combination)

        for _ in abc:
            #print(_)
            self.func_press_abc(_)
            self.func_delay()

        if combination != '':
            self.keyboard.release(combination)

    def func_press_abc(self,_character):
        yo_keyboard = Controller()
        yo_keyboard.press(_character)
        yo_keyboard.release(_character)

    def func_delay(self,delay_time = 0.2):
        sleep(delay_time)

    def func_out_txt(self):
        self.func_press_key(Key.alt,'f','e','e')
        self.func_delay(1)
        #print(self.short_name)
        self.func_text_update('filename')
        self.keyboard.type(self.short_name)
        self.func_delay(1)
        self.short_name = ''
        self.func_press_key(Key.alt, 's')
        self.func_press_key(Key.left,Key.enter)
        #self.func_press_key(Key.enter)

    def func_import_txt(self):
        self.func_Listener()
        self.func_press_key(Key.alt, 'f', 'e', 'p')
        self.func_delay(1)
        # print(self.short_name)
        self.func_text_update('filename_in')
        self.keyboard.type(f'{self.short_name}.txt')
        self.func_delay(1)
        self.short_name = ''
        self.func_press_key(Key.tab, Key.down, Key.down, Key.down, Key.tab, Key.enter, Key.enter)
        self.func_delay(1)
        self.func_press_key(Key.alt, 'f', 'w')
        self.func_press_key(Key.alt, 'f', 'x')
        self.func_press_key(Key.right, Key.enter)
        self.func_delay(1)

    def func_Listener(self):
        def func_on_release(key):
            # print('{0} released'.format(key))
            if key == Key.space:
                return False

        # 监听键盘按键
        with keyboard.Listener(on_release=func_on_release) as self.listener:
            self.listener.join()
        pass

    def func_circuit(self,parm_count,parm_mode):   #循环流程
        self.func_text_update('START_')

        for _ in range(parm_count):
            self.sw_num = str(_+1)
            self.func_delay(1)
            self.func_command()
            self.func_active_builder()
            if self.dr_window_text == 'BKESysView':
                continue
            if parm_mode:
                self.func_out_txt()
            else:
                self.Text.insert(END, "空格键 开始 输入法切换至英文\n")
                self.func_import_txt()
            self.func_close_builder()
            self.func_active_function_block()
            self.func_delay(1)
            self.func_press_key(Key.down,Key.enter)

        self.func_text_update('STOP_')

    def func_scan_windows(self,hwnd, mouse):
        #遍历所有打开窗口
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
             print(GetClassName(hwnd)+'==>'+GetWindowText(hwnd))
            #print(type(GetClassName(hwnd)))
        pass

    # def active_(self):  #未使用
    #     # 打开其他应用
    #     shell = win32com.client.Dispatch("WScript.Shell")
    #     #shell.SendKeys('%')
    #     shell.Run("C:\CENTUMVP\program\BKHCallSysFunc O " + '18-PDISA-18103 TUN -SM')
    #     #pass
    #

if __name__ == "__main__":

    #print(app.listener_())
    #app.active_()

    root = Tk()
    root.geometry('640x400+100+200')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoRead.ALRM_NODE.limited_time(root)
    root.title("导入导出工具 V1.00"+"    到期日:"+limit_time)
    root.mainloop()


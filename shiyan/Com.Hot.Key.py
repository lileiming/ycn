# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
#############################################################
from pynput.keyboard import Key, Controller
from pynput import keyboard
import threading, time
from win32gui import *
import win32gui
import win32con
import win32com.client
import YokoRead   #自定义模块
from YokoRead import thread_Decorator

class Windows_NODE:
    def __init__(self):
        self.listener = keyboard.Listener()
        self.run_flag = True
        self.var_index = True
        self.all_key = []
        self.process_run()
        self.process_active()

    def func_on_press(self,key):
        self.all_key.append(str(key))
        self.all_key = list(set(self.all_key))
        print(self.all_key)
        pass

    def func_on_release(self,key):
        if self.all_key:
            self.all_key.remove(str(key))
            print(f'del {self.all_key}')
            time.sleep(0.2)
            pass

        if key == keyboard.Key.esc:
            self.run_flag = False
            self.var_index = False
            return False

    @thread_Decorator
    def process_run(self):
        while self.run_flag:
            with keyboard.Listener(
                    on_press=self.func_on_press,
                    on_release=self.func_on_release) as listener:
                # if self.pause_flag:
                listener.join()
                pass
            pass

    def process_active(self):
        while self.var_index:
            if 'Key.ctrl_l' in self.all_key and 'Key.f1' in self.all_key:
                self.func_shell("GR0003")
                time.sleep(2)
                pass
            if 'Key.ctrl_l' in self.all_key and "'\\x11'" in self.all_key:
                self.func_out_txt()
                time.sleep(2)
                pass

            pass

    def func_shell(self,var_GR_name):
        self.run_flag = False
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.Run("C:\CENTUMVP\program\BKHCallSysFunc O " + var_GR_name)
        print(var_GR_name)
        self.pause_flag = True
        self.key_char = ''
        pass

    def func_out_txt(self):
        self.func_press_key(Key.alt,'f','e','e')
        pass

    def func_import_txt(self):
        self.func_press_key(Key.alt, 'f', 'e', 'p')
        pass

    def func_press_key(self,combination = '',*abc):
        time.sleep(0.2)
        self.keyboard = Controller()

        if combination != '':
            self.keyboard.press(combination)
            pass

        for var_char in abc:
            self.keyboard.press(var_char)
            self.keyboard.release(var_char)
            time.sleep(0.2)
            pass

        if combination != '':
            self.keyboard.release(combination)
        pass

if __name__ == "__main__":
    Windows_NODE()


#********************************************************************
# from pynput.keyboard import Key, Controller
# from pynput import keyboard
# from win32gui import *
# import win32gui
# import win32con
# import win32com.client
# from time import sleep ,time
# import YokoRead   #自定义模块
# import threading
#
# class Windows_NODE:
#     def __init__(self):
#         self.timestamp_win = 0
#         self.run_flag = True
#         self.run_esc = True
#         t = threading.Thread(target=self.func_Listener)
#         t.start()
#
#     def func_active(self,key_char):
#         while self.run_esc :
#             if key_char =='q':
#                 self.run_flag = False
#                 shell = win32com.client.Dispatch("WScript.Shell")
#                 shell.Run("C:\CENTUMVP\program\BKHCallSysFunc O " + 'GR0003')
#                 self.run_flag = True
#                 key_char = ''
#             pass
#
#     def func_Listener(self):
#         def func_on_press(key):
#             print(key)
#             if func_combo_press(key, Key.cmd, 'q'):
#                 print("AAA")
#                 self.run_flag = False
#                 self.func_active('q')
#                 pass
#             elif func_combo_press(key, Key.cmd, 'w'):
#                 self.func_out_txt()
#                 pass
#
#         def func_on_release(key):
#             # print(key)
#             if key == Key.space:
#                 self.func_import_txt()
#             elif key == Key.esc:
#                 self.run_esc = False
#                 return False
#
#         def func_combo_press(key, key1, key2):
#             try:
#                 if key == key1:
#                     self.timestamp_win = time()
#                 if key.char == key2:
#                     if time() - self.timestamp_win < 1:
#                         return True
#             except AttributeError:
#                 pass
#
#         # 监听键盘按键
#         while self.run_flag:
#             with keyboard.Listener(on_press = func_on_press,
#                                    on_release = func_on_release) as self.listener:
#                 self.listener.join()
#             pass
#
#
#     def func_press_key(self,combination = '',*abc):
#         self.func_delay()
#         self.keyboard = Controller()
#
#         if combination != '':
#             self.keyboard.press(combination)
#
#         for var_char in abc:
#             self.keyboard.press(var_char)
#             self.keyboard.release(var_char)
#             self.func_delay()
#
#         if combination != '':
#             self.keyboard.release(combination)
#         pass
#
#     def func_delay(self,delay_time = 0.2):
#         sleep(delay_time)
#         pass
#
#
#
#     def func_out_txt(self):
#         self.func_press_key(Key.alt,'f','e','e')
#         pass
#
#     def func_import_txt(self):
#         self.func_press_key(Key.alt, 'f', 'e', 'p')
#         pass
#
#
# if __name__ == "__main__":
#     Windows_NODE()

#***********************************************************************************
# import os
# import sys
# import threading
# import time
#
# from pynput import keyboard
# from pynput.keyboard import Controller, Key, Listener
# from win32gui import *
# import win32gui
# import win32con
# import win32com.client
#
#
# # 每隔0.5秒 清空列表
# def doWaiting():
#     while True:
#         time.sleep(0.5)
#         all_key.clear()
#
# def func_active():
#     shell = win32com.client.Dispatch("WScript.Shell")
#     shell.Run("C:\CENTUMVP\program\BKHCallSysFunc O " + 'GR0003')
#     pass
#
# # 键盘按压
# def on_press(key):
#     pass
#
# def on_release(key):
#     # print("已经释放:", format(key))
#     all_key.append(str(key))
#     print(all_key)
#     # if keyboard.Key.ctrl_l in all_key and keyboard.Key.f5 in all_key:
#     #     print('what is your problem?')
#
#     if 'Key.ctrl_l' in all_key and "'\\x03'" in all_key:
#         print('复制快捷键')
#
#     if 'Key.ctrl_l' in all_key and "'v'" in all_key:
#         print('粘贴快捷键')
#
#     if key == Key.esc:
#         # 停止监听
#         return False
#
#
# def start_listen():
#     with Listener(on_press=None, on_release=on_release) as listener:
#         listener.join()
#
#
# if __name__ == '__main__':
#     # 开始监听,按esc退出监听
#     all_key = []
#
#     t = threading.Thread(target=doWaiting)
#     t.setDaemon(True)
#     t.start()
#
#     start_listen()
#*******************************************************************************
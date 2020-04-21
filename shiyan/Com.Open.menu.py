# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
#==========================================================
# Rev01
# 基本实现 导出DR文件的自动化流程
# https://www.codetd.com/article/1911130
# https://www.cnblogs.com/yfacesclub/p/10113053.html
# https://blog.csdn.net/qq_16234613/article/details/79155632
# https://zhuanlan.zhihu.com/p/73001806
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


def func_scan_windows(hwnd, mouse):
    # 遍历所有打开窗口
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        #print(GetClassName(hwnd) + '==>' + GetWindowText(hwnd))
        if 'Control Drawing Builder' in GetWindowText(hwnd):
            dr_window_text = GetWindowText(hwnd)
            dr_class_name = GetClassName(hwnd)
            #print(GetClassName(hwnd) + '==>' + GetWindowText(hwnd))
            dr_builder_window = win32gui.FindWindow(dr_class_name, dr_window_text)
            #print(dr_builder_window)
            #win32gui.SetForegroundWindow(dr_builder_window)
            subHandle = win32gui.FindWindowEx(dr_builder_window , 0, 'AfxControlBar140', None)
            print(subHandle)
            win32gui.SetForegroundWindow(subHandle)
            # hwndChildList = []
            # win32gui.EnumChildWindows(dr_builder_window, lambda hwnd, param: param.append(hwnd), hwndChildList)
            # aa = hwndChildList
            # print(aa)

            # menuHandle = win32gui.GetMenu(subHandle)
            # print(menuHandle)
            # # subMenuHandle = win32gui.GetSubMenu(menuHandle, 1)
            # # print(subMenuHandle)
            # menuItemHandle = win32gui.GetMenuItemID(menuHandle, 2)
            # print(menuItemHandle)
            # win32gui.PostMessage(dr_builder_window, win32con.WM_COMMAND, menuHandle, 0)

    pass

if __name__ == "__main__":
    EnumWindows(func_scan_windows, 0)  # 遍历所有窗口


    # root = Tk()
    # root.geometry('640x400+100+200')  # 窗口尺寸
    # Windows_NODE(root)
    # root.mainloop()


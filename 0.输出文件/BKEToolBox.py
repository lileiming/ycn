# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# ==========================================================
import tkinter
from tkinter import *
from sys import argv
import platform
# ===================自定义模块==============================
import YokoCustomlibrary
import BKEToolCopyGraphic   # 复制工具-流程图
import BKEToolCopyFunc      # 复制工具-功能块
import BKEToolReplaceESCL   # 替换工具-量程
import BKEToolReplaceTag    # 替换工具-位号
import BKEToolScreenshot    # 辅助工具-截图反色

import BKEToolTuning        # 辅助工具-TUNING修改 参数导入
import ExcelToolTaglist     # 维护工具-Tag_list
import BKEToolExportGraphic # 辅助工具-流程图导出
import BKEToolFindGraphic   # 辅助工具-流程图位号查漏工具
import BKEToolUnlockADsuite # 辅助工具-解锁ADsuite DR文件工具
import BKEToolTrend         # 辅助工具-趋势检查表格生成工具、趋势组态文件生成工具
if(platform.system()=='Windows'):
    import BKEToolExport        # 辅助工具-导入导出

# ==========================================================
# BK ENG Tool Box = BKEToolBox
# ENG工具箱
# **********************************************************

class Tool_Box_Window:
    def __init__(self, my_root, my_Title, flag):
        self.top = tkinter.Toplevel(my_root)
        self.top.geometry('640x400+100+200')
        self.top.title(my_Title)
        self.top.attributes('-topmost', 1)
        if flag == 1:
            BKEToolCopyGraphic.Windows_NODE(self.top)
        elif flag == 2:
            BKEToolCopyFunc.Windows_NODE(self.top)
        elif flag == 3:
            pass
        elif flag == 4:
            BKEToolReplaceESCL.Windows_NODE(self.top)
        elif flag == 5:
            BKEToolReplaceTag.Windows_NODE(self.top)
        elif flag == 6:
            BKEToolScreenshot.Windows_NODE(self.top)
        elif flag == 7 and platform.system()=='Windows':
            BKEToolExport.Windows_NODE(self.top)
        elif flag == 8:
            BKEToolTuning.Windows_NODE(self.top)
        elif flag == 9:
            BKEToolExportGraphic.Windows_NODE(self.top)
        elif flag == 10:
            BKEToolFindGraphic.Windows_NODE(self.top)
        elif flag == 11:
            self.top.geometry('640x600+100+200')
            ExcelToolTaglist.SHOW_NODE(self.top)
        elif flag == 12:
            BKEToolUnlockADsuite.Windows_NODE(self.top)
        elif flag == 13:
            BKEToolTrend.Windows_NODE(self.top)
        elif flag == 15:
            Label(self.top, text='Qiang.li@cn.yokogawa.com\nDon\'t Repeat Youself !!\n ').pack(fill=X, expand=1)
            pass
        pass

class Windows_NODE:
    def __init__(self, master):
        self.window_A = tkinter.IntVar(root, value=0)  # 只允许弹出一个窗体
        # self.window2 = tkinter.IntVar(root, value=0)  #允许同时弹出2个窗体
        self.master = master
        self.initWidgets()

    def initWidgets(self):
        # 创建顶部
        list_title = ['复制工具-流程图',
                     '复制工具-功能块',
                          '',
                     '替换工具-量程',
                     '替换工具-位号',
                     '辅助工具-截图反色',
                     '辅助工具-导入导出',
                     '辅助工具-参数导入',
                     '辅助工具-流程图导出',
                     '辅助工具-位号查漏',
                     '维护工具-Tag_list',
                     '辅助工具-解锁ADsuite',
                     '辅助工具-趋势生成工具',
                      '',
                     '预留']
        for i in range(len(list_title)):
            if list_title[i] :
                self.button_app(list_title[i], i + 1)
                pass
            pass
        Label(root,text='Don\'t Repeat Youself !!     \n ').pack(side='bottom',anchor='se')

    def button_app(self, title, window_num):
        x_index = int((window_num - 1) / 5)
        y_index = (window_num - 1) % 5
        self.button_A = tkinter.Button(root, text=title, command=lambda: self.button_fun(title, window_num))
        self.button_A.place(x=30 + x_index * 200, y=40 + y_index * 60, height=40, width=160)
        # print(30+x_index*200, 40+y_index*60)
        pass

    def button_fun(self, title, window_num):
        if self.window_A.get() == 0:
            self.window_A.set(1)
            window_first = Tool_Box_Window(root, title, window_num)
            self.button_A.wait_window(window_first.top)
            self.window_A.set(0)
            pass
        pass

if __name__ == "__main__":
    try:
        str_super = argv[1]
    except IndexError:
        str_super = ''
    root = Tk()
    root.geometry('640x400+100+200')  # 窗口尺寸
    Windows_NODE(root)
    if str_super != '-S':
        limit_time = YokoCustomlibrary.ALRM_NODE.limited_time(root)
    else:
        limit_time = '3020/1/1'
    root.title("组态ENG工具箱 V1.0" + "    到期日:" + limit_time)
    root.mainloop()
    pass

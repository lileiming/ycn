# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# ==========================================================
import tkinter
from tkinter import *
from tkinter import ttk
from sys import argv
# ===================自定义模块==============================
import YokoRead
import PVI_GR  # 流程图复制工具
import PVI_COMM  # 功能块复制工具
import PVI_ESCL  # 量程修改工具
import PVI_invter  # 截图反色工具
import Out_DrFile  # DR文件自动导出
import TagReplaceTool  # 快速替换工具
import TaglistTool  # Tag_list维护工具
import PVI_TUN  # TUNING参数修改辅助工具

class myWindow():
    def __init__(self, root, myTitle, flag):
        self.top = tkinter.Toplevel(root)
        self.top.geometry('640x400+100+200')
        self.top.title(myTitle)
        self.top.attributes('-topmost', 1)
        if flag == 1:
            PVI_GR.Windows_NODE(self.top)
        elif flag == 2:
            PVI_COMM.Windows_NODE(self.top)
        elif flag == 3:
            PVI_ESCL.Windows_NODE(self.top)
        elif flag == 4:
            PVI_invter.Windows_NODE(self.top)
        elif flag == 5:
            Out_DrFile.Windows_NODE(self.top)
        elif flag == 6:
            TagReplaceTool.Windows_NODE(self.top)
        elif flag == 7:
            self.top.geometry('640x600+100+200')
            TaglistTool.Windows_NODE(self.top)
        elif flag == 8:
            PVI_TUN.Windows_NODE(self.top)
        elif flag == 9:
            Label(self.top, text='Qiang.li@cn.yokogawa.com').pack(fill=X, expand=1)
        pass

    pass


class Windows_NODE:
    def __init__(self, master):
        self.window1 = tkinter.IntVar(root, value=0)  # 只允许弹出一个窗体
        # self.window2 = tkinter.IntVar(root, value=0)  #允许同时弹出2个窗体
        self.master = master
        self.initWidgets()

    def initWidgets(self):
        # 创建顶部

        title = ['流程图复制工具',
                 '功能块复制工具',
                 '量程修改工具',
                 '截图反色工具',
                 'DR文件自动导出工具',
                 'TAG替换工具',
                 'IOlist维护工具',
                 'TUNING参数修改工具',
                 '预留']
        for i in range(len(title)):
            self.button_app(title[i], i + 1)
            pass
        pass

    def button_app(self, title, window_num):
        xindex = int((window_num - 1) / 5)
        yindex = (window_num - 1) % 5
        self.button1 = tkinter.Button(root, text=title, command=lambda: self.button_fun(title, window_num))
        self.button1.place(x=30 + xindex * 200, y=40 + yindex * 60, height=40, width=160)
        # print(30+xindex*200, 40+yindex*60)
        pass

    def button_fun(self, title, window_num):
        if self.window1.get() == 0:
            self.window1.set(1)
            w1 = myWindow(root, title, window_num)
            self.button1.wait_window(w1.top)
            self.window1.set(0)
        pass

    pass


if __name__ == "__main__":
    try:
        str_ = argv[1]
    except:
        str_ = ''
    root = Tk()
    root.geometry('640x400+100+200')  # 窗口尺寸
    Windows_NODE(root)
    # limit_time = YokoRead._ALRM_NODE_.limited_time(root)
    if str_ != '-S':
        limit_time = YokoRead._ALRM_NODE_.limited_time(root)
    else:
        limit_time = '3020/1/1'
    root.title("组态工具箱 V0.1" + "    到期日:" + limit_time)
    root.mainloop()
    pass

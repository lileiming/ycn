# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# **********************************************************
# BK ENG Tool Export Graphic = BKEToolExportGraphic
# **********************************************************

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import re
from time import sleep
from shutil import copyfile
import YokoCustomlibrary   #自定义模块
from YokoCustomlibrary import time_Decorator,thread_Decorator

class Windows_NODE(YokoCustomlibrary.FILE_NODE):
    def __init__(self, master):
        self.master = master
        self.here = 'C:\CENTUMVP\eng\BKProject'
        self.copy_here = os.getcwd()
        self.initWidgets()
        help_doc = '本程序为流程图快速导出工具 \n'
        self.text_update(help_doc)
        pass

    def initWidgets(self):
        # 创建顶部
        top_frame = LabelFrame(self.master, text='源目录', height=150, width=615)
        top_frame.pack(fill=X, padx=15, pady=5)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame, width=65, textvariable=self.e1)
        self.e1.set(self.here)
        self.entry.pack(fill=X, expand=YES, side=LEFT, pady=10)
        ttk.Button(top_frame, text='源目录', command=self.open_dir).pack(side=LEFT)

        # 创建中部
        mid_frame = LabelFrame(self.master, text='目标目录')
        mid_frame.pack(fill=X, padx=15, pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(mid_frame, width=65, textvariable=self.e2)
        self.e2.set(self.copy_here)
        self.entry2.pack(fill=X, expand=YES, side=LEFT, pady=10)
        ttk.Button(mid_frame, text='目标目录', command=self.open_dir2).pack(side=LEFT)

        # 创建中下
        bot_frame1 = LabelFrame(self.master, text='结果')
        bot_frame1.pack(fill=X, side=TOP, padx=15, pady=0)
        self.Scroll = Scrollbar(bot_frame1)
        self.Text = Text(bot_frame1, width=83, height=13, yscrollcommand=self.Scroll.set)
        self.Text.pack(side=LEFT, padx=0, pady=5)
        self.Scroll = Scrollbar(bot_frame1)
        self.Scroll.pack(side=LEFT, fill=Y)
        self.Scroll.config(command=self.Text.yview)

        # 创建底部
        bot_frame = LabelFrame(self.master)
        bot_frame.pack(fill=X, side=TOP, padx=15, pady=8)
        self.e = StringVar()
        ttk.Label(bot_frame, width=60, textvariable=self.e).pack(side=LEFT, fill=BOTH, expand=YES, pady=10)
        self.e.set('程序员美德：懒惰、不耐烦、傲慢')
        ttk.Button(bot_frame, text='确定', command=self.command).pack(side=RIGHT)

    def open_dir(self):
        self.entry.delete(0,END)
        dir_path = filedialog.askdirectory(title=u'选择HIS流程图源文件夹',initialdir = self.here)
        path0 = dir_path
        path1 = path0+'/'
        self.entry.insert('insert', path1)

    def open_dir2(self):
        self.entry2.delete(0,END)
        dir_path = filedialog.askdirectory(title=u'选择HIS流程图目标文件夹',initialdir = self.copy_here)
        path0 = dir_path
        path1 = path0+'/'
        self.entry2.insert('insert', path1)

    def get_filelist(self):
        Filelist = []
        path = self.entry.get()
        for home, dirs, files in os.walk(path):
            for filename in files:
                Filelist.append(os.path.join(home, filename))
        return Filelist

    @thread_Decorator
    @time_Decorator
    def command(self):
        self.text_update('START_')
        Filelist = self.get_filelist()
        copypath = self.entry2.get()
        for file in Filelist:
            if 'Main.xaml' in file:
                print(file)
                script_dir = os.path.dirname(file)
                var_short_dir = (re.findall(r'[a-zA-Z0-9]*(?=~EDF)', script_dir))
                #print(var_short_dir[0])
                filename = f'{copypath}{var_short_dir[0]}.xaml'
                self.text_update(f'{filename}\n')
                copyfile(file, filename)
        pass
        self.text_update('STOP_')
        sleep(2)


    def text_update(self,show):
        if show == 'START_':
            self.Text.insert(END, "=============程序开始=============\n")
        elif show == 'STOP_':
            self.Text.insert(END, "=============程序结束=============\n")
        else:
            self.Text.insert(END,show)
            pass
        self.Text.update()
        self.Text.see(END)
        #self.text_update('STOP_')
        pass

if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400+640+0')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoCustomlibrary.ALRM_NODE.limited_time(root)
    root.title("流程图到处工具工具 V1.00"+"    到期日:"+limit_time)
    root.mainloop()

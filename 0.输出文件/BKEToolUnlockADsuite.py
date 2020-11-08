# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# **********************************************************
# BK ENG Tool Unlock ADsuite
# **********************************************************
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import re
import os
# import YokoCustomlibrary   #自定义模块
# from time import sleep
# from YokoCustomlibrary import time_Decorator,thread_Decorator

class Windows_NODE:
    def __init__(self, master):
        self.master = master
        self.here = 'C:/Users/Administrator/Documents/python/0.输出文件/ToolUnlockADsuite'
        self.initWidgets()
        help_doc = '本程序用于大量解锁ADsuite生成的DR文件，使其不再为绑定状态。\n'
        self.text_update(help_doc)
        pass

    def initWidgets(self):
        # 创建顶部
        top_frame = LabelFrame(self.master, text='DR导出文件目录', height=150, width=615)
        top_frame.pack(fill=X, padx=15, pady=0)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame, width=65, textvariable=self.e1)
        print(self.here)
        self.e1.set(self.here)
        self.entry.pack(fill=X, expand=YES, side=LEFT, pady=10)
        ttk.Button(top_frame, text='DR文件目录', command=self.open_dir).pack(side=LEFT)
     # 创建中下
        bot_frame1 = LabelFrame(self.master, text='结果')
        bot_frame1.pack(fill=X, side=TOP, padx=15, pady=0)
        self.Scroll = Scrollbar(bot_frame1)
        self.Text = Text(bot_frame1, width=83, height=18, yscrollcommand=self.Scroll.set)
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
        dir_path = filedialog.askdirectory(title=u'DR导出文件目录',initialdir = self.here)
        path0 = dir_path
        path1 = path0+'/'
        self.entry.insert('insert', path1)

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

    @property
    def command(self):
        def read_txt(txt_file_name):
            # 读取txt文档
            with open(txt_file_name, 'r') as file_data:
                file_detail = file_data.read()
            return file_detail

        def out_txt(txt_file_name, out_result):
            out_file_name = txt_file_name
            with open(out_file_name, 'w+', encoding='GBK') as out_file:  # 保存为ANSI格式
                out_file.write(out_result)
            pass


        self.text_update('START_')
        path = self.entry.get()
        FPRI_in_files = os.listdir(path)
        for FPRI_txt in FPRI_in_files:
          if '.txt' in FPRI_txt:
            txt_name = path + FPRI_txt
            allContent = read_txt(txt_name)
            del_find = (re.findall(r'(:FPRI[\w\W]*?::FPRI)', allContent))
            try:
                del_result = allContent.replace(del_find[0], "", 1)
                out_txt(txt_name, del_result)
            except:
                print("end")
            self.text_update(f'INFO:{FPRI_txt}转换结束\n')
        self.text_update('STOP_')

if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400+640+0')  # 窗口尺寸
    Windows_NODE(root)
    root.mainloop()
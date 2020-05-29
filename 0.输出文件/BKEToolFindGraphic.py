# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# **********************************************************
# BK ENG Tool Find Graphic  = BKEToolFindGraphic
# 流程图位号查漏工具
# **********************************************************

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import re
import YokoCustomlibrary   #自定义模块
from time import sleep
from YokoCustomlibrary import time_Decorator,thread_Decorator

class Windows_NODE(YokoCustomlibrary.FILE_NODE):
    def __init__(self, master):
        self.master = master
        self.here = os.getcwd()
        self.initWidgets()
        help_doc = '本程序为流程图位号查漏工具 \n'
        self.text_update(help_doc)

    def initWidgets(self):
        test_path = r'C:\Users\Administrator\Documents\python\0.输出文件\ToolFindGraphic\PVI_TAG_list.xls'
        var_dir = r'C:\Users\Administrator\Documents\python\0.输出文件\ToolFindGraphic\copy'
        # 创建顶部
        top_frame = LabelFrame(self.master, text='源目录', height=150, width=615)
        top_frame.pack(fill=X, padx=15, pady=5)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame, width=65, textvariable=self.e1)
        self.e1.set(var_dir)
        self.entry.pack(fill=X, expand=YES, side=LEFT, pady=10)
        ttk.Button(top_frame, text='源目录', command=self.open_dir).pack(side=LEFT)

        # 创建中部
        mid_frame = LabelFrame(self.master, text='数据列表')
        mid_frame.pack(fill=X, padx=15, pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(mid_frame, width=45, textvariable=self.e2)
        self.e2.set(test_path)
        self.entry2.pack(fill=X, expand=YES, side=LEFT, pady=10)
        self.e3 = StringVar()
        self.comboxlist = ttk.Combobox(mid_frame, width=15, textvariable=self.e3)
        self.comboxlist.pack(side=LEFT)
        self.e3.set('Find_TAG_temp')
        ttk.Button(mid_frame, text='数据列表', command=self.open_file2).pack(side=LEFT)

        # 创建中下
        bot_frame1 = LabelFrame(self.master, text='结果')
        bot_frame1.pack(fill=X, side=TOP, padx=15, pady=0)
        self.Scroll = Scrollbar(bot_frame1)
        self.Text = Text(bot_frame1, width=83, height=12, yscrollcommand=self.Scroll.set)
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
        ttk.Button(bot_frame, text='确定', command=self.command).pack(side=RIGHT, padx=10)

    def open_dir(self):
        self.entry.delete(0,END)
        dir_path = filedialog.askdirectory(title=u'选择HIS流程图源文件夹',initialdir = self.here)
        path0 = dir_path
        path1 = path0+'/'
        self.entry.insert('insert', path1)

    def open_file2(self):
        file_path = filedialog.askopenfilename(title=u'选择数据列表', initialdir=self.here)
        file_text = file_path
        self.entry2.delete(0, END)
        self.entry2.insert('insert', file_text)
        sheetName = self.get_sheet(file_text)
        sheetNameT = tuple(sheetName)
        self.comboxlist["values"] = sheetNameT
        self.comboxlist.current(0)
        pass

    @thread_Decorator
    @time_Decorator
    def command(self):
        self.dict_tag = {}
        #开始
        self.text_update('START_')
        #读取界面 文件信息
        file_name = self.entry2.get()
        sheet_name = self.comboxlist.get()
        list_Key_words = list(next(self.get_data_Tag(file_name, sheet_name)))
        Key_index = list_Key_words.index('TAG')
        for list_Details in self.get_data(file_name, sheet_name):
            tag_key = list_Details[list_Key_words[Key_index]]
            self.dict_tag[tag_key] = 0

        self.list_tag = (list(self.dict_tag.keys()))
        list_File_Name = self.func_get_file_list()

        for var_file_name in list_File_Name:
            # print(var_file_name)
            with open(var_file_name, 'r', encoding='utf-8') as Maintxt:
                allContent = Maintxt.read()

            for var_tag in self.list_tag:
                head_find = (re.findall(f'{var_tag}"', allContent))
                var_num = int(self.dict_tag[var_tag]) + len(head_find)
                self.dict_tag[var_tag] = var_num
        self.func_dict_out_txt()
        #结束
        self.text_update('STOP_')
        sleep(2)

    def func_get_file_list(self):
        list_File_Name = []
        var_src_path = self.entry.get()
        for var_src_home, var_src_dirs, var_src_files in os.walk(var_src_path):
            for var_file_name in var_src_files:
                list_File_Name.append(os.path.join(var_src_home, var_file_name))
        return list_File_Name

    def func_dict_out_txt(self):
        var_line_Details = ''
        for var_tag in self.list_tag:
            if self.dict_tag[var_tag] == 0:
                var_line_Details = var_line_Details + f'{var_tag}\n'
                self.text_update(var_tag)

        var_file_name = self.entry2.get()
        var_file_path, var_full_file_name = os.path.split(var_file_name)
        result_latest = os.path.join(var_file_path, 'OUT.txt')
        self.out_txt(result_latest, var_line_Details)
        pass

    def text_update(self,show):
        if show == 'START_':
            self.Text.insert(END, "=============程序开始=============\n")
        elif show == 'STOP_':
            self.Text.insert(END, "=============程序结束=============\n")
            self.Text.insert(END, "=OUT.txt文件中的位号未在所有流程图中发现，需要再次人工确认=\n")
        else:
            self.Text.insert(END,show)
            self.Text.insert(END, "\n")
        self.Text.update()
        self.Text.see(END)
        #self.text_update('START_')
        pass

if __name__ == "__main__":
        root = Tk()
        root.geometry('640x400')  # 窗口尺寸
        Windows_NODE(root)
        limit_time = YokoCustomlibrary.ALRM_NODE.limited_time(root)
        root.title("流程图位号查漏工具" + "    到期日:" + limit_time)
        root.mainloop()

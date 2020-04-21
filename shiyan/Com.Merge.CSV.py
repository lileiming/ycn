# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8

import  sys
import os
from tkinter import *
from tkinter import ttk,filedialog


class Windows_NODE:
    def __init__(self, master):
        self.master = master
        self.here = r'C:\Users\Administrator\Documents\python\shiyan\MergeCSV'
        self.initWidgets()
        pass

    def initWidgets(self):
        # 创建顶部
        top_frame = LabelFrame(self.master, text='目录', height=150, width=615)
        top_frame.pack(fill=X, padx=15, pady=5)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame, width=65, textvariable=self.e1)
        self.e1.set(self.here)
        self.entry.pack(fill=X, expand=YES, side=LEFT, pady=10)
        ttk.Button(top_frame, text='图片目录', command=self.open_dir).pack(side=LEFT)

        # 创建底部
        bot_frame = LabelFrame(self.master)
        bot_frame.pack(fill=X, side=TOP, padx=15, pady=8)
        self.e = StringVar()
        ttk.Label(bot_frame, width=60, textvariable=self.e).pack(side=LEFT, fill=BOTH, expand=YES, pady=10)
        self.e.set('程序员美德：懒惰、不耐烦、傲慢')
        ttk.Button(bot_frame, text='确定', command=self.function_command).pack(side=RIGHT)
        ttk.Button(bot_frame, text='复原', command=self.function_re_command).pack(side=RIGHT)

    def open_dir(self):
        self.entry.delete(0,END)
        dir_path = filedialog.askdirectory(title=u'选择文件夹',initialdir = self.here)
        self.path0 = dir_path
        self.path1 = self.path0+'/'
        self.entry.insert('insert', self.path1)

    def out_txt(self,txt_file_name, out_result):
        out_file_name = txt_file_name
        with open(out_file_name, 'w+', encoding='GBK') as out_file:  # 保存为ANSI格式
            out_file.write(out_result)
        pass

    def function_command(self):
        line = ''
        sys.path.append(self.path1)
        csvFiles = os.listdir(self.path0)
        for csvFilename in csvFiles:
            portion = os.path.splitext(csvFilename)
            if portion[1] == '.csv':
                new_name = f'{portion[0]}.txt'
                filenamedir = self.path1 + csvFilename
                new_name_dir = self.path1 + new_name
                os.rename(filenamedir, new_name_dir)
        pass
        pathDir = os.listdir(self.path1)
        for allDir in pathDir:
            child = self.path1 + allDir
            file = open(child, 'r+')
            fileCsv = file.read()
            file.seek(0, 0)
            line = line + fileCsv
        if 'Analog' in csvFiles[0]:
            out_file_name = r'C:\Users\Administrator\Documents\python\shiyan\allCSV\Analog-out.csv'
        elif 'Status' in csvFiles[0]:
            out_file_name = r'C:\Users\Administrator\Documents\python\shiyan\allCSV\Status-out.csv'
        else:
            out_file_name = r'C:\Users\Administrator\Documents\python\shiyan\allCSV\Other-out.csv'
        self.out_txt(out_file_name,line)

        print("结束")

    def function_re_command(self):
        sys.path.append(self.path1)
        csvFiles = os.listdir(self.path0)
        for csvFilename in csvFiles:
            portion = os.path.splitext(csvFilename)
            if portion[1] == '.txt':
                new_name = f'{portion[0]}.csv'
                filenamedir = self.path1 + csvFilename
                new_name_dir = self.path1 + new_name
                os.rename(filenamedir, new_name_dir)
        pass
if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400')  # 窗口尺寸
    Windows_NODE(root)
    root.title("CSV文件合并")
    root.mainloop()

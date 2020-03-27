# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
#==========================================================
# Rev01
# 参数修改，SFC语句生成工具
#==========================================================

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import re
import YokoRead   #自定义模块
from time import sleep
from YokoRead import time_Decorator,thread_Decorator

class Windows_NODE(YokoRead._FILE_NODE_):
    def __init__(self, master):
        self.master = master
        self.here = os.getcwd()
        self.initWidgets()
        help_doc = '本程序为TUNING修改工具 \n'
        self.text_update(help_doc)


    def initWidgets(self):
        testpath = 'C:/Users/Administrator/Documents/python/0.输出文件/PVI_TUN/PVI_TUN_list.xls'
        # 创建中部
        mid_frame = LabelFrame(self.master, text='数据列表')
        mid_frame.pack(fill=X, padx=15, pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(mid_frame, width=45, textvariable=self.e2)
        self.e2.set(testpath)
        self.entry2.pack(fill=X, expand=YES, side=LEFT, pady=10)
        self.e3 = StringVar()
        self.comboxlist = ttk.Combobox(mid_frame, width=15, textvariable=self.e3)
        self.comboxlist.pack(side=LEFT)
        self.e3.set('Tuning_temp')
        ttk.Button(mid_frame, text='数据列表', command=self.open_file2).pack(side=LEFT)

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
        self.e.set('懒惰、不耐烦、傲慢')
        ttk.Button(bot_frame, text='确定', command=self.command).pack(side=RIGHT, padx=10)

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
        #开始
        self.text_update('START_')
        #读取界面 文件信息
        file_name = self.entry2.get()
        sheet_name = self.comboxlist.get()
        # 文本生成
        line = ''
        line2 = '\n'
        Keywords= list(next(self.get_data_Tag(file_name, sheet_name)))
        for i in self.get_data(file_name, sheet_name):
            tag_index = i[Keywords[0]]
            tag_key = i[Keywords[1]]
            tag_func = i[Keywords[2]]
            line = line +'global block '+ tag_func +' ' +tag_index +' alias '+ tag_key+'\n'
            # global block PVI TAG83 alias 6200PIC11102A
            for item in Keywords[3:]: #从第4项开始为TAG.ITEM
                tag_item = str(i[item])
                if tag_item != "" :
                    line2 = line2 + tag_index +'.'+ item + ' = '+ tag_item +'\n'
                    # TAG01.HH = 11.0
                    pass
            self.text_update('>>>>' + tag_key + '\n')
            pass
        line = line + line2
        # 文本写入
        filepath, fullflname = os.path.split(file_name)
        self.outtxt = os.path.join(filepath, 'OUT.txt')
        self.out_txt(self.outtxt, line)
        #结束
        self.text_update('STOP_')
        sleep(2)
        pass

    def text_update(self,show):
        if show == 'START_':
            self.Text.insert(END, "=============程序开始=============\n")
        elif show == 'STOP_':
            self.Text.insert(END, "=============程序结束=============\n")
            self.Text.insert(END, "=将结果粘贴进入SEBOL功能块即可使用=\n")
        else:
            self.Text.insert(END,show)
        self.Text.update()
        self.Text.see(END)
        #self.text_update('START_')
        pass

if __name__ == "__main__":
        root = Tk()
        root.title("V1.00")
        root.geometry('640x400')  # 窗口尺寸
        Windows_NODE(root)
        limit_time = YokoRead._ALRM_NODE_.limited_time(root)
        root.title("TUNING参数修改工具" + "    到期日:" + limit_time)
        root.mainloop()

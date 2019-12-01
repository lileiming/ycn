#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
import os, sys
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter import ttk
#from tkinter.messagebox import *
#import tkinter.filedialog as tkFileDialog
#import tkinter.simpledialog as tkSimpleDialog    #askstring()
 
class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Form1')
        self.master.geometry('780x580')
        self.createWidgets()
 
    def createWidgets(self):
        self.top = self.winfo_toplevel()
 
        self.style = Style()
 
        self.TabStrip1 = Notebook(self.top)
        self.TabStrip1.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.TabStrip1__Tab1 = Frame(self.TabStrip1)
        self.TabStrip1.add(self.TabStrip1__Tab1, text='量程变更')
        #self.TabStrip1__Tab1Lbl = Label(self.TabStrip1__Tab1, text='Please add widgets in code.')
        #self.TabStrip1__Tab1Lbl.place(relx=0.1,rely=0.5)

        top_frame = LabelFrame(self.TabStrip1__Tab1, text='DR文件目录', height=150, width=615)
        top_frame.pack(fill=X, padx=15, pady=10)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame, width=65, textvariable=self.e1)
        self.e1.set('IN')
        self.entry.pack(fill=X, expand=YES, side=LEFT, pady=10)
        ttk.Button(top_frame, text='DR文件目录', command=self.foo).pack(side=LEFT)

        # 创建中部
        mid_frame = LabelFrame(self.TabStrip1__Tab1, text='数据列表')
        mid_frame.pack(fill=X, padx=15, pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(mid_frame, width=45, textvariable=self.e2)
        self.e2.set('TagRange_list.xls')
        self.entry2.pack(fill=X, expand=YES, side=LEFT, pady=10)
        self.e3 = StringVar()
        self.comboxlist = ttk.Combobox(mid_frame, width=15, textvariable=self.e3)
        self.comboxlist.pack(side=LEFT)
        self.e3.set('Range')
        ttk.Button(mid_frame, text='数据列表', command=self.foo).pack(side=LEFT)

        # 创建中下
        bot_frame1 = LabelFrame(self.TabStrip1__Tab1, text='结果')
        bot_frame1.pack(fill=X, side=TOP, padx=15, pady=0)
        self.Scroll = Scrollbar(bot_frame1)
        self.Text = Text(bot_frame1, width=83, height=13, yscrollcommand=self.Scroll.set)
        self.Text.pack(side=LEFT, padx=0, pady=5)
        self.Scroll = Scrollbar(bot_frame1)
        self.Scroll.pack(side=LEFT, fill=Y)
        self.Scroll.config(command=self.Text.yview)

        # 创建底部
        bot_frame = LabelFrame(self.TabStrip1__Tab1)
        bot_frame.pack(fill=X, side=TOP, padx=15, pady=8)
        self.e = StringVar()
        ttk.Label(bot_frame, width=60, textvariable=self.e).pack(side=LEFT, fill=BOTH, expand=YES, pady=10)
        self.e.set('组态工具集')
        ttk.Button(bot_frame, text='量程替换', command=self.foo).pack(side=RIGHT)





        self.TabStrip1__Tab2 = Frame(self.TabStrip1)
        self.TabStrip1.add(self.TabStrip1__Tab2, text='找游戏')
        self.TabStrip1__Tab2Lbl = Label(self.TabStrip1__Tab2, text='Please add widgets in code.')
        self.TabStrip1__Tab2Lbl.place(relx=0.1,rely=0.5)
 
    def foo(self):
        pass
 
class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
 
if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
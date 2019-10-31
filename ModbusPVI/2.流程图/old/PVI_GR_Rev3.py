# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================

# Rev01
# 读取模板

# ReV02
# 操作界面

# ReV03
# 直接读取GR样本文档

#==========================================================

from tkinter import *
# 导入ttk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import xlrd
import os
import re
import sys
import math
import time
import tkinter.messagebox 

class App:
    def __init__(self, master):
        self.master = master
        self.initWidgets()
        
    def initWidgets(self):
        # 创建顶部
        top_frame = LabelFrame(self.master,text='参考文档',height = 150,width = 615)
        top_frame.pack(fill=X,padx=15,pady=0)
        #top_frame.pack(fill=X,expand=YES,side=TOP,padx=15,pady=0)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame,width=65,textvariable = self.e1)
        self.e1.set("GRtemp.xaml")
        self.entry.pack(fill=X,expand=YES,side=LEFT,pady=10)
        ttk.Button(top_frame,text='参考文档',command=self.open_file).pack(side=LEFT)

        # 创建中部
        mid_frame = LabelFrame(self.master,text='数据列表')
        mid_frame.pack(fill=X,padx=15,pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(mid_frame,width=45,textvariable = self.e2)
        self.e2.set("GR_PVI_list.xls")
        self.entry2.pack(fill=X,expand=YES,side=LEFT,pady=10)
        self.e3 = StringVar()
        self.comboxlist=ttk.Combobox(mid_frame,width=15,textvariable = self.e3) 
        self.comboxlist.pack(side=LEFT)
        self.e3.set("DATE1")
        ttk.Button(mid_frame, text='数据列表', command=self.open_file2).pack(side=LEFT)

        # 创建中下
        bot_frame1 = LabelFrame(self.master,text='结果')
        bot_frame1.pack(fill=X,side=TOP,padx=15,pady=0)
        self.Scroll = Scrollbar(bot_frame1)
        self.Text = Text(bot_frame1 ,width=83,height=13,yscrollcommand = self.Scroll.set)
        self.Text.pack(side=LEFT,padx=0,pady=5)
        self.Scroll = Scrollbar(bot_frame1 )
        self.Scroll.pack(side = LEFT, fill = Y)
        self.Scroll.config(command = self.Text.yview)

        # 创建底部
        bot_frame = LabelFrame(self.master)
        bot_frame.pack(fill=X,side=TOP,padx=15,pady=8)
        self.e = StringVar()
        #self.lable(bot_frame,text = '欢迎使用',width = 60,height = 20).pack(side=LEFT)
        ttk.Label(bot_frame,width = 60,textvariable = self.e).pack(side=LEFT, fill=BOTH, expand=YES,pady=10)
        self.e.set("转换工具")
        ttk.Button(bot_frame, text='转换', command=self.get_entry).pack(side=RIGHT)

    def open_file(self):
        self.entry.delete(0,END)
        file_path = filedialog.askopenfilename(title=u'选择参考文档', initialdir=(os.path.expanduser('H:/')))
        file_text = file_path
        self.entry.insert('insert', file_text)
        
    def open_file2(self):
        self.entry2.delete(0,END)
        file_path = filedialog.askopenfilename(title=u'选择数据列表', initialdir=(os.path.expanduser('H:/')))
        file_text = file_path
        self.entry2.insert('insert', file_text)
        sheetName = get_sheet(file_text)
        sheetNameT = tuple(sheetName)
        self.comboxlist["values"] = sheetNameT
        self.comboxlist.current(0)
        
    def get_entry(self):
        try:
            samplePVI = self.entry.get()
            resultDR = 'GR_output.xaml'
            modbusList = self.entry2.get()
            #listSheet = "DATE"
            listSheet = self.comboxlist.get()
            #print (listSheet)
            maintxt = open(samplePVI,'r',encoding='utf-8')
            OutFile = open(resultDR,'w+',encoding='utf-8')
            
            # 读取所有样本流程图
            alls = maintxt.read()
            # 读取所有样本流程图=====头部
            head1 = (re.findall('<!--P([\w\W]*)Visual Layer" />',alls))
            head = ('<!--P' + str(head1[0]) +'Visual Layer" />')
            ##print(head1)
            # 读取所有样本流程图=====内容
            s1 = (re.findall('Function Link Component0" />([\w\W]*)</yiapcspvgbdc0:GroupComponent>',alls))
            s = (str(s1[0]) +'</yiapcspvgbdc0:GroupComponent>')
            #print(s)
            # 读取所有样本流程图=====底部
            foot = '</Canvas>'
            # 读取所有样本流程图=====位置信息
            #Canvas.Left="60"
            LeftData = (re.findall('Canvas.Left="\w+"',alls))
            #print(LeftData[0])
            TopData = (re.findall('Canvas.Top="\w+"',alls))
            LeftDataCount = 0
            
            self.Text.insert('insert', "=============转换开始===============\n")
            OutFile.seek(0,0)
            datalist = list(get_data_Tag(modbusList,listSheet))
            datalist_tag = tuple(datalist[0].values())
            #print(datalist_tag[0])

            OutFile.write(head)   #写入头部
            OutFile.write("\n")
            
            for i in get_data(modbusList,listSheet):
                for j in datalist_tag:
                    if j ==datalist_tag[0]:
                        TAG = i[j]
                        inValue = j
                        outValue = str(TAG)
                        line = s.replace (inValue,outValue)
                    if j !=datalist_tag[0]:                    
                        TAG = i[j]
                        inValue = j
                        outValue = str(TAG)
                        line = line.replace (inValue,outValue)
                 
                #修改坐标===
                inValue = LeftData[0]
                outValue = 'Canvas.Left="'+ str(LeftDataCount*10+100) +'"'
                line = line.replace (inValue,outValue)
                inValue = TopData[0]
                outValue = 'Canvas.Top="'+ str(LeftDataCount*15+100) +'"'
                line = line.replace (inValue,outValue)
                LeftDataCount += 1
                    
                self.Text.insert('insert','INFO: '+ TAG + " 转换结束\n")
                OutFile.write(line) #写入内容
                OutFile.write("\n")
             
            OutFile.write(foot)#写入底部
            
            maintxt.close
            OutFile.close
            self.Text.insert('insert', "转换结束：结果已输出至 DR_output.xaml")
            self.Text.see(END)

        except FileNotFoundError as e:
            self.e.set(e)
        except UnicodeDecodeError as e:
            self.e.set(e)

def get_data_Tag(filename,sheet_name):
    dir_case = filename
    data = xlrd.open_workbook(dir_case)
    table = data.sheet_by_name(sheet_name)
    nor = table.nrows
    nol = table.ncols
    #print(nol)
    dict = {}
    #for i in range(0,nor):
    for j in range(nol):
        title = table.cell_value(0,j)
        #print(title)
        dict[title] = title
    yield dict

def get_sheet(filename):
    dir_case = filename
    data = xlrd.open_workbook(dir_case)
    sheetN = data.sheet_names()
    return sheetN            
  
def get_data(filename,sheet_name):
    dir_case = filename
    data = xlrd.open_workbook(dir_case)
    table = data.sheet_by_name(sheet_name)
    nor = table.nrows
    nol = table.ncols
    dict = {}
    for i in range(1,nor):
        for j in range(nol):
            title = table.cell_value(0,j)
            value = table.cell_value(i,j)
            dict[title] = value
        yield dict
       
if __name__ == "__main__":
    ticks = time.time()
    #print(ticks)
    limitTime = 1571498236+2592000
    localtime = time.strftime("%Y/%m/%d", time.localtime(limitTime))
    if (ticks < limitTime):
        #============================================================
        root = Tk()
        root.title("列表流程图生成工具 V3.01  有效期至"+localtime)
        root.geometry('640x400')  # 窗口尺寸
        App(root)
        root.mainloop()
    else:
        tkinter.messagebox.showinfo('提示','软件过期需要重新编译' )
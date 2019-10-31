# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================

# Rev01
# 读取模板

# ReV02
# 操作界面

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
        self.e1.set("PVItemp.txt")
        self.entry.pack(fill=X,expand=YES,side=LEFT,pady=10)
        ttk.Button(top_frame,text='参考文档',command=self.open_file).pack(side=LEFT)

        # 创建中部
        mid_frame = LabelFrame(self.master,text='数据列表')
        mid_frame.pack(fill=X,padx=15,pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(mid_frame,width=45,textvariable = self.e2)
        self.e2.set("modbus.xls")
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
            resultDR = 'DR_output.txt'
            modbusList = self.entry2.get()
            #listSheet = "DATE"
            listSheet = self.comboxlist.get()
            #print (listSheet)

            maintxt = open(samplePVI,'r',encoding='utf-8')
            OutFile = open(resultDR,'a',encoding='utf-8')
            
            
            s = maintxt.read() 
            self.Text.insert('insert', "=============转换开始===============\n")
            
            
            OutFile.seek(0,0)
            for i in get_data(modbusList,listSheet):
            #===========参数
                TAG1 = i['ZZZ'] 
                TAG2 = i['AAABBBCC'] 
                TAG3 = i['DDDE']
                TAG4 = i['FFFGGGHHH']
                
                
                print(TAG2,TAG3,TAG4)
                
                
        ###   No
                inValue = "ZZZ"
                outValue = str(TAG1)
                line = s.replace (inValue,outValue)
        
                inValue = "AAABBBCC"
                outValue = str(TAG2)
                line = line.replace (inValue,outValue)
                
                inValue = "DDDE"
                outValue = str(TAG3)
                line = line.replace (inValue,outValue)

                inValue = "FFFGGGHHH"
                outValue = str(TAG4)
                line = line.replace (inValue,outValue)

                OutFile.write(line)
                OutFile.write("\n")
            maintxt.close
            OutFile.close

            self.e.set("转换结束：结果已输出至 DR_output.txt")  
            #root.destroy() 
        except FileNotFoundError as e:
            self.e.set(e)
        except UnicodeDecodeError as e:
            self.e.set(e)  
  
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
        
def get_sheet(filename):
    dir_case = filename
    data = xlrd.open_workbook(dir_case)
    sheetN = data.sheet_names()
    return sheetN


if __name__ == "__main__":
    root = Tk()
    root.title("modbus列表生成工具 V2.0")
    root.geometry('640x400')  # 窗口尺寸
    App(root)
    root.mainloop()

# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
#==========================================================

# Rev01
# 读取模板

# ReV02
# 操作界面

# Rev02.01
# UTF-8 代码错误订正
#==========================================================

from tkinter import *
# 导入ttk
from tkinter import ttk
from tkinter import filedialog
import os
import xlrd
import sys
from time import sleep
import YokoRead   #自定义模块
from YokoRead import time_Decorator,thread_Decorator

class Windows_NODE(YokoRead._FILE_NODE_):

    def __init__(self, master):
        self.master = master
        self.here = os.getcwd()
        self.initWidgets()
        help_doc = '本程序为快速替换组态工具。 \n ' \
                   '使用方法：\n' \
                   '1.通过按钮选择数据列表文件，使用下拉菜单选择相对应的表格（sheet）\n' \
                   '2.通过按钮选择目标文件文件夹.\n' \
                   '3.点击[替换 CSV 文件]按钮执行替换 CSV 文件、\n' \
                   '4.点击[替换 TxT 文件]按钮执行替换 TXT 文件、\n'
        self.Text.insert('insert', help_doc)
        
    def initWidgets(self):
        # top_frame ===================================
        top_frame = LabelFrame(self.master,text='数据列表')
        top_frame.pack(fill=X,padx=15,pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(top_frame,width=45,textvariable = self.e2)
        self.e2.set("replaceExc.xlsx")
        self.entry2.pack(fill=X,expand=YES,side=LEFT,pady=10)
        self.e3 = StringVar()
        self.comboxlist=ttk.Combobox(top_frame,width=18,textvariable = self.e3)
        self.comboxlist.pack(side=LEFT)
        self.e3.set("DATE")
        ttk.Button(top_frame, text='数据列表', command=self.open_file2).pack(side=LEFT)

        # mid_frame1 ===================================
        mid_frame = LabelFrame(self.master,text='结果:')
        mid_frame.pack(fill=X,side=TOP,padx=15,pady=10)
        self.Scroll = Scrollbar(mid_frame)
        self.Text = Text(mid_frame,width=83, height=16, yscrollcommand=self.Scroll.set)
        self.Text.pack(side=LEFT,fill = BOTH)
        self.Scroll = Scrollbar(mid_frame)
        self.Scroll.pack(side = RIGHT, fill = Y)
        self.Scroll.config(command = self.Text.yview)

        # bot_frame ===================================
        bot_frame = LabelFrame(self.master)
        bot_frame.pack(fill=X,side=TOP,padx=15,pady=10)
        ttk.Button(bot_frame,text='选择目标文件夹',command=self.open_dir).pack(side=LEFT,padx=10,pady=10)
        ttk.Button(bot_frame,text='替换 CSV 文件',command=self.Csv).pack(side=RIGHT,padx=10)
        ttk.Button(bot_frame,text='替换 Txt 文件',command=self.Txt).pack(side=RIGHT,padx=10)

    def text_insert(self,flag):

        if flag == 'path1':
            self.Text.insert('insert', 'File directory：\n' + self.path1 + '\n')
            pass
        if flag == 'csv':
            self.Text.insert('insert', 'INFO: ****Start converting csv files.****\n')
            pass
        if flag == 'completed':
            self.Text.insert('insert', 'INFO: ****All file Conversion completed.****\n')
            self.Text.see(END)
            pass
        if flag == 'txt':
            self.Text.insert('insert', 'INFO: ****Start converting txt files.****\n')
            pass
        if flag == 'error':
            self.Text.insert('insert', 'ERROR：File format error'+'\n')
            pass

        self.Text.update()
        pass
        
    def open_dir(self):
        self.Text.delete(0.0,END)
        dir_path = filedialog.askdirectory(title=u'Select file directory', initialdir=self.here)
        self.path0 = dir_path
        self.path1 = self.path0+'/'
        self.text_insert('path1')

    def open_file2(self):
        self.entry2.delete(0,END)
        file_path = filedialog.askopenfilename(title=u'选择数据列表', initialdir=self.here)
        file_text = file_path
        self.entry2.insert('insert', file_text)
        sheetName = self.get_sheet(file_text)
        sheetNameT = tuple(sheetName)
        self.comboxlist["values"] = sheetNameT
        self.comboxlist.current(0)

    @thread_Decorator
    @time_Decorator
    def Csv(self):
        self.text_insert('csv')
        self.flag = 1
        self.reName2txt()
        self.readExcel()
        self.eachFile()
        self.flag = 0
        self.text_insert('completed')
        sleep(1)

    @thread_Decorator
    @time_Decorator
    def Txt(self):
        self.text_insert('txt')
        self.flag = 0
        self.readExcel()
        self.eachFile()
        self.flag = 0   
        self.text_insert('completed')
        sleep(1)

    def reName2txt(self):
        sys.path.append(self.path1)
        csvFiles = os.listdir(self.path0)
        for csvFilename in csvFiles:
            portion = os.path.splitext(csvFilename)
            if (portion[1] == '.csv'): 
                newname = portion[0] + '.txt' 
                self.filenamedir=self.path1 + csvFilename
                newnamedir=self.path1 + newname
                os.rename(self.filenamedir,newnamedir)
            else:
                self.text_insert('error')
        
    def readExcel(self):
        filename = self.entry2.get()
        sheet_name = self.comboxlist.get()
        self.inValue = []
        self.outValue = []
        count = 1
        filePath = os.path.join(os.getcwd(), filename)
        x1 = xlrd.open_workbook(filePath)
        sheet1 = x1.sheet_by_name(sheet_name)
        self.rowsNum = sheet1.nrows
        
        while (count < self.rowsNum):
           count = count + 1
           in1=sheet1.cell_value(count-1,0)
           self.inValue.append(in1)
           out1=sheet1.cell_value(count-1,1)
           self.outValue.append(out1)
        
    def eachFile(self):
        pathDir = os.listdir(self.path1)
        for allDir in pathDir:
            self.child = self.path1 + allDir
            if (self.flag) == 1:
                self.readfile()
            else:
                self.readTXTfile()
                
    def readfile(self):
        with open(self.child,'r+')as f1:
            s = f1.read()
        f1.seek(0,0)
        line = s.replace (self.inValue[0],self.outValue[0])
        num = 1
        while (num < self.rowsNum):
            line = line.replace (self.inValue[num-1],self.outValue[num-1])
            num = num +1
        f1.write(line)
        
        self.startNo = s.index('%')

        NodeSolt = s[self.startNo:self.startNo+5]
        IOM = NodeSolt[1]
        if (IOM == 'Z' ):
            nodeX = NodeSolt[2]
            nodeY = NodeSolt[3]
            soltX = NodeSolt[4]
            flienameNS = self.path1+'N'+nodeX+nodeY+'S'+soltX+'.csv'
            repeatName = 'N'+nodeX+nodeY+'S'+soltX+'.csv'
            try:
                os.renames(self.child,flienameNS)
                self.Text.insert('insert', 'INFO:'+repeatName+' Conversion completing...\n')
            except WindowsError as e:
                self.Text.insert('insert', 'ERROR:'+repeatName+' Because Double name skip\n')
                    
        elif (IOM == 'S' ):
            SWX = NodeSolt[3]
            flienameNS = self.path1+'SwitchDef'+SWX+'.csv'
            repeatName = 'SwitchDef'+SWX+'.csv'
            try:
                os.renames(self.child,flienameNS)
                self.Text.insert('insert', 'INFO:'+repeatName+'Conversion completing...\n')
            except WindowsError as e:
                self.Text.insert('insert', 'ERROR:'+repeatName+' Because Double name skip\n')

        elif (IOM == 'A' ):
            ANX = NodeSolt[2]
            flienameNS = self.path1+'AN'+'.csv'
            repeatName = 'AN'+ANX+'.csv'
            try:
                os.renames(self.child,flienameNS)
                self.Text.insert('insert', 'INFO:'+repeatName+'Conversion completing...\n')
            except WindowsError as e:
                self.Text.insert('insert', 'ERROR:'+repeatName+' Because Double name skip\n')
        else:
            self.Text.insert('insert', 'ERROR:'+self.child+'Content not recognized\n')
        self.Text.update()

    def readTXTfile(self):
        self.stortNameApp()
        self.flag = 0
        f1 = open(self.child,'r+')
        try:
            s=f1.read()        
        except UnicodeDecodeError as e:
                self.Text.insert('insert', 'WARNING: '+self.ShortName+' is UTF-8 format.\n')
                self.Text.update()
                f1 = open(self.child,'r+',encoding='utf-8')
                s=f1.read()  

        DRfindNum = s.find('DR0')

    #======================================================
        f1.seek(0,0)
        line = s.replace (self.inValue[0],self.outValue[0])
        num = 1
        while (num < self.rowsNum):
            line = line.replace (self.inValue[num-1],self.outValue[num-1])
            num = num +1
        f1.write(line)
        f1.close()
    #======================================================
        if DRfindNum > 0 :
            DR0X = s[DRfindNum+3]
            DR00Y = s[DRfindNum+4]
            DR000Z = s[DRfindNum+5]
            #print "DR0"+DR0X+DR00Y+DR000Z
            flienameNS = self.path1+"DR0"+DR0X+DR00Y+DR000Z+'.txt'
            repeatName = "DR0"+DR0X+DR00Y+DR000Z+'.txt'
            try:
               os.renames(self.child,flienameNS)
               self.Text.insert('insert', 'INFO: '+self.ShortName+' Conversion completing...\n')
            except WindowsError as e:
               self.Text.insert('insert', 'ERROR: '+self.ShortName+' Because Double name skip.\n')
        else:
            self.Text.insert('insert', 'WARNING: '+self.ShortName+' does not conform to the DR format.\n')
        self.Text.update()
            
    def stortNameApp(self):
        self.ShortName = os.path.basename(self.child)


if __name__ == "__main__":
    root = Tk()
    root.title("Tag replacement tool V2.01")
    root.geometry('640x400')  # Window size
    Windows_NODE(root)
    root.mainloop()


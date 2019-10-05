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
import os
import xlrd
import linecache
import sys 
import csv


class App:

    def __init__(self, master):
        self.master = master
        self.initWidgets()
        
    def initWidgets(self):
        # top_frame ===================================
        top_frame = LabelFrame(self.master,text='Result:')
        top_frame.pack(fill=BOTH, expand=YES)
        # top_frame1 ===================================
        top_frame1 = LabelFrame(top_frame)
        top_frame1.pack(fill=BOTH,expand=YES,side=TOP)
        self.Scroll = Scrollbar(top_frame1)
        self.Text = Text(top_frame1,yscrollcommand = self.Scroll.set,width=87)
        self.Text.pack(side=LEFT,fill = BOTH)
        self.Scroll = Scrollbar(top_frame1)
        self.Scroll.pack(side = RIGHT, fill = Y)
        self.Scroll.config(command = self.Text.yview)
        
        
        # mid_frame ===================================
        mid_frame = LabelFrame(self.master)
        mid_frame.pack(fill=BOTH,expand=YES,side=TOP)
        ttk.Button(mid_frame,text='Select Directory',command=self.open_dir).pack(side=LEFT,padx=15)
        ttk.Button(mid_frame,text='Replace CSV file',command=self.Csv).pack(side=RIGHT,padx=15)
        ttk.Button(mid_frame,text='Replace Txt file',command=self.Txt).pack(side=RIGHT,padx=15)
        
    def open_dir(self):
        self.Text.delete(0.0,END)
        dir_path = filedialog.askdirectory(title=u'Select file directory')
        self.path0 = dir_path
        self.path1 = self.path0+'/'
        self.Text.insert('insert', 'File directory：\n'+self.path1+'\n')
                  
    def Csv(self):
        self.Text.insert('insert', 'INFO: ****Start converting csv files.****\n')
        self.flag = 1
        self.reName2txt()
        self.readExcel()
        self.eachFile()
        self.flag = 0   
        self.Text.insert('insert', 'INFO: ****All file Conversion completed.****\n') 
        self.Text.see(END)
        
    def Txt(self):
        self.Text.insert('insert', 'INFO: ****Start converting csv files.****\n')
        self.flag = 0
        self.readExcel()
        self.eachFile()
        self.flag = 0   
        self.Text.insert('insert', 'INFO: ****All file Conversion completed.****\n') 
        self.Text.see(END)
        
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
                self.Text.insert('insert', 'ERROR：File format error'+'\n')
        
    def readExcel(self):
        filename = "replaceExc.xlsx"
        sheetname = "Sheet1"
        self.inValue = []
        self.outValue = []
        count = 1
        filePath = os.path.join(os.getcwd(), filename)
        x1 = xlrd.open_workbook(filePath)
        sheet1 = x1.sheet_by_name(sheetname)
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
        f1 = open(self.child,'r+')
        s=f1.read()
        f1.seek(0,0)
        line = s.replace (self.inValue[0],self.outValue[0])
        num = 1
        while (num < self.rowsNum):
            line = line.replace (self.inValue[num-1],self.outValue[num-1])
            num = num +1
        f1.write(line)
        f1.close()
        
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
            repeatName = 'AN'+'.csv'
            try:
                os.renames(self.child,flienameNS)
                self.Text.insert('insert', 'INFO:'+repeatName+'Conversion completing...\n')
            except WindowsError as e:
                self.Text.insert('insert', 'ERROR:'+repeatName+' Because Double name skip\n')
                
        else:
            self.Text.insert('insert', 'ERROR:'+self.childOnlyName+'Content not recognized\n')

    def readTXTfile(self):
        self.flag = 0
        f1 = open(self.child,'r+')
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
               self.Text.insert('insert', 'INFO: '+repeatName+'Conversion completing...\n')
            except WindowsError as e:
               self.Text.insert('insert', 'ERROR: '+self.child+'Because Double name skip.\n')
        else:
            self.Text.insert('insert', 'ERROR: '+self.child+' does not conform to the format.\n')

               
               
if __name__ == "__main__":
    root = Tk()
    root.title("Tag replacement tool V2.0")
    root.geometry('640x400')  # Window size
    App(root)
    root.mainloop()


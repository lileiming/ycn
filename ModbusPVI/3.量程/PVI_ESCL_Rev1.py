# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================
# Rev01

#==========================================================
from tkinter import *
# 导入ttk
from tkinter import ttk
from tkinter import filedialog
import time
import tkinter.messagebox

import os
import xlrd
import re


class  _FILE_NODE_:
    #读取模块
#    def __init__(self):
    def read_txt(self,txt_file_name):
        #读取txt文档
        file_data = open(txt_file_name,'r')
        file_detail = file_data.read()
        return file_detail

    def out_txt(self,txt_file_name,out_result):
        out_file_name = txt_file_name
        out_file = open(out_file_name, 'w+', encoding='GBK')  #保存为ANSI格式
        out_file.write(out_result)
        out_file.close()

    def get_sheet(self,filename):
        dir_case = filename
        data = xlrd.open_workbook(dir_case)
        sheetN = data.sheet_names()
        return sheetN

    def get_data_Tag(self,filename, sheet_name):
        dir_case = filename
        data = xlrd.open_workbook(dir_case)
        table = data.sheet_by_name(sheet_name)
        nor = table.nrows
        nol = table.ncols
        # print(nol)
        dict = {}
        # for i in range(0,nor):
        for j in range(nol):
            title = table.cell_value(0, j)
            # print(title)
            dict[title] = title
        yield dict

    def get_data(self,filename, sheet_name):
        dir_case = filename
        data = xlrd.open_workbook(dir_case)
        table = data.sheet_by_name(sheet_name)
        nor = table.nrows
        nol = table.ncols
        dict = {}
        for i in range(1, nor):
            for j in range(nol):
                title = table.cell_value(0, j)
                value = table.cell_value(i, j)
                dict[title] = value
            yield dict

class PROCESS_NODE(_FILE_NODE_):
    # 处理模块
    def __init__(self):
        self.excel_file_name = 'TagRange_list.xls'
        self.sheet_name = 'Range'
        self.path0 = 'IN'
        self.recording = []

    def find_keyword(self,txt_file):
        #寻找关键字
        self.txt_file = txt_file
        self.file_detail = self.read_txt(self.txt_file)
        #print(file_detail)
        self.find_result = (re.findall(':FNRM([\w\W]*?)::FNRM', self.file_detail))

    def process_key(self):
        #处理关键字
        file_name = self.excel_file_name
        sheet_name = self.sheet_name
        #datalist = list(self.get_data_Tag(file_name, sheet_name))
        #datalist_tag = tuple(datalist[0].values())
        for i in self.get_data(file_name, sheet_name):
            #print(i)
            self.tag_key = i['TAG']
            lower = i['LOWER']
            upper = i['UPPER']
            unit  = i['UNIT']
            #print(self.tag_key,lower,upper,unit )
            self.range_rep(upper,lower,unit)

    def range_rep(self,upper,lower,unit):
        # Condition 1:
        range_key = 'ESCL:1:100.0:0.0;'
        range_new_key = "ESCL:1:"+ str(upper) +":"+ str(lower) +";"
        # Condition 2:
        unit_key = 'EUNT:1:%;'
        unit_new_key = "EUNT:1:"+ str(unit) + ";"

        for _ in self.find_result:
            #print(_)
            #self.recording = self.txt_file_name
            if self.tag_key in _:
                #print(self.tag_key)
                # Condition 1:
                self.good_result = str(_).replace(range_key, range_new_key, 1)
                # Condition 2:
                self.good_result = self.good_result.replace(unit_key,unit_new_key,1)
                #print(self.good_result)
                self.file_detail = str(self.file_detail).replace(_,self.good_result,1)
                #print(self.file_detail)
                #self.recording = self.txt_file_name
                self.recording.append(self.txt_file_name)

        self.out_txt(self.outtxt,self.file_detail)

    def process_out(self):
        txt_in_files = os.listdir(self.path0)
        for _txt in txt_in_files:
            self.txt_file_name = self.path0 + '/' +_txt
            #print(txt_file_name )
            self.outtxt =  self.path0 + '/' + 'OUT-' +_txt

            if self.txt_file_name.find('OUT')<0:
                self.find_keyword(self.txt_file_name)
                self.process_key()
        print(set(self.recording))


if __name__ == "__main__":
        app = PROCESS_NODE()
        app.process_out()
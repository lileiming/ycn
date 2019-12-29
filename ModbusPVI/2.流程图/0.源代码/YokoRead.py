import os
import xlrd
import re
import time
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox

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
        pass

    def get_sheet(self,filename):
        dir_case = filename
        data = xlrd.open_workbook(dir_case)
        sheetN = data.sheet_names()
        return sheetN

    def get_data_Tag(self,filename, sheet_name):
        dir_case = filename
        data = xlrd.open_workbook(dir_case)
        table = data.sheet_by_name(sheet_name)
        #nor = table.nrows
        nol = table.ncols
        # print(nol)
        dict = {}
        # for i in range(0,nor):
        for j in range(nol):
            title = table.cell_value(0, j)
            # print(title)
            dict[title] = title
        yield dict
    
    def get_data_2line(self,filename,sheet_name):
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

class _ALRM_NODE_:
    #报警模块
    def limited_time(self):
        ticks = time.time()
        print(ticks)
        limitTime = 1577633342+2592000
        localtime = time.strftime("%Y/%m/%d", time.localtime(limitTime))
        #print(localtime)
        if (ticks > limitTime):
            tkinter.messagebox.showinfo('提示', '软件过期需要重新编译'+localtime)
            exit()
        return localtime
        
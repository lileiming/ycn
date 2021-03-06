import os
import xlrd
import re
import time
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox


class _FILE_NODE_:
    # 读取模块
    #    def __init__(self):
    def read_txt(self, txt_file_name):
        # 读取txt文档
        with open(txt_file_name, 'r') as file_data:
            file_detail = file_data.read()
        return file_detail

    def out_txt(self, txt_file_name, out_result):
        out_file_name = txt_file_name
        with open(out_file_name, 'w+', encoding='GBK') as out_file:  # 保存为ANSI格式
            out_file.write(out_result)
        pass

    def get_sheet(self, filename):
        dir_case = filename
        with xlrd.open_workbook(dir_case) as data:
            sheetN = data.sheet_names()
        return sheetN

    def get_data_Tag(self, filename, sheet_name):
        dir_case = filename
        data = xlrd.open_workbook(dir_case)
        table = data.sheet_by_name(sheet_name)
        # nor = table.nrows
        nol = table.ncols
        # print(nol)
        dict = {}
        # for i in range(0,nor):
        for j in range(nol):
            title = table.cell_value(0, j)
            # print(title)
            dict[title] = title
        yield dict

    def get_data_2line(self, filename, sheet_name):
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

    def get_data(self, filename, sheet_name):
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

    def rowList(self, sheet, Cindex):
        rowList = []
        rowN = 0
        rowsNum = sheet.nrows
        colNum = sheet.ncols
        while (rowN < rowsNum):
            row_Str = sheet.cell_value(rowN, Cindex)
            rowList.append(row_Str)
            rowN = rowN + 1
        ##print rowList
        return rowList

    def colList(self, sheet):
        colList = []
        colN = 0
        rowsNum = sheet.nrows
        colNum = sheet.ncols
        while (colN < colNum):
            col_Str = sheet.cell_value(0, colN)
            colList.append(col_Str)
            colN = colN + 1
        ##print rowList
        return colList

    def dictGenerate(self, sheet, Cindex):
        dict = {}
        rowsNum1 = sheet.nrows
        colNum1 = sheet.ncols
        for rowindex in range(rowsNum1):
            if rowindex != 0:
                for colindex in range(colNum1):
                    if colindex > Cindex:
                        TAG_Str = sheet.cell_value(rowindex, Cindex)
                        condition_Str = sheet.cell_value(0, colindex)
                        dict_Str = sheet.cell_value(rowindex, colindex)
                        dict[(TAG_Str, condition_Str)] = dict_Str
        return dict

class _ALRM_NODE_:
    #报警模块
    def limited_time(self):
        ticks = time.time()
        #print(ticks)
        limitTime = 2580220256+2592000
        localtime = time.strftime("%Y/%m/%d", time.localtime(limitTime))
        #print(localtime)
        if (ticks > limitTime):
            tkinter.messagebox.showinfo('提示', '软件过期需要重新编译'+localtime)
            exit()
        return localtime
# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# ==========================================================
# lileiming@me.com
# ('程序员美德：懒惰、不耐烦、傲慢')
# ==========================================================
import xlrd
import time
import tkinter.messagebox
import threading
from time import sleep,time,strftime,localtime
#import time
import calendar


class FILE_NODE:
    """
    功能块说明：读取模块
    """
    #    def __init__(self):
    def read_txt(self, txt_file_name):
        """
        功能块说明：读取txt文档
        """
        with open(txt_file_name, 'r') as file_data:
            var_txt_detail = file_data.read()
        return var_txt_detail

    def out_txt(self, txt_file_name, out_result):
        """
        功能块说明：输出txt文档
        """
        with open(txt_file_name, 'w+', encoding='GBK') as out_file:  # 保存为ANSI格式
            out_file.write(out_result)
        pass

    def get_sheet(self, file_name):
        """
        功能块说明：读取excle 文档 的sheet 名字。
        """
        with xlrd.open_workbook(file_name) as var_data:
            var_sheet_name = var_data.sheet_names()
        return var_sheet_name

    def get_data_Tag(self, file_name, sheet_name):
        """
        功能块说明：读取excle文档sheet下内容。
        """
        data = xlrd.open_workbook(file_name)
        table = data.sheet_by_name(sheet_name)
        # nor = table.nrows
        nol = table.ncols
        # print(nol)
        dict_r = {}
        # for i in range(0,nor):
        for j in range(nol):
            title = table.cell_value(0, j)
            # print(title)
            dict_r[title] = title
        yield dict_r

    def get_data_2line(self, file_name, sheet_name):
        dir_case = file_name
        data = xlrd.open_workbook(dir_case)
        table = data.sheet_by_name(sheet_name)
        nor = table.nrows
        nol = table.ncols
        dict_r = {}
        for i in range(1, nor):
            for j in range(nol):
                title = table.cell_value(0, j)
                value = table.cell_value(i, j)
                dict_r[title] = value
            yield dict_r

    def get_data(self, file_name, sheet_name):
        dir_case = file_name
        data = xlrd.open_workbook(dir_case)
        table = data.sheet_by_name(sheet_name)
        nor = table.nrows
        nol = table.ncols
        dict_r = {}
        for i in range(1, nor):
            for j in range(nol):
                title = table.cell_value(0, j)
                value = table.cell_value(i, j)
                dict_r[title] = value
            yield dict_r

    def rowList(self, sheet, Cindex):
        rowList = []
        rowN = 0
        rowsNum = sheet.nrows
        #colNum = sheet.ncols
        while rowN < rowsNum:
            row_Str = sheet.cell_value(rowN, Cindex)
            rowList.append(row_Str)
            rowN = rowN + 1
        ##print rowList
        return rowList

    def colList(self, sheet):
        colList = []
        colN = 0
        #rowsNum = sheet.nrows
        colNum = sheet.ncols
        while colN < colNum:
            col_Str = sheet.cell_value(0, colN)
            colList.append(col_Str)
            colN = colN + 1
        ##print rowList
        return colList

    def dictGenerate(self, sheet, Cindex):
        dict_r = {}
        rowsNum1 = sheet.nrows
        colNum1 = sheet.ncols
        for rowindex in range(rowsNum1):
            if rowindex != 0:
                for colindex in range(colNum1):
                    if colindex > Cindex:
                        TAG_Str = sheet.cell_value(rowindex, Cindex)
                        condition_Str = sheet.cell_value(0, colindex)
                        dict_Str = sheet.cell_value(rowindex, colindex)
                        dict_r[(TAG_Str, condition_Str)] = dict_Str
        return dict_r

    # def thread_it(self,func,*args):
    #     # 创建
    #     t = threading.Thread(target=func, args=args)
    #     # 守护 !!!
    #     t.setDaemon(True)
    #     # 启动
    #     t.start()
    #     # 阻塞--卡死界面！


def time_Decorator(func):
    def wrapper(self,*args):
        startTime = time()
        func(self, *args)
        endTime = time()
        msecs = (endTime - startTime)*1000
        print("time is %d ms" %msecs)
    return wrapper


def thread_Decorator(func):
    def wrapper(self, *args):
        t = threading.Thread(target=func, args=(self, *args))
        t.setDaemon(True)
        t.start()
    return wrapper


# 方法记录=====================
# filepath, fullflname = os.path.split(csvFilename)  # 文件名
# portion = os.path.splitext(csvFilename)   #portion[1] 文件后缀；portion[0] 文件名字
# ShortName = os.path.basename(self.child) #短名字


#find_result = re.search(r'<yiapcspvgccdc:TouchTarget([\w\W]*?)</yiapcspvgccdc:TouchTarget>', fileCsv, flags=0).group(0)
 #找第一个
#find_result = (re.findall(r'<yiapcspvgccdc:TouchTarget([\w\W]*?)</yiapcspvgccdc:TouchTarget>', fileCsv))
 #全部找出来

 #start_Serial = fileCsv.index('%') #字符转在文本的第几个位置
# =============================

class ALRM_NODE:
    #报警模块
    def limited_time(self):
        year_now = localtime(time()).tm_year
        month_now = localtime(time()).tm_mon
        month_range = calendar.monthrange(year_now, month_now)  # 29,30,31
        month_sec = month_range[1] * 3600 *24
        ticks = time()
        print(ticks)
        limitTime = 1600392979 + month_sec
        localtime_var = strftime("%Y/%m/%d", localtime(limitTime))
        #print(localtime)

        if ticks > limitTime:
            tkinter.messagebox.showinfo('提示', '软件过期需要重新编译'+localtime_var)
            exit()
        return localtime_var

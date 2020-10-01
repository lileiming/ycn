# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# ==========================================================
# 参考文档：https://cloud.tencent.com/developer/section/1372347
#           http://c.biancheng.net/view/2539.html

# **********************************************************
# Excel Tool Tag list  = ExcelToolTaglist
# Tag_list维护工具
# **********************************************************

import xlrd
import openpyxl
import os
import openpyxl.styles as sty
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from time import sleep
import YokoCustomlibrary   #自定义模块
from YokoCustomlibrary import time_Decorator,thread_Decorator


# 计时装饰器

class Windows_NODE(YokoCustomlibrary.FILE_NODE):
    def __init__(self, master):
        self.master = master
        self.here = os.getcwd()
        self.initWidgets()
        help_doc = 'Don\'t Repeat Youself!!\n '
        self.text_update(help_doc)
        self.func_test_init()

    def initWidgets(self):
        # 创建第一层
        top_frame = LabelFrame(self.master, height=150, width=615, text="目标文件")
        top_frame.pack(side=TOP, padx=0, pady=5)
        # 目标文件名显示框
        self.tope1 = StringVar()
        self.entry = ttk.Entry(top_frame, width=85, textvariable=self.tope1)
        self.tope1.set("目标文件")
        self.entry.pack(fill=X, expand=0, side=TOP, padx=0, pady=10)
        # 目标文件Sheet框
        self.tope2 = StringVar()
        self.comboxlist = ttk.Combobox(top_frame, width=25, textvariable=self.tope2)
        self.comboxlist.pack(side=LEFT)
        self.comboxlist.bind("<<ComboboxSelected>>", self.open_combox)
        self.tope2.set("目标sheet")
        #  目标文件PID_TAG框
        self.tope3 = StringVar()
        self.comboxlist1 = ttk.Combobox(top_frame, width=25, textvariable=self.tope3)
        self.comboxlist1.pack(side=LEFT, padx=10, pady=10)
        self.tope3.set("目标TAG")
        ## 同文件选择框
        self.intVar = BooleanVar()
        # should_auto = BooleanVar()
        self.check1 = Checkbutton(top_frame, text="同文件", variable=self.intVar, command=self.change).pack(side=LEFT)
        # self.check1.select()
        self.ckeckchange = 0
        ## 目标文件选择按钮
        ttk.Button(top_frame, text='目标文件', command=self.open_file).pack(side=RIGHT, padx=5)

        # 创建第二层
        mid_frame1 = LabelFrame(self.master, height=150, width=615, text="参考文件")
        mid_frame1.pack(side=TOP, padx=0, pady=5)
        ## 参考文件名显示框
        self.mide1 = StringVar()
        self.entry2 = ttk.Entry(mid_frame1, width=85, textvariable=self.mide1)
        self.mide1.set("参考文件")
        self.entry2.pack(fill=X, expand=0, side=TOP, padx=0, pady=10)

        self.mide2 = StringVar()
        self.comboxlist2 = ttk.Combobox(mid_frame1, width=25, textvariable=self.mide2)
        self.comboxlist2.pack(side=LEFT)
        self.comboxlist2.bind("<<ComboboxSelected>>", self.open_combox2)
        self.mide2.set("参考sheet")
        self.mide3 = StringVar()
        self.comboxlist3 = ttk.Combobox(mid_frame1, width=25, textvariable=self.mide3)
        self.comboxlist3.pack(side=LEFT, padx=10, pady=10)
        self.mide3.set("参考TAG")
        ttk.Button(mid_frame1, text='参考文件', command=self.open_file2).pack(side=RIGHT, padx=5)

        # 创建第三层
        mid_frame2 = LabelFrame(self.master, height=60, width=615, text="结果")
        mid_frame2.pack(side=TOP, padx=0, pady=5)
        self.Scroll = Scrollbar(mid_frame2)
        self.Text = Text(mid_frame2, width=83, height=20, yscrollcommand=self.Scroll.set)
        self.Text.pack(side=LEFT, padx=0, pady=5)
        self.Scroll = Scrollbar(mid_frame2)
        self.Scroll.pack(side=LEFT, fill=Y)
        self.Scroll.config(command=self.Text.yview)

        # 创建底部部
        bot_frame = Frame(self.master, height=40, width=615)
        bot_frame.pack(side=TOP, padx=0, pady=5)
        ttk.Button(bot_frame, text='校队', command=self.ExcelComp).pack(side=LEFT, padx=10)
        ttk.Button(bot_frame, text='替换', command=self.ExcelSave).pack(side=LEFT, padx=10)
        ttk.Button(bot_frame, text='查看结果', command=self.OpenExcel).pack(side=LEFT, padx=10)

    @thread_Decorator
    def change(self):
        self.entry2.delete(0, END)
        self.ckeckchange = self.intVar.get()
        if self.ckeckchange:
            self.open_file2()

    def open_file(self):
        try:
            var_file_path = filedialog.askopenfilename(title=u'选择参考文档', initialdir=self.here)
            var_sheet_name = self.get_sheet(var_file_path)
            self.sheet_name_T = tuple(var_sheet_name)
            self.comboxlist["values"] = self.sheet_name_T
            self.comboxlist.current(0)
            self.entry.delete(0, END)
            self.entry.insert('insert', var_file_path)
        except xlrd.biffh.XLRDError:
            self.text_update('错误提示：文件格式错误，现在就只能处理Excel文档\n')

    def open_combox(self, *args):
        var_file_path = self.entry.get()
        var_sheet_name = self.comboxlist.get()
        self.var_col = self.get_col(var_file_path, var_sheet_name)
        self.comboxlist1["values"] = self.var_col
        self.comboxlist1.current(0)

    def open_file2(self):
        self.Text.delete(0.0, END)
        try:
            self.entry2.delete(0, END)
            if self.ckeckchange:
                var_file_path = self.entry.get()
            else:
                var_file_path = filedialog.askopenfilename(title=u'选择数据列表', initialdir=self.here)
            self.entry2.insert('insert', var_file_path)
            var_sheet_name = self.get_sheet(var_file_path)
            self.sheet_name_R = tuple(var_sheet_name)
            self.comboxlist2["values"] = self.sheet_name_R
            self.comboxlist2.current(0)
        except xlrd.biffh.XLRDError:
            self.text_update('错误提示：文件格式错误，现在就只能处理Excel文档\n')

    def open_combox2(self,*args):
        var_file = self.entry2.get()
        var_sheet = self.comboxlist2.get()
        var_file_0 = self.entry.get()
        var_sheet_0 = self.comboxlist.get()
        self.var_col2 = self.get_col(var_file, var_sheet)
        self.comboxlist3["values"] = self.var_col2
        self.comboxlist3.current(0)

        if var_file == var_file_0 and var_sheet == var_sheet_0:
            self.text_update("不是用重复文件\n")
        else:
            self.Text.delete(0.0, END)

    @thread_Decorator
    def ExcelSave(self):  # 替换功能
        try:
            self.Text.delete(0.0, END)
            self.text_update("=============替换中===============\n")
            self.Text.update()
            T_Excle_Name = self.entry.get()
            self.TSheet = self.comboxlist.get()
            T_Sheet_Num = self.sheet_name_T.index(self.TSheet)
            # print (T_Sheet_Num)
            T_tag = self.comboxlist1.get()
            T_tag_ColNum = self.var_col.index(T_tag)
            # print (T_tag_ColNum)
            R_Excle_Name = self.entry2.get()
            R_Sheet = self.comboxlist2.get()
            R_Sheet_Num = self.sheet_name_R.index(R_Sheet)
            # print (R_Sheet_Num)
            R_tag = self.comboxlist3.get()
            R_tag_ColNum = self.var_col2.index(R_tag)
            # print (R_tag_ColNum)

            T_file_path = os.path.join(os.getcwd(), T_Excle_Name)
            T_excel_file = xlrd.open_workbook(T_file_path)
            R_file_path = os.path.join(os.getcwd(), R_Excle_Name)
            R_excel_file = xlrd.open_workbook(R_file_path)
            # print excelFile.sheet_names()
            sheet_T = T_excel_file.sheet_by_index(T_Sheet_Num)
            sheet_R = R_excel_file.sheet_by_index(R_Sheet_Num)

            # ==========================================================
            #rowsNum = sheet_T.nrows
            #colNum = sheet_T.ncols
            # print "row num:", sheet_T.nrows #行
            # print "col num:", sheet_T.ncols #列
            rowlist_list = self.rowList(sheet_T, T_tag_ColNum)
            collist_list = self.colList(sheet_T)
            dict_tag = self.dictGenerate(sheet_T, T_tag_ColNum)

            # 读取更换内容==============================================
            new_tag = self.dictGenerate(sheet_R, R_tag_ColNum)
            list_TAG = list(new_tag)
            # print list_TAG # [(u'BC', u'AB')]
            TAG_index = 0
            # openpyxl 打开Yget 清单=============================================
            data = openpyxl.load_workbook(T_Excle_Name)
            table = data.worksheets[T_Sheet_Num]

            while TAG_index < len(list_TAG):
                TAG_XY = list_TAG[TAG_index]
                # print TAG_XY
                TAG_Z = new_tag[TAG_XY]
                # print TAG_Z # 7.0
                Nokey = dict_tag.get(TAG_XY, 0)  # 处理Yget 不存在的key

                if TAG_Z != "" and Nokey != 0:
                    # print(TAG_Z)
                    TAG_Z_OUT = str(TAG_Z) + '\n'
                    # Excel坐标============================================
                    New_Tag_Row_Str = list_TAG[TAG_index][0]
                    New_Tag_col_Str = list_TAG[TAG_index][1]
                    New_Tag_Row_index = rowlist_list.index(New_Tag_Row_Str) + 1
                    NewTagCel_index = collist_list.index(New_Tag_col_Str) + 1
                    # 替换Excel数据===============================================
                    TAG_ZZ = table.cell(New_Tag_Row_index, NewTagCel_index).value
                    if TAG_Z != TAG_ZZ:
                        table.cell(New_Tag_Row_index, NewTagCel_index).value = TAG_Z
                        table.cell(New_Tag_Row_index, NewTagCel_index).fill = sty.PatternFill(fill_type='solid',
                                                                                            fgColor="00FFFF")  # 对更新数据进行标注颜色
                        self.text_update(TAG_Z_OUT)
                TAG_index = TAG_index + 1
                # Excel写入===========================================================
            data.save(T_Excle_Name)
            self.text_update("=============替换结束=============\n")
        except Exception as e:
            self.text_update(e)
        sleep(2)

    @thread_Decorator
    @time_Decorator
    def ExcelComp(self):  # 比较功能
        try:
            #self.Text.delete(0.0, END)
            self.text_update("=============校队中===============\n")
            T_Excle_Name = self.entry.get()
            self.TSheet = self.comboxlist.get()
            T_Sheet_Num = self.sheet_name_T.index(self.TSheet)
            # print (T_Sheet_Num)
            T_tag = self.comboxlist1.get()
            T_tag_ColNum = self.var_col.index(T_tag)
            # print (T_tag_ColNum)
            R_Excle_Name = self.entry2.get()
            R_Sheet = self.comboxlist2.get()
            R_Sheet_Num = self.sheet_name_R.index(R_Sheet)
            # print (R_Sheet_Num)
            R_tag = self.comboxlist3.get()
            R_tag_ColNum = self.var_col2.index(R_tag)
            # print (R_tag_ColNum)

            T_file_path = os.path.join(os.getcwd(), T_Excle_Name)
            T_excel_file = xlrd.open_workbook(T_file_path)
            R_file_path = os.path.join(os.getcwd(), R_Excle_Name)
            R_excel_file = xlrd.open_workbook(R_file_path)
            # print excelFile.sheet_names()

            sheet_T = T_excel_file.sheet_by_index(T_Sheet_Num)
            sheet_R = R_excel_file.sheet_by_index(R_Sheet_Num)

            # ==========================================================
            #rowsNum = sheet_T.nrows
            #colNum = sheet_T.ncols
            # print "row num:", sheet_T.nrows #行
            # print "col num:", sheet_T.ncols #列
            rowlist_list = self.rowList(sheet_T, T_tag_ColNum)
            collist_list = self.colList(sheet_T)
            dict_tag = self.dictGenerate(sheet_T, T_tag_ColNum)

            # 读取更换内容==============================================
            new_tag = self.dictGenerate(sheet_R, R_tag_ColNum)
            list_TAG = list(new_tag)
            # print list_TAG # [(u'BC', u'AB')]
            TAG_index = 0
            # openpyxl 打开Yget 清单=============================================
            data = openpyxl.load_workbook(T_Excle_Name)
            table = data.worksheets[T_Sheet_Num]

            while TAG_index < len(list_TAG):
                TAG_XY = list_TAG[TAG_index]
                #print (TAG_XY)
                TAG_Z = new_tag[TAG_XY]
                # print TAG_Z # 7.0
                Nokey = dict_tag.get(TAG_XY, 0)  # 处理Yget 不存在的key
                if TAG_Z != "" and Nokey != 0:

                    # Excel坐标============================================
                    New_Tag_Row_Str = list_TAG[TAG_index][0]
                    New_Tag_col_Str = list_TAG[TAG_index][1]
                    New_Tag_Row_index = rowlist_list.index(New_Tag_Row_Str) + 1
                    NewTagCel_index = collist_list.index(New_Tag_col_Str) + 1
                    # 替换Excel数据===============================================
                    TAG_ZZ = table.cell(New_Tag_Row_index, NewTagCel_index).value
                    # table.cell(New_Tag_Row_index,NewTagCel_index).value = TAG_Z
                    if TAG_Z != TAG_ZZ:
                        # print (TAG_Z)
                        TAG_Z_OUT = str(TAG_Z) + '\n'
                        self.Text.insert('insert', TAG_Z_OUT)
                        self.Text.update()
                        self.Text.see(END)
                        table.cell(New_Tag_Row_index, NewTagCel_index).fill = sty.PatternFill(fill_type='solid',
                                                                                            fgColor="FF00FF")  # 对更新数据进行标注颜色
                TAG_index = TAG_index + 1
                # Excel写入===========================================================
            data.save(T_Excle_Name)
            self.text_update("=============校队结束=============\n")
        except Exception as e:
            self.text_update(e)
        sleep(2)

    def get_col(self, file_name, sheet_name):
        dir_case = file_name
        data = xlrd.open_workbook(dir_case)
        sheet = data.sheet_by_name(sheet_name)
        col_name = self.colList(sheet)
        return col_name

    def OpenExcel(self):
        try:
            os.startfile(self.entry.get())
        except FileNotFoundError:
            self.text_update('错误提示：文件不存在')
            pass

    def text_update(self,show):
        if show == 'START_':
            self.Text.insert(END, "=============程序开始=============\n")
        elif show == 'STOP_':
            self.Text.insert(END, "=============程序结束=============\n")
        else:
            self.Text.insert(END,show)
            pass
        self.Text.update()
        self.Text.see(END)
        #self.text_update('STOP_')
        pass

    def func_test_init(self):
        """
        功能块说明：快速测试初始化
        """
        self.here = f'C:/Users/Administrator/Documents/python/0.输出文件/TaglistTool'


if __name__ == "__main__":
    root = Tk()
    root.geometry('640x600+100+200')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoCustomlibrary.ALRM_NODE.limited_time(root)
    root.title("Tag_list维护工具  Ver1.0" + "    到期日:" + limit_time)
    root.mainloop()
    pass

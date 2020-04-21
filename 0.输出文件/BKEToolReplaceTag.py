# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# **********************************************************
# BK ENG Tool Replace Tag = BKEToolReplaceTag
# **********************************************************

from tkinter import *
# 导入ttk
from tkinter import ttk
from tkinter import filedialog
import os
import xlrd
import sys
from time import sleep,time,strftime,localtime
import YokoCustomlibrary   #自定义模块
from YokoCustomlibrary import time_Decorator,thread_Decorator  #Custom module


def func_find_position(csv_file_read, find_str):
    try:
        position = csv_file_read.index(find_str)
    except ValueError:
        position = -1
    return  position

class Windows_NODE(YokoCustomlibrary.FILE_NODE):
    def __init__(self, master):
        self.master = master
        self.here = os.getcwd()
        self.initWidgets()
        help_doc = '本程序为快速替换组态工具。 \n\n ' \
                   '使用方法：\n' \
                   '1.通过按钮选择数据列表文件，使用下拉菜单选择相对应的表格（sheet）\n' \
                   '2.通过按钮选择目标文件文件夹.\n' \
                   '3.点击[替换 CSV 文件]按钮执行替换 CSV 文件、\n' \
                   '4.点击[替换 TxT 文件]按钮执行替换 TXT 文件、\n'
        self.Text.insert(END, help_doc)
        self.func_test_init() #测试模块
        
    def initWidgets(self):
        """
        功能块说明：GUI界面
        """
        # top_frame ===================================
        top_frame = LabelFrame(self.master,text='数据列表')
        top_frame.pack(fill=X,padx=15,pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(top_frame,width=45,textvariable = self.e2)
        self.e2.set("replaceExc.xlsx")
        self.entry2.pack(fill=X,expand=YES,side=LEFT,pady=10)
        self.e3 = StringVar()
        self.comboxlist = ttk.Combobox(top_frame,width=18,textvariable = self.e3)
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
        ttk.Button(bot_frame, text='选择目标文件夹', command=self.open_dir).pack(side=LEFT, padx=10, pady=10)
        ttk.Button(bot_frame, text='替换 CSV 文件', command=self.func_csv_process).pack(side=RIGHT, padx=10)
        ttk.Button(bot_frame, text='替换 Txt 文件', command=self.func_txt_process).pack(side=RIGHT, padx=10)
        ttk.Button(bot_frame, text='分析TAG', command=self.func_findEtag_process).pack(side=RIGHT, padx=10)

    def open_dir(self):
        """
        功能块说明：选择文件夹
        """
        self.Text.delete(0.0,END)
        self.path0 = filedialog.askdirectory(title=u'选择文件夹', initialdir=self.here)
        self.path1 = self.path0+'/'
        self.func_text_insert_show('path1')

    def open_file2(self):
        """
        功能块说明：选择数据列表
        """
        self.entry2.delete(0,END)
        var_file_name = filedialog.askopenfilename(title=u'选择数据列表', initialdir=self.here)
        self.entry2.insert('insert', var_file_name)
        self.comboxlist["values"] = tuple(self.get_sheet(var_file_name))
        self.comboxlist.current(0)

    @thread_Decorator
    @time_Decorator
    def func_findEtag_process(self):
        # 正则表达式例子
        # find_target_A = r'[0-9%]{2,4}[A-Z]+[0-9]{1,2}' # 6200TICAS11 /6200TI11
        # find_target_A = r'[0-9%]{2,4}[A-Z]+[0-9]{1,3}' # 6200TICAS111 /6200TI111
        # find_target_B = r'[0-9A-Z%]+(?=-|_)'  # %%ITICAS11  FCS0115(FCS0115-)
        # find_target_A = r'Z'
        #
        #
        """
        功能块说明：分析按钮的处理流程
        """
        #Latest results
        self.list_latest_result = []  #最新结果
        line_content = ''
        self.func_text_insert_show('findEtag')
        self.var_flag = 2
        self.func_eachFile_method()
        var_result_ETAG = (re.findall(r'(?<=ETAG:1:).*(?=;)', self.var_txt_detail))
        var_result_RTAG = (re.findall(r'(?<=RTAG:1:).*(?=;)', self.var_txt_detail))
        var_result = var_result_ETAG + var_result_RTAG
        var_target_A = r'[0-9%]{2,4}[A-Z]+[0-9]{1,2}'
        var_result = self.func_loop_part_method(var_result, var_target_A)
        var_target_B = r'[0-9A-Z%]+(?=-|_)'
        var_result = self.func_loop_part_method(var_result, var_target_B)

        self.Text.insert(END, f'未被分类：{var_result}\n')
        self.list_latest_result.extend(var_result)
        self.list_latest_result = list(set(self.list_latest_result))  # 去重
        for _ in self.list_latest_result:
            line_content = f'{line_content}\n{_}'
            pass
        var_filepath, var_fullflname = os.path.split(self.entry2.get())
        self.out_txt(f'{var_filepath}\分析结果.txt',line_content)
        self.var_flag = 0
        self.func_text_insert_show('completed')
        sleep(1)
        pass

    def func_loop_part_method(self,result,target):
        """
        功能块说明：循环查找
        """
        var_result_copy = result.copy()
        for var_initial in var_result_copy:
            var_i = re.findall(target, var_initial)
            if len(var_i):
                result.pop(result.index(var_initial))
                self.list_latest_result.append(var_i[0])
        return result

    @thread_Decorator
    @time_Decorator
    def func_csv_process(self):
        """
        功能块说明：csv按钮的处理流程
        """
        self.func_text_insert_show('csv')
        self.var_flag = 1
        self.func_reName2txt_method()
        self.func_readExcel_method()
        self.func_eachFile_method()
        self.var_flag = 0
        self.func_text_insert_show('completed')
        sleep(1)

    @thread_Decorator
    @time_Decorator
    def func_txt_process(self):
        """
        功能块说明：txt按钮的处理流程
        """
        self.func_text_insert_show('txt')
        self.var_flag = 0
        self.func_readExcel_method()
        self.func_eachFile_method()
        self.var_flag = 0
        self.func_text_insert_show('completed')
        sleep(1)

    def func_reName2txt_method(self):
        """
        功能块说明：csv文件转换为txt文件
        """
        #sys.path.append(self.path1)
        path_dir = os.listdir(self.path1)
        for csv_file_name in path_dir:
            portion = os.path.splitext(csv_file_name)
            if portion[1] == '.csv':
                old_full_name = f'{self.path1}{csv_file_name}'
                new_full_name = f'{self.path1}{portion[0]}.txt'
                try:
                    os.rename(old_full_name,new_full_name)
                except FileExistsError as e:
                    self.Text.insert(END, f'{e}\n')
            else:
                self.func_text_insert_show('error')
        
    def func_readExcel_method(self):
        """
        功能块说明：读取数据列表
        """
        file_name = self.entry2.get()
        sheet_name = self.comboxlist.get()
        self.list_inValue = []
        self.list_outValue = []
        var_count = 1
        file_path = os.path.join(os.getcwd(), file_name)
        sheet_content = xlrd.open_workbook(file_path).sheet_by_name(sheet_name)
        self.var_rows_num = sheet_content.nrows
        while var_count < self.var_rows_num:
           var_count = var_count + 1
           self.list_inValue.append(sheet_content.cell_value(var_count-1,0))
           self.list_outValue.append(sheet_content.cell_value(var_count-1,1))
        
    def func_eachFile_method(self):
        """
        功能块说明：读取文件夹内所有文件，按照flag 选择处理模式。
        """
        self.var_txt_detail = ''
        path_dir = os.listdir(self.path1)
        for file_name in path_dir:
            self.var_child = self.path1 + file_name
            if self.var_flag == 1:
                self.func_readfile_method()
            elif self.var_flag == 2:
                file = open(self.var_child, 'r+')
                try:
                    self.var_txt_detail = self.var_txt_detail + file.read()
                except UnicodeDecodeError:
                    file = open(self.var_child, 'r+', encoding='utf-8')
                    self.var_txt_detail = self.var_txt_detail + file.read()
            else:
                self.func_read_txt_file_method()

    def func_readfile_method(self):
        """
        功能块说明：读取文件夹内csv文档，可以分辨IOM/SW/AN等文件，替换所需内容，并按照一定规范输出相应文件名字。
        """

        open_csv_file = open(self.var_child,'r+')
        csv_detail = open_csv_file.read()
        open_csv_file.seek(0,0)
        line_content = csv_detail.replace (self.list_inValue[0],self.list_outValue[0])
        for _ in range(self.var_rows_num-1):
            line_content = line_content.replace(self.list_inValue[_], self.list_outValue[_])
        open_csv_file.write(line_content)
        open_csv_file.close()
    # ======================================================
        var_filepath, var_fullflname = os.path.split(self.var_child)
        start_Serial = func_find_position(csv_detail, '%')
        if start_Serial > 0:
            mark_Node_Solt = csv_detail[start_Serial:start_Serial + 5]
            mark_IOM = mark_Node_Solt[1]
            if mark_IOM == 'Z':
                nodeX = mark_Node_Solt[2]
                nodeY = mark_Node_Solt[3]
                soltX = mark_Node_Solt[4]
                if 'Unit' in csv_detail:
                    type_IOM  ="-Analog"
                elif 'Btn1' in csv_detail:
                    type_IOM = "-Status"
                else:
                    type_IOM = "-Other"
                pass
                var_new_name = f'{self.path1}N{nodeX}{nodeY}S{soltX}{type_IOM}.csv'
                var_show_name = f'N{nodeX}{nodeY}S{soltX}.csv'
            elif mark_IOM == 'S':
                SWX = mark_Node_Solt[3]
                var_new_name = f'{self.path1}SwitchDef{SWX}.csv'
                var_show_name = f'SwitchDef{SWX}.csv'
            elif mark_IOM == 'A':
                ANX = mark_Node_Solt[2]
                var_new_name = f'{self.path1}AN{ANX}.csv'
                var_show_name = f'AN{ANX}.csv'
            else:
                if mark_IOM  not in var_fullflname:
                    var_new_name = f'{self.path1}{mark_IOM}{os.path.splitext(var_fullflname)[0]}.csv'
                    var_show_name = f'{mark_IOM}{os.path.splitext(var_fullflname)[0]}.csv'
                else:
                    var_new_name = f'{self.path1}{os.path.splitext(var_fullflname)[0]}.csv'
                    var_show_name = f'{os.path.splitext(var_fullflname)[0]}.csv'
        else:
            sheet_position = func_find_position(csv_detail, '@SHEET')
            if sheet_position > 0:
                var_mark = csv_detail[sheet_position + 9 : sheet_position + 12]
                if var_mark not in var_fullflname:
                    var_new_name = f'{self.path1}{var_mark}-{os.path.splitext(var_fullflname)[0]}.csv'
                    var_show_name = f'{var_mark}-{os.path.splitext(var_fullflname)[0]}.csv'
                else:
                    var_new_name = f'{self.path1}{os.path.splitext(var_fullflname)[0]}.csv'
                    var_show_name = f'{os.path.splitext(var_fullflname)[0]}.csv'
            else:
                var_new_name = f'{self.path1}{os.path.splitext(var_fullflname)[0]}.csv'
                var_show_name = f'{os.path.splitext(var_fullflname)[0]}.csv'
    # ======================================================
        try:
            os.renames(self.var_child, var_new_name)
            self.Text.insert(END, f'INFO: {var_show_name} 转换完成...\n')
        except WindowsError:
            self.Text.insert(END, f'ERROR: {var_show_name} 重名跳过\n')
        self.Text.update()

    def func_read_txt_file_method(self):
        """
        功能块说明：读取文件夹内txt或 xaml文档，替换所需内容，并按照一定规范输出相应文件名字。
        """
        short_name = os.path.basename(self.var_child)
        self.var_flag = 0
        open_txt_file = open(self.var_child,'r+')
        try:
            txt_detail = open_txt_file.read()
        except UnicodeDecodeError:
                self.Text.insert(END, f'WARNING: {short_name} is UTF-8 format.\n')
                self.Text.update()
                open_txt_file = open(self.var_child,'r+',encoding='utf-8')
                txt_detail = open_txt_file.read()
        var_DR_exists = txt_detail.find('DR0') # exists 存在
        var_xaml_exists = txt_detail.find('<Canvas')
    #======================================================
        open_txt_file.seek(0,0)
        line_content = txt_detail.replace (self.list_inValue[0],self.list_outValue[0])
        for _ in range(self.var_rows_num-1):
            line_content = line_content.replace(self.list_inValue[_], self.list_outValue[_])
        open_txt_file.write(line_content)
        open_txt_file.close()
    #======================================================
        if var_DR_exists > 0 :
            var_DR0XX = txt_detail[var_DR_exists+3]
            var_DR0X0Y = txt_detail[var_DR_exists+4]
            var_DR0X00Z = txt_detail[var_DR_exists+5]
            var_new_name = f'{self.path1}DR0{var_DR0XX+var_DR0X0Y+var_DR0X00Z}.txt'
            #var_show_name = f'DR0{var_DR0XX+var_DR0X0Y+var_DR0X00Z}.txt'
            try:
               os.renames(self.var_child,var_new_name)
               self.Text.insert(END, f'INFO: {short_name} 转换完成...\n')
            except WindowsError:
               self.Text.insert(END, f'ERROR: {short_name} 重名跳过\n')
        else:
            self.Text.insert(END, f'WARNING: {short_name} does not conform to the DR format.\n')
    # ======================================================
        if var_xaml_exists > 0 :
            if 'OUT' not in short_name:
                var_new_name = f'{self.path1}OUT-{short_name}'
            else:
                var_new_name = f'{self.path1}{short_name}'
            os.renames(self.var_child,var_new_name)
            self.Text.insert(END, f'INFO: {short_name} 转换完成...\n')
        self.Text.update()

    def func_text_insert_show(self,flag):
        """
        GUI 信息 输出
        """
        dict_show = {'path1':f'文件路径：\n{self.path1}\n',
                     'csv':'INFO: Start converting csv file.\n',
                     'completed':f'Generation completed.  {strftime("%Y-%m-%d %H:%M:%S", localtime())}\n\n',
                     'txt':'INFO: Start converting txt file.\n',
                     'error':'ERROR：The file format is incorrect.\n',
                     'findEtag':'INFO: Start analyze txt file.\n'}

        self.Text.insert(END, dict_show[flag])
        self.Text.update()
        self.Text.see(END)
        pass

    def func_test_init(self):
        """
        功能块说明：快速测试初始化
        """
        self.e2.set(r'C:\Users\Administrator\Documents\python\0.输出文件\ReplaceTag\replaceExc.xlsx')
        self.e3.set('不替换')
        self.here = 'C:/Users/Administrator/Documents/python/0.输出文件/ReplaceTag/IN'

if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400')  # Window size
    Windows_NODE(root)
    var_limit_time = YokoCustomlibrary.ALRM_NODE.limited_time(root)
    root.title(f'Tag replacement tool    到期日:{var_limit_time}')
    root.mainloop()

# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
#==========================================================
# lileiming@me.com
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


def findposition(csv_file_read, find_str):
    try:
        position = csv_file_read.index(find_str)
    except ValueError:
        position = -1
    return  position

class Windows_NODE(YokoRead.FILE_NODE):
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
        ttk.Button(bot_frame, text='替换 CSV 文件', command=self.Csv).pack(side=RIGHT, padx=10)
        ttk.Button(bot_frame, text='替换 Txt 文件', command=self.Txt).pack(side=RIGHT, padx=10)
        ttk.Button(bot_frame, text='分析TAG', command=self.findEtag).pack(side=RIGHT, padx=10)

    def open_dir(self):
        self.Text.delete(0.0,END)
        dir_path = filedialog.askdirectory(title=u'选择文件夹', initialdir=self.here)
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
    # find_target_A = r'[0-9%]{2,4}[A-Z]+[0-9]{1,2}' # 6200TICAS11 /6200TI11
    # find_target_A = r'[0-9%]{2,4}[A-Z]+[0-9]{1,3}' # 6200TICAS111 /6200TI111
    # find_target_B = r'[0-9A-Z%]+(?=-|_)'  # %%ITICAS11  FCS0115(FCS0115-)
    # find_target_A = r'Z'
    #
    #
    def findEtag(self):
        self.find_result_last = []
        line = ''
        self.text_insert('findEtag')
        self.flag = 2
        self.eachFile()
        find_result_ETAG = (re.findall(r'(?<=ETAG:1:).*(?=;)', self.text_detail))
        find_result_RTAG = (re.findall(r'(?<=RTAG:1:).*(?=;)', self.text_detail))
        find_result = find_result_ETAG + find_result_RTAG
        find_target_A = r'[0-9%]{2,4}[A-Z]+[0-9]{1,2}'
        find_result = self.loop_part_func(find_result, find_target_A)
        find_target_B = r'[0-9A-Z%]+(?=-|_)'
        find_result = self.loop_part_func(find_result, find_target_B)

        self.Text.insert('insert', f'未知：{find_result}\n')
        self.find_result_last.extend(find_result)
        self.find_result_last = list(set(self.find_result_last))  # 去重
        for _ in self.find_result_last:
            line = f'{line}\n{_}'
            pass
        filepath, fullflname = os.path.split(self.entry2.get())
        self.out_txt(f'{filepath}\分析结果.txt',line)
        self.flag = 0
        self.text_insert('completed')
        sleep(1)
        pass

    def loop_part_func(self,result,target):
        find_result_copy = result.copy()
        for initial in find_result_copy:
            i = re.findall(target, initial)
            if len(i):
                result.pop(result.index(initial))
                self.find_result_last.append(i[0])
        return result

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
            if portion[1] == '.csv':
                new_name = f'{portion[0]}.txt'
                self.filenamedir = self.path1 + csvFilename
                new_name_dir = self.path1 + new_name
                try:
                    os.rename(self.filenamedir,new_name_dir)
                except FileExistsError as e:
                    self.Text.insert('insert', f'{e}\n')
            else:
                self.text_insert('error')
        
    def readExcel(self):
        file_name = self.entry2.get()
        sheet_name = self.comboxlist.get()
        self.inValue = []
        self.outValue = []
        count = 1
        filePath = os.path.join(os.getcwd(), file_name)
        x1 = xlrd.open_workbook(filePath)
        sheet1 = x1.sheet_by_name(sheet_name)
        self.rowsNum = sheet1.nrows
        while count < self.rowsNum:
           count = count + 1
           in1 = sheet1.cell_value(count-1,0)
           self.inValue.append(in1)
           out1 = sheet1.cell_value(count-1,1)
           self.outValue.append(out1)
        
    def eachFile(self):
        self.text_detail = ''
        pathDir = os.listdir(self.path1)
        for allDir in pathDir:
            self.child = self.path1 + allDir
            if self.flag == 1:
                self.readfile()
            elif self.flag == 2:
                file = open(self.child, 'r+')
                try:
                    self.text_detail = self.text_detail + file.read()
                except UnicodeDecodeError:
                    file = open(self.child, 'r+', encoding='utf-8')
                    self.text_detail = self.text_detail + file.read()
            else:
                self.read_txt_file()

    def readfile(self):
        file = open(self.child,'r+')
        fileCsv = file.read()
        file.seek(0,0)
        line = fileCsv.replace (self.inValue[0],self.outValue[0])
        for _ in range(self.rowsNum-1):
            line = line.replace(self.inValue[_], self.outValue[_])
        file.write(line)
        file.close()
    # ======================================================
        filepath, fullflname = os.path.split(self.child)
        start_Serial = findposition(fileCsv, '%')
        if start_Serial > 0:
            Node_Solt = fileCsv[start_Serial:start_Serial + 5]
            IOM = Node_Solt[1]
            if IOM == 'Z':
                nodeX = Node_Solt[2]
                nodeY = Node_Solt[3]
                soltX = Node_Solt[4]
                if 'Unit' in fileCsv:
                    type_IOM  ="-Analog"
                elif 'Btn1' in fileCsv:
                    type_IOM = "-Status"
                else:
                    type_IOM = "-Other"
                pass
                flienameNS = f'{self.path1}N{nodeX}{nodeY}S{soltX}{type_IOM}.csv'
                repeatName = f'N{nodeX}{nodeY}S{soltX}.csv'
            elif IOM == 'S':
                SWX = Node_Solt[3]
                flienameNS = f'{self.path1}SwitchDef{SWX}.csv'
                repeatName = f'SwitchDef{SWX}.csv'
            elif IOM == 'A':
                ANX = Node_Solt[2]
                flienameNS = f'{self.path1}AN{ANX}.csv'
                repeatName = f'AN{ANX}.csv'
            else:
                if IOM  not in fullflname:
                    flienameNS = f'{self.path1}{IOM}{os.path.splitext(fullflname)[0]}.csv'
                    repeatName = f'{IOM}{os.path.splitext(fullflname)[0]}.csv'
                else:
                    flienameNS = f'{self.path1}{os.path.splitext(fullflname)[0]}.csv'
                    repeatName = f'{os.path.splitext(fullflname)[0]}.csv'
        else:
            sheet_position = findposition(fileCsv, '@SHEET')
            if sheet_position > 0:
                sheet3 = fileCsv[sheet_position + 9 : sheet_position + 12]
                if sheet3 not in fullflname:
                    flienameNS = f'{self.path1}{sheet3}-{os.path.splitext(fullflname)[0]}.csv'
                    repeatName = f'{sheet3}-{os.path.splitext(fullflname)[0]}.csv'
                else:
                    flienameNS = f'{self.path1}{os.path.splitext(fullflname)[0]}.csv'
                    repeatName = f'{os.path.splitext(fullflname)[0]}.csv'
            else:
                flienameNS = f'{self.path1}{os.path.splitext(fullflname)[0]}.csv'
                repeatName = f'{os.path.splitext(fullflname)[0]}.csv'
    # ======================================================
        try:
            os.renames(self.child, flienameNS)
            self.Text.insert('insert', f'INFO: {repeatName} 转换完成...\n')
        except WindowsError:
            self.Text.insert('insert', f'ERROR: {repeatName} 重名跳过\n')
        self.Text.update()

    def read_txt_file(self):
        self.ShortName = os.path.basename(self.child)
        self.flag = 0
        file = open(self.child,'r+')
        try:
            file_txt = file.read()
        except UnicodeDecodeError:
                self.Text.insert('insert', f'WARNING: {self.ShortName} is UTF-8 format.\n')
                self.Text.update()
                file = open(self.child,'r+',encoding='utf-8')
                file_txt = file.read()
        DRfindNum = file_txt.find('DR0')
        xaml_name = file_txt.find('<Canvas')
    #======================================================
        file.seek(0,0)
        line = file_txt.replace (self.inValue[0],self.outValue[0])
        for _ in range(self.rowsNum-1):
            line = line.replace(self.inValue[_], self.outValue[_])
        file.write(line)
        file.close()
    #======================================================
        if DRfindNum > 0 :
            DR0X = file_txt[DRfindNum+3]
            DR00Y = file_txt[DRfindNum+4]
            DR000Z = file_txt[DRfindNum+5]
            flienameNS = f'{self.path1}DR0{DR0X+DR00Y+DR000Z}.txt'
            #repeatName = f'DR0{DR0X+DR00Y+DR000Z}.txt'
            try:
               os.renames(self.child,flienameNS)
               self.Text.insert('insert', f'INFO: {self.ShortName} 转换完成...\n')
            except WindowsError:
               self.Text.insert('insert', f'ERROR: {self.ShortName} 重名跳过\n')
        else:
            self.Text.insert('insert', f'WARNING: {self.ShortName} does not conform to the DR format.\n')
    # ======================================================
        if xaml_name > 0 :
            if 'OUT' not in self.ShortName:
                flienameNS = f'{self.path1}OUT-{self.ShortName}'
            else:
                flienameNS = f'{self.path1}{self.ShortName}'
            os.renames(self.child,flienameNS)
            self.Text.insert('insert', f'INFO: {self.ShortName} 转换完成...\n')
        self.Text.update()

    def text_insert(self,flag):
        if flag == 'path1':
            self.Text.insert('insert', f'文件路径：\n{self.path1}\n')
            pass
        if flag == 'csv':
            self.Text.insert('insert', 'INFO: ****开始转换CSV****\n')
            pass
        if flag == 'completed':
            self.Text.insert('insert', 'INFO: ****所有转换完成。****\n\n')
            self.Text.see(END)
            pass
        if flag == 'txt':
            self.Text.insert('insert', 'INFO: ****开始转换txt文件。****\n')
            pass
        if flag == 'error':
            self.Text.insert('insert', 'ERROR：文件格式错误。\n')
            pass
        if flag == 'findEtag':
            self.Text.insert('insert', 'INFO: ****开始分析TAG****\n')
            pass

        self.Text.update()
        pass

if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400')  # Window size
    Windows_NODE(root)
    limit_time = YokoRead.ALRM_NODE.limited_time(root)
    root.title("Tag replacement tool"+"    到期日:"+limit_time)
    root.mainloop()

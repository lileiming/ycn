# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================
# Rev01
# 基本实现 量程和单位的替换
# Rev02
# 使用自定义模块
#==========================================================
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import re
import YokoRead   #自定义模块

class PROCESS_NODE(YokoRead._FILE_NODE_):
    # 处理模块
    def __init1__(self,excel_fn,sheet_n,path):
        self.excel_file_name = excel_fn
        self.sheet_name = sheet_n
        self.path0 = path
        self.recording = []

    def find_keyword(self,txt_file):
        #寻找关键字
        self.txt_file = txt_file
        self.file_detail = self.read_txt(self.txt_file)
        #print(file_detail)
        self.find_result = (re.findall(r':FNRM([\w\W]*?)::FNRM', self.file_detail))

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
        #量程单位处理子程序
        # Condition 1:
        #range_key = 'ESCL:1:100.0:0.0;'
        # Condition 2:
        #unit_key = 'EUNT:1:%;'
        for _ in self.find_result:
            #print(_)
            tag = self.tag_key +';'
            if tag in _:                #有TAG再处理
                #print(self.tag_key)
        # Condition 1:
                if re.search(r'ESCL:([\w\W]*?);', _, flags=0) != None:
                    range_key = re.search(r'ESCL:([\w\W]*?);', _, flags=0).group(0)
                    range_new_key = 'ESCL:1:' + str(upper) + ':' + str(lower) + ';'
                    print(range_key,range_new_key)
                    self.good_result = str(_).replace(range_key, range_new_key, 1)
        # Condition 2:
                if re.search(r'EUNT:([\w\W]*?);', _, flags=0) != None:
                    unit_key = re.search(r'EUNT:([\w\W]*?);', _, flags=0).group(0)
                    unit_new_key = 'EUNT:1:' + str(unit) + ';'
                    self.good_result = (self.good_result).replace(unit_key,unit_new_key,1)
        #替换完结果：
                #print(self.good_result)
                if re.search(r'ESCL:([\w\W]*?);', _, flags=0) != None:
                    self.file_detail = self.file_detail.replace(_,self.good_result,1)
                    self.recording.append(self.txt_file_name)  #记录处理过的文件
        self.out_txt(self.outtxt,self.file_detail)

    def process_out(self):
        txt_in_files = os.listdir(self.path0)
        for _txt in txt_in_files:
            self.txt_file_name = self.path0 + '/' +_txt
            self.outtxt =  self.path0 + '/' + 'OUT-' +_txt
            if self.txt_file_name.find('OUT')<0:
            #屏蔽掉之前输出的结果
                self.find_keyword(self.txt_file_name)
                self.process_key()

class Windows_NODE(PROCESS_NODE):
    def __init__(self, master):
        self.master = master
        self.initWidgets()
        help_doc = '本程序为量程替换工具 \n 使用方法：\n1.通过按钮选择需要替换的DR文件目录，默认为IN目录。\n2.通过按钮选择数据列表文件，使用下拉菜单选择相对应的表格（sheet）.\n\
3.点击按钮开始执行量程替换'
        self.Text.insert('insert',help_doc)

    def initWidgets(self):
        # 创建顶部
        top_frame = LabelFrame(self.master, text='DR文件目录', height=150, width=615)
        top_frame.pack(fill=X, padx=15, pady=0)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame, width=65, textvariable=self.e1)
        self.e1.set('IN')
        self.entry.pack(fill=X, expand=YES, side=LEFT, pady=10)
        ttk.Button(top_frame, text='DR文件目录', command=self.open_dir).pack(side=LEFT)

        # 创建中部
        mid_frame = LabelFrame(self.master, text='数据列表')
        mid_frame.pack(fill=X, padx=15, pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(mid_frame, width=45, textvariable=self.e2)
        self.e2.set('TagRange_list.xls')
        self.entry2.pack(fill=X, expand=YES, side=LEFT, pady=10)
        self.e3 = StringVar()
        self.comboxlist = ttk.Combobox(mid_frame, width=15, textvariable=self.e3)
        self.comboxlist.pack(side=LEFT)
        self.e3.set('Range')
        ttk.Button(mid_frame, text='数据列表', command=self.open_file2).pack(side=LEFT)

        # 创建中下
        bot_frame1 = LabelFrame(self.master, text='结果')
        bot_frame1.pack(fill=X, side=TOP, padx=15, pady=0)
        self.Scroll = Scrollbar(bot_frame1)
        self.Text = Text(bot_frame1, width=83, height=13, yscrollcommand=self.Scroll.set)
        self.Text.pack(side=LEFT, padx=0, pady=5)
        self.Scroll = Scrollbar(bot_frame1)
        self.Scroll.pack(side=LEFT, fill=Y)
        self.Scroll.config(command=self.Text.yview)

        # 创建底部
        bot_frame = LabelFrame(self.master)
        bot_frame.pack(fill=X, side=TOP, padx=15, pady=8)
        self.e = StringVar()
        ttk.Label(bot_frame, width=60, textvariable=self.e).pack(side=LEFT, fill=BOTH, expand=YES, pady=10)
        self.e.set('组态工具集')
        ttk.Button(bot_frame, text='量程替换', command=self.command).pack(side=RIGHT)

    def open_dir(self):
        self.entry.delete(0,END)
        dir_path = filedialog.askdirectory(title=u'选择DR文件夹')
        path0 = dir_path
        path1 = path0+'/'
        self.entry.insert('insert', path1)

    def open_file2(self):
        self.entry2.delete(0,END)
        file_path = filedialog.askopenfilename(title=u'选择数据列表', initialdir=(os.path.expanduser('H:/')))
        file_text = file_path
        self.entry2.insert('insert', file_text)
        sheetName = self.get_sheet(file_text)
        sheetNameT = tuple(sheetName)
        self.comboxlist["values"] = sheetNameT
        self.comboxlist.current(0)

    def print_record(self):
        #打印替换的文件
        record = set(self.recording)
        self.Text.delete(0.0,END)
        for _ in record:
            #print(_)
            if re.search(r'DR([\w\W]*?)txt', _, flags=0) != None:
                shortname = re.search(r'DR([\w\W]*?)txt', _, flags=0).group(0)
                #print(shortname)
                self.Text.insert('insert','INFO: '+ shortname + " 转换结束\n")

    def command(self):
        path = self.entry.get()
        excelname = self.entry2.get()
        listSheet = self.comboxlist.get()
        self.__init1__(excelname,listSheet,path)
        self.process_out()
        self.print_record()

def foo(lower_input,upper_input):
        #input = 0.0
        output = []
        upper_input1 = float(upper_input)
        lower_input1 = float(lower_input)

        if upper_input1 < 10 :
            output.append( "{:.3f}".format(lower_input1))
            output.append( "{:.3f}".format(upper_input1))
        if 10 <= upper_input1 < 100 :
            output.append( "{:.2f}".format(lower_input1))
            output.append( "{:.2f}".format(upper_input1))
        if 100 <= upper_input1:
            output.append( "{:.1f}".format(lower_input1))
            output.append( "{:.1f}".format(upper_input1))
        return output


if __name__ == "__main__":
 
        root = Tk()
        root.title("量程替换工具 V1.00")
        root.geometry('640x400')  # 窗口尺寸
        Windows_NODE(root)
        YokoRead._ALRM_NODE_.limited_time(root)
        root.mainloop()

# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
#==========================================================
# Rev01
# 读取模板

# ReV02
# 操作界面

# ReV02.1
# 增加 PVI　与 SI-1ALM 功能块
#==========================================================

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import re
import math
import YokoRead   #自定义模块
from time import sleep
from YokoRead import time_Decorator,thread_Decorator

class Windows_NODE(YokoRead._FILE_NODE_):
    def __init__(self, master):
        self.master = master
        self.here = os.getcwd()
        self.initWidgets()
        help_doc = '本程序为快速复制组态工具。 \n ' \
                   '使用方法：\n' \
                   '1.通过参考文档按钮选择需要复制的DR文件，默认为DR_template.txt。\n' \
                   '2.通过按钮选择数据列表文件，使用下拉菜单选择相对应的表格（sheet）.\n' \
                   '3.点击开始按钮执行程序复制.\n'
        self.text_update(help_doc)
        pass

    def initWidgets(self):
        # 创建顶部
        top_frame = LabelFrame(self.master,text='参考文档',height = 150,width = 615)
        top_frame.pack(fill=X,padx=15,pady=0)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame,width=65,textvariable = self.e1)
        self.e1.set("DR_template.txt")
        self.entry.pack(fill=X,expand=YES,side=LEFT,pady=10)
        ttk.Button(top_frame,text='参考文档',command=self.open_file).pack(side=LEFT)

        # 创建中部
        mid_frame = LabelFrame(self.master,text='数据列表')
        mid_frame.pack(fill=X,padx=15,pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(mid_frame,width=45,textvariable = self.e2)
        self.e2.set("modbus.xls")
        self.entry2.pack(fill=X,expand=YES,side=LEFT,pady=10)
        self.e3 = StringVar()
        self.comboxlist=ttk.Combobox(mid_frame,width=15,textvariable = self.e3)
        self.comboxlist.pack(side=LEFT)
        self.e3.set("DATE")
        ttk.Button(mid_frame, text='数据列表', command=self.open_file2).pack(side=LEFT)

        # 创建中下
        bot_frame1 = LabelFrame(self.master,text='结果')
        bot_frame1.pack(fill=X,side=TOP,padx=15,pady=0)
        self.Scroll = Scrollbar(bot_frame1)
        self.Text = Text(bot_frame1 ,width=83,height=13,yscrollcommand = self.Scroll.set)
        self.Text.pack(side=LEFT,padx=0,pady=5)
        self.Scroll = Scrollbar(bot_frame1 )
        self.Scroll.pack(side = LEFT, fill = Y)
        self.Scroll.config(command = self.Text.yview)

        # 创建底部
        bot_frame = LabelFrame(self.master)
        bot_frame.pack(fill=X,side=TOP,padx=15,pady=8)
        self.e = StringVar()
        self.e.set('懒惰、不耐烦、傲慢')
        ttk.Label(bot_frame,width = 60,textvariable = self.e).pack(side=LEFT, fill=BOTH, expand=YES,pady=10)
        ttk.Button(bot_frame, text='开始', command=self.get_entry).pack(side=RIGHT, padx=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(title=u'选择参考文档', initialdir=self.here)
        file_text = file_path
        self.entry.delete(0, END)
        self.entry.insert('insert', file_text)

    def open_file2(self):
        file_path = filedialog.askopenfilename(title=u'选择数据列表', initialdir=self.here)
        file_text = file_path
        self.entry2.delete(0, END)
        self.entry2.insert('insert', file_text)
        sheetName = self.get_sheet(file_text)
        sheetNameT = tuple(sheetName)
        self.comboxlist["values"] = sheetNameT
        self.comboxlist.current(0)

    @thread_Decorator
    @time_Decorator
    def get_entry(self):
        try:
            samplePVI = self.entry.get()
            modbusList = self.entry2.get()
            listSheet = self.comboxlist.get()
            filepath, fullflname = os.path.split(modbusList)

            # 数据读取
            with open(samplePVI,'r') as samplefile:
                sample_content = samplefile.read()
            # 数据剥离
            sample_stripping = (re.findall(r'::FHED\n([\w\W]*)::::SOURCE', sample_content)) #样本剥离
            sample_stripping_head = (re.findall(r':::SOURCE\n[\w\W]*::FHED\n', sample_content)) #head剥离
            #剥离结果
            head = sample_stripping_head[0]
            foot ="::::SOURCE"
            self.text_update('START_')
            #================
            model = 'PVI'
            #================
            max_num = 0
            limit40 = 40
            for i in self.get_data_2line(modbusList, listSheet):
                if 'CHKN' in i:
                    CHKN = i['CHKN']
                    if CHKN > max_num:
                        max_num = CHKN

            page_num = int(max_num/(limit40+1))+1

            for No_page in range(page_num):
                #处理开始resultfile
                resultDR_filename = f'DR_output{No_page}.txt'
                resultDR = os.path.join(filepath, resultDR_filename)
                resultfile = open(resultDR,'w')
                resultfile.write(head)
                for i in self.get_data_2line(modbusList,listSheet):
                    ETAG ='NULL'
#===========参数
                ### No
                    if 'CHKN' in i:
                        CHKN = i['CHKN']
                        if CHKN <= limit40*No_page  or CHKN > limit40*(No_page + 1):
                            #break   #跳出for循环 不再执行
                            continue #只跳出本次，循环继续执行
                            pass

                        CHKN = CHKN % limit40

                        if CHKN == 0:
                            CHKN = limit40
                            pass

                        inValue = self.get_linestr(sample_content, model, 'CHKN')
                        outValue = f':CHKN:1:{CHKN};'
                        line = sample_stripping[0].replace (inValue,outValue)

                        inValue = self.get_linestr(sample_content, 'PIO', 'RCHK')
                        outValue = f':RCHK:1:@{CHKN};'
                        line = line.replace (inValue,outValue)

                        inValue = self.get_linestr(sample_content, 'PIO', 'GCNC')
                        outValue = f':GCNC:3:{CHKN}$8,$6,8,AN;'
                        line = line.replace (inValue,outValue)
                ### 位置
                        if 0 < CHKN < limit40 + 1:
                            PVIX = 50
                            PVIY = 100
                            CHKNX = CHKN%10
                            if CHKNX!=0:
                                COW = math.floor(CHKN/10)
                                PVIX= int(CHKNX*150-100)
                                PVIY= 100+COW*200
                            if CHKNX==0:
                                COW = math.floor(CHKN/10)-1
                                PVIX= 9*150+50
                                PVIY= 100+COW*200
                            inValue = self.get_linestr(sample_content,model,'GBLK')
                            outValue = f':GBLK:{PVIX},{PVIY}:S1;'
                            line = line.replace (inValue,outValue)
                            PIOX= PVIX - 36
                            PIOY= PVIY + 120
                            inValue = self.get_linestr(sample_content,'PIO','GBLK')
                            outValue = f':GBLK:{PIOX},{PIOY}:S1:$5;'
                            line = line.replace (inValue,outValue)
                ### Name
                        if 'ETAG' in i:
                            ETAG = i['ETAG']
                            inValue = self.get_linestr(sample_content,'PIO','RCNC')
                            outValue = f':RCNC:1::{ETAG}.IN:O;'
                            line = line.replace (inValue,outValue)
                ### PIO地址
                        if 'CNCT' in i:
                            CNCT = i['CNCT']
                            inValue = self.get_linestr(sample_content, 'PIO', 'RTAG')
                            outValue = f':RTAG:1:{CNCT};'
                            line = line.replace (inValue,outValue)

                ### 多个数据类型
                        index_A = ['ETCM', 'EUNT', 'ESCL', 'SSI!','CNCT','ETAG']
                        index_B = [f':ETCM:1:{i[index_A[0]]};',
                                   f':EUNT:1:{i[index_A[1]]};',
                                   f':ESCL:1:{i[index_A[2]]};',
                                   f':SSI!:1:{i[index_A[3]]}:106.25:-6.25;',
                                   f':CNCT:1:IN:{i[index_A[4]]}:I;',
                                   f':ETAG:1:{i[index_A[5]]};']

                        def multi_process(indexA, indexB, lineC):
                            line_ = lineC
                            for item in range(len(indexA)):
                                if index_A[item] in i:
                                    in_Value = self.get_linestr(sample_content, model, indexA[item])
                                    line_ = line_.replace(in_Value, indexB[item])
                                pass
                            return line_

                        line = multi_process(index_A, index_B, line)
                ### 写入文件
                        resultfile.write(line)
                        pass
            ### Text显示
                    self.text_update(f">>>{ETAG}\n")
                resultfile.write(foot)
                self.text_update(f"=============导出文件:{str(resultDR_filename)}\n")

            #self.e.set("复制结束：结果已输出至 DR_output.txt")
            self.text_update('STOP_')
        except FileNotFoundError as e:
            self.e.set(e)
        except UnicodeDecodeError as e:
            self.e.set(e)
        sleep(2)
        pass

    def get_linestr(self,ds,model,CODE):
        furm = ['PVI','SI-1ALM']
        fref = ['PIO']
        find_all_str =''
        if model in furm:
            find_all_str = r':FNRM\n([\w\W]*)::FNRM'
            for _ in re.split(r'[\n]\s*', re.findall(find_all_str, ds)[0]):
                if CODE in _:
                    find_all_str = re.findall(r'(:[\w\W]*;)', str(_))[0]
                pass
            pass
        pass
        if model in fref:
            find_all_str = r':FREF\n([\w\W]*?)::FREF'
            for find_at in re.findall(find_all_str, ds):
                #print(find_at)
                if "@1" in find_at:
                    for _ in re.split(r'[\n]\s*', find_at):
                        if CODE in _:
                            find_all_str = re.findall(r'(:[\w\W]*;)', str(_))[0]
                        pass
                    pass
                pass
                if "@2" in find_at:
                    print("@2")
                pass
            pass
        pass
        return  find_all_str
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
        # 样例：self.text_update('STOP_')
        pass


if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoRead._ALRM_NODE_.limited_time(root)
    root.title("modbus列表生成工具 V2.1"+"    到期日:"+limit_time)
    root.mainloop()

# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================

# Rev01
# 读取模板

# ReV02
# 操作界面

# ReV03
# 直接读取GR样本文档

# ReV04
# 修改读取样本bug
#==========================================================

from tkinter import *
# 导入ttk
from tkinter import ttk
from tkinter import filedialog
import os
import re
from time import sleep
import YokoRead   #自定义模块
from YokoRead import time_Decorator,thread_Decorator


class Windows_NODE(YokoRead._FILE_NODE_):
    def __init__(self, master):
        self.master = master
        #self.here = os.path.abspath(os.path.dirname(__file__))
        self.here = os.getcwd()
        self.initWidgets()
        help_doc = '本程序为流程图数据块快速复制组态工具。 \n' \
                   ' 使用方法：\n' \
                   '1.通过参考文档按钮选择需要复制的流程图样本，默认为GRtemp.xaml。\n' \
                   '2.通过按钮选择数据列表文件，使用下拉菜单选择相对应的表格（sheet）.\n' \
                   '3.点击开始按钮执行程序复制'
        self.Text.insert('insert', help_doc)
        pass

    def initWidgets(self):
        # 创建顶部
        top_frame = LabelFrame(self.master,text='参考文档',height = 150,width = 615)
        top_frame.pack(fill=X,padx=15,pady=0)
        #top_frame.pack(fill=X,expand=YES,side=TOP,padx=15,pady=0)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame,width=65,textvariable = self.e1)
        self.e1.set('GRtemp.xaml')
        self.entry.pack(fill=X,expand=YES,side=LEFT,pady=10)
        ttk.Button(top_frame,text='参考文档',command=self.open_file).pack(side=LEFT)

        # 创建中部
        mid_frame = LabelFrame(self.master,text='数据列表')
        mid_frame.pack(fill=X,padx=15,pady=0)
        self.e2 = StringVar()
        self.entry2 = ttk.Entry(mid_frame,width=45,textvariable = self.e2)
        self.e2.set('GR_PVI_list.xls')
        self.entry2.pack(fill=X,expand=YES,side=LEFT,pady=10)
        self.e3 = StringVar()
        self.comboxlist=ttk.Combobox(mid_frame,width=15,textvariable = self.e3) 
        self.comboxlist.pack(side=LEFT)
        self.e3.set('DATE1')
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

        self.e11 = StringVar()
        ttk.Label(bot_frame,width = 6,textvariable = self.e11).pack(side=LEFT,padx=5,pady=5)
        self.e11.set('间隔数:')
        self.e12 = StringVar()
        self.entry12= ttk.Entry(bot_frame,width=5,textvariable = self.e12)
        self.entry12.pack(side=LEFT, pady=5)
        self.e12.set('50')

        self.e13 = StringVar()
        ttk.Label(bot_frame,width = 6,textvariable = self.e13).pack(side=LEFT,padx=5,pady=5)
        self.e13.set('行间距:')
        self.e14 = StringVar()
        self.entry14 = ttk.Entry(bot_frame, width=5, textvariable=self.e14)
        self.entry14.pack(side=LEFT, pady=5)
        self.e14.set('15')

        ttk.Button(bot_frame, text='开始', command=self.command).pack(side=RIGHT)
        pass

    def open_file(self):
        file_path = filedialog.askopenfilename(title=u'选择参考文档', initialdir=self.here)
        file_text = file_path
        self.entry.delete(0, END)
        self.entry.insert('insert', file_text)
        pass

    def open_file2(self):
        file_path = filedialog.askopenfilename(title=u'选择数据列表', initialdir=self.here)
        file_text = file_path
        self.entry2.delete(0, END)
        self.entry2.insert('insert', file_text)
        sheetName = self.get_sheet(file_text)
        sheetNameT = tuple(sheetName)
        self.comboxlist["values"] = sheetNameT
        self.comboxlist.current(0)
        pass

    @thread_Decorator
    @time_Decorator
    def command(self):
        try:
            samplePVI = self.entry.get()
            resultDR = 'PVI_GR/GR_output.xaml'
            modbusList = self.entry2.get()
            listSheet = self.comboxlist.get()
            Maintxt = open(samplePVI,'r',encoding='utf-8')
            OutFile = open(resultDR,'w+',encoding='utf-8')
            # 读取所有样本流程图
            alls = Maintxt.read()
            # 读取所有样本流程图=====头部
            head1 = (re.findall(r'<!--P([\w\W]*?)<yiapcspvgbdc0',alls))
            #正则表达式 两字符串之间的内容。
            head = ('<!--P' + str(head1[0]) + '\n')
            # 读取所有样本流程图=====内容
            s1 = (re.findall(r'Function Link Component0" />([\w\W]*)</yiapcspvgbdc0:GroupComponent>',alls))
            s = (str(s1[0]) + r'</yiapcspvgbdc0:GroupComponent>')
            # 读取所有样本流程图=====底部
            foot = '</Canvas>'
            # 读取所有样本流程图=====位置信息
            LeftData = (re.findall(r'Canvas.Left="\w+"',alls))
            TopData = (re.findall(r'Canvas.Top="\w+"',alls))
            LeftDataCount = 0
            self.Text.delete(0.0, END)
            self.Text.insert('insert', "=============转换开始===============\n")
            self.Text.update()
            datalist = list(self.get_data_Tag(modbusList,listSheet))
            datalist_tag = tuple(datalist[0].values())

            OutFile.write(head)   #写入头部
            line = ""
            TAG = ""
            gapNum = int(self.entry12.get())
            outValueGap = int(self.entry14.get())
            for i in (self.get_data(modbusList,listSheet)):
                for j in datalist_tag:
                    if j == datalist_tag[0]:
                        TAG = i[j]
                        inValue = j
                        outValue = str(TAG)
                        line = s.replace (inValue,outValue)
                    if j != datalist_tag[0]:
                        TAG = i[j]
                        inValue = j
                        outValue = str(TAG)
                        line = line.replace (inValue,outValue)
                pass
                #修改坐标===
                x = int(LeftDataCount/gapNum)

                inValue = LeftData[0]
                outValue = 'Canvas.Left="'+ str(LeftDataCount*2+20) +'"'
                line = line.replace (inValue,outValue)
                inValue = TopData[0]
                outValue = 'Canvas.Top="'+ str((LeftDataCount+x)*outValueGap+20) +'"'
                line = line.replace (inValue,outValue)
                LeftDataCount += 1
                pass
                self.Text.insert('insert','INFO: '+ TAG + " 转换结束\n")
                self.Text.update()
                self.Text.see(END)

                OutFile.write(line) #写入内容
                OutFile.write("\n")
            OutFile.write(foot)#写入底部
            self.Text.insert('insert', "转换结束：结果已输出至 DR_output.xaml")
            self.Text.see(END)

        except FileNotFoundError as e:
            self.e.set(e)
        except UnicodeDecodeError as e:
            self.e.set(e)
        except  IndexError :
            err = "\n错误提示：确认复制元素是否Group"
            self.Text.insert('insert', err)
        sleep(2)

if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoRead._ALRM_NODE_.limited_time(root)
    root.title("列表流程图生成工具 V4.01"+"    到期日:"+limit_time)
    root.mainloop()

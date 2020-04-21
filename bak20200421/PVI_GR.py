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
import re
from time import sleep
import YokoRead   #自定义模块
from YokoRead import time_Decorator,thread_Decorator

class Windows_NODE(YokoRead.FILE_NODE):
    def __init__(self, master):
        self.master = master
        self.here = os.getcwd()
        self.initWidgets()
        help_doc = '本程序为流程图数据块快速复制组态工具。 \n' \
                   ' 使用方法：\n' \
                   '1.通过参考文档按钮选择需要复制的流程图样本，默认为GRtemp.xaml。\n' \
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
        self.combox_list=ttk.Combobox(mid_frame,width=15,textvariable = self.e3)
        self.combox_list.pack(side=LEFT)
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
        sheet_Name = self.get_sheet(file_text)
        sheet_Name_T = tuple(sheet_Name)
        self.combox_list["values"] = sheet_Name_T
        self.combox_list.current(0)
        pass

    @thread_Decorator
    @time_Decorator
    def command(self):
        try:
            sample_PVI = self.entry.get()
            modbus_list = self.entry2.get()
            sheet_list = self.combox_list.get()
            filepath, fullflname = os.path.split(modbus_list)
            DR_result = os.path.join(filepath, 'GR_output.xaml')

           # Maintxt = open(sample_PVI,'r',encoding='utf-8')
            with open(sample_PVI,'r',encoding='utf-8') as Maintxt:
                # 读取所有样本流程图
                allContent = Maintxt.read()
            # 读取所有样本流程图=====头部
            head_find = (re.findall(r'<!--P([\w\W]*?)<yiapcspvgbdc0',allContent))
            #正则表达式 两字符串之间的内容。
            head_last = ('<!--P' + str(head_find[0]) + '\n')
            # 读取所有样本流程图=====内容
            find_Content = (re.findall(r'Function Link Component0" />([\w\W]*)</yiapcspvgbdc0:GroupComponent>',allContent))
            content = f'{find_Content[0]}</yiapcspvgbdc0:GroupComponent>'
            # 读取所有样本流程图=====底部
            foot = '</Canvas>'
            # 读取所有样本流程图=====位置信息
            Left_Data = (re.findall(r'Canvas.Left="\w+"',allContent))
            Top_Data = (re.findall(r'Canvas.Top="\w+"',allContent))
            Left_Data_Count = 0
            self.text_update('START_')
            data_list = list(self.get_data_Tag(modbus_list,sheet_list))
            data_list_tag = tuple(data_list[0].values())

            Out_file = open(DR_result, 'w+', encoding='utf-8')
            Out_file.write(head_last)   #写入头部
            result_line = ""
            tag_now = ""
            gap_Num = int(self.entry12.get())
            out_ValueGap = int(self.entry14.get())
            for all_tag in (self.get_data(modbus_list,sheet_list)):
                for serial in data_list_tag:
                    tag_now = all_tag[serial]
                    in_Value = serial
                    out_Value = str(tag_now)
                    if serial == data_list_tag[0]:
                        result_line = content.replace (in_Value,out_Value)
                    else:
                        result_line = result_line.replace (in_Value,out_Value)
                pass
                #修改坐标===
                x = int(Left_Data_Count/gap_Num)

                in_Value = Left_Data[0]
                out_Value = f'Canvas.Left="{(Left_Data_Count * 2 + 20)}"'
                result_line = result_line.replace (in_Value,out_Value)
                in_Value = Top_Data[0]
                out_Value = f'Canvas.Top="{((Left_Data_Count + x) * out_ValueGap + 20)}"'
                result_line = result_line.replace (in_Value,out_Value)
                Left_Data_Count += 1
                pass
                self.text_update(f'INFO:{tag_now}转换结束\n')
                result_line = result_line +'\n'
                Out_file.write(result_line)     #写入内容
            Out_file.write(foot)         #写入底部
            self.text_update("结果已输出至 DR_output.xaml\n")
            self.text_update('STOP_')

        except FileNotFoundError as e:
            self.text_update(e)
        except UnicodeDecodeError as e:
            self.text_update(e)
        except  IndexError :
            err = "\n错误提示：确认复制元素是否Group"
            self.text_update(err)
        sleep(1)

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
if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoRead.ALRM_NODE.limited_time(root)
    root.title("列表流程图生成工具 V4.01"+"    到期日:"+limit_time)
    root.mainloop()

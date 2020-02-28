# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
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
import time


class Windows_NODE(YokoRead._FILE_NODE_):
    def __init__(self, master):
        self.master = master
        self.here = os.getcwd()
        self.initWidgets()
        help_doc = '本程序为快速复制组态工具。 \n 使用方法：\n1.通过参考文档按钮选择需要复制的DR文件，默认为DR_template.txt。\n2.通过按钮选择数据列表文件，使用下拉菜单选择相对应的表格（sheet）.\n\
3.点击开始按钮执行程序复制'
        self.Text.insert('insert', help_doc)
        pass

    def initWidgets(self):
        # 创建顶部
        top_frame = LabelFrame(self.master,text='参考文档',height = 150,width = 615)
        top_frame.pack(fill=X,padx=15,pady=0)
        #top_frame.pack(fill=X,expand=YES,side=TOP,padx=15,pady=0)
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
        #self.lable(bot_frame,text = '欢迎使用',width = 60,height = 20).pack(side=LEFT)
        ttk.Label(bot_frame,width = 60,textvariable = self.e).pack(side=LEFT, fill=BOTH, expand=YES,pady=10)
        self.e.set('懒惰、不耐烦、傲慢')
        ttk.Button(bot_frame, text='开始', command=lambda: self.thread_it(self.get_entry)).pack(side=RIGHT, padx=10)

    def open_file(self):
        self.entry.delete(0,END)
        file_path = filedialog.askopenfilename(title=u'选择参考文档', initialdir=self.here)
        file_text = file_path
        self.entry.insert('insert', file_text)
        
    def open_file2(self):
        self.entry2.delete(0,END)
        file_path = filedialog.askopenfilename(title=u'选择数据列表', initialdir=self.here)
        file_text = file_path
        self.entry2.insert('insert', file_text)
        sheetName = self.get_sheet(file_text)
        sheetNameT = tuple(sheetName)
        self.comboxlist["values"] = sheetNameT
        self.comboxlist.current(0)
        
    def get_entry(self):
        try:
            samplePVI = self.entry.get()
            resultDR = 'DR_output.txt'
            modbusList = self.entry2.get()
            #listSheet = "DATE"
            listSheet = self.comboxlist.get()
            #print (listSheet)
            # 数据读取
            samplefile = open(samplePVI,'r')
            resultfile = open(resultDR,'w')
            # 数据剥离
            sample_content = samplefile.read()
            sample_stripping = (re.findall(r'::FHED\n([\w\W]*)::::SOURCE', sample_content)) #样本剥离
            sample_stripping_head = (re.findall(r':::SOURCE\n[\w\W]*::FHED\n', sample_content)) #head剥离
            #剥离结果
            head = sample_stripping_head[0]
            foot ="::::SOURCE"
            #处理开始
            resultfile.write(head)
            self.Text.delete(0.0,END)
            self.Text.insert('insert', "=============复制开始===============\n")
            #================
            model = 'PVI'
            #================
            for i in self.get_data_2line(modbusList,listSheet):
                ETAG ='NULL'
            #===========参数
        ###   No
                if 'CHKN' in i:
                    CHKN = i['CHKN']
                    if (CHKN > 40):
                        break
                    inValue = self.get_linestr(sample_content, model, 'CHKN')
                    outValue = ":CHKN:1:"+str(CHKN)+";"
                    line = sample_stripping[0].replace (inValue,outValue)

                    inValue = self.get_linestr(sample_content, 'PIO', 'RCHK')
                    outValue = ":RCHK:1:@"+str(CHKN)+";"
                    line = line.replace (inValue,outValue)

                    inValue = self.get_linestr(sample_content, 'PIO', 'GCNC')
                    outValue = ":GCNC:3:"+str(CHKN)+"$8,$6,8,AN;"
                    line = line.replace (inValue,outValue)
            ### 位置
                    if(CHKN>0 and CHKN<41):
                        PVIX = 50
                        PVIY = 100
                        if (CHKN>40):
                            break
                        CHKNX = CHKN%10
                        if(CHKNX!=0):
                            COW = math.floor(CHKN/10)
                            PVIX= int(CHKNX*150-100)
                            PVIY= 100+COW*200
                        if(CHKNX==0):
                            COW = math.floor(CHKN/10)-1
                            PVIX= 9*150+50
                            PVIY= 100+COW*200
                        #print(str(PVIX)+"-"+str(PVIY))
                        inValue = self.get_linestr(sample_content,model,'GBLK')
                        outValue = ":GBLK:"+str(PVIX)+","+str(PVIY)+":S1;"
                        line = line.replace (inValue,outValue)
                        #print(outValue)
                        PIOX= PVIX - 36
                        PIOY= PVIY + 120
                        #print(str(PIOX)+"-"+str(PIOY))
                        inValue = self.get_linestr(sample_content,'PIO','GBLK')
                        outValue = ":GBLK:"+str(PIOX)+","+str(PIOY)+":S1:$5;"
                        line = line.replace (inValue,outValue)
            ### Name
                    if 'ETAG' in i:
                        ETAG = i['ETAG']
                        inValue = self.get_linestr(sample_content, model, 'ETAG')
                        outValue = ":ETAG:1:"+ETAG+";"
                        line = line.replace (inValue,outValue)

                        inValue = self.get_linestr(sample_content,'PIO','RCNC')
                        outValue = ":RCNC:1::"+ETAG+".IN:O;"
                        line = line.replace (inValue,outValue)
            ### 注释
                    if 'ETCM' in i:
                        ETCM = i['ETCM']
                        inValue = self.get_linestr(sample_content, model, 'ETCM')
                        outValue = ":ETCM:1:"+ETCM+";"
                        line = line.replace (inValue,outValue)
            ### PIO地址
                    if 'CNCT' in i:
                        CNCT = i['CNCT']
                        inValue = self.get_linestr(sample_content, model, 'CNCT')
                        outValue = ":CNCT:1:IN:"+CNCT+":I;"
                        line = line.replace (inValue,outValue)

                        inValue = self.get_linestr(sample_content, 'PIO', 'RTAG')
                        outValue = ":RTAG:1:"+CNCT+";"
                        line = line.replace (inValue,outValue)
            ### 量程
                    if 'LO' in i and 'HI' in i:
                        LO = i['LO']
                        HI = i['HI']
                        inValue = self.get_linestr(sample_content, model, 'HI')
                        outValue = ":ESCL:1:" + str(HI) + ":" + str(LO) + ";"
                        line = line.replace(inValue, outValue)
            ### 单位
                    if 'UNIT' in i:
                        UNIT = i['UNIT']
                        inValue = self.get_linestr(sample_content, model, 'EUNT')
                        outValue = ":EUNT:1:" + UNIT + ";"
                        line = line.replace(inValue, outValue)
            ### 比例系数
                    if 'SSIK' in i and 'SSIB' in i:
                        SSIK = i['SSIK']
                        SSIB = i['SSIB']
                        inValue = self.get_linestr(sample_content, model, 'SSI!')
                        outValue = ":SSI!:1:" + str(SSIK) + ":" + str(SSIB) + ":106.25:-6.25;"
                        line = line.replace(inValue, outValue)
            ### 写入文件
                    resultfile.write(line)
        ### Text显示
                self.Text.insert('insert', ">>>"+ETAG+"\n")
                self.Text.update()

            resultfile.write(foot)
                #messagebox.showinfo(title='通知', message="转换结束")
            self.Text.insert('insert', "=============复制结束===============\n")
            self.Text.update()
            self.Text.see(END)
            self.e.set("复制结束：结果已输出至 DR_output.txt")
            #root.destroy() 
        except FileNotFoundError as e:
            self.e.set(e)
        except UnicodeDecodeError as e:
            self.e.set(e)
        time.sleep(2)
        pass

    def get_linestr(self,ds,model,CODE):
        funrm = ['PVI','SI-1ALM']
        fref = ['PIO']
        find_all_str =''
        if model in funrm:
            find_all_str = r':FNRM\n([\w\W]*)::FNRM'
            pass
        if model in fref:
            find_all_str = r':FREF\n([\w\W]*)::FREF'
            pass
        ds1 = (re.findall(find_all_str, ds))
        #print(ds1)
        dline = ds1[0]
        dline1 = re.split(r'[\n]\s*', dline)
        for _ in dline1:
            if CODE in _:
                linestr = str(_)
                find_all_str = linestr[1:len(linestr)]
        return  find_all_str
        pass

  
if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoRead._ALRM_NODE_.limited_time(root)
    root.title("modbus列表生成工具 V2.1"+"    到期日:"+limit_time)
    root.mainloop()

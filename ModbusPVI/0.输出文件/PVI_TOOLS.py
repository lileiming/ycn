# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================
import tkinter
from tkinter import *

#===================自定义模块==============================
import YokoRead
import PVI_GR    #流程图复制工具
import PVI_COMM  #功能块复制工具
import PVI_ESCL  #量程修改工具
import PVI_invter   #截图反色工具
import OutDrFile #DR文件自动导出



class myWindow():
    def __init__(self, root, myTitle, flag):
        self.top = tkinter.Toplevel(root)
        self.top.geometry('640x400+550+200')
        self.top.title(myTitle)
        self.top.attributes('-topmost', 1)
        if flag == 1:
            PVI_GR.Windows_NODE(self.top)
        elif flag == 2:
            PVI_COMM.Windows_NODE(self.top)
        elif flag == 3:
            PVI_ESCL.Windows_NODE(self.top)
        elif flag == 4:
            PVI_invter.Windows_NODE(self.top)
        elif flag == 5:
            OutDrFile.Windows_NODE(self.top)
    pass
pass

class Windows_NODE():
    def __init__(self, master):
        self.master = master
        self.initWidgets()
        pass

    def initWidgets(self):
        # 创建顶部
        self.window1 = tkinter.IntVar(root, value=0) #只允许弹出一个窗体
        #self.window2 = tkinter.IntVar(root, value=0)  #允许同时弹出2个窗体
        title1 = '流程图复制工具'
        self.button1 = tkinter.Button(root,text= title1 , command=lambda :self.button_fun(title1,1))
        self.button1.place(x=70, y=40, height=40, width=160)
        title2 = '功能块复制工具'
        self.button2 = tkinter.Button(root,text= title2 , command=lambda :self.button_fun(title2,2))
        self.button2.place(x=70, y=100, height=40, width=160)
        title3 = '量程修改工具'
        self.button3 = tkinter.Button(root,text= title3 , command=lambda :self.button_fun(title3,3))
        self.button3.place(x=70, y=160, height=40, width=160)
        title4 = '截图反色工具'
        self.button4 = tkinter.Button(root,text= title4 , command=lambda :self.button_fun(title4,4))
        self.button4.place(x=70, y=220, height=40, width=160)
        title5 = 'DR文件自动导出工具'
        self.button5 = tkinter.Button(root, text= title5 , command=lambda :self.button_fun(title5,5))
        self.button5.place(x=70, y=280, height=40, width=160)
        pass

    def button_fun(self,title,window_num):
        if self.window1.get()==0:
            self.window1.set(1)
            w1 = myWindow(root, title, window_num)
            self.button1.wait_window(w1.top)
            self.window1.set(0)
        pass

if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400+200+200')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoRead._ALRM_NODE_.limited_time(root)
    root.title("组态工具箱 V0.1"+"    到期日:"+limit_time)
    root.mainloop()




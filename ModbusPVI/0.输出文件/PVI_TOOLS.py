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

class myWindow():
    def __init__(self, root, myTitle, flag):
        self.top = tkinter.Toplevel(root, width=640, height=400)
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
        self.button1 = tkinter.Button(root, text='流程图复制工具', command=self.buttonClick1)
        self.button1.place(x=70, y=40, height=40, width=160)
        self.button2 = tkinter.Button(root, text='功能块复制工具', command=self.buttonClick2)
        self.button2.place(x=70, y=100, height=40, width=160)
        self.button3 = tkinter.Button(root, text='量程修改工具', command=self.buttonClick3)
        self.button3.place(x=70, y=160, height=40, width=160)
        self.button4 = tkinter.Button(root, text='截图反色工具', command=self.buttonClick4)
        self.button4.place(x=70, y=220, height=40, width=160)
        pass

    def buttonClick1(self):
        if self.window1.get()==0:
            self.window1.set(1)
            w1 = myWindow(root, '流程图复制工具', 1)
            self.button1.wait_window(w1.top)
            self.window1.set(0)
        pass
    pass

    def buttonClick2(self):
        if self.window1.get()==0:
            self.window1.set(1)
            w1 = myWindow(root, '功能块复制工具', 2)
            self.button1.wait_window(w1.top)
            self.window1.set(0)
        pass
    pass

    def buttonClick3(self):
        if self.window1.get()==0:
            self.window1.set(1)
            w1 = myWindow(root, '量程修改工具', 3)
            self.button1.wait_window(w1.top)
            self.window1.set(0)
        pass
    pass

    def buttonClick4(self):
        if self.window1.get()==0:
            self.window1.set(1)
            w1 = myWindow(root, '截图反色工具', 4)
            self.button1.wait_window(w1.top)
            self.window1.set(0)
        pass
    pass

if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoRead._ALRM_NODE_.limited_time(root)
    root.title("组态工具箱 V0.1"+"    到期日:"+limit_time)
    root.mainloop()




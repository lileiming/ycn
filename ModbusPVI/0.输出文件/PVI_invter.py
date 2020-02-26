# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================
# Rev01
# 实现截图反色及转换为PNG格式
#https://blog.csdn.net/qq_42572322/article/details/89401474?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
#https://blog.csdn.net/derek881122/article/details/101875726?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
#==========================================================
import cv2 as cv
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import time
import YokoRead   #自定义模块
import threading

class Windows_NODE():
    def __init__(self, master):
        self.master = master
        self.here = 'C:/CENTUMVP/his/save/bmp/'
        self.initWidgets()
        help_doc = '本程序为截图反色工具 \n 使用方法：\n1.通过按钮选择需要反色的图片目录，默认为IN目录。\n2.点击确认按钮开始执行图片反色\n'
        self.Text.insert('insert',help_doc)
        pass

    def initWidgets(self):
        # 创建顶部
        top_frame = LabelFrame(self.master, text='图片目录', height=150, width=615)
        top_frame.pack(fill=X, padx=15, pady=5)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame, width=65, textvariable=self.e1)
        print(self.here)
        self.e1.set(self.here)
        self.entry.pack(fill=X, expand=YES, side=LEFT, pady=10)
        ttk.Button(top_frame, text='图片目录', command=self.open_dir).pack(side=LEFT)

        # 创建中部
        mid_frame = LabelFrame(self.master, text='功能选择')
        mid_frame.pack(fill=X, padx=15, pady=0)
        ## 同文件选择框
        self.intVar = BooleanVar()
        self.intVar1 = BooleanVar()
        self.intVar.set(True)
        self.intVar1.set(True)
        # should_auto = BooleanVar()
        self.check1 = Checkbutton(mid_frame, text="反色", variable=self.intVar).pack(side=LEFT)
        self.check2 = Checkbutton(mid_frame, text="转换为png", variable=self.intVar1).pack(side=LEFT)
        self.ckeckchange = 1

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
        self.e.set('懒惰、不耐烦、傲慢')
        ttk.Button(bot_frame, text='确定', command=lambda :self.thread_it(self.command)).pack(side=RIGHT)
        # lambda :thread_it(music, songs)
    def open_dir(self):
        self.entry.delete(0,END)
        dir_path = filedialog.askdirectory(title=u'选择图片文件夹',initialdir = self.here)
        path0 = dir_path
        path1 = path0+'/'
        self.entry.insert('insert', path1)


    def command(self):
        self.Text.insert(END, "==============转换开始============\n")
        self.Text.update()
        path = self.entry.get()
        bmp_in_files = os.listdir(path)
        for _bmp in bmp_in_files:
          if '.bmp' in _bmp or '.jpg' in _bmp:
            bmpname = path + _bmp
            image = cv.imread(bmpname, 1)
            self.inverse_color(image)
            #self.show_img(self.inver_bmp)
            if self.intVar1.get():
                split_bmpname = os.path.splitext(bmpname)
                pngname = split_bmpname[0] + '.png'
                pass
            else:
                pngname = bmpname
            cv.imwrite(pngname, self.inver_bmp)
            self.text_update(pngname)
        self.text_update('0')
        time.sleep(3)

    def text_update(self,show):
        if show == '0':
            self.Text.insert(END, "==============转换结束============\n")
        else:
            self.Text.insert(END,'INFO: '+ show + " 转换结束\n")
        self.Text.update()
        self.Text.see(END)

    def inverse_color(self,image):
        height,width,temp = image.shape
        img2 = image.copy()
        if self.intVar.get():
            for i in range(height):
                for j in range(width):
                    img2[i,j] = (255-image[i,j][0],255-image[i,j][1],255-image[i,j][2])
        self.inver_bmp = img2

    def show_img(self,img):
        cv.namedWindow("Image")
        cv.imshow("Image",img)
        cv.waitKey(0)
        #释放窗口
        #cv.destroyAllWindows()

    def thread_it(self,func,*args):
        # 创建
        t = threading.Thread(target=func, args=args) 
        # 守护 !!!
        t.setDaemon(True) 
        # 启动
        t.start()
        # 阻塞--卡死界面！


if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoRead._ALRM_NODE_.limited_time(root)
    root.title("图片批量反色工具 V1.00"+"    到期日:"+limit_time)
    root.mainloop()
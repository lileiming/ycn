# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
#==========================================================
# Rev01
# 实现截图反色及转换为PNG格式

#==========================================================
import cv2 as cv
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import YokoRead   #自定义模块
from time import sleep
from YokoRead import time_Decorator,thread_Decorator

class Windows_NODE(YokoRead.FILE_NODE):
    def __init__(self, master):
        self.master = master
        self.here = 'C:/CENTUMVP/his/save/bmp/'
        self.initWidgets()
        help_doc = '本程序为截图反色工具 \n 使用方法：\n1.通过按钮选择需要反色的图片目录，默认为IN目录。\n2.点击确认按钮开始执行图片反色\n\n\n**********************\n' \
                   '截图10张数量限制修改方法：\n' \
                   'WIN+R 输入 regedit \n' \
                   '找到 HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\YOKOGAWA\CS3K\HIS\PRINTER\HDCPCNT\n' \
                   '将HDCPCNT 的原来的值（10进制）修改即可\n'
        self.text_update(help_doc)
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
        self.intVar.set(False)
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
        self.e.set('程序员美德：懒惰、不耐烦、傲慢')
        ttk.Button(bot_frame, text='确定', command=self.command).pack(side=RIGHT)

    def open_dir(self):
        self.entry.delete(0,END)
        dir_path = filedialog.askdirectory(title=u'选择图片文件夹',initialdir = self.here)
        path0 = dir_path
        path1 = path0+'/'
        self.entry.insert('insert', path1)

    @thread_Decorator
    @time_Decorator
    def command(self):
        self.text_update('START_')
        path = self.entry.get()
        bmp_in_files = os.listdir(path)
        for _bmp in bmp_in_files:
          if '.bmp' in _bmp or '.jpg' in _bmp:
            bmp_name = path + _bmp
            image = cv.imread(bmp_name, 1)
            self.inverse_color(image)
            #self.show_img(self.inver_bmp)
            if self.intVar1.get():
                split_bmpname = os.path.splitext(bmp_name)
                png_name = f'{split_bmpname[0]}.png'
                pass
            else:
                png_name = bmp_name
            cv.imwrite(png_name, self.inver_bmp)
            self.text_update(f'INFO:{png_name}转换结束\n')
        self.text_update('STOP_')
        sleep(1)

    def inverse_color(self,image):
        height,width,temp = image.shape
        img_last = image.copy()

        if self.intVar.get():
            for i in range(height):
                for j in range(width):
                    img_last[i,j] = (255-image[i,j][0],255-image[i,j][1],255-image[i,j][2])
        self.inver_bmp = img_last
        pass

    def show_img(self,img):
      cv.namedWindow("Image")
      cv.imshow("Image",img)
      cv.waitKey(0)
      #释放窗口
      #cv.destroyAllWindows()

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

    def foo(self):  #未启用
        path = self.entry.get()
        dir_num = len([lists for lists in os.listdir(path) if os.path.isdir(os.path.join(path, lists))])
        file_num = len([lists for lists in os.listdir(path) if os.path.isfile(os.path.join(path, lists))])
        pr_dir_num = '文件夹:' + str(dir_num) +'个\n'
        pr_file_num = '文件数量:' + str(file_num) +'个\n'
        self.Text.insert(END, pr_dir_num )
        self.Text.insert(END, pr_file_num)

        for all_list in os.listdir(path):
            if '.png' in all_list:
                print(os.path.join(path, all_list))
        pass

if __name__ == "__main__":
    root = Tk()
    root.geometry('640x400+640+0')  # 窗口尺寸
    Windows_NODE(root)
    limit_time = YokoRead.ALRM_NODE.limited_time(root)
    root.title("图片批量反色工具 V1.00"+"    到期日:"+limit_time)
    root.mainloop()
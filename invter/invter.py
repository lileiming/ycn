import cv2 as cv
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import re
import time
 


class Windows_NODE():
    def __init__(self, master):
        self.master = master
        self.initWidgets()
        help_doc = '本程序为截图反色工具 \n 使用方法：\n1.通过按钮选择需要反色的图片目录，默认为IN目录。\n2.点击按钮开始执行图片反色\n'
        self.Text.insert('insert',help_doc)

    def initWidgets(self):
        # 创建顶部
        top_frame = LabelFrame(self.master, text='图片目录', height=150, width=615)
        top_frame.pack(fill=X, padx=15, pady=0)
        self.e1 = StringVar()
        self.entry = ttk.Entry(top_frame, width=65, textvariable=self.e1)
        self.e1.set('IN')
        self.entry.pack(fill=X, expand=YES, side=LEFT, pady=10)
        ttk.Button(top_frame, text='图片目录', command=self.open_dir).pack(side=LEFT)

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
        ttk.Button(bot_frame, text='图片反色', command=self.command).pack(side=RIGHT)

    def open_dir(self):
        self.entry.delete(0,END)
        dir_path = filedialog.askdirectory(title=u'选择图片文件夹')
        self.path0 = dir_path
        path1 = self.path0+'/'
        self.entry.insert('insert', path1)

    def command(self):
        bmp_in_files = os.listdir(self.path0)
        for _bmp in bmp_in_files:
          if '.bmp' in _bmp or '.jpg' in _bmp:
            bmpname = self.path0 + '/' + _bmp
            #print(self.bmpname)
            image = cv.imread(bmpname,1)
            self.inverse_color(image)
            #self.show_img(self.inver_bmp)
            split_bmpname = os.path.splitext(bmpname)
            pngname = split_bmpname[0] + '.png'
            print(pngname)
            cv.imwrite(pngname, self.inver_bmp)
            self.foo(pngname)
            
            
    def foo(self,show):
      self.Text.insert(END,'INFO: '+ show + " 转换结束\n")
      time.sleep(10)
      
      pass


    def inverse_color(self,image):
        height,width,temp = image.shape
        img2 = image.copy()
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
    
if __name__ == "__main__":

  root = Tk()
  root.title("图片批量反色工具 V1.00")
  root.geometry('640x400')  # 窗口尺寸
  Windows_NODE(root)
  root.mainloop()   

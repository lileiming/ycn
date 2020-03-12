# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================
# Script Name	:  auto assign hardware
# Author		: lileiming@me.com
# Created		: 2019/11/4
# Last Modified	: 2019/11/11
# Version			: 1.0

# Modifications	: 0.1 frist version
# Modifications	: 1.0 基本实现卡件排布

# Description		: Automatically assign hardware locations based on big data.
#==========================================================

import xlrd
import pandas as pd
import math
#import xlwt
from openpyxl import load_workbook


class App():
    def __init__(self):
        self.Excelfile = '1.xls'                                          #定义文件名
        self.data = pd.read_excel(self.Excelfile,"IO_DB_For FCS0701")                      #读取样本数据

    def toFile(self):
        #输出文件
        try:
            self.data.to_excel("out.xlsx", "Sheet1")
            #writer.save()
            #writer.close()
        except PermissionError as e:
            print("输出文件未关闭")

    def test(self):

        self.data = self.data.sort_values(by=['Channel','NODE_Seq_No'], ascending=True)
        #print(self.data.loc['Channel'])
        #print(self.data.loc[:, ['IOMODULE']])
        #print(self.data.loc[:1, ['IOMODULE']])

       # print(self.data.columns)  # 列索引名称

        aList = list(self.data.columns)
        Y_List =['NODE_Seq_No', 'SLOT_Seq_No', 'IOMODULE','DUPLEX']
        for  Y_name in Y_List:
            Yindex = aList.index(Y_name)
            Y_results = self.data.iloc[0,Yindex]
            print(Y_results)



        #print(self.data)


if __name__ == "__main__":
    app = App()
    #app.myCardNum()
    app.test()
    #app.ReadAllData()
    #app.ProCalcu()
    #app.card()
    #app.Requeue()
    #app.toFile()



# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.7
#==========================================================
# Script Name	:  auto assign hardware
# Author		: lileiming@me.com
# Created		: 2019/11/4
# Last Modified	: 2019/11/4
# Version			: 0.1

# Modifications	: 0.1 frist version

# Description		: Automatically assign hardware locations based on big data.
#==========================================================

import xlrd
import pandas as pd
#import xlwt
class App():
    def __init__(self):
        self.Excelfile = 'Sample.xlsx'
        self.data = pd.read_excel(self.Excelfile,"Sheet0")
        self.MaxIndex = len(self.data.index)
        self.NodeSlotList = [[] for col in range(80)]
        self.NodeSlotCal =  [[] for col in range(80)]

    def card(self,Cardtype,Cardnum):
        self.data = self.data.sort_values(by=Cardtype, ascending=False)
        self.data.index = range(self.MaxIndex)
        for X in range(Cardnum):
            if self.data.iloc[X, 2] == True:
                self.data.iloc[X, 2] = str(Cardtype)
                for Y in range(12):
                    self.data.iloc[X, (Y + 3)] = 0
        return (self.data)

    def Requeue(self):
        self.data = self.data.sort_values(by="NO.")
        self.data.index = range(self.MaxIndex)
        #return (self.data)

    def ReadData(self,sheetName):
        data = pd.read_excel(self.Excelfile, sheetName)
        for X in range(5):
            for Y in range(8):
                dataF = data.iloc[5*(X+1), (24 + Y)] # F面数据
                self.NodeSlotList[X * 8 + Y].append(dataF)
                #print(dataF)
        for X in range(5):
            for Y in range(8):
                dataR = data.iloc[5*(X+1), (42 + Y)] # R面数据
                self.NodeSlotList[X * 8 + Y + 40].append(dataR)
                #print(dataR)
        #print(self.NodeSlotList)

    def ProCalcu(self): #Proportional calculation 比例计算
        Sum = 0.0
        self.colName = list(self.data.columns.values)

        for Y in range(80):
            Sum = 0.0
            len1 = len(self.NodeSlotList[Y])
            for X in self.colName[3:14]:
                count1 = self.NodeSlotList[Y].count(X)
                Cal = ((count1 / len1) * 0.98 + 0.001)* 100
                Sum = Sum + Cal
                self.NodeSlotCal[Y].append(Cal)
            self.NodeSlotCal[Y].append(100 - Sum)
            #print(self.NodeSlotCal[Y])
        for Y in range(80):
            for X in range(12):
                self.data.iloc[Y, (X + 3)] = self.NodeSlotCal[Y][X]

    def toFile(self):
        self.data.to_excel('out.xlsx', "Sheet0")

    def Sheetnamelist(self):
        self.SheetnameDict = pd.read_excel(self.Excelfile,None)
        return list(self.SheetnameDict.keys())

    def ReadAllData(self):
        for X in self.Sheetnamelist()[1:]:   #读取第2张 Sheet 开始的数据。
            self.ReadData(X)

    def test(self):
        print(self.data)


if __name__ == "__main__":
    # app.test()
    app = App()
    app.ReadAllData()
    app.ProCalcu()
    app.card("AAI143/R",20)
    app.Requeue()
    app.toFile()



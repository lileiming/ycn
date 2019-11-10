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
import math
#import xlwt
class App():
    def __init__(self):
        self.Excelfile = 'Sample.xlsx'
        self.data = pd.read_excel(self.Excelfile,"Sheet0")
        self.MaxIndex = len(self.data.index)
        self.NodeSlotList = [[] for col in range(80)]
        self.NodeSlotCal =  [[] for col in range(80)]
        self.Card = []

    def myCardNum(self):
        total = 0
        self.rowName = list(self.data.Nodeslot.unique())
        self.cardTypeNum = len(self.rowName) - 1

        for _ in range(self.cardTypeNum):
            cardtpye = self.data.iloc[_, 1]
            cardnum = self.data.iloc[_, 2]

            for i in range(int(cardnum)):
                self.Card.append(cardtpye)
                total = total + 1


        self.nodeNum = math.ceil (total / 8)
        self.total = int(self.nodeNum * 8)
        #print(self.total)
        #print(self.Card)
        for i in range(self.total):
            self.data.iloc[12, i+2] = -1
        #print(self.data)

    def card(self):
        self.colName = list(self.data.columns.values)
        #print(self.cardTypeNum)
        for Y in range(self.cardTypeNum):
            if (self.Card != []):
                #print(self.total)
                #for X in range(self.total)
                for Z in range(4): #0~4
                    for X in range(self.nodeNum):  # Node = 1-10
                        for W in range(2): # 0~1
                            Q = 8*X+2*Z+W+2   #先扫描 S1&S2  在扫 S3&S4
                            #print(Q)
                            if (self.data.iloc[12,Q] == -1):
                                self.data = self.data.sort_values(by=str(self.colName[Q]), ascending=False)
                                #print(self.colName[X + 2])
                                nowCard = self.data.iloc[Y, 1]
                                if nowCard in self.Card:
                                    nowIndex = self.Card.index(nowCard)
                                    #print(nowIndex)
                                    self.data.iloc[self.cardTypeNum, Q] = self.data.iloc[Y, 1]
                                    del self.Card[nowIndex]
                        self.Requeue()
        print(self.Card)

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

    def ReadAllData(self):
        for X in self.Sheetnamelist()[1:]:   #读取第2张 Sheet 开始的数据。
            self.ReadData(X)

    def ProCalcu(self): #Proportional calculation 比例计算
        Sum = 0.0
        #self.rowName = list(self.data.Nodeslot.unique())
        #print(self.colName)
        for Y in range(self.total):
            Sum = 0.0
            len1 = len(self.NodeSlotList[Y])
            #print(len1)
            for X in self.rowName[0:11]:
                count1 = self.NodeSlotList[Y].count(X)
                Cal = ((count1 / len1) * 0.98 + 0.001)* 100
                Sum = Sum + Cal
                self.NodeSlotCal[Y].append(Cal)
            self.NodeSlotCal[Y].append(100 - Sum)
            #print(self.NodeSlotCal[Y])
        for Y in range(self.cardTypeNum):
            for X in range(self.total):
                self.data.iloc[(Y), (X+2)] = self.NodeSlotCal[X][Y]

    def toFile(self):
        try:
            self.data.to_excel('out.xlsx', "Sheet0")
        except PermissionError as e:
            print("输出文件未关闭")


    def Sheetnamelist(self):
        self.SheetnameDict = pd.read_excel(self.Excelfile,None)
        return list(self.SheetnameDict.keys())

    def test(self):
        #print(self.data.NO.unique())
        #print(self.data.iloc[13, 80])
        #print(self.NodeSlotCal[79][11])
        #self.data = self.data.sort_values(by='N1S1',ascending=False)
        print(self.data)
        #self.data.iloc[12,1] = self.data.iloc[0,0]
        print(self.data.iloc[12,1])


if __name__ == "__main__":
    app = App()
    app.myCardNum()
    #app.test()
    app.ReadAllData()
    app.ProCalcu()
    app.card()
    #app.Requeue()
    app.toFile()



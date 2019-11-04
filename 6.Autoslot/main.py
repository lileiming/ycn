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
        self.data = pd.read_excel('slotmap.xlsx',"Sheet1")
        self.MaxIndex = len(self.data.index)

    def card(self,Cardtype,Cardnum):
        self.data = self.data.sort_values(by=Cardtype, ascending=False)
        self.data.index = range(self.MaxIndex)
        for X in range(Cardnum):
            if self.data.iloc[X, 2] == True:
                self.data.iloc[X, 2] = str(Cardtype + '-' + self.data.iloc[X, 1])
                self.data.iloc[X, 3] = 0.0
                self.data.iloc[X, 4] = 0.0
                self.data.iloc[X, 5] = 0.0
                self.data.iloc[X, 6] = 0.0
        return (self.data)

    def Requeue(self):
        self.data = self.data.sort_values(by="NO.")
        self.data.index = range(self.MaxIndex)
        return (self.data)


if __name__ == "__main__":
    app = App()
    app.card("AI",3)
    app.card("AO",3)
    app.card("DI",3)
    app.card("DO",3)
    data1 = app.Requeue()


    print(data1)
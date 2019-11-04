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
class App:
    def __init__(self, master):
        self.master = master
        self.data = pd.read_excel('slotmap.xlsx',"Sheet1")
        self.MaxIndex = len(self.data.index)

    def card(self,Cardtype,Cardnum):
        self.data = selfdata.sort_values(by=Cardtype, ascending=False)
        self.data.index = range(self.MaxIndex)
        for X in range(Cardnum):
            if self.data.iloc[X, 2] == True:
                self.data.iloc[X, 2] = str(Cardtype + '-' + self.data.iloc[X, 1])

if __name__ == "__main__":
    data = pd.read_excel('slotmap.xlsx',"Sheet1")
    MaxIndex = len(data.index)

    Cardtype = "AI"
    Cardnum = 3
    data = data.sort_values(by=Cardtype,ascending=False)
    data.index = range(MaxIndex)
    for X in range(Cardnum):
        if data.iloc[X,2] == True:
             data.iloc[X,2] = str(Cardtype +'-'+ data.iloc[X,1])

    Cardtype = "AO"
    Cardnum = 3
    data = data.sort_values(by=Cardtype,ascending=False)
    data.index = range(MaxIndex)
    for X in range(Cardnum):
        if data.iloc[X,2] == True:
             data.iloc[X,2] = str(Cardtype +'-'+ data.iloc[X,1])

    #data = data.sort_values(by='AO', ascending=False)
    print(data)
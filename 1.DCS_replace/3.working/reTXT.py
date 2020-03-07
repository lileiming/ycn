# -*- coding:utf-8 -*-
#!/usr/bin/python

import xlrd
import os
import re
import sys
import logging

#==========================================================
path0='./reTXTdir'
path1='./reTXTdir/'

reload(sys)
sys.setdefaultencoding('gbk')
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='reTXT.log',
    filemode='a')
#==========================================================

filename = "replaceExc.xlsx"
filePath = os.path.join(os.getcwd(), filename)
x1 = xlrd.open_workbook(filePath)

sheet1 = x1.sheet_by_name("Sheet1")
rowsNum = sheet1.nrows

print "Number of replacements:", sheet1.nrows #行 16
#print "col num:", sheet1.ncols #列 2 

inValue = []
outValue = []
count = 1
while (count < rowsNum):
   #print 'The count is:', count
   count = count + 1
   in1=sheet1.cell_value(count-1,0).encode('utf-8')
   in1=unicode(in1,"utf-8")
   inValue.append(in1)
   out1=sheet1.cell_value(count-1,1).encode('utf-8')
   out1=unicode(out1,"utf-8")
   outValue.append(out1)


#print inValue
 
def eachFile(filepath):
    pathDir = os.listdir(filepath)
    return pathDir

def readfile(name):
    f1 = open(name,'r+')
    s=f1.read()
    DRfindNum = s.find('DR0')

#======================================================
    f1.seek(0,0)
    line = s.replace (inValue[0],outValue[0])
    num = 1
    while (num < rowsNum):
        line = line.replace (inValue[num-1],outValue[num-1])
        num = num +1
    f1.write(line)
    f1.close()
#======================================================
    if DRfindNum > 0 :
        DR0X = s[DRfindNum+3]
        DR00Y = s[DRfindNum+4]
        DR000Z = s[DRfindNum+5]
        #print "DR0"+DR0X+DR00Y+DR000Z
        flienameNS = path1+"DR0"+DR0X+DR00Y+DR000Z+'.txt'
        repeatName = "DR0"+DR0X+DR00Y+DR000Z+'.txt'
        try:
           os.renames(name,flienameNS)
        except WindowsError,e:
           logging.info(name + u" 因为重名跳过")

                
#======================================================        

if __name__ == "__main__":   
        pathDir = eachFile(path0)
        for allDir in pathDir:
            child = './reTXTdir/' + allDir
            readfile(child)


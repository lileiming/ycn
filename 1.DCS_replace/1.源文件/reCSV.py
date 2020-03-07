# -*- coding:utf-8 -*-
#!/usr/bin/python

import xlrd
import os
import re
import sys
import linecache
import logging

#==========================================================
path0='./reCSVdir'
path1='./reCSVdir/'

reload(sys)
sys.setdefaultencoding('gbk')
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #datefmt='%a, %d %b %Y %H:%M:%S',
    datefmt='%Y %b %d %H:%M:%S',
    filename='reCSV.log',
    filemode='a')
#==========================================================

def reName2txt(path0,path1):

    sys.path.append(path1)
    csvFiles = os.listdir(path0)
    #print('files',csvFiles)

    for csvFilename in csvFiles:
        portion = os.path.splitext(csvFilename)
        if (portion[1] == '.csv'): 
                newname = portion[0] + '.txt' 
                filenamedir=path1 + csvFilename
                newnamedir=path1 + newname
                try:
                    os.rename(filenamedir,newnamedir)
                except WindowsError,e:
                    logging.info(csvFilename + u" 因为重名跳过")
#==========================================================
filename = "replaceExc.xlsx"
inValue = []
outValue = []
count = 1

filePath = os.path.join(os.getcwd(), filename)
x1 = xlrd.open_workbook(filePath)
sheet1 = x1.sheet_by_name("Sheet1")
rowsNum = sheet1.nrows
print "Number of replacements:", sheet1.nrows #行 16
#print "col num:", sheet1.ncols #列 2 
while (count < rowsNum):
   #print 'The count is:', count
   count = count + 1
   in1=sheet1.cell_value(count-1,0).encode('utf-8')
   in1=unicode(in1,"utf-8")
   #print in1
   inValue.append(in1)
   out1=sheet1.cell_value(count-1,1).encode('utf-8')
   out1=unicode(out1,"utf-8")
   print out1
   outValue.append(out1)
#print inValue

#==========================================================
   
def eachFile(filepath):
    pathDir = os.listdir(filepath)
    return pathDir

def readfile(name):
   # print(name)
    f1 = open(name,'r+')
    s=f1.read()
    f1.seek(0,0)
    line = s.replace (inValue[0],outValue[0])
    num = 1
    while (num < rowsNum):
        line = line.replace (inValue[num-1],outValue[num-1])
        num = num +1
    f1.write(line)
    f1.close()
    #====================================================
    NodeSolt = linecache.getline(name,6)
    IOM = NodeSolt[1]
    if (IOM == 'Z' ):
        nodeX = NodeSolt[2]
        nodeY = NodeSolt[3]
        soltX = NodeSolt[4]
        flienameNS = path1+'N'+nodeX+nodeY+'S'+soltX+'.csv'
        repeatName = 'N'+nodeX+nodeY+'S'+soltX+'.csv'
        try:
           os.renames(name,flienameNS)
        except WindowsError,e:
           logging.info(name + u" 因为重名跳过")
            
    if (IOM == 'S' ):
        SWX = NodeSolt[3]
        flienameNS = path1+'SwitchDef'+SWX+'.csv'
        repeatName = 'SwitchDef'+SWX+'.csv'
        try:
           os.renames(name,flienameNS)
        except WindowsError,e:
           logging.info(name + u" 因为重名跳过")
        
    if (IOM == 'A' ):
        ANX = NodeSolt[2]
        flienameNS = path1+'AN'+'.csv'
        repeatName = 'AN'+'.csv'
        try:
           os.renames(name,flienameNS)
        except WindowsError,e:
           logging.info(name + u" 因为重名跳过")

           
#==========================================================
if __name__ == "__main__":
        reName2txt(path0,path1)
        pathDir = eachFile(path1)

        for allDir in pathDir:
            child = './reCSVdir/' + allDir
            readfile(child)


# print('files',csvFiles)




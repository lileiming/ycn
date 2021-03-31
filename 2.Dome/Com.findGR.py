from tkinter import *
# 导入ttk
from tkinter import ttk
from tkinter import filedialog
import os
import re
from time import sleep

var_dir = r'C:\Users\Administrator\Documents\python\shiyan\findEtag\copy'

def get_filelist():
    Filelist = []
    path = var_dir
    for home, dirs, files in os.walk(path):
        for filename in files:
            Filelist.append(os.path.join(home, filename))
    return Filelist

Filelist = get_filelist()

dict_tag = {}
list_tag = ['6200DCC3A40019', '6200DCC3A40061', '6200DCC3A40091','6200DCC3A4006','6200DCC3A40061A']
for tag in list_tag:
    dict_tag[tag] = '0'
#print(dict_tag)

var_num = 0

for var_file_name in Filelist:
    #print(var_file_name)
    with open(var_file_name, 'r', encoding='utf-8') as Maintxt:
        allContent = Maintxt.read()

    for var_tag in list_tag:
        head_find = (re.findall(f'{var_tag}"',allContent))
        #print(len(head_find))
        var_num = int(dict_tag[var_tag]) + len(head_find)
        dict_tag[var_tag] = var_num
# #
print(dict_tag)
# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# **********************************************************
# BK ENG Tool Screenshot command = BKEToolScreenCD
# **********************************************************

import os
import time
#from shutil import copyfile
from cv2 import imread
from cv2 import imwrite

def func_get_file_list():
    list_File_Name = []
    var_src_path = 'C:\CENTUMVP\his\save\\bmp'
    for var_src_home, var_src_dirs, var_src_files in os.walk(var_src_path):
        for var_file_name in var_src_files:
            list_File_Name.append(os.path.join(var_src_home, var_file_name))
        pass
    pass
    return list_File_Name

def command():
    # src = source 源
    # dst = destination 目的

    list_File_Name = func_get_file_list()
    var_dst_path = os.path.join(os.path.expanduser("~/Pictures"), "Screenshots")  # 放到Screenshots子文件夹中
    print(var_dst_path)
    #var_dst_path = os.path.join(os.path.expanduser("\\\Cpc439-da7234\\abc"), "Screenshots")  # 放到Screenshots子文件夹中
    if not os.path.exists(var_dst_path):
        os.mkdir(var_dst_path)
    pass

    for var_file in list_File_Name:

        if '.bmp' in var_file:
            var_file_create = time.localtime(os.path.getctime(var_file))                            #.bmp创建时间
            var_file_create_date = time.strftime("%Y-%m-%d", var_file_create)                       #.bmp创建时间-日期
            var_file_create_time = time.strftime("%H-%M-%S", var_file_create)                       #.bmp创建时间-时分秒
            #print(var_file_create_date,var_file_create_time)

            var_file_basename = os.path.basename(var_file)
            var_split_name = os.path.splitext(var_file_basename)
            var_file_png = f'{var_split_name[0]}.PNG'

            var_dst_path_c = f'{var_dst_path}\\{var_file_create_date}'
            isExists = os.path.exists(var_dst_path_c)
            if not isExists:
                os.makedirs(var_dst_path_c)
            pass

            var_dst_listdir = os.listdir(var_dst_path_c)  # 遍历目标文件已有文件，防止重复

            var_file_new_name = f'{var_dst_path_c}\\{var_file_create_time}_{var_file_png}'
            #print(var_file_new_name)
            if not os.path.exists(var_file_new_name):
            #if f'{var_file_create_time}_{var_file_basename}' not in var_dst_listdir:

                image = imread(var_file, 1)
                img_last = image.copy()
                imwrite(var_file_new_name, img_last)

                #copyfile(var_file, var_file_new_name)  # 复制命令
                print("copying...")
            pass
        pass
    pass

if __name__ == "__main__":
    command()
# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# **********************************************************
# BK ENG Tool Report Move command = BKEToolReportMoveCD
# **********************************************************

import os
import regex as re
from shutil import copyfile
import configparser

# 开始
class DIR_FILE:
    def __init__(self):
        self.func_init_path()
        #self.var_src_path = 'C:\CENTUMVP\his\save\REPORT\HISTORY'
        self.command()

    def func_get_dir_list(self):
        list_dir_Name = [self.var_src_path]
        for var_src_home, var_src_dirs, var_src_files in os.walk(self.var_src_path):
            for var_dir_name in var_src_dirs:
                list_dir_Name.append(os.path.join(var_src_home, var_dir_name))
            pass
        pass
        return list_dir_Name

    def func_get_file_list(self,path):
        list_File_Name = []
        var_src_path = path
        for var_src_home, var_src_dirs, var_src_files in os.walk(var_src_path):
            for var_file_name in var_src_files:
                list_File_Name.append(os.path.join(var_src_home, var_file_name))
            pass
        pass
        return list_File_Name

    def command(self):
        # src = source 源
        # dst = destination 目的
        list_Dir_Name = self.func_get_dir_list()
        for var_dir in list_Dir_Name:
            var_foo = os.path.split(self.var_src_path)[1]+"\\\\"
            regex = re.compile(r'(?<=%s).*'%var_foo)
            var_dir_final = regex.findall(var_dir)
            #var_dir_final = (re.findall(r'(?<=HISTORY\\).*', var_dir))
            var_dst_path = os.path.join(os.path.expanduser(self.var_dst_path_bas))
            if not var_dir_final==[]:
                var_dst_path = os.path.join(os.path.expanduser(self.var_dst_path_bas), var_dir_final[0])  # 放到Screenshots子文件夹中
                # #var_dst_path = os.path.join(os.path.expanduser("\\\Cpc439-da7234\\abc"), "Screenshots")  # 放到其他电脑子文件夹中
                if not os.path.exists(var_dst_path):
                    os.mkdir(var_dst_path)
                pass

            list_File_Name = self.func_get_file_list(var_dir)
            for var_file in list_File_Name:
                var_file_basename = os.path.basename(var_file)
                var_dst_path_c = f'{var_dst_path}'
                var_file_new_name = f'{var_dst_path_c}\\{var_file_basename}'

                if not os.path.exists(var_file_new_name):
                    copyfile(var_file, var_file_new_name)  # 复制命令
                    print("copying...")
                pass
            pass

    def  func_init_path(self):
        try:
            self.cf = configparser.ConfigParser()
            self.cf.read("ReportMove.ini")
            self.var_src_path = self.cf.get('section_1', 'src_path')
            self.var_dst_path_bas = self.cf.get('section_1', 'dst_path')
        except configparser.NoSectionError:
            self.var_src_path = 'C:\CENTUMVP\his\save\REPORT\HISTORY'
            self.var_dst_path_bas = '~/Pictures'
        pass

if __name__ == "__main__":
    DIR_FILE()
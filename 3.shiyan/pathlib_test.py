# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# ==========================================================
#  pathlib 文件管理的模块
#
# ==========================================================

from pathlib import Path

p = Path(r'auto_test.py')
print(p.resolve())                     # 文档显示是absolute path, 这里感觉只能用在获取当前绝对路径上
# WindowsPath('C:\Users\Administrator\Documents\python\3.shiyan\auto_test.py')

p = Path(r'C:\Users\Administrator\Documents\python\3.shiyan\auto_test.py')
print(p.name)                          # 获取文件名
# auto_test.py
print(p.stem)                          # 获取文件名除后缀的部分
# auto_test
print(p.suffix)                        # 文件后缀
# .py
#print(p.suffixs)                       # 文件的后缀们...
# # ['.txt', '.bk']
print(p.parent)                        # 相当于dirnanme
# WindowsPath('C:\Users\Administrator\Documents\python\3.shiyan')
print(p.parents)                       # 返回一个iterable, 包含所有父目录
# <WindowsPath.parents>
for i in p.parents:
    print(i)
# C:\Users\Administrator\Documents\python\3.shiyan
# C:\Users\Administrator\Documents\python
# C:\Users\Administrator\Documents
# C:\Users\Administrator
# C:\Users
# C:\

print(p.parts)                         # 将路径通过分隔符分割成一个元祖
# ('C:\\', 'Users', 'Administrator', 'Documents', 'python', '3.shiyan', 'auto_test.py')

p = Path(r'C:\Users\Administrator\Documents\python\3.shiyan')
p = Path(p, 'auto_test.py')           # 字符串拼接
print(p)
print(f'It exists is {p.exists()}')                      # 判断文件是否存在
print(f'This is a file is {p.is_file()}')                # 判断是否是文件
print(f'This is a folder is {p.is_dir()}')               # 判断是否是目录

# C:\Users\Administrator\Documents\python\3.shiyan\auto_test.py
# It exists is True
# This is a file is True
# This is a folder is False

p = Path(r'C:/Users\Administrator\Documents\python\3.shiyan')  #会自动纠正\ /
print(p)
# WindowsPath('C:\Users\Administrator\Documents\python\3.shiyan')
print(p.iterdir())                     # 相当于os.listdir 遍历所有文件及文件夹
for i in p.iterdir():
    print(i)
print("=======")
# C:\Users\Administrator\Documents\python\3.shiyan\trend
# C:\Users\Administrator\Documents\python\3.shiyan\untitled.py

# p.glob('*.py')                     # 相当于os.listdir, 但是可以添加匹配条件
for i in p.glob('*.py'):
    print(i)
print("=======")
# C:\Users\Administrator\Documents\python\3.shiyan\xianxin.py
# C:\Users\Administrator\Documents\python\3.shiyan\YokoCustomlibrary.py
# C:\Users\Administrator\Documents\python\3.shiyan\YokoRead.py

# p.rglob('*.py')                    # 相当于os.walk, 也可以添加匹配条件
for i in p.rglob('*.py'):
    print(i)
print("=======")
# C:\Users\Administrator\Documents\python\3.shiyan\YokoRead.py
# C:\Users\Administrator\Documents\python\3.shiyan\delTouchTarget\Com.del.TouchTarget.py
# C:\Users\Administrator\Documents\python\3.shiyan\findEtag\findEtag.py
# C:\Users\Administrator\Documents\python\3.shiyan\pyqt_ui\BKEToolBox.py
# C:\Users\Administrator\Documents\python\3.shiyan\pyqt_ui\dome\dome.py

p = Path(r'C:\Users\Administrator\Documents\python\3.shiyan\add')
p.mkdir(exist_ok=True)          # 创建文件目录(前提是add`目录存在, 否则会报错)
# 一般我会使用下面这种创建方法
p.mkdir(exist_ok=True, parents=True) # 递归创建文件目录

p = Path(r'C:\Users\Administrator\Documents\python\3.shiyan\auto_test.py')
print(p.stat())                        # 获取详细信息
print(p.stat().st_size)               # 文件大小
print(p.stat().st_ctime)               # 创建时间
print(p.stat().st_mtime)               # 修改时间

# os.stat_result(st_mode=33206, st_ino=16044073672816648, st_dev=1922266888, st_nlink=1, st_uid=0, st_gid=0, st_size=949, st_atime=1604897357, st_mtime=1605678847, st_ctime=1604897357)
# 949
# 1604897357.7071967
# 1605678847.9771051
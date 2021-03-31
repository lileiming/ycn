
"""
:arg 线性回归 linregress

# https://blog.csdn.net/robert_chen1988/article/details/103551261

#线性

"""

import pandas as pd
import  matplotlib.pyplot as plt
from scipy.stats import linregress

x = [1,2,3,4,5,3.45]
y = [0,3,6,9,12,8]

#datas = pd.read_excel(r'C:\Users\Administrator\Documents\python\3.shiyan\Stock\history_A_stock_k_data.xlsx') # 读取 excel 数据，引号里面是 excel 文件的位置

# x = datas.iloc[:, 0] # 因变量为第 2 列数据
# y = datas.iloc[:, 5]# 自变量为第 3 列数据

print(y)

slope, intercept, r, p, std_err = linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

speed = myfunc(8)
print(r*r)
print(speed)

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()

# list 过滤
# def filterForLi(li):
#   info = ">>>>>使用普通过滤列表<<<<<"
#   print(info)
#   li = [element for element in li if not "Unnamed" in  element]  # int类型没有长度，所以需要首先排除
#   print(li)
#
#
# # 定义一个列表
# #li = [1, 2, 3, 4, 5, "a", "b", "c", "apple", "banana", "orange", "juice"]
# li = ['Unnamed: 0', '位号1', 'Unnamed: 2', '位号', '是否属于不改造内容', 'Unnamed: 5', 'Unnamed: 6']
# filterForLi(li)


"""
:arg 线性回归 linregress

# https://blog.csdn.net/robert_chen1988/article/details/103551261
"""

import pandas as pd
import  matplotlib.pyplot as plt
from scipy.stats import linregress

# x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
# y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

datas = pd.read_excel(r'C:\Users\Administrator\Documents\python\3.shiyan\Stock\history_A_stock_k_data.xlsx') # 读取 excel 数据，引号里面是 excel 文件的位置

x = datas.iloc[:, 0] # 因变量为第 2 列数据
y = datas.iloc[:, 5]# 自变量为第 3 列数据

print(y)

slope, intercept, r, p, std_err = linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

speed = myfunc(20)
print(r*r)
print(speed)

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()

# 参考网页 https://www.php.cn/python-tutorials-442473.html

import pandas as pd


# 方法一：默认读取第一个表单

df = pd.read_excel("C:\\Users\\Administrator\\Documents\\python\\0.输出文件\\ToolTaglist\\ToolTest.xlsx",header = 1)  # 直接默认读取到Excel的第一个表单
#pd.read_excel('filename.xlsx', header = 1)
data = df.head()  # 默认读取前5行的数据

print("获取到所有的值：\n{0}".format(data))  # 格式化输出

# print(data["Address"])
#
# print()

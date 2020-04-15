import re
import os

text_detail = ""

def eachFile(path1):
    detail = ""
    pathDir = os.listdir(path1)
    for allDir in pathDir:
        child = path1 + allDir
        detail = detail + read_txt(child)
    return detail

def read_txt(txt_file_name):
    # 读取txt文档
    with open(txt_file_name, 'r') as file_data:
        file_detail = file_data.read()
    return file_detail

def out_txt(txt_file_name, out_result):
    out_file_name = txt_file_name
    with open(out_file_name, 'w+', encoding='GBK') as out_file:  # 保存为ANSI格式
        out_file.write(out_result)
    pass

text_detail = text_detail + eachFile(r'C:\\Users\\Administrator\\Documents\\python\\shiyan\\findEtag\\txt\\')
find_result = (re.findall(r'(?<=ETAG:1:).*(?=;)', text_detail))
#1:RTAG:1:6200MSC11802A;
find_result = find_result + (re.findall(r'(?<=RTAG:1:).*(?=;)', text_detail))
#find_result.append('%%IITDF1821A') #加入一个重复值
#find_result = list(set(find_result))  #去重

find_result_copy = find_result.copy()
find_result_last = []
for initial in find_result_copy:
    i = re.findall(r'[0-9%]{2,4}[A-Z]+[0-9]{1,3}', initial)
    #i = re.findall(r'[0-9 A-Z %]+(?=-|_)', initial)
    if len(i):
        find_result.pop(find_result.index(initial))
        find_result_last.append(i[0])
    # else:
    #     print('err',initial)
    pass
#print(find_result)
find_result_last.extend(find_result)
find_result_last = list(set(find_result_last))  #去重
#print(find_result_last)


line =''
for _ in find_result_last:
    line = f'{line}\n{_}'
    pass

out_txt('out.txt',line)





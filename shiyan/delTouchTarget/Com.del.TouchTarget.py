import re
child = 'delTouchTarget.txt'

file = open(child,'r+',encoding='utf-8')
fileCsv = file.read()

# find_result_new = ''
find_result = (re.findall(r'<yiapcspvgccdc:TouchTarget([\w\W]*?)</yiapcspvgccdc:TouchTarget>', fileCsv))
ISenable = 'IsEnabled="True"'
new_ISenable = 'IsEnabled="False"'
Visible='Visibility="Visible"'
new_Visible =f'{Visible}\n        {new_ISenable}'
for _ in find_result:
    if new_ISenable not in _:
        print("A1")
        if ISenable in _:
            find_result_new = _.replace(ISenable, new_ISenable, 1)
            pass
        else:
            find_result_new = _.replace(Visible, new_Visible, 1)
            pass
        fileCsv = fileCsv.replace(_, find_result_new, 1)

with open(child, 'w+', encoding='utf-8') as out_file:  # 保存为ANSI格式
    out_file.write(fileCsv)
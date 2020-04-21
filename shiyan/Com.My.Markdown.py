import calendar
from time import sleep,time,strftime,localtime


#3.1|周日|<font color =#FF0000>0H|周末||

def outMarkDown(Year,Month):
    default_txt = '|-|CN19NSA0601|'
    weekday_dict = {0: f'|周一|0H{default_txt}',
                    1: f'|周二|0H{default_txt}',
                    2: f'|周三|0H{default_txt}',
                    3: f'|周四|0H{default_txt}',
                    4: f'|周五|0H{default_txt}',
                    5: f'|周六|<font color =#FF0000>0H|周末||',
                    6: f'|周日|<font color =#FF0000>0H|周末||'}

    WorkRecord = '日期| 星期 |加班时间| 工作内容|工作问题|工作计划\n' \
                 '---|---|---|---|---|---\n'

    month_range = calendar.monthrange(Year, Month) #29,30,31

    for i in range(month_range[1]):
        weekday_ = calendar.weekday(int(Year), int(Month), int(i + 1))
        weekday_value = weekday_dict[weekday_]
        WorkRecord = f'{WorkRecord}{Month}.{(i + 1)}{weekday_value}\n'
        pass

    out_txt("out.txt",WorkRecord)
    pass

def out_txt(txt_file_name, out_result):
    out_file_name = txt_file_name
    with open(out_file_name, 'w+', encoding='GBK') as out_file:  # 保存为ANSI格式
        out_file.write(out_result)
    pass


if __name__ == "__main__":
    Year_ = localtime(time()).tm_year
    Month_ = localtime(time()).tm_mon
    try:
        Year_ = int(input(f"年：默认（{Year_})="))
    except ValueError:
        Year_ = Year_
    pass

    try:
        Month_= int(input(f"月：默认（{Month_})="))
    except ValueError:
        Month_ = Month_
    pass
    print(f"为你输出{Year_}年{Month_}月工作表格。")

    outMarkDown(Year_,Month_)
    pass

# print(f"为你输出{Year_}") 字符串前加 f 可以打印表达式
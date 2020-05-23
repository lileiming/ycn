# -*- coding:utf-8 -*-
#!/usr/bin/python
# python 3.8
# ==========================================================

var_Domain = 1
var_Station =64
try:
    var_Domain = int(input(f"域号：默认（{var_Domain})="))
except ValueError:
    var_Domain = var_Domain
pass

try:
    var_Station = int(input(f"站号：默认（{var_Station})="))
except ValueError:
    var_Station = var_Station
pass


var_Vnet_ip = f'    Vnet ip = 172.16.{var_Domain}.{var_Station}'
var_VnetOpen_ip = f'VnetOPen ip = 192.168.{var_Domain+128}.{var_Station+129}'
var_Enet_ip = f'    Enet ip = 172.17.{var_Domain}.{var_Station}'
var_Domain_str = '{:0>7b}'.format(var_Domain)
var_Station_str = '{:0>7b}'.format(var_Station)

def func_Odd_check(var_str):
    """
    功能块说明：奇校验
    """
    count = 0
    for i in var_str:
        if i == '1' :
            count = count +1
            pass
        else:
            count = count
            pass
    if count % 2 ==1:
        out = '0'
    else:
        out = '1'
    return out

var_Odd_Domain_str = func_Odd_check(var_Domain_str)
var_Odd_Station_str = func_Odd_check(var_Station_str)

out_txt = (f'HIS{"{:0>2d}".format(var_Domain)}{"{:0>2d}".format(var_Station)}的IP地址：\n'
          f'{var_Vnet_ip}\n'
          f'{var_VnetOpen_ip}\n'
          f'{var_Enet_ip}\n'
          f'HIS{"{:0>2d}".format(var_Domain)}{"{:0>2d}".format(var_Station)}的拨码开关：\n'
          f'域的拨码开关 = {var_Odd_Domain_str}{var_Domain_str}\n'
          f'站的拨码开关 = {var_Odd_Station_str}{var_Station_str}')

print(out_txt)



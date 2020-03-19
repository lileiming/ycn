import os
import requests
from bs4 import BeautifulSoup
import win32api, win32con, win32gui


def download_bing_wallpaper(filepath):
    url = "https://cn.bing.com"
    #url = "https://bing.ioliu.cn"
    try:
        r = requests.get(url)
    except:
        print("下载失败，请检查你的网络连接！")
        input("\n请按任意键退出:")
        exit()

    soup = BeautifulSoup(r.text, features="lxml")
    ls = soup.select("link")
    url_img = url + ls[0].attrs["href"]  # 获取图片链接
    jj = ls[0].attrs["href"].split("&")
    j = jj[0].split("=")
    fname = j[1]  # 获取图片文件名
    fjf = soup.select("#sh_cp")
    des = fjf[0].attrs["title"]  # 获取图片描述

    with open(os.path.join(filepath, fname), "wb") as f:
        f.write(requests.get(url_img).content)  # 保存图片
    print(fname)
    print(des)
    return os.path.join(filepath, fname)


def set_wallpaper(filepath):
    """适用于win10系统"""
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, filepath, win32con.SPIF_SENDWININICHANGE)


if __name__ == "__main__":
    subdir = os.path.join(os.path.expanduser("~/Pictures"), "Wallpaper")  # 放到wallpaper子文件夹中
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    #set_wallpaper(download_bing_wallpaper(filepath=subdir))
    download_bing_wallpaper(filepath=subdir)
    input("\n桌面壁纸设置完成，请按任意键退出:")


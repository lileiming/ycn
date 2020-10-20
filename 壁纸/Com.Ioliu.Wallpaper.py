import os
import re
import requests

def func_getHtmlList(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/51.0.2704.63 Safari/537.36'}
        r = requests.get(url, headers = headers, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("err")
        pass

def func_download_wallpaper(filepath,var_pic):
    file_name = var_pic.split('/')[-1]  # 获取图片文件名
    with open(os.path.join(filepath, file_name), "wb") as f:
        f.write(requests.get(var_pic).content)  # 保存图片
    return os.path.join(filepath, file_name)
    pass


if __name__ == "__main__":
    var_page_num = 3
    for var_num in range(var_page_num):
        var_url = f'https://bing.ioliu.cn/?p={var_num + 1}'
        #var_url = f'https://bing.ioliu.cn/ranking?p={var_num + 1}'
        var_text = func_getHtmlList(var_url)
        list_find_result = (re.findall(r'data-progressive="([\w\W]*?)640x480.jpg\?imageslim', var_text))
        list_pic_result = [f'{var_i}1920x1080.jpg' for var_i in list_find_result]

        var_subdir = os.path.join(os.path.expanduser("~/Pictures"), "Wallpaper")  # 放到wallpaper子文件夹中
        if not os.path.exists(var_subdir):
            os.mkdir(var_subdir)
        var_cycles_num = 1
        for var_pic_addr in list_pic_result:
            var_pic_name = var_pic_addr.split('/')[-1]
            print(f'{var_cycles_num + var_num*12}/{var_page_num*12}     {var_pic_name}')
            func_download_wallpaper(filepath = var_subdir, var_pic = var_pic_addr)
            var_cycles_num = var_cycles_num + 1

    input("\n桌面壁纸设置完成，请按任意键退出:")

    # var_url = "https://bing.ioliu.cn/"
    # data-progressive="http://h1.ioliu.cn/bing/BarnOwlMigration_ZH-CN8579914070_640x480.jpg?imageslim"
    # 1920x1080

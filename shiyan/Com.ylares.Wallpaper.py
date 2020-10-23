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
    file_name = 'bing.lylares.com-2020-06-29-4k.jpg'  # 获取图片文件名
    with open(os.path.join(filepath, file_name), "wb") as f:
        f.write(requests.get(var_pic).content)  # 保存图片
    return os.path.join(filepath, file_name)


if __name__ == "__main__":
    var_url = f'https://bing.lylares.com/'
    var_text = func_getHtmlList(var_url)
    #print(var_text)
    list_find_result = (re.findall(r'<a class="text-primary" href="([\w\W]*?)"></i>必应壁纸</a>', var_text))
    print(len(list_find_result))
    # for i in list_find_result:
    #     print(i)
    var_url1 = list_find_result[0]
    var_text1 = func_getHtmlList(var_url1)
    #print(var_text1)
    var_find_result = (re.findall(r'<a class="btn btn-success hd-mb " href="([\w\W]*?)" target="_blank"', var_text1))
    print(var_find_result[0])
    # <a class="btn btn-success hd-mb " href="
    # https://bing.lylares.com/download/4k/2020-06-29?did=c55aebdd3dc7306dbb3b0337f4e72046&amp;t=1593441117&amp;crf=e0df3f9d45d455c258eb69936dadd02e
    # "target="_blank" download="bing.lylares.com-2020-06-29-4k.jpg">

    var_subdir = os.path.join(os.path.expanduser("~/Pictures"), "Wallpaper")  # 放到wallpaper子文件夹中
    if not os.path.exists(var_subdir):
        os.mkdir(var_subdir)
    var_pic_name = 'bing.lylares.com-2020-06-29-4k.jpg'
    func_download_wallpaper(filepath = var_subdir, var_pic = var_find_result[0])

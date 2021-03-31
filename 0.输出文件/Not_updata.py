from subprocess import call
from pip._internal.utils.misc import get_installed_distributions # pip 10 以后没有pip.get...
 
 
for dist in get_installed_distributions():
    call("pip install --upgrade " + dist.project_name + ' -i https://pypi.tuna.tsinghua.edu.cn/simple', shell=True) # 个人自己修改 我的是pip37
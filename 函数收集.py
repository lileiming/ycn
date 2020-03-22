"""
for i,v in enumerate(['A','B','C']):
    print(i,v)
    pass

v = enumerate(['A','B','C'])
print(v.__next__())
print(v.__next__())
"""

import winreg

key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\WOW6432Node\YOKOGAWA\CS3K\HIS")

value, type = winreg.QueryValueEx(key, "pw")

print(value)

#winreg.SetValue(key, "pw", winreg.REG_SZ, "202001")
winreg.SetValueEx(key, "pw", 0, winreg.REG_SZ, "202001")
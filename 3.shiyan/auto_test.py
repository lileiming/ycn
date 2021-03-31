# from pywinauto.application import Application
# app = Application().start("notepad.exe")
#
# app.UntitledNotepad.menu_select("帮助(&H)->关于记事本(A)")
# about_dlg = app.window_(title_re = u"关于", class_name = "#32770")
# about_dlg.print_control_identifiers()
#
# OK = u'确定'
# about_dlg[OK].click()
#
#
# # app.AboutNotepad.OK.click()
# #
# app.UntitledNotepad.Edit.type_keys("pywinauto Works!", with_spaces = True)

# from pywinauto.application import Application
# app = Application().start(u"C:\CENTUMVP\program\BKESysView.exe")
# # app.BKESystemViewClass.menu_select("Help->")
# # about_dlg = app.window_(title_re = u"关于", class_name = "#32770")
# dlg_spec = app['System View (CENTUM VP) - FUNCTION_BLOCK']
# dlg_spec.print_control_identifiers()

from subprocess import Popen
from pywinauto import Desktop

Popen('calc.exe', shell=True)
dlg = Desktop(backend="uia").Calculator
dlg.wait('visible')

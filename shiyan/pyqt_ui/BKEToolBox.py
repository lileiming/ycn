# -*- coding: utf-8 -*-
"""
#=============================

# BK ENG Tool Box = BKEToolBox

# ENG工具箱

#https://blog.csdn.net/shangxiaqiusuo1/article/details/85253264

#=============================
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtWidgets
import BKEToolCopyGraphic  # 复制工具-流程图
import BKEToolCopyFunc  # 复制工具-功能块


class UiMenuWindows(QMainWindow):
    def __init__(self):
        super(UiMenuWindows, self).__init__()
        self.setupUi()

    def setupUi(self):
        """
        Menu界面的ui组态
        """
        self.setObjectName("ENGTools")
        self.resize(570, 460)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setNativeMenuBar(False)   #MacOS
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.Menu1 = QtWidgets.QMenu(self.menubar)
        self.Menu1.setObjectName("Menu1")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.MenuCopy1 = QtWidgets.QAction(self)
        self.MenuCopy1.setObjectName("MenuCopy1")
        self.MenuCopy2 = QtWidgets.QAction(self)
        self.MenuCopy2.setObjectName("MenuCopy2")
        self.Menu1.addAction(self.MenuCopy1)
        self.Menu1.addAction(self.MenuCopy2)
        self.menubar.addAction(self.Menu1.menuAction())
        self.re_translate_Ui()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.function_all_menu_triggered()

    def re_translate_Ui(self):
        """
        中英文翻译
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ENGTools", "组态ENG工具箱 V1.0"))
        self.Menu1.setTitle(_translate("ENGTools", "复制工具"))
        self.MenuCopy1.setText(_translate("ENGTools", "流程图"))
        self.MenuCopy2.setText(_translate("ENGTools", "功能块"))

    def function_all_menu_triggered(self):
        """
        Menu 按钮的跳转链接
        """
        self.MenuCopy1.triggered.connect(lambda: self.slot_btn_function('MenuCopy1'))  # Menu 按钮触发语句
        self.MenuCopy2.triggered.connect(lambda: self.slot_btn_function('MenuCopy2'))
        pass

    def slot_btn_function(self, var_Menu_name):
        """
        Menu 按钮的跳转程序
        """
        self.hide()
        if var_Menu_name == 'MenuCopy1':
            self.Class_Page = MENU_COPY1_SHOW()
            pass
        if var_Menu_name == 'MenuCopy2':
            self.Class_Page = MENU_COPY2_SHOW()
            pass
        self.Class_Page.show()


class MENU_COPY1_SHOW(BKEToolCopyGraphic.Ui, UiMenuWindows):
    """
    MENU_COPY1 复制工具-流程图
    """

    def __init__(self):
        super(MENU_COPY1_SHOW, self).__init__()
        BKEToolCopyGraphic.Ui.__init__(self)

    pass


class MENU_COPY2_SHOW(BKEToolCopyFunc.Execute, UiMenuWindows):
    """
    MENU_COPY2 复制工具-功能块
    """

    def __init__(self):
        super(MENU_COPY2_SHOW, self).__init__()
        BKEToolCopyFunc.Execute.__init__(self)

    pass


def main():
    """
    主线程序
    """
    app = QApplication(sys.argv)
    Windows_UI = UiMenuWindows()
    Windows_UI.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

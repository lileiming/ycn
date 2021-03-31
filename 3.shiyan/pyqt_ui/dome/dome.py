# Menu
# https://www.cnblogs.com/ygzhaof/p/10070523.html

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

class Ui_ENGTools(object):
    def setupUi(self, ENGTools):
        ENGTools.setObjectName("ENGTools")
        ENGTools.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ENGTools)
        self.centralwidget.setObjectName("centralwidget")
        ENGTools.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ENGTools)
        self.menubar.setNativeMenuBar(False)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.Menu1 = QtWidgets.QMenu(self.menubar)
        self.Menu1.setObjectName("Menu1")
        ENGTools.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ENGTools)
        self.statusbar.setObjectName("statusbar")
        ENGTools.setStatusBar(self.statusbar)
        self.MenuCopy1 = QtWidgets.QAction(ENGTools)
        self.MenuCopy1.setObjectName("MenuCopy1")
        self.MenuCopy2 = QtWidgets.QAction(ENGTools)
        self.MenuCopy2.setObjectName("MenuCopy2")
        self.Menu1.addAction(self.MenuCopy1)
        self.Menu1.addAction(self.MenuCopy2)
        self.menubar.addAction(self.Menu1.menuAction())
        self.retranslateUi(ENGTools)
        QtCore.QMetaObject.connectSlotsByName(ENGTools)
        self.MenuCopy1.triggered.connect(self.processtrigger)  # Menu 按钮触发语句

    def retranslateUi(self, ENGTools):
        _translate = QtCore.QCoreApplication.translate
        ENGTools.setWindowTitle(_translate("ENGTools", "ENGTools"))
        self.Menu1.setTitle(_translate("ENGTools", "复制工具"))
        self.MenuCopy1.setText(_translate("ENGTools", "流程图"))
        self.MenuCopy2.setText(_translate("ENGTools", "功能块"))

    def processtrigger(self):
        print('A')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_ENGTools()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
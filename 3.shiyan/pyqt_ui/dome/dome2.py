# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class one(QMainWindow):
    sig_1 = pyqtSignal()

    def __init__(self):
        super(one, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(300, 200)
        self.setWindowTitle('1')
        self.btn_1 = QPushButton(self)
        self.btn_1.setText('Emit')
        self.btn_1.setGeometry(100, 80, 100, 40)
        self.btn_1.clicked.connect(self.slot_btn_1)
        self.sig_1.connect(self.sig_1_slot)

    def slot_btn_1(self):
        self.sig_1.emit()

    def sig_1_slot(self):
        self.t = two()
        self.t.show()


class two(QMainWindow):

    def __init__(self):
        super(two, self).__init__()
        self.resize(500, 100)
        self.setWindowTitle('two')


def ui_main():
    app = QApplication(sys.argv)
    w = one()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':

    ui_main()

    # import sys
    # from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
    # from PyQt5.QtGui import QIcon
    #
    #
    # class App(QWidget):
    #
    #     def __init__(self):
    #         super().__init__()
    #         self.title = 'PyQt5 file dialogs - pythonspot.com'
    #         self.left = 10
    #         self.top = 10
    #         self.width = 640
    #         self.height = 480
    #         self.initUI()
    #
    #     def initUI(self):
    #         self.setWindowTitle(self.title)
    #         self.setGeometry(self.left, self.top, self.width, self.height)
    #
    #         self.openFileNameDialog()
    #         self.openFileNamesDialog()
    #         self.saveFileDialog()
    #
    #         self.show()
    #
    #     def openFileNameDialog(self):
    #         options = QFileDialog.Options()
    #         options |= QFileDialog.DontUseNativeDialog
    #         fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
    #                                                   "All Files (*);;Python Files (*.py)", options=options)
    #         if fileName:
    #             print(fileName)
    #
    #     def openFileNamesDialog(self):
    #         options = QFileDialog.Options()
    #         options |= QFileDialog.DontUseNativeDialog
    #         files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
    #                                                 "All Files (*);;Python Files (*.py)", options=options)
    #         if files:
    #             print(files)
    #
    #     def saveFileDialog(self):
    #         options = QFileDialog.Options()
    #         options |= QFileDialog.DontUseNativeDialog
    #         fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
    #                                                   "All Files (*);;Text Files (*.txt)", options=options)
    #         if fileName:
    #             print(fileName)
    #
    #
    # if __name__ == '__main__':
    #     app = QApplication(sys.argv)
    #     ex = App()
    #     sys.exit(app.exec_())
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.init_ui()

    def init_ui(self):
        # self.resize(500, 350)
        # self.setWindowTitle('First Ui')
        self.btn_1 = QPushButton(self)
        self.btn_1.setText('Emit')
        self.btn_1.setGeometry(100, 100, 100, 40)
        pass
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.init_ui()

    def init_ui(self):
        # self.resize(500, 350)
        # self.setWindowTitle('First Ui')
        self.btn = QPushButton('流程图', self)
        self.btn.setGeometry(50, 100, 100, 50)
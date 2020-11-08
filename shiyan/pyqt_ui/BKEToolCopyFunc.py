from PyQt5.QtWidgets import QMainWindow,QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets

import os
import re
import math
from time import sleep

from YokoCustomlibrary import time_Decorator,thread_Decorator,FILE_NODE

class Ui(QMainWindow,FILE_NODE):
    def __init__(self):
        super(Ui, self).__init__()
        self.init_ui()
        pass

    def init_ui(self):
        #Top_groupBox
        self.Top_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.Top_groupBox.setGeometry(QtCore.QRect(10, 10, 550, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Top_groupBox.setFont(font)
        self.Top_groupBox.setObjectName("Top_groupBox")
        #Top_lineEdit
        self.Top_lineEdit = QtWidgets.QLineEdit(self.Top_groupBox)
        self.Top_lineEdit.setGeometry(QtCore.QRect(10, 23, 431, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Top_lineEdit.sizePolicy().hasHeightForWidth())
        self.Top_lineEdit.setSizePolicy(sizePolicy)
        self.Top_lineEdit.setObjectName("Top_lineEdit")
        #Top_pushButton
        self.Top_pushButton = QtWidgets.QPushButton(self.Top_groupBox)
        self.Top_pushButton.setGeometry(QtCore.QRect(450, 19, 91, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Top_pushButton.sizePolicy().hasHeightForWidth())
        self.Top_pushButton.setSizePolicy(sizePolicy)
        self.Top_pushButton.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setWeight(75)
        self.Top_pushButton.setFont(font)
        self.Top_pushButton.setObjectName("Top_pushButton")
        #Mid_groupBox
        self.Mid_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.Mid_groupBox.setGeometry(QtCore.QRect(10, 80, 550, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Mid_groupBox.setFont(font)
        self.Mid_groupBox.setObjectName("Mid_groupBox")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.Mid_groupBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 431, 30))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        #Mid_lineEdit
        self.Mid_lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mid_lineEdit.sizePolicy().hasHeightForWidth())
        self.Mid_lineEdit.setSizePolicy(sizePolicy)
        self.Mid_lineEdit.setObjectName("Mid_lineEdit")
        self.horizontalLayout_2.addWidget(self.Mid_lineEdit)
        #Mid_comboBox
        self.Mid_comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        self.Mid_comboBox.setObjectName("Mid_comboBox")
        self.horizontalLayout_2.addWidget(self.Mid_comboBox)
        #Mid_pushButton
        self.Mid_pushButton = QtWidgets.QPushButton(self.Mid_groupBox)
        self.Mid_pushButton.setGeometry(QtCore.QRect(450, 20, 91, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mid_pushButton.sizePolicy().hasHeightForWidth())
        self.Mid_pushButton.setSizePolicy(sizePolicy)
        self.Mid_pushButton.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setWeight(75)
        self.Mid_pushButton.setFont(font)
        self.Mid_pushButton.setObjectName("Mid_pushButton")

        #Low_groupBox
        self.Low_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.Low_groupBox.setGeometry(QtCore.QRect(10, 150, 550, 201))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Low_groupBox.setFont(font)
        self.Low_groupBox.setObjectName("Low_groupBox")
        #Low_textEdit
        self.Low_textEdit = QtWidgets.QTextEdit(self.Low_groupBox)
        self.Low_textEdit.setGeometry(QtCore.QRect(10, 20, 531, 171))
        self.Low_textEdit.setObjectName("Low_textEdit")
        #Bottom_line
        self.Bottom_line = QtWidgets.QFrame(self.centralwidget)
        self.Bottom_line.setGeometry(QtCore.QRect(205, 385, 250, 20))
        self.Bottom_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.Bottom_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Bottom_line.setObjectName("Bottom_line")
        #Bottom_label
        self.Bottom_label = QtWidgets.QLabel(self.centralwidget)
        self.Bottom_label.setGeometry(QtCore.QRect(20, 372, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.Bottom_label.setFont(font)
        self.Bottom_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Bottom_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Bottom_label.setObjectName("Bottom_label")
        #Bottom_pushButton
        self.Bottom_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Bottom_pushButton.setGeometry(QtCore.QRect(460, 370, 91, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Bottom_pushButton.sizePolicy().hasHeightForWidth())
        self.Bottom_pushButton.setSizePolicy(sizePolicy)
        self.Bottom_pushButton.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setWeight(75)
        self.Bottom_pushButton.setFont(font)
        self.Bottom_pushButton.setObjectName("Bottom_pushButton")

        #self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.command()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        # self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Bottom_label.setText(_translate("MainWindow", "程序员美德：懒惰、不耐烦、傲慢"))
        self.Bottom_pushButton.setText(_translate("MainWindow", "确定"))
        self.Top_groupBox.setTitle(_translate("MainWindow", "参考文档"))
        self.Top_lineEdit.setPlaceholderText(_translate("MainWindow", "DR_template.txt"))
        self.Top_pushButton.setText(_translate("MainWindow", "参考文档"))
        self.Mid_groupBox.setTitle(_translate("MainWindow", "数据列表"))
        self.Mid_lineEdit.setPlaceholderText(_translate("MainWindow", "modbus.xls"))
        self.Mid_pushButton.setText(_translate("MainWindow", "数据列表"))
        self.Low_groupBox.setTitle(_translate("MainWindow", "结果"))

    def command(self):
        self.Top_pushButton.clicked.connect(lambda: self.openFileNameDialog('Top_txt'))
        self.Mid_pushButton.clicked.connect(lambda: self.openFileNameDialog('Mid_excel'))
        self.Bottom_pushButton.clicked.connect(lambda: self.get_entry())
        pass

    def openFileNameDialog(self,position):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if position == 'Top_txt':
            fileName, _ = QFileDialog.getOpenFileName(self,"打开参考文档", "","All Files (*);;Template Files (*.txt)", options=options)
            if fileName:
                #print(fileName)
                self.Top_lineEdit.setText(fileName)
        if position == 'Mid_excel':
            fileName, _ = QFileDialog.getOpenFileName(self,"打开数据文档", "","All Files (*);;Excel Files (*.xls *.xlsx)", options=options)
            if fileName:
                #print(fileName)
                self.Mid_lineEdit.setText(fileName)
                sheet_Name = self.get_sheet(fileName)
                sheet_Name_T = tuple(sheet_Name)
                self.Mid_comboBox.addItems(sheet_Name_T)

    def text_update(self, show):
        if show == 'START_':
            self.Low_textEdit.append("=============程序开始=============\n")
        elif show == 'STOP_':
            self.Low_textEdit.append("=============程序结束=============\n")
        else:
            self.Low_textEdit.append(show)
            pass
        pass

    @thread_Decorator
    @time_Decorator
    def get_entry(self):
        try:
            sample_PVI = self.Top_lineEdit.text()
            modbus_list = self.Mid_lineEdit.text()
            sheet_list = self.Mid_comboBox.currentText()
            filepath, fullflname = os.path.split(modbus_list)

            # 数据读取
            with open(sample_PVI, 'r') as samplefile:
                sample_content = samplefile.read()
            # 数据剥离
            sample_stripping = (re.findall(r'::FHED\n([\w\W]*)::::SOURCE', sample_content))  # 样本剥离
            sample_stripping_head = (re.findall(r':::SOURCE\n[\w\W]*::FHED\n', sample_content))  # head剥离
            # 剥离结果
            head = sample_stripping_head[0]
            foot = "::::SOURCE"
            self.text_update('START_')
            # ================
            model = 'PVI'
            # ================
            max_num = 0
            limit40 = 40
            for i in self.get_data_2line(modbus_list, sheet_list):
                if 'CHKN' in i:
                    CHKN = i['CHKN']
                    if CHKN > max_num:
                        max_num = CHKN

            page_num = int(max_num / (limit40 + 1)) + 1

            for No_page in range(page_num):
                # 处理开始result_file
                result_DR_filename = f'DR_output{No_page}.txt'
                result_DR = os.path.join(filepath, result_DR_filename)
                result_file = open(result_DR, 'w')
                result_file.write(head)
                for i in self.get_data_2line(modbus_list, sheet_list):
                    ETAG = 'NULL'
                    # ===========参数
                    ### No
                    if 'CHKN' in i:
                        CHKN = i['CHKN']
                        if CHKN <= limit40 * No_page or CHKN > limit40 * (No_page + 1):
                            # break   #跳出for循环 不再执行
                            continue  # 只跳出本次，循环继续执行
                            pass

                        CHKN = CHKN % limit40

                        if CHKN == 0:
                            CHKN = limit40
                            pass

                        in_Value = self.get_linestr(sample_content, model, 'CHKN')
                        out_Value = f':CHKN:1:{CHKN};'
                        result_line = sample_stripping[0].replace(in_Value, out_Value)

                        in_Value = self.get_linestr(sample_content, 'PIO', 'RCHK')
                        out_Value = f':RCHK:1:@{CHKN};'
                        result_line = result_line.replace(in_Value, out_Value)

                        in_Value = self.get_linestr(sample_content, 'PIO', 'GCNC')
                        out_Value = f':GCNC:3:{CHKN}$8,$6,8,AN;'
                        result_line = result_line.replace(in_Value, out_Value)
                        ### 位置
                        if 0 < CHKN < limit40 + 1:
                            PVIX = 50
                            PVIY = 100
                            CHKNX = CHKN % 10
                            if CHKNX != 0:
                                COW = math.floor(CHKN / 10)
                                PVIX = int(CHKNX * 150 - 100)
                                PVIY = 100 + COW * 200
                            if CHKNX == 0:
                                COW = math.floor(CHKN / 10) - 1
                                PVIX = 9 * 150 + 50
                                PVIY = 100 + COW * 200
                            in_Value = self.get_linestr(sample_content, model, 'GBLK')
                            out_Value = f':GBLK:{PVIX},{PVIY}:S1;'
                            result_line = result_line.replace(in_Value, out_Value)
                            PIOX = PVIX - 36
                            PIOY = PVIY + 120
                            in_Value = self.get_linestr(sample_content, 'PIO', 'GBLK')
                            out_Value = f':GBLK:{PIOX},{PIOY}:S1:$5;'
                            result_line = result_line.replace(in_Value, out_Value)
                        ### Name
                        if 'ETAG' in i:
                            ETAG = i['ETAG']
                            in_Value = self.get_linestr(sample_content, 'PIO', 'RCNC')
                            # out_Value = f':RCNC:1::{ETAG}.OUT:I;'
                            out_Value = f':RCNC:1::{ETAG}.IN:O;'
                            result_line = result_line.replace(in_Value, out_Value)
                        ### PIO地址
                        if 'CNCT' in i:
                            CNCT = i['CNCT']
                            in_Value = self.get_linestr(sample_content, 'PIO', 'RTAG')
                            out_Value = f':RTAG:1:{CNCT};'
                            result_line = result_line.replace(in_Value, out_Value)

                        ### 多个数据类型
                        index_A = ['ETCM', 'EUNT', 'ESCL', 'SSI!', 'CNCT', 'ETAG']
                        index_B = [f':ETCM:1:{i[index_A[0]]};',
                                   f':EUNT:1:{i[index_A[1]]};',
                                   f':ESCL:1:{i[index_A[2]]};',
                                   f':SSI!:1:{i[index_A[3]]}:106.25:-6.25;',
                                   f':CNCT:1:IN:{i[index_A[4]]}:I;',
                                   f':ETAG:1:{i[index_A[5]]};']

                        def multi_process(indexA, indexB, lineC):
                            multu_line = lineC
                            for item in range(len(indexA)):
                                if index_A[item] in i:
                                    multi_in_Value = self.get_linestr(sample_content, model, indexA[item])
                                    multu_line = multu_line.replace(multi_in_Value, indexB[item])
                                pass
                            return multu_line

                        result_line = multi_process(index_A, index_B, result_line)
                        ### 写入文件
                        result_file.write(result_line)
                        pass
                    ### Text显示
                    self.text_update(f">>>{ETAG}\n")
                result_file.write(foot)
                self.text_update(f"=============导出文件:{str(result_DR_filename)}\n")

            # self.e.set("复制结束：结果已输出至 DR_output.txt")
            self.text_update('STOP_')
        except FileNotFoundError as e:
            self.text_update(e)
        except UnicodeDecodeError as e:
            self.text_update(e)
        sleep(2)
        pass

    def get_linestr(self, ds, model, CODE):
        furm = ['PVI', 'SI-1ALM']
        fref = ['PIO']
        find_all_str = ''
        if model in furm:
            find_all_str = r':FNRM\n([\w\W]*)::FNRM'
            for _ in re.split(r'[\n]\s*', re.findall(find_all_str, ds)[0]):
                if CODE in _:
                    find_all_str = re.findall(r'(:[\w\W]*;)', str(_))[0]
                pass
            pass
        pass
        if model in fref:
            find_all_str = r':FREF\n([\w\W]*?)::FREF'
            for find_at in re.findall(find_all_str, ds):
                # print(find_at)
                if "@1" in find_at:
                    for _ in re.split(r'[\n]\s*', find_at):
                        if CODE in _:
                            find_all_str = re.findall(r'(:[\w\W]*;)', str(_))[0]
                        pass
                    pass
                pass
                if "@2" in find_at:
                    print("@2")
                pass
            pass
        pass
        return find_all_str
        pass
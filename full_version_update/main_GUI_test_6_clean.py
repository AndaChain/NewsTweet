from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtGui import*

from main_backend_test6nof import main
from manage_file import ManageFile

import time
import pandas
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from mpl_finance import candlestick_ohlc
import plotly.graph_objects as go
from datetime import timedelta, datetime

class Ui_MainWindow(QMainWindow, main):
    class pandasModel(QAbstractTableModel):
        def __init__(self, data):
            QAbstractTableModel.__init__(self)
            self._data = data

        def rowCount(self, parent=None):
            return self._data.shape[0]

        def columnCount(self, parnet=None):
            return self._data.shape[1]

        def data(self, index, role=Qt.DisplayRole):
            if index.isValid():
                if role == Qt.DisplayRole:
                    return str(self._data.iloc[index.row(), index.column()])
            return None

        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self._data.columns[col]
            return None

    class Worker_twitter(QObject):
        finished = pyqtSignal()
        progress = pyqtSignal(pandas.core.frame.DataFrame ,pandas.core.frame.DataFrame, pandas.core.frame.DataFrame, str, str)
        def __init__(self, lang, count, text_input, since_gui, until_gui, type_work, type_data):
            super().__init__()
            self.lang = lang
            self.count = count
            self.text_input = text_input
            self.since_gui = since_gui
            self.until_gui = until_gui
            self.type_work = type_work
            self.type_data = type_data

        def run(self):
            # DATA
            ########################################################################################
            start6 = time.time()
            Main = main()
            Main.run_twitter(self.lang, self.count, self.text_input, self.since_gui, self.until_gui)
            df_1 = Main.ranking_twitter(self.text_input, self.lang)
            df_2 = Main.sentiment_show_twi()
            df_map = Main.geometry_map(self.text_input, self.lang)

            print(time.time() - start6, "Backend Twitter")
            ########################################################################################
            
            # --------------Map--------------------------
            Ui_MainWindow.polt_map(Ui_MainWindow, df_map)
            # -------------------------------------------
            
            self.progress.emit(df_1, df_2, df_map, self.type_work, self.type_data)
            self.finished.emit()

    class Worker_webcrawler(QObject):
        finished = pyqtSignal()
        progress = pyqtSignal(pandas.core.frame.DataFrame, pandas.core.frame.DataFrame, pandas.core.frame.DataFrame, str, str)
        def __init__(self, lang, text_input, since_gui, until_gui, type_work, type_data):
            super().__init__()
            self.lang = lang
            self.text_input = text_input
            self.since_gui = since_gui
            self.until_gui = until_gui
            self.type_work = type_work
            self.type_data = type_data

        def run(self):
            # DATA
            ###############################################################################
            start6 = time.time()
            Main = main()
            Main.run_webcrawler(self.lang, self.text_input, self.since_gui, self.until_gui)
            df_1 = Main.ranking_webcrawler(self.text_input, self.lang)
            df_2 = Main.sentiment_show_web()
            #print(self.text_input, self.lang)
            df_3 = Main.ranking_domain(self.text_input, self.lang)
            #df_map = self.geometry_map(self.text_input, self.lang)
            print(time.time() - start6, "Backend Webcrawler")
            ###############################################################################
            self.progress.emit(df_1, df_2, df_3, self.type_work, self.type_data)
            self.finished.emit()

    def __init__(self):
        start = time.time()
        super().__init__()

        #self.df_hit = self.hit_trends_show()

        self.check_thread_1 = [True]
        self.check_thread_2 = [True]

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 635)
        MainWindow.setMinimumSize(QtCore.QSize(1300, 735))
        MainWindow.setMaximumSize(QtCore.QSize(1300, 735))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        now_day = str(datetime.now()).split(" ")[0]
        now_day = now_day.split("-")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(10, 50, 151, 22))
        self.dateEdit.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.dateEdit.setCalendarPopup(True)
        #self.dateEdit.setTimeSpec(QtCore.Qt.TimeZone)
        self.dateEdit.setDate(QtCore.QDate( int(now_day[0]), int(now_day[1]), int(now_day[2]) ))
        self.dateEdit.setObjectName("dateEdit")
        
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_2.setGeometry(QtCore.QRect(170, 50, 141, 22))
        self.dateEdit_2.setTime(QtCore.QTime(0, 0, 1))
        self.dateEdit_2.setCalendarPopup(True)
        #self.dateEdit_2.setTimeSpec(QtCore.Qt.LocalTime)
        self.dateEdit_2.setDate(QtCore.QDate( int(now_day[0]), int(now_day[1]), int(now_day[2]) ))
        self.dateEdit_2.setObjectName("dateEdit_2")

        self.textBrowser_6 = QtWidgets.QTextBrowser(self.centralwidget) # ranking
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.textBrowser_6.setGeometry(QtCore.QRect(200, 110, 889, 371))
        self.textBrowser_6.hide()

        self.textBrowser_6_2 = QtWidgets.QTextBrowser(self.centralwidget) # ranking type two web
        self.textBrowser_6_2.setObjectName("textBrowser_6_2")
        self.textBrowser_6_2.setGeometry(QtCore.QRect(644, 110, 444, 371))
        self.textBrowser_6_2.hide()

        self.textBrowser_6_3 = QtWidgets.QTextBrowser(self.centralwidget) # ranking type two web
        self.textBrowser_6_3.setObjectName("textBrowser_6_3")
        self.textBrowser_6_3.setGeometry(QtCore.QRect(200, 110, 444, 371))
        self.textBrowser_6_3.hide()

        self.textBrowser_7 = QtWidgets.QTextBrowser(self.centralwidget) # sentiment
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.textBrowser_7.setGeometry(QtCore.QRect(200, 110, 889, 371))
        self.textBrowser_7.hide()

        self.textBrowser_7_2 = QtWidgets.QTextBrowser(self.centralwidget) # sentiment type two web
        self.textBrowser_7_2.setObjectName("textBrowser_7_2")
        self.textBrowser_7_2.setGeometry(QtCore.QRect(644, 110, 444, 371))
        self.textBrowser_7_2.hide()

        self.textBrowser_7_3 = QtWidgets.QTextBrowser(self.centralwidget) # sentiment type two web
        self.textBrowser_7_3.setObjectName("textBrowser_7_3")
        self.textBrowser_7_3.setGeometry(QtCore.QRect(200, 110, 444, 371))
        self.textBrowser_7_3.hide()

        self.textBrowser_8 = QtWidgets.QTextBrowser(self.centralwidget) # stock
        self.textBrowser_8.setObjectName("textBrowser_8")
        self.textBrowser_8.setGeometry(QtCore.QRect(200, 110, 889, 371))
        self.textBrowser_8.hide()

        # ปุ่ม
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(210, 110, 60, 30))
        self.pushButton_5.setObjectName("pushButton_5") # sentiment
        self.pushButton_5.hide()
        self.pushButton_5_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5_2.setGeometry(QtCore.QRect(654, 110, 60, 30))
        self.pushButton_5_2.setObjectName("pushButton_5_2") # sentiment
        self.pushButton_5_2.hide()
        self.pushButton_5_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5_3.setGeometry(QtCore.QRect(210, 110, 60, 30))
        self.pushButton_5_3.setObjectName("pushButton_5_3") # sentiment
        self.pushButton_5_3.hide()

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(270, 110, 60, 30))
        self.pushButton_6.setObjectName("pushButton_6") # ranking
        self.pushButton_6.hide()
        self.pushButton_6_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6_2.setGeometry(QtCore.QRect(714, 110, 60, 30))
        self.pushButton_6_2.setObjectName("pushButton_6_2") # ranking
        self.pushButton_6_2.hide()
        self.pushButton_6_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6_3.setGeometry(QtCore.QRect(270, 110, 60, 30))
        self.pushButton_6_3.setObjectName("pushButton_6_3") # ranking
        self.pushButton_6_3.hide()

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(330, 110, 60, 30))
        self.pushButton_7.setObjectName("pushButton_7") # stock
        self.pushButton_7.hide()

        print(time.time() - start)

    def setupUi(self, MainWindow, count):
        self.count = count

        self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox2.setGeometry(QtCore.QRect(790, 0, 61, 25))
        self.comboBox2.setObjectName("comboBox2")
        self.comboBox2.addItem("")
        self.comboBox2.addItem("")
        self.comboBox2.addItem("")

        self.line_edit()
        self.push_button()
        self.text_browser()
        self.labeles()

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_6.setFont(font)
        self.label_6.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def line_edit(self):
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(410, 0, 180, 31))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit2.setGeometry(QtCore.QRect(600, 0, 180, 31))
        self.lineEdit2.setObjectName("lineEdit2")

        self.lineEdit3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit3.setGeometry(QtCore.QRect(1000, 0, 180, 31))
        self.lineEdit3.setObjectName("lineEdit3")

    def push_button(self):
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 0, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.clickme) # clicked
        self.pushButton.setEnabled(self.check_thread_1[0] and self.check_thread_2[0])

        #self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        #self.pushButton_2.setGeometry(QtCore.QRect(320, 40, 81, 31))
        #self.pushButton_2.setObjectName("pushButton_2")
        #self.pushButton_2.clicked.connect(self.clickme_update) # clicked

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(1000, 40, 180, 31))
        self.pushButton_4.setObjectName("pushButton_4") # stock
        self.pushButton_4.clicked.connect(self.create_graph_stock_2) # clicked

        # ปุ่มเปลียน
        self.pushButton_5.clicked.connect(self.clickme_ranking_one) # clicked
        self.pushButton_5_2.clicked.connect(self.clickme_ranking_two)
        self.pushButton_5_3.clicked.connect(self.clickme_ranking_three)

        self.pushButton_6.clicked.connect(self.clickme_sentiment_one) # clicked
        self.pushButton_6_2.clicked.connect(self.clickme_sentiment_two)
        self.pushButton_6_3.clicked.connect(self.clickme_sentiment_three)

        self.pushButton_7.clicked.connect(self.clickme_stock_one) # clicked

    def text_browser(self):

        self.tableView_3 = QTableView(self.centralwidget)
        self.tableView_3.setGeometry(QtCore.QRect(1100, 440, 181, 271))
        self.tableView_3.setObjectName("tableView_3")

        self.tableView = QTableView(self.centralwidget)
        
        self.tableView.setGeometry(QtCore.QRect(10, 440, 191, 271)) #บ่อย
        self.tableView.setObjectName("tableView")


        self.tableView_4 = QTableView(self.centralwidget)
        self.tableView_4.setGeometry(QtCore.QRect(1100, 110, 191, 271)) # domain
        self.tableView_4.setObjectName("tableView_4")

        self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_4.setGeometry(QtCore.QRect(200, 520, 891, 191)) # map
        self.textBrowser_4.setObjectName("textBrowser_4")

    def labeles(self):
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 410, 191, 21)) # บ่อย
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1100, 410, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_3.setLineWidth(1)
        self.label_3.setMidLineWidth(0)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.tableView_2 = QTableView(self.centralwidget)
        self.tableView_2.setGeometry(QtCore.QRect(10, 110, 191, 271))
        self.tableView_2.setObjectName("tableView_2")

        df = self.hit_trends_show()
        self.model_2 = self.pandasModel(df)
        self.tableView_2.setModel(self.model_2)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 80, 891, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_4.setFont(font)
        self.label_4.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(200, 490, 891, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_5.setFont(font)
        self.label_5.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")



        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 0, 301, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_6.setFont(font)
        self.label_6.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 20, 151, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_7.setFont(font)
        self.label_7.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(170, 20, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_8.setFont(font)
        self.label_8.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(1100, 80, 191, 21)) # domain
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_10.setFont(font)
        self.label_10.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")

        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(410, 40, 180, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_11.setFont(font)
        self.label_11.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")

        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(600, 40, 180, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_12.setFont(font)
        self.label_12.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")


        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.label.setText(_translate("MainWindow", "พูดคำนี้ด้วย \"บ่อย\""))
        self.label_2.setText(_translate("MainWindow", "Hit! twitter"))
        self.label_3.setText(_translate("MainWindow", "Hit! keyword"))
        self.label_4.setText(_translate("MainWindow", "Graph"))
        self.label_5.setText(_translate("MainWindow", "Map"))
        self.dateEdit.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.dateEdit_2.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.label_6.setText(_translate("MainWindow", "กำหนดเวลา"))
        self.label_7.setText(_translate("MainWindow", "ตั้งแต่"))
        self.label_8.setText(_translate("MainWindow", "ถึง"))
        self.label_10.setText(_translate("MainWindow", "Website ที่พูดถึง"))
        self.label_11.setText(_translate("MainWindow", "Twitter"))
        self.label_12.setText(_translate("MainWindow", "Website"))

        self.comboBox2.setItemText(0, _translate("MainWindow", "EN"))
        self.comboBox2.setItemText(1, _translate("MainWindow", "TH"))
        self.comboBox2.setItemText(2, _translate("MainWindow", "ALL"))

        """self.comboBox3.setItemText(0, _translate("MainWindow", "EN"))
        self.comboBox3.setItemText(1, _translate("MainWindow", "TH"))
        self.comboBox3.setItemText(2, _translate("MainWindow", "ALL"))"""

        #self.pushButton_2.setText(_translate("MainWindow", "UpdateData"))
        self.pushButton_4.setText(_translate("MainWindow", "Go stock!"))
        self.pushButton_5.setText(_translate("MainWindow", "Ranking"))
        self.pushButton_6.setText(_translate("MainWindow", "Sentiment"))
        self.pushButton_7.setText(_translate("MainWindow", "Stock"))

        self.pushButton_5_2.setText(_translate("MainWindow", "Ranking"))
        self.pushButton_6_2.setText(_translate("MainWindow", "Sentiment"))

        self.pushButton_5_3.setText(_translate("MainWindow", "Ranking"))
        self.pushButton_6_3.setText(_translate("MainWindow", "Sentiment"))

    # -------------------------------------------------------------------------------------------------------------
    def create_piechart_ranking(self, data, type_work, type_data):
        se = QPieSeries()

        for i,j in zip(data['keyword'][:10],data['number'][:10]):
            se.append(i,int(j))
        chart = QChart()
        chart.addSeries(se)
        chart.legend().setFont(QtGui.QFont("Arial", 12))
        chart.setTitle("พูดคำนี้ด้วย \"บ่อย\" Pie Chart")
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,700,700)
        chartview.setRenderHint(QPainter.Antialiasing)

        path = ManageFile("GUI_show").path.replace("\\", "/")

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save(f"{path}/a.png", "PNG")

        if(type_work == "one"):
            self.textBrowser_6.setStyleSheet(f'border-image:url({path}/a.png);')
            self.textBrowser_7.hide()
            self.textBrowser_6_2.hide()
            self.textBrowser_7_2.hide()
            self.textBrowser_7_3.hide()

            self.textBrowser_6.show()

        elif(type_work == "two" and type_data == "Twitter"):
            self.textBrowser_6_3.setStyleSheet(f'border-image:url({path}/a.png);')
            self.textBrowser_6.hide()
            self.textBrowser_7.hide()
            self.textBrowser_6_2.hide()
            self.textBrowser_7_2.hide()
            self.textBrowser_7_3.hide()

            self.textBrowser_6_3.show()

        elif(type_work == "two" and type_data == "Webcrawler"):
            self.textBrowser_6_2.setStyleSheet(f'border-image:url({path}/a.png);')
            self.textBrowser_6.hide()
            self.textBrowser_7.hide()
            self.textBrowser_7_2.hide()
            self.textBrowser_7_3.hide()

            self.textBrowser_6_2.show()

    def create_piechart_sentiment(self, data, type_work, type_data):
        se = QPieSeries()

        for i,j in zip(data['sentiment'],data['number']):
            se.append(i,int(j))
        chart = QChart()
        chart.addSeries(se)
        chart.legend().setFont(QtGui.QFont("Arial", 27))
        chart.setTitle("พูดคำนี้ด้วย \"บ่อย\" Pie Chart")
        chartview = QChartView(chart)
        chartview.setGeometry(0,0,700,700)
        chartview.setRenderHint(QPainter.Antialiasing)

        path = ManageFile("GUI_show").path.replace("\\", "/")

        self.savepi = QPixmap(chartview.grab())
        self.savepi.save(f"{path}/a.png", "PNG")

        if(type_work == "one"):
            self.textBrowser_7.setStyleSheet(f'border-image:url({path}/a.png);')
            self.textBrowser_6.hide()
            self.textBrowser_6_2.hide()
            self.textBrowser_7_2.hide()
            self.textBrowser_6_3.hide()
            self.textBrowser_7_3.hide()

            self.textBrowser_7.show()
        elif(type_work == "two" and type_data == "Twitter"):
            self.textBrowser_7_3.setStyleSheet(f'border-image:url({path}/a.png);')
            self.textBrowser_6.hide()
            self.textBrowser_7.hide()
            self.textBrowser_6_2.hide()
            self.textBrowser_7_2.hide()
            self.textBrowser_6_3.hide()

            self.textBrowser_7_3.show()
        elif(type_work == "two" and type_data == "Webcrawler"):
            self.textBrowser_7_2.setStyleSheet(f'border-image:url({path}/a.png);')
            self.textBrowser_6.hide()
            self.textBrowser_7.hide()
            self.textBrowser_6_2.hide()
            self.textBrowser_7_3.hide()

            self.textBrowser_7_2.show()

    def create_graph_stock_2(self):

        self.pushButton_5.show()
        self.pushButton_6.show()
        self.pushButton_7.show()

        since = str(self.dateEdit.date().toPyDate())
        until = str(self.dateEdit_2.date().toPyDate())
        self.stock(self.lineEdit3.text(), since, until)

        plt.style.use('ggplot')

        # Extracting Data for plotting
        data = pandas.read_csv('GUI_show/stock.csv')
        ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
        ohlc['Date'] = pandas.to_datetime(ohlc['Date'])
        ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
        ohlc['SMA5'] = ohlc['Close'].rolling(5).mean()
        ohlc = ohlc.astype(float)

        # Creating Subplots
        fig, ax = plt.subplots()
        ax.plot(ohlc['Date'], ohlc['SMA5'], color='green', label='SMA5')


        candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

        # Setting labels & titles
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        fig.suptitle('Chart Stock of '+str(self.lineEdit3.text()))
        plt.legend()

        # Formatting Date
        date_format = mpl_dates.DateFormatter('%d-%m-%Y')
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()

        fig.tight_layout()

        path = ManageFile("GUI_show").path.replace("\\", "/")
        plt.savefig(f"{path}/stock.png")

        self.textBrowser_8.clear()
        self.textBrowser_8.setStyleSheet(f'border-image:url({path}/stock.png);')

    def polt_map(self, df):
        print("start Map")
        start6 = time.time()
        fig = go.Figure(go.Scattergeo())
        fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})

        print("start Figure")
        fig = go.Figure(data=go.Scattergeo(
                lon = df['long'],
                lat = df['lati'],
                text = df['places'],
                mode = 'markers'
                ))
        print("start file")
        path = ManageFile("GUI_show").path.replace("\\", "/")
        print("write_image")
        fig.write_image(f"{path}/map.png")
        print(path)

        print(time.time()-start6, "Map")

    def set_format_time(self, time):
        if(time.day < 10):
            if(time.month < 10):
                #print(f"{time.year}-0{time.month}-0{time.day}")
                return f"{time.year}-0{time.month}-0{time.day}"
            else:
                #print(f"{time.year}-{time.month}-0{time.day}")
                return f"{time.year}-{time.month}-0{time.day}"
        else:
            if(time.month < 10):
                #print(f"{time.year}-0{time.month}-{time.day}")
                return f"{time.year}-0{time.month}-{time.day}"
            else:
                #print(f"{time.year}-{time.month}-{time.day}")
                return f"{time.year}-{time.month}-{time.day}"

    def check_thread_fun1(self, type_work):
        if(type_work == "one"):
            self.check_thread_1[0] = True
            self.check_thread_2[0] = True
            self.pushButton.setEnabled(self.check_thread_1[0] and self.check_thread_2[0])
        else:
            self.check_thread_1[0] = True
            self.pushButton.setEnabled(self.check_thread_1[0] and self.check_thread_2[0])

    def check_thread_fun2(self, type_work):
        if(type_work == "one"):
            self.check_thread_1[0] = True
            self.check_thread_2[0] = True
            self.pushButton.setEnabled(self.check_thread_1[0] and self.check_thread_2[0])
        else:
            self.check_thread_2[0] = True
            self.pushButton.setEnabled(self.check_thread_1[0] and self.check_thread_2[0])

    def data_twitter(self, type_work, type_data):
        # RUN twitter
        self.text_input = self.input_twitter
        print(self.text_input)

        # DATA
        self.thread_2 = QThread()
        self.worker_2 = self.Worker_twitter(self.lang, self.count, self.text_input, self.since_gui, self.until_gui, type_work, type_data)
        self.worker_2.moveToThread(self.thread_2)
        self.thread_2.started.connect(self.worker_2.run)
        self.worker_2.finished.connect(self.thread_2.quit)
        self.worker_2.finished.connect(self.worker_2.deleteLater)
        self.thread_2.finished.connect(self.thread_2.deleteLater)
        self.worker_2.progress.connect(self.show_data_twitter)

        self.thread_2.start()
        self.pushButton.setEnabled(False)
        self.check_thread_1[0] = False
        self.thread_2.finished.connect(lambda : self.check_thread_fun2(type_work))

    def show_data_twitter(self, df_1, df_2, df_map, type_work, type_data):

        # Clear
        if(type_work == "one"):
            clear_df = pandas.DataFrame(columns=['time','header', 'content', 'link'])
            model = self.pandasModel(clear_df)
            self.tableView_3.setModel(model)

            clear_df = pandas.DataFrame(columns=["keyword", "number"])
            model = self.pandasModel(clear_df)
            self.tableView_4.setModel(model)

        # SHOW
        start6 = time.time()
        ########################################################################################
        self.model = self.pandasModel(df_1[:10]) # ranking
        self.tableView.setModel(self.model)
        self.create_piechart_ranking(df_1, type_work, type_data)
        self.create_piechart_sentiment(df_2, type_work, type_data)

        # *****map*****
        path = ManageFile("GUI_show").path.replace("\\", "/")
        self.textBrowser_4.clear()
        self.textBrowser_4.setStyleSheet(f'border-image:url({path}/map.png);')
        # *************
        ########################################################################################
        print(time.time()-start6, "Show Twitter")
        print(time.time() - self.start, "Done")

    def data_webcrawler(self, type_work, type_data):
        # RUN crawler
        self.text_input = self.input_web
        print(self.text_input)

        self.thread = QThread()
        self.worker = self.Worker_webcrawler(self.lang, self.text_input, self.since_gui, self.until_gui, type_work, type_data)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.show_data_webcrawler)

        self.thread.start()
        self.pushButton.setEnabled(False)
        self.check_thread_2[0] = False
        self.thread.finished.connect(lambda : self.check_thread_fun1(type_work))

    def show_data_webcrawler(self, df_1, df_2, df_3, type_work, type_data):

        # Clear 
        if(type_work == "one"):
            clear_df = pandas.DataFrame(columns=['time', 'content', 'places'])
            model = self.pandasModel(clear_df)
            self.tableView.setModel(model)
            self.textBrowser_4.clear()
        # SHOW
        start6 = time.time()
        ###############################################################################
        self.model_3 = self.pandasModel(df_1[:10])
        self.model_4 = self.pandasModel(df_3) # domain
        self.tableView_3.setModel(self.model_3)
        self.tableView_4.setModel(self.model_4)
        self.create_piechart_ranking(df_1, type_work, type_data)
        self.create_piechart_sentiment(df_2, type_work, type_data)
        ###############################################################################
        print(time.time()-start6, "Show Webcrawler")
        print(time.time() - self.start, "Done")

    def clickme(self):
        self.start = time.time()

        self.lang = self.comboBox2.currentText().lower()
        self.input_twitter = self.lineEdit.text().lower()
        self.input_web = self.lineEdit2.text().lower()
        self.since_gui = str(self.dateEdit.date().toPyDate())
        self.until_gui = str(self.dateEdit_2.date().toPyDate())

        if(self.input_twitter == ""):
            self.pushButton_5_2.hide()
            self.pushButton_5_3.hide()
            self.pushButton_6_2.hide()
            self.pushButton_6_3.hide()
            self.pushButton_7.hide()
            self.data_webcrawler("one", "Webcrawler")
            self.pushButton_5.show()
            self.pushButton_6.show()
            self.pushButton_7.show()

        elif(self.input_web == ""):
            self.pushButton_5_2.hide()
            self.pushButton_5_3.hide()
            self.pushButton_6_2.hide()
            self.pushButton_6_3.hide()
            self.pushButton_7.hide()
            self.data_twitter("one", "Twitter")
            self.pushButton_5.show()
            self.pushButton_6.show()
            self.pushButton_7.show()
        elif(self.input_web != "" and self.input_twitter != ""):
            self.pushButton_5.hide()
            self.pushButton_6.hide()
            self.pushButton_7.hide()

            self.data_webcrawler("two", "Webcrawler")
            self.data_twitter("two", "Twitter")
            

            self.pushButton_5_2.show()
            self.pushButton_5_3.show()
            self.pushButton_6_2.show()
            self.pushButton_6_3.show()
            self.pushButton_7.show()

        else:
            self.data_twitter("one", "Twitter")

    def clickme_sentiment_one(self):
        self.textBrowser_6.hide()
        self.textBrowser_8.hide()

        self.textBrowser_7.show()

    def clickme_ranking_one(self):
        self.textBrowser_7.hide()
        self.textBrowser_8.hide()

        self.textBrowser_6.show()

    def clickme_sentiment_two(self):
        self.textBrowser_6_2.hide()
        self.textBrowser_8.hide()

        self.textBrowser_7_2.show()

    def clickme_ranking_two(self):
        self.textBrowser_7_2.hide()
        self.textBrowser_8.hide()

        self.textBrowser_6_2.show()

    def clickme_sentiment_three(self):
        self.textBrowser_6_3.hide()
        self.textBrowser_8.hide()

        self.pushButton_5_2.show()
        self.pushButton_6_2.show()

        self.textBrowser_7_3.show()

    def clickme_ranking_three(self):
        self.textBrowser_7_3.hide()
        self.textBrowser_8.hide()

        self.pushButton_5_2.show()
        self.pushButton_6_2.show()

        self.textBrowser_6_3.show()

    def clickme_stock_one(self):
        self.textBrowser_6.hide()
        self.textBrowser_7.hide()
        self.textBrowser_6_2.hide()
        self.textBrowser_7_2.hide()
        self.textBrowser_6_3.hide()
        self.textBrowser_7_3.hide()

        self.pushButton_5_2.hide()
        self.pushButton_6_2.hide()

        self.textBrowser_8.show()

    def clickme_update(self):
        logic = QMessageBox.question(self, 'MessageBox', "ต้องการ Update หรือไม่?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        self.lang = self.comboBox2.currentText().lower()

        since = str(self.dateEdit.date().toPyDate())
        until = str(self.dateEdit_2.date().toPyDate())
        #print(since, until)

        if(logic == QMessageBox.Yes):
            self.update_program( self.lang, self.count, self.lineEdit.text().lower(), since, until)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv) #1
    MainWindow = QMainWindow() #2

    ui = Ui_MainWindow() #3
    ui.setupUi(MainWindow, 50) #4

    MainWindow.show()
    sys.exit(app.exec_())

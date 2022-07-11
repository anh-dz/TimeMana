import sys
import time
import random
import json

from PyQt6.QtCore import QTimer, Qt, QThread
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt6.QtGui import QIntValidator, QIcon, QPixmap
from win10toast_click import ToastNotifier
from datetime import datetime, timedelta
from main import *
from PyQt6.QtCharts import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis, QBarSeries, QValueAxis
from os import startfile, system

from . other import *
from . dataTim import *
from . createFileStartup import *

class Settings(QThread):
    def run(self):
        self.allowEdit = False
        with open(f"C://Users//{user}//AppData//Roaming//TimeMana//settings.json", "r") as openfile:
            self.data = json.load(openfile)
        wgs.btnEdit.clicked.connect(self.saveEdit)
        wgs.btnReset.clicked.connect(self.resetSettings)
        wgs.lineSetting_1.setValidator(QIntValidator())

    def saveEdit(self):
        allow = QIcon()
        allow.addPixmap(QPixmap("assert/allow edit.png"), QIcon.Mode.Normal, QIcon.State.Off)
        notAllow = QIcon()
        notAllow.addPixmap(QPixmap("assert/not allow edit.png"), QIcon.Mode.Normal, QIcon.State.Off)
        if self.allowEdit == False:
            self.allowEdit = True
            wgs.btnEdit.setIcon(allow)
            wgs.lineSetting_1.setReadOnly(False)
            wgs.checkBox_1.setEnabled(True)
            wgs.checkBox_2.setEnabled(True)
            wgs.checkBox_3.setEnabled(True)
        else:
            with open(f"C://Users//{user}//AppData//Roaming//TimeMana//settings.json", "w") as outfile:
                self.data["alarmDur"] = int(wgs.lineSetting_1.text())
                self.data["startWithSys"] = wgs.checkBox_1.isChecked()
                self.data["openUI"] = wgs.checkBox_2.isChecked()
                self.data["sound"] = wgs.checkBox_3.isChecked()
                json.dump(self.data, outfile)
            self.allowEdit = False
            wgs.btnEdit.setIcon(notAllow)
            wgs.lineSetting_1.setReadOnly(True)
            wgs.checkBox_1.setDisabled(True)
            wgs.checkBox_2.setDisabled(True)
            wgs.checkBox_3.setDisabled(True)
            self.start_with_active(self.data["startWithSys"])

    def resetSettings(self):
        with open(f"C://Users//{user}//AppData//Roaming//TimeMana//settings.json", "w") as outfile:
            self.data["alarmDur"] = 30
            self.data["startWithSys"] = False
            self.data["openUI"] = True
            self.data["sound"] = True
            json.dump(self.data, outfile)
            wgs.lineSetting_1.setText(str(self.data["alarmDur"]))
            wgs.checkBox_1.setChecked(self.data["startWithSys"])
            wgs.checkBox_2.setChecked(self.data["openUI"])
            wgs.checkBox_3.setChecked(self.data["sound"])

    def start_with_active(self, startWithSys):
        if startWithSys:
            create_shortcut()
        else:
            delete_file("Microsoft//Windows//Start Menu//Programs//Startup//TimeMana.lnk")

class alarmClock(QThread):
    def __init__(self):
        super(alarmClock, self).__init__()
        self._isRunning = True

    def run(self):
        with open(f"C://Users//{user}//AppData//Roaming//TimeMana//settings.json", "r") as openfile:
            self.data = json.load(openfile)
            self.alarmDur = self.data["alarmDur"]
            self.turn_hourd_mind(self.alarmDur)
            self.set_next_alarm()
        while self._isRunning:
            with open(f"C://Users//{user}//AppData//Roaming//TimeMana//settings.json", "r") as openfile:
                time.sleep(0.1)
                self.data = json.load(openfile)
                newDur = self.data["alarmDur"]
            if newDur != self.alarmDur:
                self.alarmDur = newDur
                self.turn_hourd_mind(self.alarmDur)
                self.set_next_alarm()
            timeNow = datetime.now()
            if self.nextAlarm == timeNow.strftime("%Y-%b-%d %H:%M:%S"):
                self.alarm_call()
                self.nextAlarm = (timeNow + timedelta(hours=self.hourd, minutes=self.mind)).strftime("%Y-%b-%d %H:%M:%S")

    def set_next_alarm(self):
        self.nextAlarm = (datetime.now() + timedelta(hours=self.hourd, minutes=self.mind)).strftime("%Y-%b-%d %H:%M:%S")

    def turn_hourd_mind(self, minutes):
        self.hourd = minutes // 60
        self.mind = minutes % 60

    def alarm_call(self):
        toaster = ToastNotifier()
        toaster.show_toast(
            "TimeMana", # title
            "Bạn đã vất vả rồi, hãy dành chút thời gian uống nước và vận động thôi nào",
            icon_path="logo.ico",
            duration=7,
            threaded=True,
            callback_on_click=self.open_app
        )

    def open_app(self):
        #mainwindows.show()
        if mainwindows.windowState() == Qt.WindowState.WindowMinimized:
            mainwindows.setWindowState(Qt.WindowState.WindowNoState)

    def stop(self):
        self._isRunning = False

class ClockMana:
    def __init__(self, widgets: ViewControl):
        global wgs
        wgs = widgets
        self.widgets = widgets   
        self.widgets.label.setText("00:00:00")
        if create_folder():
            default_data()
            
        with open(f'C://Users//{user}//AppData//Roaming//TimeMana//tim.json', 'r') as openfile:
            self.data = json.load(openfile)
        
        with open(f'C://Users//{user}//AppData//Roaming//TimeMana//day.json', 'r') as openfile:
            self.day = json.load(openfile)
        
        #Lay du lieu
        if self.data["last day"] != datetime.today().strftime('%A'):
            self.data_day2()
            self.widgets.label.setText("00:00:00")
            self.save_time()

        self.my_qtimer = QTimer()
        # self.widget_counter_int = None
        self.current_page = 0
        self.widgets.btnAbout.clicked.connect(self.switch_about)
        self.widgets.btnSetting.clicked.connect(self.switch_setting)
        self.chartIndex = 0
        self.widgets.btnPrevious.clicked.connect(self.previous_chart)
        self.widgets.btnNext.clicked.connect(self.next_chart)
        #self.widgets.btnQuestion.clicked.connect(lambda: system("hdsd.pdf"))
        self.widgets.btnQuestion.clicked.connect(lambda: startfile("hdsd.pdf"))

        self.widgets.btnFa.clicked.connect(lambda:  QDesktopServices.openUrl(QUrl("https://www.facebook.com/timemana")))
        self.widgets.btnIg.clicked.connect(lambda:  QDesktopServices.openUrl(QUrl("https://www.instagram.com/_timemana/")))

        self.seconds = 0
        self.hours = 0
        self.minutes = 0
        #self.widgets.textEdit.setAlignment(Qt.AlignHCenter)
        self.time = datetime.now()
        self.widgets.btnStart.clicked.connect(self.timer_start)

        self.widgets.textAdvise.setFont(QFont('MS Shell Dlg 2', 11))

            
        self.settings = Settings()
        self.settings.start()

        self.remove_week()
        self.widgets.label.setText(self.data["last time"])
        self.create_all_bar()
        self.onoff = False       
        
    def switch_about(self):
        if self.current_page != 1:
            self.current_page = 1
            self.widgets.stackedWidget.setCurrentIndex(1)
        else:
            self.current_page = 0
            self.widgets.stackedWidget.setCurrentIndex(0)

    def switch_setting(self):
        if self.current_page != 2:
            with open(f"C://Users//{user}//AppData//Roaming//TimeMana//settings.json", "r") as openfile:
                self.dataSettings = json.load(openfile)
                self.widgets.lineSetting_1.setText(str(self.dataSettings["alarmDur"]))
                self.widgets.checkBox_1.setChecked(self.dataSettings["startWithSys"])
                self.widgets.checkBox_2.setChecked(self.dataSettings["openUI"])
                self.widgets.checkBox_3.setChecked(self.dataSettings["sound"])
            self.current_page = 2
            self.widgets.stackedWidget.setCurrentIndex(2)
        else:
            self.current_page = 0
            self.widgets.stackedWidget.setCurrentIndex(0)

    def arrows(self):
        back_off = QIcon()
        back_off.addPixmap(QPixmap("assert/back off.png"), QIcon.Mode.Normal, QIcon.State.Off)
        back = QIcon()
        back.addPixmap(QPixmap("assert/back.png"), QIcon.Mode.Normal, QIcon.State.Off)
        right_off = QIcon()
        right_off.addPixmap(QPixmap("assert/right off.png"), QIcon.Mode.Normal, QIcon.State.Off)
        right = QIcon()
        right.addPixmap(QPixmap("assert/right.png"), QIcon.Mode.Normal, QIcon.State.Off)
        if self.chartIndex == 0:
            self.widgets.btnPrevious.setIcon(back_off)
        elif self.chartIndex == 2:
            self.widgets.btnNext.setIcon(right_off)
        else:
            self.widgets.btnPrevious.setIcon(back)
            self.widgets.btnNext.setIcon(right)

    def previous_chart(self):
        if self.chartIndex != 0:
            self.chartIndex -= 1
            self.arrows()
            self.widgets.chartStackedWidget.setCurrentIndex(self.chartIndex)

    def next_chart(self):
        if self.chartIndex != 2:
            self.chartIndex += 1
            self.arrows()
            self.widgets.chartStackedWidget.setCurrentIndex(self.chartIndex)

    def timer_start(self):
        if self.onoff == False:
            self.onoff = True
            self.widgets.btnStart.setIcon(QtGui.QIcon(QtGui.QPixmap("assert/pause light mode.png")))
            self.alarm = alarmClock()
            self.alarm.start()
        else:
            self.onoff = False
            self.widgets.btnStart.setIcon(QtGui.QIcon(QtGui.QPixmap("assert/start light mode.png")))
            self.alarm.stop()
        data = self.widgets.label.text()
        list = data.split(":")

        second = int(list[2])
        minute = int(list[1])
        hour = int(list[0])

        #calculate total seconds
        if second >= 0 or minute >= 0 or hour >= 0:
            self.total_seconds = hour * 3600 + minute * 60 + second
            self.my_qtimer.timeout.connect(self.timer_calculate)
            if self.onoff == True:
                self.my_qtimer.start(1000)
            else:
                self.my_qtimer.disconnect()

    def timer_calculate(self):
        self.total_seconds += 1
        self.hours = self.total_seconds // 3600
        total_seconds_for_minutes_and_seconds = self.total_seconds - (self.hours * 3600)
        self.minutes = total_seconds_for_minutes_and_seconds // 60
        self.seconds = total_seconds_for_minutes_and_seconds - (self.minutes * 60)
        if self.total_seconds <= 0:
            self.my_qtimer.disconnect()
        self.update_timer()
        
        if self.time.hour == 0 and self.time.minute == 0 and self.time.second == 0:            
            self.data_day1()
            self.remove_week()
            self.widgets.label.setText("00:00:00")
            self.create_all_bar()
            
    def update_timer(self):
        self.widgets.label.setText("{:02d}:{:02d}:{:02d}".format(int(self.hours),
                                                                int(self.minutes),
                                                                int(self.seconds)))
        #self.widgets.label.setAlignment(Qt.AlignHCenter)
    
    def save_time(self):
        self.data['last time'] = self.widgets.label.text()
        self.data['last day'] = datetime.today().strftime('%A')
        with open(f"C://Users//{user}//AppData//Roaming//TimeMana//tim.json", "w") as outfile:
            json.dump(self.data, outfile)

    def data_day1(self):
        self.yesterday = datetime.today() - timedelta(days=1)
        self.date = self.yesterday.strftime('%A')
        self.current_time = self.widgets.label.text()
        self.day["5"][self.date] = int(self.current_time[:2])
        with open(f"C://Users//{user}//AppData//Roaming//TimeMana//day.json", "w") as outfile:
            json.dump(self.day, outfile)
    
    def data_day2(self):
        self.current_time = self.widgets.label.text()
        self.day["5"][self.data["last day"]] = int(self.current_time[:2])
        with open(f"C://Users//{user}//AppData//Roaming//TimeMana//day.json", "w") as outfile:
            json.dump(self.day, outfile)
            
    def remove_week(self):
        if datetime.today().strftime('%A') == "Monday":
            self.day["1"] = self.day["2"]
            self.day["2"] = self.day["3"]
            self.day["3"] = self.day["4"]
            self.day["4"] = self.day["5"]
            self.day["5"] = dict.fromkeys(self.day["5"], 0)
            
    def create_bar1(self):
        self.gridLayout = QGridLayout(self.widgets.widgetChart1)
        self.chart1 = QBarSet("Giờ")
        self.chart1 << self.day["5"]["Monday"] << self.day["5"]["Tuesday"] << self.day["5"]["Wednesday"] << self.day["5"]["Thursday"] << self.day["5"]["Friday"] << self.day["5"]["Saturday"] << self.day["5"]["Sunday"]
        self.series1 = QBarSeries()
        self.series1.append(self.chart1)
        
        self.bar_chart1 = QChart()
        self.bar_chart1.addSeries(self.series1)
        self.bar_chart1.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.bar_chart1.setTitle("Ngọn lửa nhiệt huyết của bạn trong tuần")
     
        #self.axisX = QBarCategoryAxis()
        
        self.categories1 = ("Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ nhật")
        self.axisX = QBarCategoryAxis()
        self.axisX.append(self.categories1)
        self.bar_chart1.addAxis(self.axisX, Qt.AlignmentFlag.AlignBottom)
        self.series1.attachAxis(self.axisX)
        
        self.axisY = QValueAxis()
        
        self.bar_chart1.addAxis(self.axisY, Qt.AlignmentFlag.AlignLeft)
        self.series1.attachAxis(self.axisY)
        
        self.axisY.applyNiceNumbers()
        
        self.chartview_chart = QChartView(self.bar_chart1)
        if self.gridLayout.count():
            self.gridLayout.itemAt(0).widget().setParent(None)
        self.gridLayout.addWidget(self.chartview_chart)

    def create_bar2(self):
        self.gridLayout = QGridLayout(self.widgets.widgetChart2)
        self.chart2 = QBarSet("Giờ")
        self.data1 = (self.day["3"]["Monday"] + self.day["3"]["Tuesday"] + self.day["3"]["Wednesday"] + self.day["3"]["Thursday"] + self.day["3"]["Friday"] + self.day["3"]["Saturday"] + self.day["3"]["Sunday"]) / 7
        self.data2 = (self.day["4"]["Monday"] + self.day["4"]["Tuesday"] + self.day["4"]["Wednesday"] + self.day["4"]["Thursday"] + self.day["4"]["Friday"] + self.day["4"]["Saturday"] + self.day["4"]["Sunday"]) / 7
        self.quote = trietlycuocsong
        self.quote_data = random.choice(self.quote)
        if self.data1 == 0:
            self.widgets.textAdvise.setText("")
        else:
            self.percent = abs(int((self.data2-self.data1)/self.data1*100))
            if self.data1 > self.data2:
                self.widgets.textAdvise.setText(f'- Tuần trước, bạn đã học ít hơn tuần trước nữa {self.percent}%. \n- Hãy uống nước, vận động để giữ gìn sức khỏe. \n- "{self.quote_data}"')
            elif self.data1 < self.data2:
                self.widgets.textAdvise.setText(f'- Tuần trước, bạn đã học nhiều hơn tuần trước nữa {self.percent}%. \n- Hãy uống nước, vận động để giữ gìn sức khỏe. \n- "{self.quote_data}"')
        self.chart2 << self.data1 << self.data2
        self.series2 = QBarSeries()
        self.series2.append(self.chart2)
        
        self.bar_chart2 = QChart()
        self.bar_chart2.addSeries(self.series2)
        self.bar_chart2.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.bar_chart2.setTitle("So sánh sự cố gắng của bạn trong hai tuần gần nhất")
        
        self.categories1 = ("Tuần 1", "Tuần 2")
        self.axisX = QBarCategoryAxis()
        self.axisX.append(self.categories1)
        self.bar_chart2.addAxis(self.axisX, Qt.AlignmentFlag.AlignBottom)
        self.series2.attachAxis(self.axisX)
        
        self.axisY = QValueAxis()
        
        self.bar_chart2.addAxis(self.axisY, Qt.AlignmentFlag.AlignLeft)
        self.series2.attachAxis(self.axisY)
        
        self.axisY.applyNiceNumbers()
        
        self.chartview_chart = QChartView(self.bar_chart2)
        if self.gridLayout.count():
            self.gridLayout.itemAt(0).widget().setParent(None)
        self.gridLayout.addWidget(self.chartview_chart)
    
    def create_bar3(self):
        self.gridLayout = QGridLayout(self.widgets.widgetChart3)
        self.chart3 = QBarSet("Giờ")
        self.data1 = (self.day["1"]["Monday"] + self.day["1"]["Tuesday"] + self.day["1"]["Wednesday"] + self.day["1"]["Thursday"] + self.day["1"]["Friday"] + self.day["1"]["Saturday"] + self.day["1"]["Sunday"]) / 7
        self.data2 = (self.day["2"]["Monday"] + self.day["2"]["Tuesday"] + self.day["2"]["Wednesday"] + self.day["2"]["Thursday"] + self.day["2"]["Friday"] + self.day["2"]["Saturday"] + self.day["2"]["Sunday"]) / 7
        self.data3 = (self.day["3"]["Monday"] + self.day["3"]["Tuesday"] + self.day["3"]["Wednesday"] + self.day["3"]["Thursday"] + self.day["3"]["Friday"] + self.day["3"]["Saturday"] + self.day["3"]["Sunday"]) / 7
        self.data4 = (self.day["4"]["Monday"] + self.day["4"]["Tuesday"] + self.day["4"]["Wednesday"] + self.day["4"]["Thursday"] + self.day["4"]["Friday"] + self.day["4"]["Saturday"] + self.day["4"]["Sunday"]) / 7
        self.chart3 << self.data1 << self.data2 << self.data3 << self.data4
        self.series3 = QBarSeries()
        self.series3.append(self.chart3)
        
        self.bar_chart3 = QChart()
        self.bar_chart3.addSeries(self.series3)
        self.bar_chart3.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.bar_chart3.setTitle("Sự nhiệt huyết của bạn trong 4 tuần gần nhất")
        
        self.categories1 = ("Tuần 1", "Tuần 2", "Tuần 3", "Tuần 4")
        self.axisX = QBarCategoryAxis()
        self.axisX.append(self.categories1)
        self.bar_chart3.addAxis(self.axisX, Qt.AlignmentFlag.AlignBottom)
        self.series3.attachAxis(self.axisX)
        
        self.axisY = QValueAxis()
        
        self.bar_chart3.addAxis(self.axisY, Qt.AlignmentFlag.AlignLeft)
        self.series3.attachAxis(self.axisY)
        
        self.axisY.applyNiceNumbers()
        
        self.chartview_chart = QChartView(self.bar_chart3)
        if self.gridLayout.count():
            self.gridLayout.itemAt(0).widget().setParent(None)
        self.gridLayout.addWidget(self.chartview_chart)
        
    def create_all_bar(self):
        self.create_bar1()
        self.create_bar2()
        self.create_bar3()

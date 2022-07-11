# TIME MANA 1.0 OPEN SOURCE
# OS: WINDOWS 10
#
# DEVELOPER: TEAM 7
# LEADER: NGUYEN MAI NHAT ANH
# CODER: LUU VIET BACH, HAN HUU DANG
# DESIGNER: DINH THI PHUONG ANH
# RESEARCHER: PHAN MINH DUY
#
# COPYRIGHT 2022 TIMEMANA

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from view.tm import *
from control.tmcontrol import *
from view.conFrontEnd import *
import sys

class ViewControl(Ui_MainWindow):
    def __init__(self):
        super().__init__()

class MainApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

app = QApplication(sys.argv)
mainwindows = MainApp()

def main():
    fixBackground()

    widgets = ViewControl()
    widgets.setupUi(mainwindows)
    
    about(widgets)

    model_obj = ClockMana(widgets)
    mainwindows.show()
    app.exec()

    model_obj.save_time()

if __name__ == '__main__':
    main()

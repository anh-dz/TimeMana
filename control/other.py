import os
import json
from win32com.client import Dispatch
from . dataTim import *

def delete_file(file):
	if os.path.exists(f'C://Users//{user}//AppData//Roaming//{file}'):
		os.remove(f'C://Users//{user}//AppData//Roaming//{file}')

def create_shortcut():    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(f'C://Users//{user}//AppData//Roaming//Microsoft//Windows//Start Menu//Programs//Startup//TimeMana.lnk')

    currentDir = os.path.abspath(os.path.dirname(__file__))
    wDir = os.path.dirname(currentDir)
    shortcut.Targetpath = wDir + "\\TimeMana.exe"
    #shortcut.Targetpath = wDir + "\\main.py"
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = wDir + "\\logo.ico"
    shortcut.save()

def default_data():
    day = {"1": {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0},
                "2": {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0},
                "3": {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0},
                "4": {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0},
                "5": {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}}
    data = {"last time": "00:34:10", "last day": "Thursday"}
    settings_data = {"alarmDur": 30, "startWithSys": False, "openUI": True, "sound": True}
    with open(f"C://Users//{user}//AppData//Roaming//TimeMana//settings.json", "w") as outfile:
        json.dump(settings_data, outfile)
    with open(f"C://Users//{user}//AppData//Roaming//TimeMana//tim.json", "w") as outfile:
        json.dump(data, outfile)
    with open(f"C://Users//{user}//AppData//Roaming//TimeMana//day.json", "w") as outfile:
         json.dump(day, outfile)

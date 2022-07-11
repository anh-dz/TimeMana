import os
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

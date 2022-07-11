# BUGS:
# Slow app, take too much memory

import os
from main import *

def fixBackground():
  # os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%
  # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

  # path = 'assert/Background.png'
  # os.path.getsize(path) // 1024 // 1024 #Get Size Path
  # r = QtGui.QImageReader(path)
  # r.read()

  os.environ['QT_IMAGEIO_MAXALLOC'] = "1490" # FIX Problem for Show Background -> 1490MB

def about(widgets):
  with open('about.html', 'r', encoding='utf-8') as f:
    text = f.read()
    widgets.textBrowser.setHtml(text)
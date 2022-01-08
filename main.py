import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar, QCheckBox
)
import os

from MainWindow import MainWindow, CONFIG_PATH

if not os.path.isdir(os.path.dirname(CONFIG_PATH)):
    os.mkdir(os.path.dirname(CONFIG_PATH))

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

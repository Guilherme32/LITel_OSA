import sys
from traceback import format_exception
from PyQt6.QtWidgets import (
    QMessageBox, QApplication,
    QLabel, QToolBar, QStatusBar, QCheckBox
)
import os

from MainWindow import MainWindow, CONFIG_PATH

if not os.path.isdir(os.path.dirname(CONFIG_PATH)):
    os.mkdir(os.path.dirname(CONFIG_PATH))


def except_hook(type_, value, traceback):
    sys.__excepthook__(type_, value, traceback)

    dialog = QMessageBox()
    dialog.setWindowTitle("Erro")

    text = "".join(format_exception(type_, value, traceback))

    dialog.setText(text)
    dialog.exec()

    sys.exit(-1)


sys.excepthook = except_hook

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

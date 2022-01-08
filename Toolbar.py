import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar, QCheckBox
)
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt, QSize


class WindowWithToolbar(QMainWindow):
    def __init__(self):
        super().__init__()

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        config = QAction(QIcon("assets/gear.png"), "&Configurações", self)
        config.triggered.connect(self.open_config)
        config.setShortcut(QKeySequence("Ctrl+p"))
        toolbar.addAction(config)

    def open_config(self):
        pass

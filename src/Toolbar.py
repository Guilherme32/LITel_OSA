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

        config = QAction(QIcon("../assets/gear.png"), "&Configurações", self)
        config.triggered.connect(self.open_config)
        config.setShortcut(QKeySequence("Ctrl+p"))
        toolbar.addAction(config)

        calibrate = QAction(QIcon("../assets/thermometer--pencil.png"),
                            "C&alibrar", self)
        calibrate.triggered.connect(self.open_calibration)
        calibrate.setShortcut(QKeySequence("Ctrl+l"))
        toolbar.addAction(calibrate)

        split = QAction(QIcon("../assets/application-split-tile.png"),
                        "&Dividir janela", self)
        split.triggered.connect(self.split_window)
        split.setShortcut(QKeySequence("Ctrl+d"))
        toolbar.addAction(split)

    def open_config(self):
        pass

    def open_calibration(self):
        pass

    def split_window(self):
        pass

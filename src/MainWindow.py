import pandas as pd
import json
from time import time
import os
from PyQt6 import QtGui

from PlotWidget import PlotWidget
from Toolbar import WindowWithToolbar
from Loader import FileLoader
import processing
from OptionsDialog import OptionsDialog, CONFIG_PATH, DEFAULT
from Calibration1 import CalibrationWindow1
from Calibration2 import CalibrationWindow2, LAST_MODEL


class MainWindow(WindowWithToolbar):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LITel OSA")
        self.setWindowIcon(QtGui.QIcon('../assets/window_icon.png'))

        self.plot_widget = PlotWidget()
        self.setCentralWidget(self.plot_widget)

        self.show()

        self.start_time = time()
        self.spectra_info = pd.DataFrame()

        self.options = {}
        self.load_options()

        self.loader = FileLoader(self.entry_loaded,
                                 path=self.options['spectra_path'])

        if os.path.exists(LAST_MODEL):
            with open(LAST_MODEL, "r") as file:
                self.last_calibrated = json.load(file)
        else:
            self.last_calibrated = None

    def open_config(self):
        dialog = OptionsDialog(self)
        dialog.exec()
        self.on_change_options()

    def open_calibration(self):
        self.loader.pause()

        dialog = CalibrationWindow1(self)
        dialog.exec()

        if dialog.close_reason != "close":
            calibration_model = dialog.current_option
            dialog = CalibrationWindow2(calibration_model, self.options, self)
            dialog.exec()

        self.loader.resume()

    def on_change_options(self):
        self.load_options()
        self.loader.reset_config(path=self.options['spectra_path'])

    def load_options(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as file:
                self.options = json.load(file)
        else:
            self.options = DEFAULT

    def entry_loaded(self, spectrum):
        print('.', end='')

        if self.last_calibrated:
            a = self.last_calibrated["last_calibration"]["a"]
            b = self.last_calibrated["last_calibration"]["b"]
            reference = self.last_calibrated["last_calibration"]["ref"]
            function = lambda x: a * (x - reference) + b
        else:
            function = lambda x: x

        spectrum, info = processing.process(spectrum, self.options, function=function)
        info['time'] = time() - self.start_time

        info['index'] = 0
        self.spectra_info = pd.concat([self.spectra_info, pd.DataFrame([info,])], ignore_index=True)
        # self.spectra_info = processing.reorganize_valleys(self.spectra_info)

        processing.plot(spectrum,
                        self.plot_widget.axs,
                        self.spectra_info,
                        self.options)

        self.plot_widget.add_text()
        self.plot_widget.canvas.figure.canvas.draw()

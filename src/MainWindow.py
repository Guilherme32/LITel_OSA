import numpy as np
import pandas as pd
import json
from time import time
import os
from PyQt6 import QtGui
from PyQt6.QtWidgets import QMessageBox

from PlotWidget import PlotWidget
from Toolbar import WindowWithToolbar
from Loader import FileLoader
import processing
from OptionsDialog import OptionsDialog
from Calibration1 import CalibrationWindow1
from Calibration2 import CalibrationWindow2
from MultiWindow import PlotWindow

from Definitions import LAST_MODEL, CONFIG_PATH, DEFAULT_OPTIONS


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
        self.resolution = 0
        self.plot_windows = []

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

    def split_window(self):
        self.close_windows()

        valleys = len([x for x in self.spectra_info.columns if
                       "resonant_wl_power" in x])

        if valleys <= 1:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Erro")
            dlg.setText("Devem haver pelo menos 2 vales para dividir")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.exec()
            return

        for i in range(valleys):
            low_limit = self.spectra_info[f"resonant_wl_{i}"].iloc[-1] - \
                        (self.options["valley_width"]//2) * self.resolution
            low_limit = max(low_limit, self.options["wl_range"][0])

            high_limit = self.spectra_info[f"resonant_wl_{i}"].iloc[-1] + \
                         (self.options["valley_width"]//2) * self.resolution
            high_limit = min(high_limit, self.options["wl_range"][1])

            self.plot_windows.append(PlotWindow((low_limit, high_limit), i+1))

    def close_windows(self):
        for window in self.plot_windows:
            window.close()
        self.plot_windows = []

    def on_change_options(self):
        self.load_options()
        self.loader.reset_config(path=self.options['spectra_path'])

    def load_options(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as file:
                self.options = json.load(file)
        else:
            self.options = DEFAULT_OPTIONS

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
        self.resolution = abs(spectrum[1, 0] - spectrum[0, 0])

        info['index'] = 0
        self.spectra_info = pd.concat([self.spectra_info, pd.DataFrame([info,])], ignore_index=True)
        # self.spectra_info = processing.reorganize_valleys(self.spectra_info)

        processing.plot(spectrum,
                        self.plot_widget.axs,
                        self.spectra_info,
                        self.options)

        self.plot_widget.add_text()
        self.plot_widget.canvas.figure.canvas.draw()

        for window in self.plot_windows:
            window.plot(spectrum, self.spectra_info, self.options)


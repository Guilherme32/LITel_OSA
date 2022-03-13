import os

import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout
from PyQt6 import QtCore
from creator.calibrate_2 import Ui_CalibrationWindow2
import json
from math import ceil
from Loader import FileLoader
import processing
from time import time
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from PlotWidget import PlotWidget
from copy import deepcopy

from Definitions import MODELS_PATH, LAST_MODEL


class PlotWindow(QMainWindow):
    def __init__(self, limits, index, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(f"LITel OSA {index}")
        self.plot_widget = PlotWidget()
        self.setCentralWidget(self.plot_widget)
        self.show()

        self.closed = False

        self.limits = limits

    def closeEvent(self, a0):
        self.closed = True

    def plot(self, spectrum, info, _options):
        if self.closed:
            return

        options = deepcopy(_options)

        options["wl_range"] = self.limits

        valleys = len([x for x in info.columns if 'resonant_wl_power' in x])

        good_valleys = []
        for i in range(valleys):
            if self.limits[0] <= info[f"resonant_wl_{i}"].iloc[-1] <= self.limits[1]:
                good_valleys.append(i)
            else:
                info = info.drop([f"resonant_wl_{i}", f"resonant_wl_power_{i}"], axis=1)

        if not good_valleys:
            return      # Se não achou nada, não atualiza o plot

        name_map = {f"resonant_wl_{good_valleys[i]}": f"resonant_wl_{i}" for i in
                    range(len(good_valleys))}
        name_map |= {f"resonant_wl_power_{good_valleys[i]}": f"resonant_wl_power_{i}" for i in
                    range(len(good_valleys))}

        info = info.rename(columns=name_map)
        # Por enquanto considera que a região pega 1 único vale, então esse
        # que deve ser analisado. Se surgir a situação de vales muito próximos
        # essa parte deve ser reavaliada
        info["best_index"] = 0
        info["best_wl"] = info["resonant_wl_0"]
        info["best_wl_power"] = info["resonant_wl_power_0"]
        info["measurand"] = info["resonant_wl_0"]

        processing.plot(spectrum, self.plot_widget.axs, info, options)
        self.plot_widget.add_text()
        self.plot_widget.canvas.figure.canvas.draw()














import pandas as pd
from collections import defaultdict
import json
from time import time
import os

from PlotWidget import PlotWidget
from Toolbar import WindowWithToolbar
from Loader import FileLoader
import processing
from OptionsDialog import OptionsDialog, CONFIG_PATH, DEFAULT


class MainWindow(WindowWithToolbar):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LITel OSA")

        self.plot_widget = PlotWidget()
        self.setCentralWidget(self.plot_widget)

        self.show()

        self.start_time = time()
        self.spectra_info = pd.DataFrame()

        self.options = {}
        self.load_options()

        self.loader = FileLoader(self.entry_loaded, 
                                 path=self.options['spectra_path'])

    def open_config(self):
        dialog = OptionsDialog(self)
        dialog.exec()
        self.on_change_options()

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
        spectrum, info = processing.process(spectrum, self.options)
        info['time'] = time() - self.start_time

        self.spectra_info = self.spectra_info.append(info, ignore_index=True)
        # self.spectra_info = processing.reorganize_valleys(self.spectra_info)

        processing.plot(spectrum,
                        self.plot_widget.axs,
                        self.spectra_info,
                        self.options)

        self.plot_widget.canvas.figure.canvas.draw()
